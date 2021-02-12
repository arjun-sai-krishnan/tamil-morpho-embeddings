import nltk
from langdetect import detect
import time
import pickle
import string
import re
import torch

pattern = re.compile('\S*[^\u0B80-\u0BFF\s]+\S*') #\S*

def tam_word_tokenize(text):
    # split into words
    from nltk.tokenize import sent_tokenize
    from nltk.tokenize import word_tokenize
    tokens = word_tokenize(text)
    # remove punctuation from each word
    import string
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if len(word) != 0]

    final = []

    for thing in words:
        if thing.isdigit():
            final.append(thing)
        else:
            if detect(thing) == 'ta':
                final.append(thing)
         
    print(final)
    
    return final

def tam_sent_tokenize(text):
    # split into words
    from nltk.tokenize import sent_tokenize
    from nltk.tokenize import word_tokenize
    sentences = sent_tokenize(text)
    print("nltk tokenize done")
    all_sent = []
    all_words = set([])
    print("Need to go through " + str(len(sentences)) + " sentences")
    t0 = time.time()
    for i in range(len(sentences)):
        """ if i <= 5:
            print("SENTENCE")
            print(sentences[i]) """
        sentence = sentences[i]
        # sentence = pattern.sub('', sentence)
        tokens = word_tokenize(sentence)
        # remove punctuation from each word
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]
        # remove remaining tokens that are not alphabetic
        words = [pattern.sub('', word) for word in stripped if len(word) != 0]
        words = [word for word in words if len(word) != 0]
        """ if i == 0:
            print("STRIPPED")
            print(len(stripped[0]))
            print(stripped[0].encode('utf-8'))
            print("AFTER REGEX")
            print(len(words[0]))
            print(words[0].encode('utf-8')) """

        final = []

        if len(words) != 0:
            for thing in words:
                if thing.isdigit():
                    continue
                else:
                    all_words.add(thing)
                    final.append(thing)
                    """ try:
                        #if detect(thing) == 'ta':
                        all_words.add(thing)
                        final.append(thing)
                    except:
                        useless_var = -1
                        # print(thing) """
            
            if i % 20000 == 0 and time.time() > t0 + 20:
                print("Done " + str(i+1) + " sentences")
                print("time elapsed: " + str(time.time() - t0))
                t0 = time.time()
            
            all_sent.append(final)


    return all_sent, sorted(all_words)

# wordlist should be a sorted array of distinct words
# wordnum should be a dictionary
# numword should just be a list of words as done here    
def index_words(wordlist, wordnum, numword):
    # wordlist.sort() (already sorted)
    # index = 0
    # wordnum_file = open(wordnum, "w")
    numword_file = open(numword, "w")
    n = len(wordlist)
    word2num = {}
    for x in range(n):
        word = wordlist[x]
        word2num[word] = x
        numword_file.write(word + '\n')
    
    numword_file.close()

    pickle.dump(word2num, open(wordnum, 'wb'))

    """ for x in range(1, n):
        word = wordlist[x]
        prev = wordlist[x-1]
        if word == prev:
            if x == n - 1:
                wordnum_file.write(prev + " " + str(index) + "\n")
                numword_file.write(str(index) + " " + prev + "\n")
            continue
        else:
            wordnum_file.write(prev + " " + str(index) + "\n")
            numword_file.write(str(index) + " " + prev + "\n")
            index = index + 1 """

    # wordnum_file.close()
    numword_file.close()
    return word2num # so the dictionary can be used for later tasks

def segment_words(wordlist):
    word2morphemes = []
    morphemelist = set([])
    for word in wordlist:
        seg = word2atoms.morpheme_split(word, 0, 0, use_listify=True, to_stem=False)
        for i in range(3):
            for p in seg[i]:
                morphemelist.add(p)
        word2morphemes.append(seg)
    return word2morphemes, sorted(morphemelist)

# sentlist: an array of sentences, each an array of words
# word2num: a dictionary mapping words to their indices
# filename: the desired location of the indexified corpus
def indexify_corpus(sentlist, word2num, filename):
    fileout = open(filename, 'w')
    for sent in sentlist:
        for word in sent:
            fileout.write(str(word2num[word]) + ' ')
        fileout.write('\n')
    fileout.close()

# word2morphemes: an array of morpheme sequences corresponding to each word
# morphemes2num: a dictionary mapping morphemes to their indices
# filename: the desired location of the indexified morphology
def indexify_morphemes(word2morphemes, morphemes2num, filename):
    fileout = open(filename, 'w')
    for morphseq in word2morphemes:
        for p in morphseq[0]:
            fileout.write(str(morphemes2num[p]) + ' ')
        fileout.write(', ')
        for p in morphseq[1]:
            fileout.write(str(morphemes2num[p]) + ' ')
        fileout.write(', ')
        for p in morphseq[2]:
            fileout.write(str(morphemes2num[p]) + ' ')
        fileout.write('\n')
    fileout.close()

if __name__ == '__main__':
    # reading and tokenizing the text corpus produced by WikiExtractor
    t0 = time.time()
    filename = 'corpus/AA/wiki_00'
    print("Opening file")
    file = open(filename, 'rt')
    text = file.read()
    file.close()
    print("Time elapsed: " + str(time.time() - t0))

    t0 = time.time()
    print("Tokenizing text")
    sentlist, wordlist = tam_sent_tokenize(text)
    print("Time elapsed: " + str(time.time() - t0))

    # saving cleaned corpus (removed words containing non-Tamil characters)
    outfilename = 'corpus/cleaned.txt'
    fileout = open(outfilename, 'w')
    print("Must process " + str(len(sentlist)) + " sentences")
    t0 = time.time()
    for i in range(len(sentlist)):
        s = sentlist[i]
        fileout.write(' '.join(s))
        fileout.write('\n')
        if i % 20000 == 0 and time.time() > t0 + 20:
            print("Done " + str(i+1) + " sentences")
            print("Time elapsed: " + str(time.time() - t0))
            t0 = time.time()
    fileout.close()
    
    # shuffling and saving shuffled corpus
    outfilename = 'corpus/cleaned_shuffled.txt'
    fileout = open(outfilename, 'w')
    print("Must process " + str(len(sentlist)) + " sentences")
    t0 = time.time()
    for i in torch.randperm(len(sentlist)):
        s = sentlist[i]
        fileout.write(' '.join(s))
        fileout.write('\n')
        if i % 20000 == 0 and time.time() > t0 + 20:
            print("Done " + str(i+1) + " sentences")
            print("Time elapsed: " + str(time.time() - t0))
            t0 = time.time()
    fileout.close()