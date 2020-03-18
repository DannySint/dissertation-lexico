#copied from COM Text Processing by Mark Hepple / Rob Gaizauskas

import sys
import getopt
from morpheme_analysis import MorphemeAnalysis
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
    else:
        morpheme_analysis = MorphemeAnalysis(config.input_file)
    
        morpheme_analysis.score_prefixes(False);
        morpheme_analysis.pruned_word_score_prefix = morpheme_analysis.prune_affixes(morpheme_analysis.word_score_prefix); 
        prefix_list = morpheme_analysis.get_morphemes(morpheme_analysis.pruned_word_score_prefix, morpheme_analysis.output_file_prefixes);
        
        morpheme_analysis.score_suffixes(False); 
        morpheme_analysis.pruned_word_score_suffix = morpheme_analysis.prune_affixes(morpheme_analysis.word_score_suffix); 
        suffix_list = morpheme_analysis.get_morphemes(morpheme_analysis.pruned_word_score_suffix, morpheme_analysis.output_file_suffixes);
        #word_standard.write(segment_prefix("report+s", True))
        
        word_standard = open(config.output_file, 'w')
        #Outputting the list of words in morpheme-segmented form
        word_and_morphemes = []
        for word in morpheme_analysis.words:
            if len(word) != 1:
                to_output = morpheme_analysis.segment_suffix(word)
                word_and_morphemes.append(word + " " + to_output)
                word_standard.write(word + " " + to_output + "\n")
            
        #Evaluation
        evaluate = Evaluation("data/goldstd_trainset-untabbed.segmentation.eng.txt", word_and_morphemes)
        #evaluate.create_gold_standard()
        evaluate.compare_mine_to_gold(True)
        
        
    
    #for line in goldstandard:
        
        #goldstandard.append()
    
    # get a list of the morpheme segmented wordlist
    # 
#TODO: Add Evaluation with the Morpho Project Challenges' gold standard