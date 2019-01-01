from numpy import zeros
from scipy.linalg import svd
from collections import defaultdict
from math import log
from numpy import asarray, sum
import nltk

class LSA(object):

    def __init__(self):
        self.wdict = {}
        #self.wdict = defaultdict(list)
        self.dcount = 0

    def parse(self, doc):
        words = nltk.word_tokenize(doc)
        for w in words:
            if w in self.wdict:
                self.wdict[w].append(self.dcount)
            else:
                self.wdict[w] = [self.dcount]
            self.dcount += 1

    def build(self):
        self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
        '''
        for key in self.wdict.keys():
            if len(self.wdict[key]) > 1:
                self.keys = key
        '''
        self.keys.sort()
        self.A = zeros([len(self.keys), self.dcount])
        for i, k in enumerate(self.keys):
            for d in self.wdict[k]:
                self.A[i,d] += 1

    def printA(self):
        print self.A

    def TFIDF(self):
        WordsPerDoc = sum(self.A, axis=0)
        DocsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
        rows, cols = self.A.shape
        for i in range(rows):
            for j in range(cols):
                self.A[i,j] = (self.A[i,j] / WordsPerDoc[j]) * log(float(cols) / DocsPerWord[i])

    def svd(self):
        self.U, self.S, self.Vt = svd(self.A)




