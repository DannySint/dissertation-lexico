import string
import re
from lexotree import TrieNode
from lexotree import reverse
from itertools import product
import sys

CSV_FORMAT = True
DEBUG = False
SEGMENTATION_MARKER = r'_';
ENCODING = "latin-1"
punish = -1; reward = 19;
threshold = 0.05;


class MorphemeAnalysis:
    def __init__(self, input_file, number=2): #going to get the files to input and output to from the main
        self.input_file = input_file #TODO: Add opts for the wordlist and an output file for the morphemes. And a format option
        self.output_file_suffixes = "data/morphemes_suffixes-multi.csv"
        self.output_file_prefixes = "data/morphemes_prefixes-multi.csv"
        self.number = number
        
        self.words, self.words_check, self.words_reversed, self.words_check_reversed, self.frequency_dict = self.words_from_file()
        self.forward_trie = TrieNode('*')
        self.backward_trie = TrieNode('*')
        
        
        #initialise the affix word scoring
        self.word_score_suffix = dict((key, 0) for key in self.words) #self.word_score_suffix = {}
        self.word_score_prefix = dict((key, 0) for key in self.words) #self.word_score_prefix = {}        
    
        for word in self.words:
            self.forward_trie.add(word) #add(self.forward_trie, word)
            self.backward_trie.add(reverse(word)) #add(self.backward_trie, reverse(word))
            
        #self.pruned_word_score = { key:value for key, value in self.word_score_prefix.items() if value > 0 }
        #word_standard  = open("word_standard-prefix-testing.txt", 'w')
        
        self.pruned_word_score_suffix = {}
        self.pruned_word_score_prefix = {}
        
    def words_from_file(self) -> (list, set, list, set, dict):
        words = []  #much faster with a set here than a list
        words_check = set()
        words_reversed = []
        words_check_reversed = set()
        frequency_dict = dict()
        f = open(self.input_file, 'r', encoding=ENCODING) #latin-1 necessary on some systems not running English locale
        for line in f:
            if " " in line:                
                frequency, word = line.split() #"frequency word" -> _, word (for double column files)
                #word = word.lower();
                #print(line)
                #sys.exit(1)
            else:
                word = line.strip('\n').lower(); frequency = 0; #"word" ->  word (for single column files)
                #print(word); #sys.exit(1) #TODO: Fix this
            punctuation = any(char in string.punctuation for char in word)
            #TODO: Fix this probably
            #TODO: experiment with changing frequency allowed
            if (not punctuation) and ((int(frequency) == 0) or (int(frequency) >= self.number)):
                frequency_dict[word] = int(frequency)
                words.append(word)
                words_check.add(word)
                words_reversed.append(reverse(word))
                words_check_reversed.add(reverse(word))
        return words, words_check, words_reversed, words_check_reversed, frequency_dict


    #TODO: Implement Multicore processing for each different character child of the root.
    def score_suffixes(self, debug=DEBUG):
        if DEBUG: print("Running score_suffixes");
        """
        Loops through all the words to send to is_suffix
        Split words up into multi processing so it's much faster
        """
        for word in self.words:
            #add word to word_score{} with 0
            #if len(word) > 1: #no point in doing 1 letter characters.
            self.is_suffix(word[:-1], word, DEBUG)

    #recursive function that returns a suffix if the 3 conditions are met
    #for a clearer insight into the variables of this algorithm doc/is_suffix.png
    #TODO: Test if weighting the words by their frequency/total word frequency and scoring them that way is better
    def is_suffix(self, current_suffix, original, debug=DEBUG): #current_suffix is more like current_prefix
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
            if ((len(first_part) != 0) and (first_part in self.words_check)): #find_prefix(forward_trie, first_part)[0] 
                second_condition = self.forward_trie.probability(first_part_cut, first_part, DEBUG)
                if ((second_condition > 1 - threshold) and (second_condition < 1 + threshold)): #close to 1 (#TODO: Test for closer values)
                    #third condition
                    third_condition = self.forward_trie.probability(first_part, first_part_uncut, DEBUG)
                    if (third_condition < 1):
                        self.word_score_suffix[second_part] = self.word_score_suffix.get(second_part, 0) + (reward) + 1; #20 instead of 19 because they'll be -1'd anyway. It avoids a few elses #morphemes might not in the original wordlist     
            self.word_score_suffix[second_part] = self.word_score_suffix.get(second_part, 0) + punish;
            self.is_suffix(current_suffix[0:-1], original, DEBUG) #recursively cut off the last letter

    def score_prefixes(self, DEBUG):
        for word in self.words:
            if len(word) > 1:
                self.is_prefix(word[:1], word, DEBUG)
                
    #go through each word backwards and test the 3 conditions outlined in 2.2   
    def is_prefix(self, current_prefix, original, debug=DEBUG):
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
            if ((second_part in self.words_check) ): #and (not (second_part == original))
                second_condition = self.backward_trie.probability( reverse(second_part), reverse(second_part_cut), DEBUG) #could be switch cut and normal way round?
                if ((second_condition > 1 - threshold) and (second_condition < 1 + threshold)): #close to 1 (#TODO: Test closer values)
                    third_condition = self.backward_trie.probability( reverse(second_part), reverse(second_part_uncut), DEBUG)
                    if (third_condition < 1):
                        if (first_part in self.word_score_prefix):
                            self.word_score_prefix[first_part] = self.word_score_prefix.get(first_part, 0) + (reward) + 1 #20 instead of 19 because they'll be -1'd anyway. It avoids a few elses #morphemes might not in the original wordlist 
                self.word_score_prefix[first_part] = self.word_score_prefix.get(first_part, 0) + punish;#self.word_score_prefix[first_part] -= 1; #if second part is not in words we don't care
            prefix_length = len(current_prefix)
            self.is_prefix(current_prefix + original[prefix_length :prefix_length+1], original, DEBUG) #recursively add on a new letter


    def prune_affixes(self, word_score):
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

    def get_morphemes(self, pruned_word_score, output_file, csv=CSV_FORMAT) -> list:
        """
        Loop that outputs all the morphemes in word_score
        """
        o = open(output_file, 'w', encoding=ENCODING)
        morpheme_list = []
        word_score = pruned_word_score
        for word_pair in word_score:
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

    def segment_suffix(self, word, debug=DEBUG) -> str:
        suffix_list = []
        prefix_list = []
        for i in reversed(range(len(word))):
            #split = len(word)- i
            first_part = word[:i]
            second_part = word[i:]
            if second_part in self.pruned_word_score_suffix:
                prefix_list.append(first_part)
                suffix_list.append(second_part) #only 2 morpheme split
        if DEBUG: print(prefix_list)
        if DEBUG: print(suffix_list)
        
        potential_morphemes = {}
        for i in range(len(prefix_list)): #TODO: Write as a list comprehension
            if DEBUG: print(prefix_list[i] + suffix_list[i][:1])
            if DEBUG: print(prefix_list[i])
            
            peel = self.forward_trie.probability(prefix_list[i], prefix_list[i] + suffix_list[i][:1]) #Prf(B|alpha)
            if DEBUG: print(peel)
            if peel < 1:# Probability(B|alpha) = Probability(alpha + B) / Probability (B) = probability(alpha + B, alpha)
                potential_morphemes[suffix_list[i]] = peel
            if DEBUG: print()
        if DEBUG: print(potential_morphemes)
        if DEBUG: print("Min " + str(min(potential_morphemes, key=potential_morphemes.get, default=0)))
        lowest_morpheme = str(min(potential_morphemes, key=potential_morphemes.get, default=0))
        
        if (potential_morphemes == {}) or lowest_morpheme == 0:
            if DEBUG: print("Potential_morphemes is empty")
            return self.segment_prefix(word, DEBUG) #return self.segment_prefix(word)
        else: #peel apart the morphemes now
            first_part = word[0:0-len(lowest_morpheme)]
            if DEBUG: print("not empty")
            
            edited_word =  str(first_part + SEGMENTATION_MARKER + lowest_morpheme)
            #if DEBUG: print("Suffix: " + edited_word)
            return self.segment_prefix(edited_word, DEBUG)
        
    def segment_prefix(self, word, debug=DEBUG) -> str:
        suffix_list = []
        prefix_list = []
        for i in range(len(word)):
            if i == SEGMENTATION_MARKER: #no point going past the segmentation point
                break; #return segment_prefix(word)
            first_part = word[:i]
            second_part = word[i:]
            if first_part in self.pruned_word_score_prefix and (len(first_part) != 1):
                prefix_list.append(first_part)
                suffix_list.append(second_part)
        if DEBUG: print(suffix_list)
        potential_morphemes = {}
        if ((prefix_list == []) or (suffix_list == [])):
            return word
        for i in range(len(prefix_list)): #doesn't matter if it's prefix or suffix list, just pick one. 
            current_suffix = suffix_list[i].replace(SEGMENTATION_MARKER, "")
            peel = self.backward_trie.probability(reverse(prefix_list[i][-1] + current_suffix), reverse(current_suffix))
            if peel < 1:
                potential_morphemes[prefix_list[i]] = peel #
        
        lowest_morpheme = str(min(potential_morphemes, key=potential_morphemes.get, default=0))
            
        if (potential_morphemes == {}) or (lowest_morpheme == 0):
            if DEBUG: print("Potential_morphemes is empty")
            return word
        else: #peel apart the morphemes now
            second_part = word[0+len(lowest_morpheme):]
            if DEBUG: print("Lowest_morpheme: " + lowest_morpheme)
            if DEBUG: print("Second part: " + second_part)
            if DEBUG: print(str(lowest_morpheme + SEGMENTATION_MARKER + second_part))
            edited_word = str(lowest_morpheme + SEGMENTATION_MARKER + second_part).replace(SEGMENTATION_MARKER*2, SEGMENTATION_MARKER)
            return  edited_word #morphemes might be segmented in the same position
            
