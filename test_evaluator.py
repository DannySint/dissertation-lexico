class Evaluator(object):
    def __init__(self):
        self.true_positives = None #gold has a break here and so do I
        self.false_positives = None #gold has a break here and I do not
        self.false_negatives = None #gold doesn't have a break here but I do
        self.gold_breaks = None #the number of morpheme boundaries in gold
        self.precision = None #true_positives / (true_positives+false_positives)
        self.recall = None #true_positives / (true_positives+false_negatives)
        self.fscore = None #https://en.wikipedia.org/wiki/F1_score

    def calculate(self, results, golds):
        """
        Calculate the precision, recall and fscore for the results as compared
        to the gold standard. 

        Arguments:
            results: a list of length n of induced word segmentation lists
            golds: a list of length n of correct word segmentation lists
                (the same words as in results)
        """
        self._count(results, golds)
        self._calculate_precision(self.true_positives, self.false_positives)
        self._calculate_recall(self.true_positives, self.false_negatives)
        self._calculate_fscore(self.precision, self.recall)
        return (self.precision, self.recall, self.fscore)
     
    def _glue(self, word, separator='+'):
        """Concatenate segments, using separator to denote morpheme breaks."""
        glued = ''
        for i, segment in enumerate(word):
            if i == 0:
                glued = segment
            else:
                glued += separator + segment
        return glued

    def _count(self, results, golds, separator='+'):
        """Count up the number of true pos, false pos, and false neg."""
        #assert len(results) == len(golds), 'Results ({} entries) != gold ({} entries)'.format(len(results), len(gold)) 
        self.true_positives = 0 
        self.false_positives = 0
        self.false_negatives = 0
        for e, result in enumerate(results):
            gold = golds[e]
            ri = 0 #how far we are through the result word
            gi = 0 #how far we are through the gold word
            rj = self._glue(result, separator)
            gj = self._glue(gold, separator)
#            while ri < len(''.join(gold)):
            while ri < len(rj):
                rc = rj[ri]
                gc = gj[gi]
                if rc == separator and gc == separator: # common split point = TP
                    self.true_positives += 1
                    #print("ri",ri)
                    ri += 1
                    gi += 1
                elif rc == separator:       # result-only split point = FP
                    self.false_positives += 1
                    ri += 1
                elif gc == separator:       # gold-only split point = FN
                    self.false_negatives += 1
                    gi += 1
                else:
                    ri += 1
                    gi += 1
        return (self.true_positives, self.false_positives, self.false_negatives)


    def _calculate_precision(self, true_positives, false_positives):
        try:
            self.precision = true_positives / (true_positives + false_positives)
        except ZeroDivisionError:
            self.precision = 0
        return self.precision

    def _calculate_recall(self, true_positives, false_negatives):
        try:
            self.recall =  true_positives / (true_positives + false_negatives)
        except ZeroDivisionError:
            self.recall = 0
        return self.recall

    def _calculate_fscore(self, precision, recall, b=2):
        #https://en.wikipedia.org/wiki/F1_score
        try:
            self.fscore = (1+b**2) * (precision * recall) / ((b**2 * precision) + recall)
        except ZeroDivisionError:
            self.fscore = 0
        return self.fscore


if __name__ == '__main__':
    
    

    golds   = ['re+port+s', 'un+dy+ing', 'hypno+tic', 'reticient']
    results = ['re+port+s', 'undy+ing', 'hypno+tic', 'retic+ient']
    
    print()
    print('INIT-GOLD-STD:', golds)
    print('INIT-RESULTS:', results)
    print()
    
# ----------------------------
# convert the above "initial form" for data, to right form for scoring using
# the Evaluator class, i.e. to be the inputs to the "calculate" method. 

    for i in range(len(golds)):
        golds[i] = tuple(golds[i].split('+'))
        results[i] = tuple(results[i].split('+'))

    print('GOLD-STD:', golds)
    print('RESULTS:', results)
    print()
    
    eval = Evaluator()
    eval.calculate(results, golds)
    
    print('True positives:', eval.true_positives)
    print('False positives:', eval.false_positives)
    print('False negatives:', eval.false_negatives)
    print()
    print('Precision:', eval.precision)
    print('Recall:', eval.recall)
    print('F-measure>:', eval.fscore)

