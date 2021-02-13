#!/usr/bin/env python3

import argparse
from collections import Counter
from multiprocessing import set_start_method
import pdb
import re
import sys
import time
import copy

import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
from torch import optim
import torch.nn.functional as F
import torch.multiprocessing as mp

import data_producer

from word2atoms import skipgram_atoms, trivial_atoms, morpheme_split

parser = argparse.ArgumentParser()
parser.add_argument("--train", type=str, default="", help="training file")
parser.add_argument("--output", type=str, default="vectors.txt", help="output word embedding file")
parser.add_argument("--atomoutput", type=str, default="atomvectors.txt", help="output atom embedding file")
parser.add_argument("--ctxoutput", type=str, default="atomvectors.txt", help="context vectors file")
parser.add_argument("--ctxatomoutput", type=str, default="atomvectors.txt", help="context atom vectors file")
parser.add_argument("--losslog", type=str, default="all_losses.txt", help="log of training losses")
parser.add_argument("--opt", type=str, default="SGD", help="optimiser to use")
parser.add_argument("--size", type=int, default=300, help="word embedding dimension")
parser.add_argument("--cbow", type=int, default=1, help="1 for cbow, 0 for skipgram")
parser.add_argument("--window", type=int, default=5, help="context window size")
parser.add_argument("--sample", type=float, default=1e-4, help="subsample threshold")
parser.add_argument("--negative", type=int, default=10, help="number of negative samples")
parser.add_argument("--min_count", type=int, default=5, help="minimum frequency of a word")
parser.add_argument("--processes", type=int, default=4, help="number of processes")
parser.add_argument("--num_workers", type=int, default=6, help="number of workers for data processsing")
parser.add_argument("--iter", type=int, default=5, help="number of iterations")
parser.add_argument("--lr", type=float, default=-1.0, help="initial learning rate")
parser.add_argument("--momentum", type=float, default=0.0, help="momentum")
parser.add_argument("--batch_size", type=int, default=100, help="(max) batch size")
parser.add_argument("--megabatch_size", type=int, default=100000, help="(max) megabatch size")
parser.add_argument("--cuda", action='store_true', default=False, help="enable cuda")
parser.add_argument("--output_ctx", action='store_true', default=False, help="output context embeddings")
parser.add_argument("--anneal", action='store_true', default=False, help="anneal the learning rate linearly to 0")
parser.add_argument("--shuffle", action='store_true', default=False, help="shuffle the training data points")
parser.add_argument("--atomizer", type=str, choices=['fasttext', 'morphoseg', 'word2vec'], default="word2vec", help="atomizer to use (vanilla word2vec by default, can also choose fasttext or morphoseg)")
parser.add_argument("--minL", type=int, default=5, help="minimum possible length of n-grams to take when atomizing")
parser.add_argument("--maxL", type=int, default=5, help="maximum possible length of n-grams to take when atomizing")
parser.add_argument("--halfletters", action='store_true', default=False, help="whether to use half-letters/raw Unicode characters when taking n-grams, or whole Tamil letters")

MAX_SENT_LEN = 1000

# Build the vocabulary.
def file_split(f, delim=' \t\n', bufsize=1024):
    prev = ''
    while True:
        s = f.read(bufsize)
        if not s:
            break
        tokens = re.split('['+delim+']{1,}', s)
        if len(tokens) > 1:
            yield prev + tokens[0]
            prev = tokens[-1]
            for x in tokens[1:-1]:
                yield x
        else:
            prev += s
    if prev:
        yield prev

