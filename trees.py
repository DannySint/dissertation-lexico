import string
import re
from lexotree import TrieNode
from lexotree import find_prefix
from lexotree import add
from lexotree import reverse_slicing
import multiprocessing
from itertools import product

#print(string.punctuation)
PATTERN = re.compile("[\d{}]+$".format(re.escape(string.punctuation)))
#print(bool(PATTERN.match("")))
#print(bool(PATTERN.match("'''")))
#print(bool(PATTERN.match("rek'sai")))


def words_from_file(file) -> (list, set):
    words = []  #much faster with a set here than a list
    words_check = set()
    #TODO: Create a data structure that is hashable via it's alphabetical order
    #Needs to be ordered alphabetically but also benefits from O(1) access.
    f = open(file, 'r', encoding="latin-1")
    for line in f:
        _, word = line.split()
        if (not any(char in string.punctuation for char in word)):
            words.append(word)
            words_check.add(word)
    return words, words_check

def read_input(file, punctuation = True):
    wordlistFrequency = []
    f = open(file, 'r', encoding="latin-1")
    x = 0
    for line in f:
        #print(line)
        frequency, word = line.split()
        #print(word + " " + str(PATTERN.match(word)))
        if (not any(char in string.punctuation for char in word)) and punctuation: #removes punctuation.
            wordlistFrequency.append((word, frequency))
        #if (string.punctuation in word.punctuation is []):
        x += 1
            
    print(wordlistFrequency)
    print(x)

'''
Pr_f_(s|report)
Probability of the forward tree of "s" given "report"
Divide the frequency of words starting with "reports" 
by
the frequency of words starting "report"
'''
def probability(trie, str1, str2, debug=False) -> int:
    """
    Returns the probability of Pr_x(str2|str1) (where x is the trie - forward/backward)
    Value should be between 0-1.
    """
    value1 = find_prefix(trie, str1)[1]
    if debug: print("Value of " + str1 + " " + str(value1))
    value2 = find_prefix(trie, str2)[1]
    if debug: print("Value of " + str2 + " " + str(value2))
    return (value2 / value1)
    #return (str1 / str2)
    
#print(probability(forward_trie, "report", "reports")) #should this be between 0 and 1
#print(probability(forward_trie, "e", "correspond")) #should this be between 0 and 1

prefix_list = []
suffix_list = []

#recursive function that returns a suffix if the 3 conditions are met
#for a clearer insight into the variables of this algorithm doc/is_suffix.png
#TODO: Add prefix scoring too
#TODO: Test if weighting the words by their frequency/total word frequency and scoring them that way is better
def is_suffix(current_suffix, original, debug=True):
    #print("Currently at: " + original) 
    #print("current_suffix: " + current_suffix)
    if (current_suffix == ""): #exit conditions
        return "*";
    else:
    #go backwards
        # 3 conditions for possible suffix
        split = 0-(len(original)-len(current_suffix)) #the position at which the word is split 12 - 11 = 11 or -1
        first_part_uncut = original[0:split+1]
        first_part = original[0:split]
        first_part_cut = first_part[0:-1]
        second_part = original[split:];
        #print("Current Word before checking: " + current_word)
        if debug: print("First Part before checking: " + first_part)
        if debug: print("First Part Cut before checking: " + first_part_cut)
        if debug: print("First Part UnCut before checking: " + first_part_uncut)
        #print("Second Part before checking: " + second_part)
        if debug: print()
        if ((len(first_part) != 0) and (first_part in words_check)):
            if debug: print(first_part + " is a word")
            #around_one = probability(forward_trie, first_part[:1] + first_part[1:], (first_part[:1] + first_part[1:] + second_part)) 
            around_one = probability(forward_trie, first_part_cut, first_part)
            if debug: print(first_part + " value is " + str(around_one))
            if ((around_one > 0.95) and (around_one < 1.05)): #close to 1
                #third condition
                if debug: print(first_part + " passed the 2nd test with a value of " + str(around_one))
                third_part = probability(forward_trie, first_part, first_part_uncut)
                if debug: print("Dai Maho:  " + str(third_part));
                if (third_part < 1):
                    word_score[first_part] += 20; #papers says 19 but the code after this subtracts it by 1 anyway. I thought it might be faster not to add else branches
                    if (second_part in word_score):    
                        word_score[second_part] += 19; #19 because they won't be -1'd
                    else:
                        word_score[second_part] = 19; #morphemes might not in the original wordlist 
                    #leaf = find_prefix(current_suffix)
                    if debug: print("Second part is: " + second_part)
        #print(word_score)
            word_score[first_part] -= 1; #if not in words we don't care
            if debug: print("first_part: " + first_part + ". Score: " + str(word_score[first_part]))
            if debug: print()
        is_suffix(current_suffix[0:-1], original, debug) #recursively cut off the last letter

