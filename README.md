# tamil-morpho-embeddings

### Welcome

## Table of Contents

### [1 Setup and Preprocessing](#preprocessing)
### [2 Training Embeddings](#training)
### [3 Meta-Embeddings and Evaluation](#evaluation)
### [4 Acknowledgements](#acknowledgements)

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

## <a name=training></a>2 Training

## <a name=evaluation></a>3 Meta-Embeddings and Evaluation

## <a name=acknowledgements></a>4 Acknowledgements
