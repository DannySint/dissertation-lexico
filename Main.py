#CommandLine class partially copied from COM Text Processing by Mark Hepple / Rob Gaizauskas

import sys
import getopt
import string
import time
from test_evaluator import Evaluator

from morpheme_analysis import MorphemeAnalysis
from morpheme_analysis import SEGMENTATION_MARKER
from morpheme_analysis import ENCODING
from evaluation import Evaluation


class CommandLine:
    def __init__(self):
        self.input_file = None
        self.output_file = None
        self.gold_standard_file = None
        opts, args = getopt.getopt(sys.argv[1:],'hi:o:f:g:', ["help", "input", "output", "format", "gold"])
        opts = dict(opts)
        if '-h' in opts:
            self.printHelp()

#        if len(args) == 2:
#            self.keyfile = args[0]
#            self.responsefile = args[1]
#        else:
#            print('\n*** ERROR: must specify precisely 2 arg files (key,response) ***', file=sys.stderr)
#            self.printHelp()
        #Input / Output
        if '-i' in opts:
            self.input_file = opts['-i']
        else:
            self.input_file = None
        if '-o' in opts:
            self.output_file = opts['-o']
        else:
            self.output_file = None
        
        #file format (txt or csv)
        if '-f' in opts:
            self.file_format = opts['-f']
        else:
            self.file_format = 'txt'
        
        if '-g' in opts:
            self.gold_standard_file = opts['-g']
        else:
            self.gold_standard_file = None    
        #self.query_print = '-q' in opts
        #self.print_flat = '-f' in opts
        #self.show_interp_prec = '-I' in opts

#        if '-F' in opts:
#            self.print_terse_flat = True
#            self.show_interp_prec = False
#        else:
#            self.print_terse_flat = False
#
#        if '-x' in opts:
#            self.interp_points = int(opts['-i'])
#        else:
#            self.interp_points = 10

    def printHelp(self):
        print("Sorry, help is currently unavailable.")
        sys.exit()
#        progname = sys.argv[0]
#        progname = progname.split('/')[-1] # strip off extended path
#        help = __doc__.replace('<PROGNAME>', progname, 1)
#        print(help, file=sys.stderr)
#        sys.exit()

if __name__ == '__main__':
    config = CommandLine(); #forward_trie.pprint(); #backward_trie.pprint();
    
    #input_file
    if config.input_file is None:
        config.printHelp()
        print("An input file is required. Program will now exit.")
        sys.exit(1);
    morpheme_analysis = MorphemeAnalysis(config.input_file)
    
    #gold standard file
    if config.gold_standard_file is None:
        config.printHelp()
        print("A gold standard file is required. Program will now exit.")
        sys.exit(1);
    
    #Getting only the most popular words based on frequency
    word_frequency = {}
    
#    with open(config.input_file) as f:
#      if " " in f.readline():
#        for line in f:
#          frequency, words = line.strip('\n').split(' ', 1) #"frequency word" -> _, word (for double column files)
#          word_frequency[words] = int(frequency)
#          sorted_wf = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
#          top_words = sorted_wf[:400]
#          only_words = [wordline[0] for wordline in top_words if (not any(char in string.punctuation for char in wordline[0]))]              
#    print("2")
    
    #Morpheme Analysis Time
    start = time.time(); message ="Starting morpheme analysis..."
    print(message, end=' ')
    morpheme_analysis.score_prefixes(False);
    morpheme_analysis.pruned_word_score_prefix = morpheme_analysis.prune_affixes(morpheme_analysis.word_score_prefix); 
    prefix_list = morpheme_analysis.get_morphemes(morpheme_analysis.pruned_word_score_prefix, morpheme_analysis.output_file_prefixes);
    
    morpheme_analysis.score_suffixes(False); 
    morpheme_analysis.pruned_word_score_suffix = morpheme_analysis.prune_affixes(morpheme_analysis.word_score_suffix); 
    suffix_list = morpheme_analysis.get_morphemes(morpheme_analysis.pruned_word_score_suffix, morpheme_analysis.output_file_suffixes);
    #word_standard.write(segment_prefix("report+s", True))
    finish = time.time()
    print("Finished. Time taken: " + str(finish-start))
    
    #Outputting the list of words in morpheme-segmented form
    word_standard = open(config.output_file, 'w', encoding=ENCODING)
    
    start = time.time(); message = "Writing morphemes to file...";
    print(message, end=' ')
    morphemes = []
    words_and_morphemes = {}
    for word in morpheme_analysis.words: #for words in only_words:
        if len(word) != 1: #TODO: Something about this
            #print(segmented_word)
            segmented_word = morpheme_analysis.segment_suffix(word) # segment -> seg+ment
            
            word_delimiter = word + "\t"
            x = segmented_word.split(SEGMENTATION_MARKER) #[un],[requit],[ed]
            words_and_morphemes[word] = x #[[un],[requit],[ed]] #morphemes.append(x) #{"unrequited":[un,requit,ed]} 
            word_standard.write("" + SEGMENTATION_MARKER.join(x) + "\n") #"" needed to prevent a lot of nulls at beginning
    finish = time.time()
    print("Finished. Time taken: " + str(finish-start))
    
    
    #gold standard part
    gold_file = config.gold_standard_file
    golds = [gold_file]
    results = []
    separator = SEGMENTATION_MARKER
    
    #EVALUATION
    message = "Starting Evaluation... "; start = time.time();
    print(message, end=' ')
    en_gold = r"data/en_gold.txt" #en_gold = config.gold_standard_file;
    my_std = r"word_standard.txt" #my_std = config.output_file
    
    with open(en_gold, 'r') as file:
        arr = [];
        for line in file:
            arr.append(line.strip())

    with open(my_std, 'r', encoding=ENCODING) as file: #uses output file as data.. could.. just get it from the program
        results=[];
        for line in file:
            results.append(line.strip())
    
    results_dict = {result.replace(SEGMENTATION_MARKER, ""):result for result in results} #a dict of clean results
    
    golds = [];
    golds = arr.copy();
    #Creating a list of golds and results that equate the first part
    new_results = []
    for i in range(len(golds)):
        if golds[i].replace("+", "") in results_dict:
            new_results.append(tuple(results_dict[golds[i].replace("+", "")].replace(SEGMENTATION_MARKER, "+").split('+')))
            golds[i] = tuple(golds[i].split('+'))
        else:
            golds[i] = ""
    
    #print("results",new_results)
    #print()