#go through each word backwards and test the 3 conditions outlined in 2.2   
def is_prefix(current_prefix, original, debug=True):
    #print("Currently at: " + original) 
    #print("current_suffix: " + current_suffix)
    if (current_prefix == original): #exit conditions
        return "*";
    else:
    #go backwards
        # 3 conditions for possible suffix
        split = 0-(len(original)-len(current_prefix)) #the position at which the word is split 12 - 11 = 11 or -1
        #first_part_uncut = original[0:split+1]
        first_part = original[0:split]
        #first_part_cut = first_part[0:-1]
        second_part = original[split:];
        second_part_cut = second_part[1:]
        second_part_uncut = original[split-1:len(original)]
        reverse_second_part = reverse_slicing(second_part)
        reverse_second_part_uncut = reverse_slicing(second_part_uncut)
        #print("Current Word before checking: " + current_word)
#        if debug: print("First Part before checking: " + first_part)
#        if debug: print("Second Part before checking: " + second_part)
#        if debug: print("Second Part Cut before checking: " + second_part_cut)
#        if debug: print("Second Part UnCut before checking: " + second_part_uncut)
        #if debug: print()
        if (second_part in words_check):
            if debug: print(first_part + ". " + second_part + " is a word")
            if debug: print("Second Part: " + second_part)
            if debug: print("Second Part UnCut: " + second_part_uncut)
            around_one = probability(backward_trie, reverse_second_part, reverse_second_part_uncut, debug) #could be switch cut and normal way round?
            if debug: print(second_part + " second condition is " + str(around_one) + ". (should be near 1)")
            if ((around_one > 0.95) and (around_one < 1.05)): #close to 1
                #third condition
                if debug: print(second_part + " passed the 2nd test with a value of " + str(around_one))
                third_part = probability(backward_trie, reverse_second_part, reverse_second_part_uncut, debug)
                if debug: print("Dai Maho:  " + str(third_part));
                if (third_part < 1):
                    word_score[second_part] += 20; #papers says 19 but the code after this subtracts it by 1 anyway. I thought it might be faster not to add else branches
                    if (first_part in word_score):    
                        word_score[first_part] += 19; #19 because they won't be -1'd
                    else:
                        word_score[first_part] = 19; #morphemes might not in the original wordlist 
                    #leaf = find_prefix(current_suffix)
                    if debug: print("First part is: " + first_part)
            word_score[second_part] -= 1; #if second part is not in words we don't care
            if debug: print("second_part: " + second_part + ". Score: " + str(word_score[second_part]))
        if debug: print()
        prefix_length = len(current_prefix)
        #if debug: print("Current Prefix + 1 " + current_prefix + original[prefix_length :prefix_length+1])
        is_prefix(current_prefix + original[prefix_length :prefix_length+1], original, debug) #recursively add on a new letter



#TODO: Implement Multicore processing for each different character child of the root.
def score_suffixes(debug):
    """
    Split words up into multi processing so it's much faster
    
    """
    with multiprocessing.Pool() as pool:
        pool.map(is_suffix(), words)
        pool.starmap(is_suffix, product(word[:-1], word, debug, repeat=2))
    for word in words:
        #add word to word_score{} with 0
        if len(word) > 1: #no point in doing 1 letter characters.
            suffix = is_suffix(word[:-1], word, debug)


#probability(backward_trie, reverse_slicing("eports"), reverse_slicing("ports"))

#is_prefix("c", "corresponded")
is_prefix(reverse_slicing("s"), reverse_slicing("reports"))
        #is_prefix("r", "reports")
