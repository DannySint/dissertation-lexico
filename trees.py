import string
import re
from lexotree import TrieNode
from lexotree import find_prefix
from lexotree import add
from lexotree import reverse
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
    words_reversed = []
    words_check_reversed = set()
    f = open(file, 'r', encoding="latin-1")
    for line in f:
        _, word = line.split()
        if (not any(char in string.punctuation for char in word)):
            words.append(word)
            words_check.add(word)
            words_reversed.append(reverse(word))
            words_check_reversed.add(reverse(word))
    return words, words_check, words_reversed, words_check_reversed

#recursive function that returns a suffix if the 3 conditions are met
#for a clearer insight into the variables of this algorithm doc/is_suffix.png
#TODO: Add prefix scoring too
#TODO: Test if weighting the words by their frequency/total word frequency and scoring them that way is better
def is_suffix(current_suffix, original, debug=True): #current_suffix is more like current_prefix
    """
    Gets the potential suffix (more like prefix) as well as the unchanged original
    original could technically be a global variable as it remains unchanged throughout one is_suffix call
    Stores the cut, uncut, normal, and second part of the original based on the current_suffix
    Runs through the 3 conditions outlined in Pitler & Keshava (2007):
        whether the normal is in the word list
        Whether the normal word frequency / cut word frequency is around 1
        Whether the uncut word frequency / normal word frequency is less than 1
    If all these conditions are passed then the second part of the word has it's score raised by 19
    If it doesn't the second part of the word's score is reduced by 1
    This simulates a 0.05 (arbitrary) passrate (the second word -potential morpheme- needs to pass 95% of the time.)
    Returns once the word is finished
    """
    #print("Currently at: " + original) 
    #print("current_suffix: " + current_suffix)
    if (current_suffix == ""): #exit conditions
        return "*";
    else:
    #go backwards
        # 3 conditions for possible suffix
        split = (len(original)-len(current_suffix)) #the position at which the word is split 12 - 11 = 11 or -1
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
        if ((len(first_part) != 0) and (first_part in words_check)): #find_prefix(forward_trie, first_part)[0] 
            if debug: print(first_part + " is a word")
            #around_one = forward_trie.probability(first_part[:1] + first_part[1:], (first_part[:1] + first_part[1:] + second_part)) 
            around_one = forward_trie.probability(first_part_cut, first_part, debug)
            if debug: print(first_part + " value is " + str(around_one))
            if ((around_one > 0.95) and (around_one < 1.05)): #close to 1
                #third condition
                if debug: print(first_part + " passed the 2nd test with a value of " + str(around_one))
                if debug: print("|__ using probability(" + first_part_cut + ", " + first_part + ")")
                third_part = forward_trie.probability(first_part, first_part_uncut, debug)
                if debug: print("Dai Maho:  " + str(third_part));
                if (third_part < 1):
                    #word_score[first_part] += 20; #papers says 19 but the code after this subtracts it by 1 anyway. I thought it might be faster not to add else branches
                    if (second_part in word_score_suffix):    
                        word_score_suffix[second_part] += 20; #19 because they won't be -1'd
                    else:
                        word_score_suffix[second_part] = 20; #morphemes might not in the original wordlist 
                    #leaf = find_prefix(current_suffix)
                    if debug: print("Second part is: " + second_part)
        #print(word_score)
        
        word_score_suffix[second_part] = word_score_suffix.get(second_part, 0) - 1;
        #word_score[second_part] -= 1; #if not in words we don't care
        #if debug: print("first_part: " + first_part + ". Score: " + str(word_score[first_part]))
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
        split = (len(original)-len(current_prefix)) #the position at which the word is split 12 - 11 = 11 or -1
        first_part_uncut = original[0:split+1]
        first_part = original[0:split] #STILL Bb
        first_part_cut = first_part[0:-1]
        second_part = original[split:];
        second_part_cut = second_part[1:]; 
        second_part_uncut = original[split-1:len(original)];
        if debug: print("First Part UnCut before checking: " + first_part_uncut)
        if debug: print("First Part before checking: " + first_part)
        if debug: print("First Part Cut before checking: " + first_part_cut)
        if debug: print("Second Part before checking: " + second_part)
        if debug: print("Second Part before checking: " + second_part_cut)
        #if debug: print()
        if ((second_part in words_check) ): #and (not (second_part == original))
        #if (find_prefix(backward_trie, reverse(first_part))):
        #if (first_part_reversed in words_check): #is Bb a word? #looking for words ENDING in first_part so "strope" 
            #isn't going to work
            if debug: print(first_part + ". Passed through with " + second_part)
            #around_one = backward_trie.probability( first_part_cut, first_part, debug) #could be switch cut and normal way round?
            #around_one = backward_trie.probability( first_part, first_part_cut, debug) #could be switch cut and normal way round?
            around_one = backward_trie.probability( reverse(second_part), reverse(second_part_cut), debug) #could be switch cut and normal way round?
            if debug: print(second_part + " second condition is " + str(around_one) + ". (should be near 1)")
            if ((around_one > 0.95) and (around_one < 1.05)): #close to 1
                #third condition
                if debug: print(second_part + " passed the 2nd test with a value of " + str(around_one))
                if debug: print("|__ using probability(" + first_part_cut + ", " + first_part + ")")
                third_part = backward_trie.probability( reverse(second_part), reverse(second_part_uncut), debug)
                if debug: print("Dai Maho:  " + str(third_part));
                if (third_part < 1):
                    if (first_part in word_score_prefix):    
                        word_score_prefix[first_part] += 20; #19 because they won't be -1'd
                    else:
                        word_score_prefix[first_part] = 20; #morphemes might not in the original wordlist 
                    #leaf = find_prefix(current_suffix)
                    if debug: print("First part is: " + first_part)
            word_score_prefix[first_part] = word_score_prefix.get(first_part, 0) - 1;#word_score_prefix[first_part] -= 1; #if second part is not in words we don't care
        if debug: print()
        prefix_length = len(current_prefix)
        #if debug: print("Current Prefix + 1 " + current_prefix + original[prefix_length :prefix_length+1])
        is_prefix(current_prefix + original[prefix_length :prefix_length+1], original, debug) #recursively add on a new letter