def build_vocab(args):
    vocab = Counter()
    word_count = 0
    for word in file_split(open(args.train)):
        vocab[word] += 1
        word_count += 1
        if word_count % 10000 == 0:
            sys.stdout.write('%d\r' % len(vocab))
    freq = {k:v for k,v in vocab.items() if v >= args.min_count}
    word_count = sum([freq[k] for k in freq])
    word_list = sorted(freq, key=freq.get, reverse=True)
    word2idx = {}
    for i,w in enumerate(word_list):
        word2idx[w] = i

    print("Vocab size: %ld" % len(word2idx))
    print("Words in train file: %ld" % word_count)
    vars(args)['vocab_size'] = len(word2idx)
    vars(args)['train_words'] = word_count

    """ for i, word in enumerate(word_list):
        if word[-1] == '0':
            print(i, word)
        if i == 1761:
            print(word) """
    #print("Initial mattrum count")
    #print(freq['மற்றும்'])
    return word2idx, word_list, freq

def build_morph(args, word2idx, word_list, freq, atomiser):
    morph_list = []
    morph2idx = {}
    word2morph = []
    #total_morphperword = 0
    max_morphperword = 0
    #total_freq = 0
    for i, word in enumerate(word_list):
        idxs = []
        cnt = 0
        if i <= 20:
            print(word, atomiser(word))
        for morph in atomiser(word):
            if morph in morph2idx:
                idx = morph2idx[morph]
            else:
                idx = len(morph_list)
                morph_list.append(morph)
                morph2idx[morph] = idx
            idxs.append(idx)
            cnt += 1
        #total_morphperword += freq[word] * cnt
        #total_freq += freq[word]
        if cnt > max_morphperword:
            max_morphperword = cnt
        word2morph.append(torch.LongTensor(idxs))
        if i % 100 == 0:
            sys.stdout.write('%d\r' % i)
    
    # actual padding index
    word2morph.append(torch.LongTensor([len(morph2idx)]))

    word2morphfinal = torch.zeros((len(word2morph), max_morphperword), dtype=torch.long)
    word2morphfinal = word2morphfinal.fill_(len(morph2idx) +1)
    for i in range(len(word2morph)):
        row = word2morph[i]
        word2morphfinal[i, :row.shape[0]] = row

    #print(word2morphfinal.shape)
    #print(freq[word_list[0]])
    """ indices = [0]
    for index in indices:
        print(word_list[index])
        print(' '.join([morph_list[j] for j in word2morph[index]]))
    print(word2morph[816])
    print(word2morph[0])
    print(word2morph[10520]) """

    print("Morpheme size: %ld" % len(morph2idx))
    #print("Average morphemes per word: %f" % (float(total_morphperword)/total_freq))
    print("Max morphemes per word: %d" % max_morphperword)
    #vars(args)['morph_size'] = len(morph2idx)
    #vars(args)['word2morph'] = word2morph

    return morph2idx, morph_list, word2morphfinal

class CBOWMean(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x, lens):
        ctx.save_for_backward(x)
        x = torch.sum(x, 1, keepdim=True)
        x = x.permute(1,2,0) / lens
        return x.permute(2,0,1)
    @staticmethod
    def backward(ctx, g):
        x, = ctx.saved_variables
        return g.expand_as(x), None

class CBOW(nn.Module):
    def __init__(self, args):
        super(CBOW, self).__init__()
        self.emb0_lookup = nn.Embedding(args.vocab_size+1, args.size, padding_idx=args.vocab_size, sparse=True)
        self.emb1_lookup = nn.Embedding(args.vocab_size, args.size, sparse=True)
        self.emb0_lookup.weight.data.uniform_(-0.5/args.size, 0.5/args.size)
        self.emb0_lookup.weight.data[args.vocab_size].fill_(0)
        self.emb1_lookup.weight.data.uniform_(-0.5/args.size, 0.5/args.size)
        self.window = args.window
        self.negative = args.negative
        self.pad_idx = args.vocab_size

    def forward(self, data):
        ctx_indices = data[:, 0:2*self.window]
        ctx_lens = data[:, 2*self.window].float()
        word_idx = data[:, 2*self.window+1]
        neg_indices = data[:, 2*self.window+2:2*self.window+2+self.negative]
        neg_mask = data[:, 2*self.window+2+self.negative:].float()

        c_embs = self.emb0_lookup(ctx_indices)
        w_embs = self.emb1_lookup(word_idx)
        n_embs = self.emb1_lookup(neg_indices)

        c_embs = CBOWMean.apply(c_embs, ctx_lens)

        pos_ips = torch.sum(c_embs[:,0,:] * w_embs, 1)
        neg_ips = torch.bmm(n_embs, c_embs.permute(0,2,1))[:,:,0]

        # Neg Log Likelihood
        pos_loss = torch.sum( -F.logsigmoid(torch.clamp(pos_ips,max=10,min=-10)) )
        neg_loss = torch.sum( -F.logsigmoid(torch.clamp(-neg_ips,max=10,min=-10)) * neg_mask )

        return pos_loss + neg_loss

