#copied from COM Text Processing by Mark Hepple / Rob Gaizauskas

import sys
import getopt
import string
import test_evaluator

from morpheme_analysis import MorphemeAnalysis
from morpheme_analysis import SEGMENTATION_MARKER
from evaluation import Evaluation

class CommandLine:
    def __init__(self):
        self.input_file = None
        self.output_file = None
        self.gold_standard_file = None
        opts, args = getopt.getopt(sys.argv[1:],'hi:o:f:g:', ["help", "input", "output"])
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
    #forward_trie.pprint(); #backward_trie.pprint();
    config = CommandLine()
    #print(config.input_file)
    #print(config.output_file)
    if config.input_file is None:
        config.printHelp()
        print("An input file is required. Program will now exit.")
        sys.exit(1);
    morpheme_analysis = MorphemeAnalysis(config.input_file)
    
    if config.gold_standard_file is None:
        config.printHelp()
        print("A gold standard file is required. Program will not exit.")
        sys.exit(1);
    
    word_frequency = {}
    with open(config.input_file) as f:
        for line in f:
            frequency, words = line.strip('\n').split(' ', 1)
            word_frequency[words] = int(frequency)
        #mapping = dict(line.strip('\n').split(' ', 1) for line in f) #ordered via number, name currently
    sorted_wf = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
    #print(sorted_wf[:200]) #unsorted by frequency
    top_words = sorted_wf[:400]
    only_words = [wordline[0] for wordline in top_words if (not any(char in string.punctuation for char in wordline[0]))]
    #print(only_words)
    
    morpheme_analysis.score_prefixes(False);
    morpheme_analysis.pruned_word_score_prefix = morpheme_analysis.prune_affixes(morpheme_analysis.word_score_prefix); 
    prefix_list = morpheme_analysis.get_morphemes(morpheme_analysis.pruned_word_score_prefix, morpheme_analysis.output_file_prefixes);
    
    morpheme_analysis.score_suffixes(False); 
    morpheme_analysis.pruned_word_score_suffix = morpheme_analysis.prune_affixes(morpheme_analysis.word_score_suffix); 
    suffix_list = morpheme_analysis.get_morphemes(morpheme_analysis.pruned_word_score_suffix, morpheme_analysis.output_file_suffixes);
    #word_standard.write(segment_prefix("report+s", True))
    
    word_standard = open(config.output_file, 'w')
    #Outputting the list of words in morpheme-segmented form
    
    #word_and_morphemes = {} #[[words  ]
    morphemes = []
    words_and_morphemes = {}
    for word in morpheme_analysis.words: #for words in only_words:
    #for word in morpheme_analysis.words:
        if len(word) != 1: #TODO: Something about this
            #print(segmented_word)
            segmented_word = morpheme_analysis.segment_suffix(word) # segment -> seg+ment
            
            word_delimiter = word + "\t"
            #print("To output " + segmented_word)
            x = segmented_word.split(SEGMENTATION_MARKER) #[un],[requit],[ed]
            #word_and_morphemes.append(word + " " + segmented_word) # []
            words_and_morphemes[word] = x #[[un],[requit],[ed]] #morphemes.append(x) #{"unrequited":[un,requit,ed]} 
            #SEGMENTATION_MARKER.join(x[:-1]) + f'_{x[-1]}' #converts a word into it's underscore segmented form    
            #word_standard.write(word_delimiter + '_'.join(x) + "\n") #word_standard.write(word + "\t" + str(segmented_word.split('_')) + "\n")
            word_standard.write("" + SEGMENTATION_MARKER.join(x) + "\n") #"" needed to prevent a lot of nulls at beginning
            #word_standard.write("" + word + " " + " ".join(x) + "\n") #"unrequited un requit ed"
    
    #gold standard part
    gold_file = config.gold_standard_file
    golds = [gold_file]
    separator = SEGMENTATION_MARKER
    
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