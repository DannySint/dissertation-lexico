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