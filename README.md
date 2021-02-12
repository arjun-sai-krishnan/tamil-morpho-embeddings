# tamil-morpho-embeddings

### Welcome

## Table of Contents

### [1 Setup and Preprocessing](#preprocessing)
### [2_Analogy Dataset](#dataset)
### [3 Training Embeddings](#training)
### [4 Meta-Embeddings and Evaluation](#evaluation)
### [5 Acknowledgements](#acknowledgements)

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

Code for assembling the tetrads from these pairs and optionally filtering out out-of-vocabulary words can be found in ```1. Analogy Dataset Setup.ipynb```.

## <a name=training></a>3 Training

## <a name=evaluation></a>4 Meta-Embeddings and Evaluation

## <a name=acknowledgements></a>5 Acknowledgements
