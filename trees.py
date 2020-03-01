import string
import re
from lexotree import TrieNode
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
#TODO: Test if weighting the words by their frequency/total word frequency and scoring them that way is better
def is_suffix(current_suffix, original, debug=True): #current_suffix is more like current_prefix
    """
    Gets the potential suffix (more like prefix) as well as the unaltered original
    original could technically be a global variable as it remains unchanged throughout one is_suffix call
    Stores the cut, uncut, and normal of the first part as well as the second part of the original based on the current_suffix
    Runs through the 3 conditions outlined in Pitler & Keshava (2007):
        whether the normal is in the word list
        Whether the normal word frequency / cut word frequency is around 1
        Whether the uncut word frequency / normal word frequency is less than 1
    If all these conditions are passed then the second part of the word has it's score raised by 19
    If it doesn't the second part of the word's score is reduced by 1
    This simulates a 0.05 (arbitrary) passrate (the second word -potential morpheme- needs to pass 95% of the time.)
    Returns once the word is finished
    """
    if (current_suffix == ""): #exit conditions
        return "*";
    else:
        # 3 conditions for possible suffix
        split = (len(original)-len(current_suffix)) #the position at which the word is split 12 - 11 = 11 or -1
        first_part_uncut = original[0:split+1]
        first_part = original[0:split]
        first_part_cut = first_part[0:-1]
        second_part = original[split:];
        if ((len(first_part) != 0) and (first_part in words_check)): #find_prefix(forward_trie, first_part)[0] 
            second_condition = forward_trie.probability(first_part_cut, first_part, debug)
            if ((second_condition > 0.95) and (second_condition < 1.05)): #close to 1 (#TODO: Test for closer values)
                #third condition
                third_condition = forward_trie.probability(first_part, first_part_uncut, debug)
                if (third_condition < 1):
                    word_score_suffix[second_part] = word_score_suffix.get(second_part, 0) + 20; #20 instead of 19 because they'll be -1'd anyway. It avoids a few elses #morphemes might not in the original wordlist     
        word_score_suffix[second_part] = word_score_suffix.get(second_part, 0) - 1;
        is_suffix(current_suffix[0:-1], original, debug) #recursively cut off the last letter

#go through each word backwards and test the 3 conditions outlined in 2.2   
def is_prefix(current_prefix, original, debug=True):
    """
    Gets the potential prefix (more like suffix) as well as the unaltered original
    original could technically be a global variable as it remains unchanged throughout one is_prefix call
    Stores the first part of the original word divided by the split as well as the cut, uncut, and normal of the second part from the split.
    Runs through the 3 conditions outlined in Pitler & Keshava (2007):
        whether the second part of the word is in the word list
        Whether the cut word frequency / normal word frequency is around 1
        Whether the uncut word frequency / normal word frequency is less than 1
    If all these conditions are passed then the second part of the word has it's score raised by 19
    If one of these tests doesn't pass, the second part of the word's score is reduced by 1
    This simulates a 0.05 (arbitrary) passrate (the first word -potential morpheme- needs to pass 95% of the time.)
    Returns once the word is finished
    """
    if (current_prefix == original): #exit conditions
        return "*";
    else:
    #go backwards
        # 3 conditions for possible suffix
        split = (len(original)-len(current_prefix)) #the position at which the word is split 12 - 11 = 11 or -1
        first_part = original[0:split] #STILL Bb
        second_part = original[split:];
        second_part_cut = second_part[1:]; 
        second_part_uncut = original[split-1:len(original)];
        if ((second_part in words_check) ): #and (not (second_part == original))
            second_condition = backward_trie.probability( reverse(second_part), reverse(second_part_cut), debug) #could be switch cut and normal way round?
            if ((second_condition > 0.95) and (second_condition < 1.05)): #close to 1 (#TODO: Test closer values)
                third_condition = backward_trie.probability( reverse(second_part), reverse(second_part_uncut), debug)
                if (third_condition < 1):
                    if (first_part in word_score_prefix):
                        word_score_prefix[first_part] = word_score_prefix.get(first_part, 0) + 20 #20 instead of 19 because they'll be -1'd anyway. It avoids a few elses #morphemes might not in the original wordlist 
            word_score_prefix[first_part] = word_score_prefix.get(first_part, 0) - 1;#word_score_prefix[first_part] -= 1; #if second part is not in words we don't care
        prefix_length = len(current_prefix)
        is_prefix(current_prefix + original[prefix_length :prefix_length+1], original, debug) #recursively add on a new letter


def score_prefixes(debug):
    for word in words:
        if len(word) > 1:
            is_prefix(word[:1], word, debug)

