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