#    golds = [];
#    golds = arr.copy();
#    for i in range(len(golds)):
#        golds[i] = tuple(golds[i].split('+'))
#        results[i] = tuple(results[i].split(SEGMENTATION_MARKER))

            
            #flag them for deletion
    #why is it not working now???
    #because there are words that presumably exist in gold but aint in my wordfile don't exist in 
    #remove all flagged words in gold I suppose?
    golds = [gold for gold in golds if not (gold == "")] #[wordingold]
    #print("golds",golds)
    #sys.exit()
    eva = Evaluator(); 
    
    score = eva.calculate(new_results, golds)
    finish = time.time()
    print("Finished. Time taken: " + str(finish-start))
    score_message = "Precision: {0}; Recall: {1}; F-Score: {2}"
    print(score_message.format(*score))
    
#    en_gold = r"data/en_gold.txt";
#    #create array of gold files
#    with open(en_gold, "r") as file: 
#    for line in file:
#        x = line.strip()
#        arr.append(x)
#    """Read the gold file which contains correctly segmented words."""
    """
    golds = []
    with open(gold_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            gold = line.strip().split(separator)
            golds.append(gold_file)
    
    #Evaluation - # build up list of words and the gold standard equivalent.. together
    #dev = words_and_morphemes#[['pre', 'cogni', 'tion'], ['devalue'], ['evalua', 'te'], ['ef', 'fect']]
    gold = []
    gold_list = [re.sub(SEGMENTATION_MARKER, '', word) for word in gold] #set() of gold words for checking #{s for s in [1, 2, 1, 0]}
    gold_check = {re.sub(SEGMENTATION_MARKER, '', word) for word in gold} #set() of gold words for checking #{s for s in [1, 2, 1, 0]}
    word_list = [word_and_morpheme for word_and_morpheme in words_and_morphemes if word_and_morpheme[0] in gold_check] #[wordingold] #list of words if they're in the gold standard
    
    #if word in gold then get word_and_morpheme from words_and_morpheme:
    #creating wordlist
    word_list = []
    for word in gold: #looping through gold to get any words 
        if word in words_and_morphemes:
            word_list.append(word)
            #new_gold.append(gold)
    
    for word in only_words:
        #put a list of the morphemes for each word in words_and_morphemes into the gold
        if word in gold_standard_dictionary:
            gold.append(gold_standard_dictionary[word])
            new_wordlist.append
        else:
            removed_wordlist = 
    gold = [['pre', 'cogni', 'tion'], ['de', 'value'], ['eval', 'uate'], ['effect']]
    evaluator = pyport_evaluation.Evaluator()
    tp, fp, fn = evaluator._count(dev, gold)
    """
#        evaluate = Evaluation("data/goldstd_trainset-untabbed.segmentation.eng.txt", word_and_morphemes)
#        #evaluate.create_gold_standard()
#        evaluate.compare_mine_to_gold(True)
    
        

    #for line in goldstandard:
        
        #goldstandard.append()
    
    # get a list of the morpheme segmented wordlist
    # 
#TODO: Add Evaluation with the Morpho Project Challenges' gold standard