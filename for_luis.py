words = ["reports","report","re","s"]
words_check = set(words)
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