#is_suffix("corresponde", "corresponded")
#is_suffix("report", "reports");
#report = "reports"
#print(probability(forward_trie, "r", report))
#print(probability(forward_trie, "re", report))
#print(probability(forward_trie, "rep", report))
#print(probability(forward_trie, "repo", report))
#print(probability(forward_trie, "repor", report))
#print(probability(forward_trie, "report", report))
#print(probability(forward_trie, "reports", report))
#print(probability(forward_trie, "repor", "report"))
#print(probability(forward_trie, "correspon", "correspond"))

#corr = "corresponded"
#print(probability(forward_trie, "c", corr))
#print(probability(forward_trie, "co", corr))
#print(probability(forward_trie, "cor", corr))
#print(probability(forward_trie, "corr", corr))
#print(probability(forward_trie, "correspond", corr))
#print()
#print(probability(forward_trie, corr, "c"))
#print(probability(forward_trie, corr, "co"))
#print(probability(forward_trie, corr, "cor"))
#print(probability(forward_trie, corr, "corr"))
#print(probability(forward_trie, corr, "correspond"))

def prune_affixes():
    """
    Go through the morphemes list 
    where a morpheme is comprised of 2 morphemes
    and
    Those 2 morphemes have a better score
    Remove the original morpheme
    
    TODO: Perhaps this can be done recursively for splitting multiple morphemes 
    """
    for word in word_score:
        for letter in range(len(word)):
            first_morpheme = word[0:letter]; #the first word_part
            second_morpheme = word[letter:]; #the second part of the word
            if (first_morpheme in word_score) and (second_morpheme in word_score):
                first_morpheme_score = word_score[first_morpheme] #the score of the first word_part
                second_morpheme_score = word_score[second_morpheme]
            
                if ((first_morpheme_score > word_score[word]) and (second_morpheme_score > word_score[word])):
                    word_score[word] = -1 #flag the morpheme to be deleted
              
        #isSplittable(word, len(word))
        
    #remove all negative scoring words
    pruned_word_score = { key:value for key, value in word_score.items() if value > 0}
    return pruned_word_score 
    #return word_score #global variable usage would be preferable.
        
def pruning_testing():
    word_score = {"s": 5000, "ers": 3000, "er": 4000};
    word_score = prune_affixes()
    print(word_score)

def isSplittable(word, k):
    word_parts = {}
    if ((word == "") or (k == 0)):
        print(word + " was empty or k==0?");
        return ((word == "") and (k == 0))
    
    for i in range(len(word)):
        first = word[0:i]; last = word[i:]
        
        if ((first in words_check) and (last in words_check)):
            word_parts[first] = word_parts.get(first, 0) + 1; word_parts[last] = word_parts.get(last, 0) + 1; 
            #print("First: " + first)
            #print("Last: " + last)
            #print()
        if (first in words_check) and (isSplittable(last, k-1)):
            print("Solution: " + first + " + " + last)
            return True;
    print(word_parts)
    return False
#words = ["re", "ports", "reports", "port", "s"]
#word_score["reports"] = 19; word_score["re"] = 19; word_score["ports"] = 19;
#print("isSplittable(reports)? " + str(isSplittable("reports", len("reports"))));
word_score = {}
def get_morphemes(pruned_word_score) -> list:
    """
    Simple loop that outputs all the morphemes in word_score
    """
    morpheme_list = []
    word_score = pruned_word_score
    for word_pair in word_score:
        #print('word_pair',word_pair)
        #print(word_score[word_pair])
        if (word_score[word_pair] != 0):
            morpheme_list.append(word_pair)
            print(word_pair + " Score: " + str(word_score[word_pair]))
    return morpheme_list

file = "wordlist-2007-trimmed.eng" #TODO: Add opts for the wordlist and an output file for the morphemes
words, words_check = words_from_file(file)
forward_trie = TrieNode('*')
backward_trie = TrieNode('*')
for word in words:
    add(forward_trie, word)
    add(backward_trie, reverse_slicing(word))


for word in words:
    word_score[word] = 0;
    
if __name__ == "__main__":
    #print(words)
    #forward_trie.pprint(); #backward_trie.pprint();
    #score_suffixes(False);
    #pruned_word_score = prune_affixes();
    #get_morphemes(pruned_word_score);
    
#TODO: Add Evaluation with the Morpho Project Challenges' gold standard