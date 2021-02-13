from tamil_segmenter_modified import stem
#import Stemmer

# SECTION: helper methods

extra_chars = set(['ஂ', 'ா', 'ி', 'ீ', 'ு', 'ூ', 'ெ', 'ே', 'ை', 'ொ', 'ோ', 'ௌ', '்', 'ௗ'])

# splitting the word into natural Tamil characters rather than the
# the Unicode characters
def listify(word):
    l = list(word)
    i = 0
    while i < len(l):
        if l[i] in extra_chars:
            l[i-1] = l[i-1] + l[i]
            l.pop(i)
        else:
            i += 1
    return l

# source: https://www.geeksforgeeks.org/longest-common-substring-dp-29/
# This code is contributed by Soumen Ghosh

# This is needed here to deal with both prefix and suffix morphemes, and also the weird consonant changes where
# morphemes

# Returns length of longest common  
# substring of X[0..m-1] and Y[0..n-1]  
def LCSubStr(X, Y, m, n): 
      
    # Create a table to store lengths of 
    # longest common suffixes of substrings.  
    # Note that LCSuff[i][j] contains the  
    # length of longest common suffix of  
    # X[0...i-1] and Y[0...j-1]. The first 
    # row and first column entries have no 
    # logical meaning, they are used only 
    # for simplicity of the program. 
      
    # LCSuff is the table with zero  
    # value initially in each cell 
    LCSuff = [[0 for k in range(n+1)] for l in range(m+1)] 
      
    # To store the length of  
    # longest common substring 
    result = 0
    # to track where the longest common substring is in X
    end_in_X = -1
    end_in_Y = -1
  
    # Following steps to build 
    # LCSuff[m+1][n+1] in bottom up fashion 
    for i in range(m + 1): 
        for j in range(n + 1): 
            if (i == 0 or j == 0): 
                LCSuff[i][j] = 0
            elif (X[i-1] == Y[j-1]): 
                LCSuff[i][j] = LCSuff[i-1][j-1] + 1
                if LCSuff[i][j] > result:
                    result = LCSuff[i][j]
                    end_in_X = i
                    end_in_Y = j
            else: 
                LCSuff[i][j] = 0
    return result, end_in_X, end_in_Y

def get_ngrams(wordL, k):
    ret = []
    for i in range(len(wordL) + 1 - k):# range(1-k, len(wordL)):
        ret.append(''.join(wordL[i:i+k]))
        # ret.append(word[max(i, 0) : min(i+k, len(word)-1)])
    #if len(ret) == 0 and len(wordL) > 0: # word is shorter than n-gram window
    #    ret.append(''.join(wordL))
    return ret

# SECTION: "atomisation" methods that are used in fastText

def trivial_atoms(word):
    return [word]

def stem_only(word):
    st = stem(word, morphemes=False)
    if len(st) > 0:
        return [st]
    else:
        return [word]

def skipgram_atoms(word, minL=5, maxL=5):
    bigword = '<' + word + '>'
    wordL = list(bigword)

    ret = []
    for window in range(minL, maxL+1):
        for substr in get_ngrams(wordL, window):
            ret.append(substr)

    if len(bigword) > maxL:
        ret.append(bigword)

    return ret

""" test_words = ['abcabc']
for w in test_words:
    print(' '.join(skipgram_atoms(w, 3, 6))) """

# SECTION: actual segmentation methods

# all of these take a word as input and output something of the form
# [list of prefix atoms, list of stem atoms, list of suffix atoms]

# pre-stem, stem, after-stem
def basic_split(word, use_listify=True):
    st = stem(word, morphemes=False)
    if use_listify:
        wordL = listify(word)
        stL = listify(st)
    else:
        wordL = list(word)
        stL = list(st)

    if len(stL) > 0:
        length, endW, endS = LCSubStr(wordL, stL, len(wordL), len(stL))
    else: # in case the stemmer says the word is stemless
        length = 0
        st2, prefixout2, suffixout2 = stem(word, morphemes=True)
        if len(prefixout2) == 0: # the whole word is suffix
            endW = 0
        else: # the whole word is prefix
            endW = len(wordL)

    prefixL = wordL[: endW - length]
    suffixL = wordL[endW :]

    if len(prefixL) > 0:
        prefixout = [''.join(prefixL)]
    else:
        prefixout = []

    if len(st) > 0:
        stout = [st]
    else:
        stout = []

    if len(suffixL) > 0:
        suffixout = [''.join(suffixL)]
    else:
        suffixout = []
    
    # stem_in_word = ''.join(wordL[endW-length : endW])
    return [prefixout, stout, suffixout]

