# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 23:36:56 2020

@author: Admin
"""
import string

def words_from_file(file, output):
    words = []
    f = open(file, 'r', encoding="latin-1")
    o = open(output, 'w', encoding="latin-1")
    for line in f:
        frequency, word = line.split()
        #if (frequency==1): print(frequency)
        if (not any(char in string.punctuation for char in word)):
            if (frequency == "1"):
                x = 0;
            else:
                o.write(str(frequency) + " " + word + "\n")
            #words.append(word)
    o.close()
            
    

file = "wordlist-2007.eng";
output = "wordlist-2007-trimmed.eng";
#read_input(file)
words_from_file(file, output) #(freqency, word)