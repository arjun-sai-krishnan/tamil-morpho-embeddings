import numpy as np

# file template
# each row is "rel_id rel_type word1 word2"
# rel_type is 0 if not any subword information and any integer > 0 identifies the particular type of morphological relation

# filters out any words that aren't in the model vocabulary
def clean_dset(inpath, outpath, model):
    filein = open(inpath, 'r')
    fileout = open(outpath, 'w')
    kicked_cnt = 0
    total_cnt = 0
    
    stuff = filein.readline()
    seen_pairs = set([])
    while stuff != '':
        stuff = stuff.split()
        rel_id = int(stuff[0])
        
        if (stuff[2], stuff[3]) in seen_pairs or (stuff[3], stuff[2]) in seen_pairs:
            print("Duplicate found", stuff[2], stuff[3])
            assert(False)
        seen_pairs.add((stuff[2], stuff[3]))
        
        if stuff[2] in model.vocab and stuff[3] in model.vocab:
            fileout.write(str(rel_id) + " " + stuff[1] + " " + stuff[2] + " " + stuff[3] + "\n")
        else:
            kicked_cnt += 1
            print("Kicked out " + str(stuff[2]) + " " + str(stuff[3]))
        total_cnt += 1
        stuff = filein.readline()
    print("Kicked", kicked_cnt, "out of", total_cnt, "pairs")
    filein.close()
    fileout.close()
    
def extract_dset(path):
    filein = open(path, 'r')
    ret = {}
    stuff = filein.readline()
    while stuff != '':
        stuff = stuff.split()
        rel_id = int(stuff[0])
        rel_type = int(stuff[1])
        
        if rel_id not in ret:
            ret[rel_id] = {}
        if rel_type not in ret[rel_id]:
            ret[rel_id][rel_type] = []
            
        ret[rel_id][rel_type].append([stuff[2], stuff[3]])
        stuff = filein.readline()
    return ret

def extract_analogy_dset(path):
    filein = open(path, 'r')
    ret = {}
    stuff = filein.readline()
    while stuff != '':
        stuff = stuff.split()
        rel_id = int(stuff[0])
        if rel_id not in ret:
            ret[rel_id] = []
        ret[rel_id].append([stuff[1], stuff[2], stuff[3], stuff[4]])
        stuff = filein.readline()
    return ret

def construct_analogy_dset(dset, subpath, nonsubpath):
    subfile = open(subpath, 'w')
    nonsubfile = open(nonsubpath, 'w')
    
    for rel_id in dset:
        # process all analogies involving type 0 first
        if 0 in dset[rel_id]:
            # type 0, type 0
            rel = dset[rel_id][0]
            length = len(rel)
            for first in range(length):
                for second in range(first+1, length):
                    pair1 = rel[first]
                    pair2 = rel[second]
                    string = str(rel_id) + " " + pair1[0] + " " + pair1[1] + " " + pair2[1] + " " + pair2[0]
                    nonsubfile.write(string + '\n')
                    
            # type 0, all other types
            for k in dset[rel_id]:
                if k != 0:
                    rel2 = dset[rel_id][k]
                    length2 = len(rel2)
                    for first in range(length):
                        for second in range(length2):
                            pair1 = rel[first]
                            pair2 = rel2[second]
                            string = str(rel_id) + " " + pair1[0] + " " + pair1[1] + " " + pair2[1] + " " + pair2[0]
                            nonsubfile.write(string + '\n')
        
        # now everything not involving type 0
        types = sorted(dset[rel_id].keys())
        for dummy1 in range(len(types)):
            type1 = types[dummy1]
            if type1 == 0:
                continue
                
            # process same-type analogies first - these are the ones that use subword information
            rel = dset[rel_id][type1]
            length = len(rel)
            for first in range(length):
                for second in range(first+1, length):
                    pair1 = rel[first]
                    pair2 = rel[second]
                    string = str(rel_id) + " " + pair1[0] + " " + pair1[1] + " " + pair2[1] + " " + pair2[0]
                    subfile.write(string + '\n')
                    
            # now different type analogies
            for dummy2 in range(dummy1+1, len(types)):
                type2 = types[dummy2]
                rel2 = dset[rel_id][type2]
                length2 = len(rel2)
                
                for first in range(length):
                    for second in range(length2):
                        pair1 = rel[first]
                        pair2 = rel2[second]
                        string = str(rel_id) + " " + pair1[0] + " " + pair1[1] + " " + pair2[1] + " " + pair2[0]
                        nonsubfile.write(string + '\n')
                
    subfile.close()
    nonsubfile.close()
    
# takes an analogy dset as input, and splits them 80/20
def train_test_split(dset, train_path, test_path, p=0.8):
    train_out = open(train_path, 'w')
    test_out = open(test_path, 'w')
    
    for rel_id in dset:
        tetrads = list(dset[rel_id])
        np.random.shuffle(tetrads)
        
        num_train = int(p * len(tetrads))
        
        for i in range(num_train):
            train_out.write(str(rel_id) + " " + tetrads[i][0] + " " + tetrads[i][1] + " " + tetrads[i][2] + " " + tetrads[i][3] + "\n")
        for i in range(num_train, len(tetrads)):
            test_out.write(str(rel_id) + " " + tetrads[i][0] + " " + tetrads[i][1] + " " + tetrads[i][2] + " " + tetrads[i][3] + "\n")
            
        print("Id", rel_id, "train", num_train, "test", len(tetrads) - num_train)
            
    train_out.close()
    test_out.close()