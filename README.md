# tamil-morpho-embeddings

### Welcome
This repository holds our pipeline and code for our NAACL-SRW 2021 submission, for the paper "Morphology-Aware Meta-Embeddings for Tamil". Here we detail and document the steps of our meta-embeddings pipeline, as shown in the table of contents below, and provide our data as well as source. We also provide here a number of Testing and Evaluation ipynb notebooks that can be used to generate analogies from word pairs, evaluate embeddings on our analogy dataset, and train new embeddings with the methods we describe in the paper. 

## Table of Contents

### [1 Setup and Preprocessing](#preprocessing)
### [2 Analogy Dataset](#dataset)
### [3 Training Embeddings](#training)
### [4 Meta-Embeddings and Evaluation](#evaluation)

## <a name=preprocessing></a>1 Setup and Preprocessing

### 1.1 Requirements

* Python 3
* PyTorch
* langdetect
* NLTK
* numpy
* scikit-learn

### 1.2 Corpus Preprocessing

The first step of corpus preprocessing is to process the XML wikidump (obtainable from [WikiMedia](https://dumps.wikimedia.org)), which we do using Giuseppe Attardi's [WikiExtractor repository](https://github.com/attardi/wikiextractor). Starting from our root directory, run the following commands:

```
cd preprocessing/wikiextractor-master
python WikiExtractor.py XML_DUMP_PATH --output ../corpus --bytes SIZE_OF_DUMP
```

This will create a single text file with the entire corpus at ```preprocessing/corpus/AA/wiki_00```. We note that we modified the code very slightly to exclude headers and footers.

Next, we remove words containing non-Tamil characters and shuffle the corpus, which can be done as follows:

```
cd preprocessing
python tamil_tokenize.py
```

This will create a cleaned corpus text file at ```preprocessing/corpus/cleaned.txt``` and another file with sentences shuffled at ```preprocessing/corpus/cleaned_shuffled.txt```.

## <a name=dataset></a>2 Analogy Dataset

The fundamental component of our dataset is the file ```evaluation/analogies/full_dataset/pairs.txt```. This contains all the pairs forming our dataset. Each row contains one pair annotated by two numbers. The first number identifies the semantic relation between those two words. The second number identifies whether there is a particular morphological relation between those two words. The second number is 0 if either the two words have no morphological relationship or the two words have a morphological relation that does not appear elsewhere in the dataset. Each other morphological relation is identified by a positive integer.

The reason for this labelling is to enable the separation of tetrads into subword and non-subword tetrads. A tetrad is placed in the subword category if both of its constituent pairs belong to the same relation and share the same morphological relation (so the second numbers are the same positive integer). A key describing the relation represented by each id (first number) can be found at ```evaluation/analogies/relation_key.txt```.

Code for assembling the tetrads from these pairs and optionally filtering out out-of-vocabulary words can be found in ```Analogy Dataset Setup.ipynb```.

Below is the list of numbered analogy pair categories with a description, name, and example.


SEMANTIC 
  ----
0 |male-female 
--- | ---
1 |me-my 
--- | --- 
2 | profession-product  
--- | ---
3 | fruit_A-tree_A 
--- | ---
4 | verb_form-noun_form 
--- | ---
5 | animal-young 
--- | ---
6 | kin_elder-kin_young (same gender) 
--- | ---
7 | kin_elder_male-kin_young_female 
--- | ---
8 | kin_elder_female-kin_young_male 
--- | ---
9 | positive-negative 
--- | ---

MORPHOLOGICAL 
10 nom-acc
11 nom-dat
12 adjective-adverb
13 verb-past_respect
14 past-past_completive1_inanimate
15 verb-for_those_who_verb
16 past-past_completive2_male
17 past-past_completive2_female
18 male_past-female_past
19 verb-doer_female
20 verb-doer_male
21 verb-passive_plural_inanimate
22 verb-past_inanimate



## <a name=training></a>3 Training

Our code for training our individual models can be found in the folder ```pytorch-word2vec-master``` and is based on Tzu-Ray Su's [word2vec repository](https://github.com/ray1007/pytorch-word2vec). Our primary addition is the introduction of various atomizers, including n-gram atomizations as in FastText and morphological atomizations. These atomizers can be found at ```pytorch-word2vec-master/word2atoms.py```. The atomizers incorporating morphological segmentation use the rules-based segmenter in ```pytorch-word2vec-master/tamil_segmenter_modified.py```. To construct this segmenter, we took [this rules-based stemmer](https://github.com/rdamodharan/tamil-stemmer) developed by Damodharan Rajalingam in Snowball and converted it to Python using Florian Brucker's [sbl2py repository](https://github.com/torfsen/sbl2py). We then modified the stemmer by hand so that it would record each morpheme as it stripped it away to obtain the stem.

We list below commands for training the three base models evaluated in our paper on a GPU. The following setup command should be run first:

```python3 setup.py build_ext --inplace```

**Trivial atomization:** this is just standard skipgram word2vec.

```python3 main.py --cuda --train [CORPUS_PATH] --output [INPUT_VECTOR_PATH] --atomoutput [INPUT_ATOM_VECTOR_PATH] --ctxoutput [CONTEXT_VECTOR_PATH] --ctxatomoutput [CONTEXT_ATOM_VECTOR_PATH] --losslog [LOSSES_PATH] --cbow 0 --size 300 --window 5 --sample 1e-4 --negative 5 --iter 5 --batch_size 100 --anneal --processes [NUM_PROCESSES] --atomizer word2vec```

**Character 5-grams (FastText model):** this takes character 5-grams of the word, and the entire word itself as atoms. Here we break the word down into "half-letters" when taking n-grams i.e. we break the word down into its full Unicode representation so that many characters that appear to be single Tamil letters are actually being treated as two "half-letters".

```python3 main.py --cuda --train [CORPUS_PATH] --output [INPUT_VECTOR_PATH] --atomoutput [INPUT_ATOM_VECTOR_PATH] --ctxoutput [CONTEXT_VECTOR_PATH] --ctxatomoutput [CONTEXT_ATOM_VECTOR_PATH] --losslog [LOSSES_PATH] --cbow 0 --size 300 --window 5 --sample 1e-4 --negative 5 --iter 5 --batch_size 100 --anneal --processes [NUM_PROCESSES] --atomizer fasttext --minL 5 --maxL 5 --halfletters```

**Morphemes + stem (1-3)-grams (MorphoSeg model):** this takes the stem and constituent morphemes of the word as well as character (1-3)-grams of the stem. Here we work with "whole letters" i.e. each Tamil letter is treated as a single letter.

```python3 main.py --cuda --train [CORPUS_PATH] --output [INPUT_VECTOR_PATH] --atomoutput [INPUT_ATOM_VECTOR_PATH] --ctxoutput [CONTEXT_VECTOR_PATH] --ctxatomoutput [CONTEXT_ATOM_VECTOR_PATH] --losslog [LOSSES_PATH] --cbow 0 --size 300 --window 5 --sample 1e-4 --negative 5 --iter 5 --batch_size 100 --anneal --processes [NUM_PROCESSES] --atomizer morphoseg --minL 1 --maxL 3```

## <a name=evaluation></a>4 Meta-Embeddings and Evaluation

### 4.1 Meta-Embeddings

The code for each of our individual meta-embedding techniques (concatenation and PCA) is available at ```evaluation/metaembeddings.py```, and the construction of our final meta-embedding (including the Merge operation) can be found in ```Meta-Embeddings and Evaluation on Analogy Dataset.ipynb```. Our four base models and our final meta-embedding can all be found in the ```models``` folder.

### 4.2 Evaluation on Analogy Dataset

The code for our evaluation function can be found at ```evaluation/evaluation.py```, and each of our models is evaluated on our test set in ```Meta-Embeddings and Evaluation on Analogy Dataset.ipynb```.