class SG(nn.Module):
    def __init__(self, args):
        super(SG, self).__init__()
        self.emb0morph_lookup = nn.Embedding(args.morph_size+2, args.size, padding_idx=args.morph_size, sparse=True)
        self.emb1morph_lookup = nn.Embedding(args.ctxmorph_size+2, args.size, padding_idx=args.ctxmorph_size, sparse=True)

        #self.emb0_lookup = nn.Embedding(args.vocab_size+1, args.size, padding_idx=args.vocab_size, sparse=True)
        #self.emb1_lookup = nn.Embedding(args.vocab_size, args.size, sparse=True)

        self.emb0morph_lookup.weight.data.uniform_(-0.5/args.size, 0.5/args.size)
        self.emb0morph_lookup.weight.data[args.morph_size+1].fill_(0)
        # randomly initialise context vectors
        #self.emb1morph_lookup.weight.data.uniform_(-0.5/args.size, 0.5/args.size)
        #self.emb1morph_lookup.weight.data[args.ctxmorph_size+1].fill_(0)

        # OR zero initialise them as usual
        self.emb1morph_lookup.weight.data.zero_()

        #self.emb0_lookup.weight.data.uniform_(-0.5/args.size, 0.5/args.size)
        #self.emb1_lookup.weight.data.zero_()
        #self.emb1morph_lookup.weight.data.zero_()

        #self.emb0morph_lookup.weight.data[args.morph_size+1].requires_grad = False

        self.window = args.window
        self.negative = args.negative
        self.pad_idx = args.vocab_size
        self.morph_size = args.morph_size

    def forward(self, data, word2morph, word2morph_mask, ctx2morph, ctx2morph_mask):
        word_idx = data[:, 0]
        ctx_idx = data[:, 1]
        neg_indices = data[:, 2:2+self.negative]
        neg_mask = data[:, 2+self.negative:].float()

        #print(word2morph.shape)
        #print(word2morph_mask.shape)

        #print(torch.max(word2morph))
        #print("MORPHEMES")
        #print(word2morph[3])
        #print(torch.norm(self.emb0morph_lookup.weight.data[-1]))
        #print(torch.norm(torch.squeeze(word2morph_mask), dim=0)) # should start nonzero, then eventually be 0

        #print((self.emb0morph_lookup(word2morph[:, 0]) * word2morph_mask[:, 0]).shape)
        #t = self.emb0morph_lookup(word2morph) * word2morph_mask
        #print(t.shape)
        #print(torch.sum(t, dim=1).shape)
        w_embs = torch.sum(self.emb0morph_lookup(word2morph) * word2morph_mask, dim=1)
        #w_embs = self.emb0_lookup(word_idx)

        #t = self.emb1morph_lookup(ctx2morph[:, 0]) * ctx2morph_mask[:, 0]
        #print(t.shape)
        #print(torch.sum(t, dim=1).shape)
        #print((self.emb0morph_lookup(word2morph[:, 1]) * word2morph_mask[:, 1]).shape)
        c_embs = torch.sum(self.emb1morph_lookup(ctx2morph[:, 0]) * ctx2morph_mask[:, 0], dim=1)
        #c_embs = self.emb1_lookup(ctx_idx)
        
        #t = self.emb1morph_lookup(ctx2morph[:, 1:1+self.negative]) * ctx2morph_mask[:, 1:1+self.negative]
        #print(t.shape)
        #print(torch.sum(t, dim=2).shape)
        #print((self.emb0morph_lookup(word2morph[:, 2:2+self.negative]) * word2morph_mask[:, 2:2+self.negative]).shape)
        n_embs = torch.sum(self.emb1morph_lookup(ctx2morph[:, 1:1+self.negative]) * ctx2morph_mask[:, 1:1+self.negative], dim=2)
        #n_embs = self.emb1_lookup(neg_indices)

        pos_ips = torch.sum(w_embs * c_embs, 1)
        neg_ips = torch.bmm(n_embs, torch.unsqueeze(w_embs,1).permute(0,2,1))[:,:,0]

        # Neg Log Likelihood
        pos_loss = torch.sum( -F.logsigmoid(torch.clamp(pos_ips,max=10,min=-10)) )
        neg_loss = torch.sum( -F.logsigmoid(torch.clamp(-neg_ips,max=10,min=-10)) * neg_mask )

        return pos_loss + neg_loss

