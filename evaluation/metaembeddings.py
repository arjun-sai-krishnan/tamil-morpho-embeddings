import gensim
from gensim.models import KeyedVectors
import numpy as np
from sklearn.decomposition import PCA

# concatenating two models
def concat(model1, model2, mag1=1.0, mag2=1.0, outpath=None, norm=True):
    if '</s>' in model1.vocab:
        weights = np.zeros((len(model1.vocab)-1, model1.vector_size + model2.vector_size), dtype=np.float32)
    else:
        weights = np.zeros((len(model1.vocab), model1.vector_size + model2.vector_size), dtype=np.float32)
    wordlist = []
    i = 0
    for word in model1.vocab:
        if word == '</s>':
            continue
        #print(i)
        v1 = model1.get_vector(word)
        v2 = model2.get_vector(word)
        #print(v1.shape)
        #print(v2.shape)
        #print(weights[i].shape)
        
        if norm:
            s1 = mag1/np.linalg.norm(v1)
            s2 = mag2/np.linalg.norm(v2)
        else:
            s1 = mag1
            s2 = mag2
            
        weights[i] = np.concatenate((s1 * v1, s2 * v2))
        wordlist.append(word)
        i += 1

    combined = KeyedVectors(model1.vector_size + model2.vector_size)
    combined.add(wordlist, weights)
    if outpath != None:
        combined.save_word2vec_format(outpath)
    return combined

# concatenating three models
def concat3(model1, model2, model3, mag1=1.0, mag2=1.0, mag3 = 1.0, outpath=None, norm=True):
    weights = np.zeros((len(model1.vocab), model1.vector_size + model2.vector_size + model3.vector_size), dtype=np.float32)
    wordlist = []
    for i, word in enumerate(model1.vocab):
        #print(i)
        v1 = model1.get_vector(word)
        v2 = model2.get_vector(word)
        v3 = model3.get_vector(word)
        #print(v1.shape)
        #print(v2.shape)
        #print(weights[i].shape)
        
        if norm:
            s1 = mag1/np.linalg.norm(v1)
            s2 = mag2/np.linalg.norm(v2)
            s3 = mag3/np.linalg.norm(v3)
        else:
            s1 = mag1
            s2 = mag2
            s3 = mag3
            
        weights[i] = np.concatenate((s1 * v1, s2 * v2, s3 * v3))
        wordlist.append(word)

    combined = KeyedVectors(model1.vector_size + model2.vector_size + model3.vector_size)
    combined.add(wordlist, weights)
    if outpath != None:
        combined.save_word2vec_format(outpath)
    return combined

# dim reducing a model
def dim_reduce(model, target_dim, start_idx=0, outpath=None):
    pca = PCA(n_components=target_dim, svd_solver='arpack')
    X = model[model.wv.vocab][start_idx:]
    result = pca.fit_transform(X)
    
    wordlist = []
    for i, word in enumerate(model.vocab):
        if i >= start_idx:
            wordlist.append(word)
    
    reduced_model = KeyedVectors(target_dim)
    reduced_model.add(wordlist, result) 
    if outpath != None:
        reduced_model.save_word2vec_format(outpath)
    return reduced_model

# removing the first D singular components
def PPA(model, D, start_idx=0, outpath=None):
    X = model[model.wv.vocab][start_idx:]
    U, S, VT = np.linalg.svd(X, full_matrices=False)
    S[:D] = 0
    result = np.matmul(U, np.matmul(np.diag(S), VT))
    
    wordlist = []
    for i, word in enumerate(model.vocab):
        if i >= start_idx:
            wordlist.append(word)
            
    reduced_model = KeyedVectors(X.shape[1])
    reduced_model.add(wordlist, result)
    
    if outpath != None:
        reduced_model.save_word2vec_format(outpath)
    return reduced_model