def decompose_words(self, word, word_score) -> [()]: #return a list of potential tuples containing the morpheme pairs
    #should it choose the best one? Can it even do that..
    print("ff@20")

def isSplittable(self, word, k):
    """
    The start of making words splittable into multiple morphemes.
    """
    word_parts = {} #word_parts needs to be a dictionary with the word pieces and then score
    #word_parts = {{un, re, quit, ed:10},{desu:0}}x
    if ((word == "") or (k == 0)):
        print(word + " was empty or k==0?");
        return ((word == "") and (k == 0))
    
    for i in range(len(word)):
        first = word[0:i]; last = word[i:]
        
        if ((first in self.words_check) and (last in self.words_check)):
            word_parts[first] = word_parts.get(first, 0) + 1; word_parts[last] = word_parts.get(last, 0) + 1; 
            #print("First: " + first)
            #print("Last: " + last)
            #print()
        if (first in self.words_check) and (isSplittable(last, k-1)):
            print("Solution: " + first + " + " + last)
            return True;
    print(word_parts)
    return False

#def testScoring():
#    ma = MorphemeAnalysis("data/wordlist-2007.eng") 
#    ma.is_suffix("report", "reports")
#    ma.is_suffix("mountain", "mountains")
#    ma.is_prefix("re", "reports")
#    ma.is_prefix("re", "report")
#    ma.is_prefix("re", "retaking")
#    ma.is_prefix("re", "resupply")
#    pruned_suffixes = ma.prune_affixes(ma.word_score_suffix)
#    pruned_prefixes = ma.prune_affixes(ma.word_score_prefix)
#    print(pruned_suffixes)
#    print(pruned_prefixes)
#
#if __name__ == '__main__':
#    ma = MorphemeAnalysis("data/wordlist-2007.eng") 
#    ma.score_prefixes(False);
#    ma.pruned_word_score_prefix = ma.prune_affixes(ma.word_score_prefix); 
#    prefix_list = ma.get_morphemes(ma.pruned_word_score_prefix, ma.output_file_prefixes);
#    
#    ma.score_suffixes(False); 
#    ma.pruned_word_score_suffix = ma.prune_affixes(ma.word_score_suffix); 
#    suffix_list = ma.get_morphemes(ma.pruned_word_score_suffix, ma.output_file_suffixes);
#    print(ma.segment_suffix("results"))
#    print(ma.segment_suffix("staying"))
#    print(ma.segment_suffix("falling"))
#    print(ma.segment_suffix("purchased"))
#    print(ma.segment_suffix("root"))
#    print(ma.segment_suffix("beneficiaries"))
#    print(ma.segment_prefix("disillusion"))
#    print(ma.segment_prefix("unhappy"))
#    print(ma.segment_prefix("undoing"))
#    print(ma.segment_prefix("unfold"))
#    print(ma.segment_prefix("disability"))
    