# Initialize model.
def init_net(args):
    if args.cbow == 1:
        if args.lr == -1.0:
            vars(args)['lr'] = 0.05
        return CBOW(args)
    elif args.cbow == 0:
        if args.lr == -1.0:
            vars(args)['lr'] = 0.025
        return SG(args)

# Training
def train_process_sent_producer(p_id, data_queue, word_count_actual, word2idx, word_list, freq, args):
    if args.negative > 0:
        table_ptr_val = data_producer.init_unigram_table(word_list, freq, args.train_words)

    train_file = open(args.train)
    file_pos = args.file_size * p_id // args.processes
    train_file.seek(file_pos, 0)
    while True:
        try:
            train_file.read(1)
        except UnicodeDecodeError:
            file_pos -= 1
            train_file.seek(file_pos, 0)
        else:
            train_file.seek(file_pos, 0)
            break

    batch_count = 0
    if args.cbow == 1:
        batch_placeholder = np.zeros((args.megabatch_size, 2*args.window+2+2*args.negative), 'int64')
    else:
        batch_placeholder = np.zeros((args.megabatch_size, 2+2*args.negative), 'int64')
    #mattrum_cnt = 0
    for it in range(args.iter):
        train_file.seek(file_pos, 0)

        last_word_cnt = 0
        word_cnt = 0
        sentence = []
        prev = ''
        eof = False
        while True:
            if eof or train_file.tell() > file_pos + args.file_size / args.processes:
                break

            while True:
                s = train_file.read(1)
                if not s:
                    eof = True
                    break
                elif s == ' ' or s == '\t':
                    if prev in word2idx:
                        sentence.append(prev)
                    prev = ''
                    if len(sentence) >= MAX_SENT_LEN:
                        break
                elif s == '\n':
                    if prev in word2idx:
                        sentence.append(prev)
                    prev = ''
                    break
                else:
                    prev += s

            if len(sentence) > 0:
                #print("Full sentence")
                #print(' '.join(sentence))
                # subsampling
                sent_id = []
                trimmed = []
                if args.sample != 0:
                    sent_len = len(sentence)
                    i = 0
                    while i < sent_len:
                        word = sentence[i]
                        f = freq[word] / args.train_words
                        pb = (np.sqrt(f / args.sample) + 1) * args.sample / f

                        if pb > np.random.random_sample():
                            sent_id.append( word2idx[word] )
                            """ if word2idx[word] == 'மற்றும்' and mattrum_cnt % 1000 == 0:
                                print("Hit another 1000 mattrums")
                                mattrum_cnt += 1
                        else:
                            trimmed.append(word) """
                        i += 1

                if len(sent_id) < 2:
                    word_cnt += len(sentence)
                    sentence.clear()
                    continue
                
                #print("Killed words")
                #print(' '.join(trimmed))
                #print("Trimmed sentence")
                #print(' '.join([word_list[index] for index in sent_id]))

                next_random = (2**24) * np.random.randint(0, 2**24) + np.random.randint(0, 2**24)
                if args.cbow == 1: # train CBOW
                    chunk = data_producer.cbow_producer(sent_id, len(sent_id), table_ptr_val,
                                args.window, args.negative, args.vocab_size, args.batch_size, next_random)
                elif args.cbow == 0: # train skipgram
                    chunk = data_producer.sg_producer(sent_id, len(sent_id), table_ptr_val,
                                args.window, args.negative, args.vocab_size, args.batch_size, next_random)
                
                #print("Data points")
                #print(chunk)
                
                chunk_pos = 0
                while chunk_pos < chunk.shape[0]:
                    remain_space = args.megabatch_size - batch_count
                    remain_chunk = chunk.shape[0] - chunk_pos

                    if remain_chunk < remain_space:
                        take_from_chunk = remain_chunk
                    else:
                        take_from_chunk = remain_space

                    batch_placeholder[batch_count:batch_count+take_from_chunk, :] = chunk[chunk_pos:chunk_pos+take_from_chunk, :]
                    batch_count += take_from_chunk

                    if batch_count == args.megabatch_size:
                        if args.shuffle:
                            p = torch.randperm(batch_count)
                            batch_placeholder = batch_placeholder[p]

                        start = 0
                        while start < batch_count:
                            data_queue.put(batch_placeholder[start : min(start + args.batch_size, batch_count)])
                            start += args.batch_size
                        #print("Batch placeholder")
                        #print(batch_placeholder)
                        batch_count = 0

                    chunk_pos += take_from_chunk

                word_cnt += len(sentence)
                if word_cnt - last_word_cnt > 10000:
                    with word_count_actual.get_lock():
                        word_count_actual.value += word_cnt - last_word_cnt
                    last_word_cnt = word_cnt
                sentence.clear()

        with word_count_actual.get_lock():
            word_count_actual.value += word_cnt - last_word_cnt

    #print("Total occurrences of mattrum: " + str(mattrum_cnt))
    #print("Total non-occurrences of mattrum: " + str(non_mattrum_cnt))
    if batch_count > 0:
        if args.shuffle:
            p = torch.randperm(batch_count)
            batch_placeholder[:batch_count] = batch_placeholder[p]

        start = 0
        while start < batch_count:
            data_queue.put(batch_placeholder[start : min(start + args.batch_size, batch_count)])
            start += args.batch_size
        #print("Batch placeholder")
        #print(batch_placeholder)
        batch_count = 0
    data_queue.put(None)

