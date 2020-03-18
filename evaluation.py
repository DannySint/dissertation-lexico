#Evaluation
class Evaluation:
    def __init__(self, gold_standard_file_input, words_and_morphemes, my_standard_file_input=None):
        self.gold_standard_file = open(gold_standard_file_input, 'r')
        self.gold_standard_dictionary = {}
        #self.create_gold_standard()
        self.my_standard_file = open("word_standard.txt")
        self.words_and_morphemes = words_and_morphemes
        with self.gold_standard_file as gold_standard:
            for line in gold_standard:
            #line = gold_standard.readline();
                word__and_morphemes = line.split(' ')
                original_word = word__and_morphemes[0]
                morphemes = word__and_morphemes[1:]
                morpheme_list = list()
                for morpheme in morphemes:
                    morpheme_isolated = morpheme.split(':')[0]
                    if not (morpheme_isolated in morpheme_list):
                        morpheme_list.append(morpheme_isolated)
                self.gold_standard_dictionary[original_word] = morpheme_list #{ablatives: [ablative, s]}
        
    #def create_gold_standard(self):

        
#print("Morphemes: " + str(morpheme_list))

#print(gold_standard_dictionary)
        
    def compare_mine_to_gold(self, debug):
        print("Starting comparison")
        #with my_standard_file as my_standard:
        #words_and_morphemes = open(self.my_standard_file_input, 'r')
        #self.words_and_morphemes = words_and_morphemes = ["sabah sabah", "sales sale_s", "regulations re_gulat_ions"]
        true_positives = true_negatives = false_positives = false_negatives = 0
        
        for my_word in self.words_and_morphemes: 
            original, segmented_word = my_word.split(' ')#[0]
            #print("Original",original)
            #print("Segmented word",segmented_word)
            if '_' in my_word:
                segmented_words = segmented_word.split('_')
                #print("Segmented words: " + str(segmented_words))
                #go through each morpheme
                if original in self.gold_standard_dictionary: #should be improved to take the position into account as well
                        if debug: print(original + " is in gold_standard dictionary with morphemes: " + str(self.gold_standard_dictionary[original]))
                        for segment in segmented_words:
                            if original in self.gold_standard_dictionary[original]:
                                self.gold_standard_dictionary[original].remove(original) #the morpheme can exist within the list as it's full form e.g. 'relics' == 'relics'
                            
                            if segment in self.gold_standard_dictionary[original]:
                                #for prefixes check only the first
                                #for suffixes check only the last
                                #make sure these are not the same
                                if debug: print(segment + " is in " + str(self.gold_standard_dictionary[original]))
                                true_positives += 1
                                self.gold_standard_dictionary[original].remove(segment) #remove the true_positive found segments    
                            else:
                                if debug: print(segment + " is NOT in " + str(self.gold_standard_dictionary[original]))
                                false_negatives += 1
                            leftovers = len(self.gold_standard_dictionary[original])
                            #true_negatives += leftovers #for anything it doesn't find in the gold dictionary are 
                            false_negatives += leftovers
                        #else:
                            #if the word doesn't exist in the gold standard just ignore it
            else:
                if original in self.gold_standard_dictionary:
                    if original in self.gold_standard_dictionary[original]:
                        #count = 0
                        if original in self.gold_standard_dictionary[original]:
                            self.gold_standard_dictionary[original].remove(original) #the morpheme can exist within the list as it's full form e.g. 'relics' == 'relics'
                        list_length = len(self.gold_standard_dictionary)
                        false_positives += list_length
                    #count how many morphemes the 
                    #discount the case where the gold morpheme == my segment
   
        recall = true_positives / (true_positives + false_positives)
        precision = true_positives / (true_positives + false_negatives)
        f_measure = (2 * precision * recall) / (precision + recall) 
        print("Precision",precision)
        print("Recall",recall)
        print("F-Measure",f_measure)