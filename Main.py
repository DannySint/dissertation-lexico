#copied from COM Text Processing by Mark Hepple / Rob Gaizauskas

import sys
import getopt

class CommandLine:
    def __init__(self):
        self.input_file = None
        self.output_file = None
        opts, args = getopt.getopt(sys.argv[1:],'hi:o:f:', ["help", "input", "output"])
        opts = dict(opts)
        print(opts)
        if '-h' in opts:
            self.printHelp()

#        if len(args) == 2:
#            self.keyfile = args[0]
#            self.responsefile = args[1]
#        else:
#            print('\n*** ERROR: must specify precisely 2 arg files (key,response) ***', file=sys.stderr)
#            self.printHelp()
        print(args)            
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
            self.file_format = opts['f']
        else:
            self.file_format = 'txt'
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
    config = CommandLine()
    print(config.input_file)
    print(config.output_file)