#TODO: Implement Multicore processing for each different character child of the root.
def score_suffixes(debug):
    """
    Loops through all the words to send to is_suffix
    Split words up into multi processing so it's much faster
    """
    #word_pairs = [[word[:-1], word] for word in words if len(word) > 1]#create list of [word[:-1], word]'s
    #print(word_pairs)
#    word_pairs = [ ["wor","word"], ["report","reports"] ]
#    with multiprocessing.Pool(processes=2) as pool:
#        pool.map(is_suffix, word_pairs)
        
        
        #pool.starmap(is_suffix, product(word[:-1], word, debug, repeat=2))
    for word in words:
        #add word to word_score{} with 0
        if len(word) > 1: #no point in doing 1 letter characters.
            is_suffix(word[:-1], word, debug)    

def prune_affixes(word_score):
    """
    Go through the morphemes list 
    where a morpheme is comprised of 2 morphemes
    and
    Those 2 smaller morphemes have a higher score than the first morpheme
    Then remove the original morpheme 
    TODO: Test if adding the original morphemes score to the 2 smaller morphemes affects anything.
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
    
def decomposed_words(word, word_score) -> [()]: #return a list of potential tuples containing the morpheme pairs
    #should it choose the best one? Can it even do that..
    print("ff@20")

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


csv_format = True
def get_morphemes(pruned_word_score, output_file, csv=csv_format) -> list:
    """
    Simple loop that outputs all the morphemes in word_score
    """
    o = open(output_file, 'w')
    morpheme_list = []
    word_score = pruned_word_score
    for word_pair in word_score:
        #print('word_pair',word_pair)
        #print(word_score[word_pair])
        if (word_score[word_pair] != 0):
            morpheme_list.append(word_pair)
    #print(word_score)
    sorted_word_score = {key: value for key, value in sorted(word_score.items(), key=lambda item: item[1], reverse=True)}
    for word_pair in sorted_word_score:
        if csv:
            o.write(word_pair + "," + str(sorted_word_score[word_pair]) + "\n")
        else:
            o.write(word_pair + " Score: " + str(sorted_word_score[word_pair]) + "\n")
    return morpheme_list

def segment_suffix(word, debug=False) -> str:
#    for word in words:#go through the list of words
#        if word in word_score_suffix: #if a word is a morpheme just leave it
#            print(word + " is a morpheme")
#            return word
#        else: #if it's not:
#            #scan the word from beginning to end
    suffix_list = []
    prefix_list = []
    for i in reversed(range(len(word))):
        #split = len(word)- i
        first_part = word[:i]
        second_part = word[i:]
        if second_part in pruned_word_score_suffix:
            #affix_list.append([first_part, second_part]) #only 2 morpheme split currently.#TODO: Add k splitting
            prefix_list.append(first_part)
            suffix_list.append(second_part) #only 2 morpheme split
    if debug: print(prefix_list)
    if debug: print(suffix_list)
    
        #compare Prb values
        #list comprehension getting the lowest value iff the Prx value is < 1
        #even_squares = [x * x for x in range(10) if x % 2 == 0]
    potential_morphemes = {}
    #prefix_list = ["report", "repor", "repo",  "re"]
    #suffix_list = ['s', 'ts', 'rts', 'ports']
    for i in range(len(prefix_list)): #TODO: Write as a list comprehension
        if debug: print(prefix_list[i] + suffix_list[i][:1])
        if debug: print(prefix_list[i])
        
        peel = forward_trie.probability(prefix_list[i], prefix_list[i] + suffix_list[i][:1]) #Prf(B|alpha)
        #not sure this is right... shouldn't the first argument be the full word?
        if debug: print(peel)
        if peel < 1:# Probability(B|alpha) = Probability(alpha + B) / Probability (B) = probability(alpha + B, alpha)
            potential_morphemes[suffix_list[i]] = peel
        if debug: print()
    if debug: print(potential_morphemes)
    if debug: print("Min " + str(min(potential_morphemes, key=potential_morphemes.get, default=0)))
    lowest_morpheme = str(min(potential_morphemes, key=potential_morphemes.get, default=0))
    #prefix_list = [['report','s'],['repor','ts'],['repo','rts'],['re','ports']]
    #potential_morphemes = [suffix[1] for suffix in suffix_list if forward_trie.probability(suffix, ) < 1]
    
    #potential_morphemes = min([suffix[1] for suffix_list if forward_trie.probability(suffix) < 1], default=0)
    if (potential_morphemes == {}) or lowest_morpheme == 0:
        if debug: print("Potential_morphemes is empty")
        return segment_prefix(word, debug) #return segment_prefix(word)
    else: #peel apart the morphemes now
        first_part = word[0:0-len(lowest_morpheme)]
        if debug: print("not empty")
        return segment_prefix(str(first_part + "_" + lowest_morpheme), debug)
        #return segment_prefix(str(first_part + "_" + lowest_morpheme))
        #word = potential_morphemes
        
def segment_prefix(word, debug=True) -> str:
    if debug: print("Starting segment prefix with " + word)
    suffix_list = []
    prefix_list = []
    for i in range(len(word)):
        if i == '+': #no point going past the +
            break; #return segment_prefix(word)
        first_part = word[:i]
        second_part = word[i:]
        if first_part in pruned_word_score_prefix:
            prefix_list.append(first_part)
            suffix_list.append(second_part)        
    if debug: print(prefix_list)
    if debug: print(suffix_list)
    potential_morphemes = {}
    if ((prefix_list == []) or (suffix_list == [])):
        return word
    for i in range(len(prefix_list)): #doesn't matter if it's prefix or suffix list, just pick one.
        if debug: print("Suffix_list[i]: " + suffix_list[i])
        if debug: print("prefix_list[i][:1]: " + prefix_list[i][:1])
        #print("prefix list + suffix_list[]: " + prefix_list[i][:1] + suffix_list[i])
        #print("Reversed prefix list + suffix_list[]: " + reverse(suffix_list[:i] + prefix_list[i][:1]))
        if debug: print("First test: " + reverse(suffix_list[i]))
        if debug: print("Second test: " + reverse(prefix_list[i][-1])) #aA B = suffix_list[i]; A = prefix_list[i][:-1]
        if debug: print("Removed + from " + reverse(re.sub('[+]', '',suffix_list[i])));
        #peel = backward_trie.probability(suffix_list[i], reverse(prefix_list[i][:1] + suffix_list[i] ))
        #peel = backward_trie.probability(reverse(suffix_list[:i]), reverse(suffix_list[:i] + prefix_list[i][1]))
        peel = backward_trie.probability(reverse(prefix_list[i][-1]), reverse(re.sub('[+]', '',suffix_list[i]))) 
        if debug: print("Peel: " + str(peel))
        ###### THIS IS PROBABLY INCORRECT ###### 
        if peel < 1:
            potential_morphemes[prefix_list[i]] = peel
        lowest_morpheme = str(min(potential_morphemes, key=potential_morphemes.get, default=0))
        if debug: print(lowest_morpheme)
        if (potential_morphemes == {}) or lowest_morpheme == 0:
            if debug: print("Potential_morphemes is empty")
            return word
        else: #peel apart the morphemes now
            second_part = word[0+len(lowest_morpheme):]
            if debug: print("Lowest_morpheme: " + lowest_morpheme)
            if debug: print("Second part: " + second_part)
            if debug: print(str(lowest_morpheme + "+" + second_part))
            return re.sub('[_][_]', '_',str(lowest_morpheme + "+" + second_part)) #morphemes might be segmented in the same position
file = "data/wordlist-2007.eng" #TODO: Add opts for the wordlist and an output file for the morphemes. And a format option
output_file_suffixes = "data/morphemes_suffixes-multi.csv"
output_file_prefixes = "data/morphemes_prefixes-multi.csv"

word_score_suffix = {}
word_score_prefix = {}


words, words_check, words_reversed, words_check_reversed = words_from_file(file)
forward_trie = TrieNode('*')
backward_trie = TrieNode('*')

for word in words:
    add(forward_trie, word)
    add(backward_trie, reverse(word))
    word_score_suffix[word] = 0;
    word_score_prefix[word] = 0;
debug = False
pruned_word_score = { key:value for key, value in word_score_prefix.items() if value > 0 }
#word_standard  = open("word_standard-prefix-testing.txt", 'w')
word_standard  = open("word_standard.txt", 'w')

if __name__ == "__main__":
    #print(words)
    #forward_trie.pprint(); #backward_trie.pprint();
        
    score_prefixes(False); pruned_word_score_prefix = prune_affixes(word_score_prefix); prefix_list = get_morphemes(pruned_word_score_prefix, output_file_prefixes);
    score_suffixes(False); pruned_word_score_suffix = prune_affixes(word_score_suffix); suffix_list = get_morphemes(pruned_word_score_suffix, output_file_suffixes);
    #word_standard.write(segment_prefix("report+s", True))
    for word in words:
        if len(word) != 1:
            word_standard.write(segment_suffix(word) + "\n")

    
#TODO: Add Evaluation with the Morpho Project Challenges' gold standard