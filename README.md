## Introduction

Dissertation 'Lexico' is part of my dissertation to analyse and segment morphemes in words in order to analyse previously undiscovered or undocumented languages.  

Examples of use could be to aid educators of languages determining the most popular affixes to teach or could aid researchers wanting to discover more about a particular language.

### Usage

start.bat is a batch script to run the program. It contains all the parameters you might want to use.  
-i is the input word file. The format should be similar to data/wordlist-2007.eng (frequency<space>word<newline>).   
-o is the output file. This will return a wordlist file in their segmented method.  
-g is the gold standard data text to which the output file will be tested against.  
-t is an optional testing file. The program will use -i to test if unspecified. Otherwise it will use this file to test the gold standard against.  

Main.py is the entry point where the functions are run.  
lexotree.py is the data structure class for a Trie node and functions relating to insertion and searching the trie node structure are held.  
morpheme_analysis.py is where the scoring for each morphemes is done as well as the segmentation.  
evaluation.py contains the criteria for evaluating the output file against the gold standard file.  


### Resources

The method has been based on transitional probabilities (likelihood of the next letter being x given the current word is y). This has been shown to be an effective method of segmentation because morphemes are generally concatonative. This work has been based on Keshava and Pitler.