def train_process(p_id, word_count_actual, word2idx, word_list, freq, args, model, word2morph, word2morph_mask, ctx2morph, ctx2morph_mask):
    data_queue = mp.SimpleQueue()

    if args.opt == "Adagrad":
        optimizer = optim.Adagrad(model.parameters(), lr=args.lr)
    elif args.opt == "SGD":
        optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)
    elif args.opt == 'SparseAdam':
        optimizer = optim.SparseAdam(model.parameters(), lr=args.lr)

    t = mp.Process(target=train_process_sent_producer, args=(p_id, data_queue, word_count_actual, word2idx, word_list, freq, args))
    t.start()

    # get from data_queue and feed to model
    prev_word_cnt = 0
    losses_cnt = 0
    total_loss = 0.0
    losses_file = open(args.losslog, 'w')
    lr = args.lr
    #mattrum_cnt = 0
    #non_mattrum_cnt = 0
    while True:
        d = data_queue.get()
        if d is None:
            break
        else:
            # lr anneal
            if args.anneal:
                if word_count_actual.value - prev_word_cnt > 10000:
                    lr = args.lr * (1 - word_count_actual.value / (args.iter * args.train_words))
                    if lr < 0.0001 * args.lr:
                        lr = 0.0001 * args.lr
                    for param_group in optimizer.param_groups:
                        param_group['lr'] = lr
            else:
                lr = args.lr

            if args.cuda:
                data = Variable(torch.LongTensor(d).cuda(), requires_grad=False)
            else:
                data = Variable(torch.LongTensor(d), requires_grad=False)

            if args.cbow == 1:
                optimizer.zero_grad()
                loss = model(data)
                loss.backward()
                optimizer.step()
                model.emb0_lookup.weight.data[args.vocab_size].fill_(0)
            elif args.cbow == 0:
                optimizer.zero_grad()
                #print("WORD")
                #print(data[3][0])
                loss = model(data, word2morph[data[:, 0]], word2morph_mask[data[:, 0]], ctx2morph[data[:, 1:2+args.negative]], ctx2morph_mask[data[:, 1:2+args.negative]])
                loss.backward()
                #model.emb0morph_lookup.weight.data.grad[args.morph_size+1].fill_(0)
                optimizer.step()
                #model.emb0morph_lookup.weight.data[args.morph_size+1].zero_()
            
            losses_cnt += data.shape[0]
            total_loss += loss

            # output
            if word_count_actual.value - prev_word_cnt > 10000:
                avg_loss = total_loss/losses_cnt
                sys.stdout.write("\rAlpha: %0.8f, Loss: %0.8f, Progress: %0.2f, Words/sec: %f" % (lr, avg_loss, word_count_actual.value / (args.iter * args.train_words) * 100, word_count_actual.value / (time.monotonic() - args.t_start)))
                sys.stdout.flush()
                prev_word_cnt = word_count_actual.value
                losses_cnt = 0
                total_loss = 0.0
                losses_file.write(str(avg_loss.item()) + '\n')

    losses_file.close()
    t.join()