def score_prefixes(debug):
    for word in words:
        if len(word) > 1:
            prefix = is_prefix(word[:1], word, debug)

#TODO: Implement Multicore processing for each different character child of the root.
def score_suffixes(debug):
    """
    Loops through all the words to send to is_suffix
    Split words up into multi processing so it's much faster
    """
#    word_pairs = [[word[:-1], word] for word in words if len(word) > 1]#create list of [word[:-1], word]'s
#    #print(word_pairs)
#    with multiprocessing.Pool(processes=2) as pool:
#        pool.map(is_suffix, word_pairs)
        
        
        #pool.starmap(is_suffix, product(word[:-1], word, debug, repeat=2))
    for word in words:
        #add word to word_score{} with 0
        if len(word) > 1: #no point in doing 1 letter characters.
            suffix = is_suffix(word[:-1], word, debug)


#backward_trie.probability( reverse("eports"), reverse("ports"))


            #is_prefix(reverse("reports")[:1], reverse("reports"))


def prune_affixes(word_score):
    """
    Go through the morphemes list 
    where a morpheme is comprised of 2 morphemes
    and
    Those 2 morphemes have a better score
    Remove the original morpheme
    
    TODO: Perhaps this can be done recursively for 'k' morphemes by splitting morphemes multiple times.
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
    pruned_word_score = { key:value for key, value in word_score.items() if value > 0 }
    return pruned_word_score 
    #return word_score #global variable usage would be preferable.
        

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

word_score_suffix = {}
word_score_prefix = {}
csv_format = True

def get_morphemes(pruned_word_score, csv=csv_format) -> list:
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
            if csv:
                print(word_pair + "," + str(word_score[word_pair]))
            else:
                print(word_pair + " Score: " + str(word_score[word_pair]))
    return morpheme_list

file = "data/wordlist-2007-trimmed.eng" #TODO: Add opts for the wordlist and an output file for the morphemes
output = "data/"
words, words_check, words_reversed, words_check_reversed = words_from_file(file)
forward_trie = TrieNode('*')
backward_trie = TrieNode('*')

for word in words:
    add(forward_trie, word)
    add(backward_trie, reverse(word))
    word_score_suffix[word] = 0;
    word_score_prefix[word] = 0;
debug = True
#print(backward_trie.probability( "s", "", debug))
#print(backward_trie.probability( "st", "s", debug))
#print(backward_trie.probability( "str", "st", debug))
#print(backward_trie.probability( "stro", "str", debug))
#print(backward_trie.probability( "strop", "stro", debug))
#print(backward_trie.probability( "strope", "strop", debug))
#print(backward_trie.probability( "stroper", "strope", debug))
pruned_word_score = { key:value for key, value in word_score_prefix.items() if value > 0 }

#TODO: switch to writing to file instead of outputting to 'log'


#if __name__ == "__main__":
    #print(words)
    #forward_trie.pprint(); #backward_trie.pprint();
score_prefixes(False); pruned_word_score = prune_affixes(word_score_prefix); prefix_list = get_morphemes(pruned_word_score);
#score_suffixes(False); pruned_word_score = prune_affixes(word_score_suffix); suffix_list = get_morphemes(pruned_word_score, False);

    
#TODO: Add Evaluation with the Morpho Project Challenges' gold standard