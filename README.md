# Neural Code Translator

Neural Code Translator provides instructions, datasets, and a deep learning infrastructure (based on [seq2seq](https://google.github.io/seq2seq/)) that aims at learning *code transformations*.
An Recurrent Neural Network (RNN) Encoder-Decoder model is trained to learn, from a set of known transformations, to translate the code *before* a transformation to the code *after*.

The set of known transformation defines the behavior of the model, and the expected translations. One can instantiate and train a specific model that aims at performing particular types of code transformations. Here is a list of potential models, where in parenthesys we report the code (*before* -> *after*):
- Bug Fixing (buggy -> fixed);
- Mutation (fixed -> buggy);
- Refactoring (original -> refactored);
- Code Review (original -> reviewed);
- Code Smells (smelly -> clean);
- any other types of changes.

## Code Transformations
We formally define *code transformation* as a pair of code fragments (*code_before*, *code_after*), where *code_after* is the code obtained after some particular changes applied to *code_before*. The types, locations, and number of changes applied to the code can vary. There can be many different types of code transformations, such as: bug-fixes, refactorings, and many other maintenance operations. These code transformations can be mined from source code repositories, issue trackers, and code review systems. We provide mined code transformations:
- [Bug-Fixes](https://sites.google.com/view/learning-fixes/data)
- [Code Reviews](https://sites.google.com/view/learning-codechanges/data)

We used code transformaitons ad method-level granularities, however other granularities, such as fragment, class or file could be used.

## Representing Source Code
The sequence-to-sequence model `seq2seq` expects the input, and the corresponding target output, to be represented as a stream of tokens in a single line (one line for the input, one line for the output), in a parallel corpus. Therefore, the source code in (*code_before*, *code_after*) needs to be represented as two lines. Different types of pre-processing can be applied at this stage. 

We suggest to use our tool [src2abs](https://github.com/micheletufano/src2abs), which relies on a Java Lexer and Parser to generate an abstracted version of the source code. The abstracted version contains Java keywords and separators, while the identifiers and literals are replaced with particular typified IDs. A list of identifiers/literals that need to be preserved in the abstract representation can be specified (*i.e.,* idioms). More info can be found in the [src2abs](https://github.com/micheletufano/src2abs) GitHub repository.

Particular attention should be observed when deciding the vocabulary, that is the total number of unique tokens in the corpus. In src2abs you can control the size of the vocabulary with the number of idioms considered. We suggest to cap the vocabulary to no more than 1,000 tokens.

## Datasets
In this repository we provide two large datasets of code transformations in the parallel corpus format. The datasets `bug-fixes` and `reviews` can be found in the folder `datasets/`. Each dataset is split in three folders:
- `train`: code transformations used for training the model (80% of the data);
- `eval`: code transformations used for validation of the model (10% of the data);
- `test`: code transformations used for testing the model (10% of the data);

Each folder contains two files:
- `buggy.txt` : the source code before the code transformation;
- `fixed.txt` : the source code after the code transformation;

The two pair of files represent a parallel corpus, where the i-th line in buggy.txt and the i-th line in fixed.txt reprensent the i-th transformation pair (*code_before*, *code_after*).

## Installation
Before using the scripts provided in this repository, make sure to have a working installation of [seq2seq](https://google.github.io/seq2seq/). Run some example tests to make sure that all the required libraries are installed and running properly.
Next, download the content of this repository.

## Model & Configurations
`seq2seq` implements an NMT model comprising an Encoder and Decoder, both are RNN that are trained jointly. The Encoder encodes a sequence of terms *x* into a vector representation *h*, while the Decoder decodes the representation *h* into  a sequence of terms *y*, representing the transalation of *x*.

The model can be configured in terms of number of layers, units, type of RNN cells, optimizer, etc.
We provide 20 sample configurations in the `seq2seq/configs` folder, 10 for small-sized sentences (no longer than 50 tokens), and 10 for medium-sized sentences (no longer than 100 tokens). This table provides an overview of the configurations:

| ID | Embedding | Encoder #Layers |  Encoder #Units | Decoder #Layers | Decoder #Units | Cell Type | 
| --- | --- | --- | --- | --- | --- | --- | 
|1|256|1|256|2|256|GRU|
|2|256|1|256|2|256|LSTM|
|3|256|2|256|4|256|GRU|
|4|256|2|256|4|256|LSTM|
|5|256|2|512|4|512|GRU|
|6|256|2|512|4|512|LSTM|
|7|512|2|512|4|512|GRU|
|8|512|2|512|4|512|LSTM|
|9|512|1|256|2|256|GRU|
|10|512|1|256|2|256|LSTM|

New configurations can be created by editing the `.yml` files.

## Training & Testing
In the folder `seq2seq` we provide additional scripts that facilitate the training and testing of the NMT model.
The script `train_test.sh` trains and tests the model on a given dataset:
```
./train_test.sh <dataset_path> <num_iterations> <model_path> <config_ID>
```
Arguments:
- `dataset_path` : path to the dataset containing the folders: train, eval, test (e.g., see `dataset` folder);
- `num_iterations` : number of training iterations;
- `model_path` : path where to save the model's checkpoints and predictions;
- `config_ID` : ID of the configuration to be used. The IDs are the file names (without the `.yml` extension) available in the folder `config`

### Example
```
mkdir -p ../model/bug-fixes/small/
./train_test.sh ../dataset/bug-fixes/small/ 50000 ../model/bug-fixes/small/ small_10
```

## Inference
The script `inference.sh` performs inference on a trained model. The inference is performed using Beam Search. The following figure shows an example of Beam Search with beam width *k* = 3.

<p align="center">
  <img src="https://drive.google.com/uc?export=view&id=1Nh5AtRLq9EX4u_H9phYVvhF6MYEtdgmb"/>
</p>

The values of *k* can be specified in the script where the `beam_widths` array is initialized (line #20).
```
./inference.sh <dataset_path> <model_path>
```
Arguments:
- `dataset_path` : path to the dataset containing the folders: train, eval, test (e.g., see `dataset` folder). Only the data in `test` is used during inference;
- `model_path` : path of the trained model;

### Example
```
./inference.sh ../dataset/bug-fixes/small/ ../model/bug-fixes/small/
```

## Credits
`NeuralCodeTranslator` was built by [Michele Tufano](http://www.cs.wm.edu/~mtufano/) on top of [seq2seq](https://google.github.io/seq2seq/), and used and adapted in the context of the following research projects. If you are using `NeuralCodeTranslator` for research purposes, please cite:

[1] On Learning Meaningful Code Changes via Neural Machine Translation
[2] An Empirical Study on Learning Bug-Fixing Patches in the Wild via Neural Machine Translation

## Bibliography
### [1] On Learning Meaningful Code Changes via Neural Machine Translation
```
@inproceedings{Tufano-Learning-CodeChanges,
    Author = {Michele Tufano and Jevgenija Pantiuchina and Cody Watson and Gabriele Bavota and Denys Poshyvanyk},
    title = {On Learning Meaningful Code Changes via Neural Machine Translation},
    booktitle = {Proceedings of the 41st International Conference on Software Engineering},
    series = {ICSE '19},
    year = {2019},
    location = {Montréal, Candada},
    numpages = {12}
}
```
### [2] An Empirical Study on Learning Bug-Fixing Patches in the Wild via Neural Machine Translation
```
@article{DBLP:journals/corr/abs-1812-08693,
  author    = {Michele Tufano and Cody Watson and Gabriele Bavota and Massimiliano Di Penta and Martin White and Denys Poshyvanyk},
  title     = {An Empirical Study on Learning Bug-Fixing Patches in the Wild via Neural Machine Translation},
  journal   = {CoRR},
  volume    = {abs/1812.08693},
  year      = {2018}
}
```