if __name__ == '__main__':
    set_start_method('forkserver')

    args = parser.parse_args()
    print("Starting training using file %s" % args.train)
    train_file = open(args.train)
    train_file.seek(0, 2)
    vars(args)['file_size'] = train_file.tell()

    word2idx, word_list, freq = build_vocab(args)
    # constructing and applying atomizer to all words
    minL = args.minL
    maxL = args.maxL
    use_listify = not args.halfletters
    if args.atomizer == 'word2vec':
        atomizer = lambda w: trivial_atoms(w)
    elif args.atomizer == 'fasttext':
        atomizer = lambda w: skipgram_atoms(w, minL=minL, maxL=maxL)
    elif args.atomizer == 'morphoseg':
        atomizer = lambda w: morpheme_split(w, minL=minL, maxL=maxL, use_listify=use_listify, to_stem=True)
    
    morph2idx, morph_list, word2morph = build_morph(args, word2idx, word_list, freq, atomizer)
    vars(args)['morph_size'] = len(morph2idx)

    ctxmorph2idx, ctxmorph_list, ctx2morph = build_morph(args, word2idx, word_list, freq, trivial_atoms)
    vars(args)['ctxmorph_size'] = len(ctxmorph2idx)

    #print(word2morph.shape)
    #print(ctx2morph.shape)
    

    """ idx = 200
    word = word_list[idx]
    print("Word: " + word)
    print("Index should be: " + str(word2idx[word]))
    all_morphs = word2morph[idx]
    for midx in all_morphs:
        print("Morpheme: " + morph_list[midx])
        print("Index used for lookup: " + str(midx))
        print("Index retrieved: " + str(morph2idx[morph_list[midx]])) """

    word_count_actual = mp.Value('L', 0)

    model = init_net(args)
    model.share_memory()
    word2morph_mask = torch.unsqueeze((word2morph <= args.morph_size), dim=2).type(model.emb0morph_lookup.weight.data.dtype)
    ctx2morph_mask = torch.unsqueeze((ctx2morph <= args.ctxmorph_size), dim=2).type(model.emb1morph_lookup.weight.data.dtype)
    
    if args.cuda:
        model.cuda()
        word2morph = word2morph.cuda()
        word2morph_mask = word2morph_mask.cuda()
        ctx2morph = ctx2morph.cuda()
        ctx2morph_mask = ctx2morph_mask.cuda()

    #print(word2morph_mask.shape)
    #print(ctx2morph_mask.shape)

    vars(args)['t_start'] = time.monotonic()
    processes = []
    for p_id in range(args.processes):
        p = mp.Process(target=train_process, args=(p_id, word_count_actual, word2idx, word_list, freq, args, model, word2morph, word2morph_mask, ctx2morph, ctx2morph_mask))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    torch.cuda.empty_cache()

    # print out the atom input vectors
    if args.cuda:
        embs = model.emb0morph_lookup.weight.data.cpu().numpy()
    else:
        embs = model.emb0morph_lookup.weight.data.numpy()
    
    #print(embs.shape)
    data_producer.write_embs(args.atomoutput, morph_list, embs, args.morph_size, args.size)
    del embs
    torch.cuda.empty_cache()

    wordembs = np.zeros((word2morph.shape[0], args.size), dtype=np.float32)
    print(wordembs.shape)
    # word input vectors
    if args.cuda:
        numpieces = 5
        cnt = word2morph.shape[0] // numpieces
        print("Need to handle " + str(word2morph.shape[0]) + " words")
        for j in range(numpieces):
            start = j * cnt
            end = start + cnt
            if j == numpieces - 1:
                end = word2morph.shape[0]
            print("Handling all words from " + str(start) + " to " + str(end))
            wordembs[start:end] = torch.sum(model.emb0morph_lookup(word2morph[start:end]) * word2morph_mask[start:end], dim=1).detach().cpu().numpy()
    else:
        wordembs = torch.sum(model.emb0morph_lookup(word2morph) * word2morph_mask, dim=1).detach().numpy()

    #print(wordembs.shape)
    data_producer.write_embs(args.output, word_list, wordembs, args.vocab_size, args.size)
    del wordembs
    torch.cuda.empty_cache()

    # atom context vectors
    if args.cuda:
        atembs = model.emb1morph_lookup.weight.data.cpu().numpy()
    else:
        atembs = model.emb1morph_lookup.weight.data.numpy()
    
    #print(atembs.shape)
    data_producer.write_embs(args.ctxatomoutput, ctxmorph_list, atembs, args.ctxmorph_size, args.size)
    del atembs
    torch.cuda.empty_cache()

    # word context vectors
    ctxembs = np.zeros((ctx2morph.shape[0], args.size), dtype=np.float32)
    print(ctxembs.shape)
    if args.cuda:
        numpieces = 5
        cnt = ctx2morph.shape[0] // numpieces
        print("Need to handle " + str(ctx2morph.shape[0]) + " words")
        for j in range(numpieces):
            start = j * cnt
            end = start + cnt
            if j == numpieces - 1:
                end = ctx2morph.shape[0]
            print("Handling all words from " + str(start) + " to " + str(end))
            ctxembs[start:end] = torch.sum(model.emb1morph_lookup(ctx2morph[start:end]) * ctx2morph_mask[start:end], dim=1).detach().cpu().numpy()
    else:
        ctxembs = torch.sum(model.emb1morph_lookup(ctx2morph) * ctx2morph_mask, dim=1).detach().numpy()

    #print(ctxembs.shape)
    data_producer.write_embs(args.ctxoutput, word_list, ctxembs, args.vocab_size, args.size)
    del ctxembs
    torch.cuda.empty_cache()

    print("")

