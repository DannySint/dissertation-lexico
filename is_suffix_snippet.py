word_score = {} #{reports: 19}

def is_suffix(current_suffix, original, debug=True):
    if (current_suffix == ""): #exit conditions
        return "*";
    else:
        split = (len(original)-len(current_suffix)) #the position at which the word is split 12 - 11 = 11 or -1
        first_part_uncut = original[0:split+1]
        first_part = original[0:split]
        first_part_cut = first_part[0:-1]
        second_part = original[split:];
        
        if ((len(first_part) != 0) and (first_part in words_check)):
            around_one = probability(forward_trie, first_part_cut, first_part, debug)
            if ((around_one > 0.95) and (around_one < 1.05)): #close to 1
                third_part = probability(forward_trie, first_part, first_part_uncut, debug)
                if (third_part < 1):
                    if (second_part in word_score):    
                        word_score[second_part] += 20; #19 because they won't be -1'd
                    else:
                        word_score[second_part] = 20; #morphemes might not in the original wordlist 
        word_score[second_part] = word_score.get(second_part, 0) - 1;
        is_suffix(current_suffix[0:-1], original, debug) #recursively cut off the last letter