# same as above but also splitting either part into n-grams
# word: the word to be stemmed
# minL, maxL: the range of lengths of n-grams taken
# use_listify: self-explanatory
# to_affix: whether to apply n-grams to the prefix and suffix
# to_stem: whether to apply n-grams to the stem

# in Bojanowski et al: minL = 3, maxL = 6, to_affix = to_stem = True essentially
# slight differences: they include specialised begin and end characters
# they also include n-grams across stem-affix boundaries, which we will not have here
# but this is a strictly good thing for us
def ngram_split(word, minL, maxL, use_listify=True, to_affix=True, to_stem=True):
    st = stem(word, morphemes=False)
    if use_listify:
        wordL = listify(word)
        stL = listify(st)
    else:
        wordL = list(word)
        stL = list(st)
    
    if len(stL) > 0:
        length, endW, endS = LCSubStr(wordL, stL, len(wordL), len(stL))
    else: # in case the stemmer says the word is stemless
        length = 0
        st2, prefixout2, suffixout2 = stem(word, morphemes=True)
        if len(prefixout2) == 0: # the whole word is suffix
            endW = 0
        else: # the whole word is prefix
            endW = len(wordL)

    prefixL = wordL[: endW - length]
    suffixL = wordL[endW :]
    prefixout = []
    suffixout = []
    stout = []

    if to_affix:
        for window in range(minL, maxL+1):
            for gram in get_ngrams(prefixL, window):
                prefixout.append(gram)
            for gram in get_ngrams(suffixL, window):
                suffixout.append(gram)
        if len(prefixout) == 0 and len(prefixL) > 0:
            prefixout.append(''.join(prefixL))
        if len(suffixout) == 0 and len(suffixL) > 0:
            suffixout.append(''.join(suffixL))
    else:
        if len(prefixL) > 0:
            prefixout.append(''.join(prefixL))
        if len(suffixL) > 0:
            suffixout.append(''.join(suffixL))

    if to_stem:
        for window in range(minL, maxL+1):
            for gram in get_ngrams(stL, window):
                stout.append(gram)
        if len(stout) == 0 and len(st) > 0:
            stout.append(st)
    elif len(st) > 0:
        stout.append(st)

    return [prefixout, stout, suffixout]

# splitting into morphemes
# including an option for still applying n-grams over the stem
# minL, maxL only matter if this is done
def morpheme_split(word, minL=5, maxL=5, use_listify=False, to_stem=False):
    st, prefixout, suffixout = stem(word, morphemes=True)
    if use_listify:
        stL = listify(st)
    else:
        stL = list(st)

    stout = []
    if to_stem:
        for window in range(minL, maxL+1):
            for gram in get_ngrams(stL, window):
                stout.append(gram)
        # if the stem is too short to be added then we should add it
        # if the stem is too long then we should also add it
        if (len(stout) == 0 or len(stL) > maxL) and len(st) > 0:
            stout.append(st)
    elif len(st) > 0:
        stout.append(st)
    
    ret = []
    for stuff in prefixout:
        ret.append(stuff)
    for stuff in stout:
        ret.append(stuff)
    for stuff in suffixout:
        ret.append(stuff)
    return ret

""" words = ['மகன்தான்', 'வர', 'வர்', 'தர', 'வந்த', 'தந்த', 'வந்தவர்', 'தந்தவர்', 'வந்தவர்கள்', 'தந்தவர்கள்', 'அமைய']
for w in words:
    print("Word: " + w)
    print("Stem: " + stem(w, morphemes=False))
    print("Morphemes with whole letters")
    print(morpheme_split(w, minL=1, maxL=3, use_listify=True, to_stem=True))
    print("Morphemes with partial letters")
    print(morpheme_split(w, minL=3, maxL=5, use_listify=False, to_stem=True)) """