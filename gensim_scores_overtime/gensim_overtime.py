#!/usr/bin/env python3

import gensim
import sys
import logging
import re
import os
import json
import itertools
print(sys.executable)
print(sys.version)

basepath = "../trained_models/test/"

class get_word2vec():

    def __init__(self):

        self.doctype = []
        self.fromdate = []
        self.todate = []
        self.nmodel = 0
        self.combinations_crime = []
        self.combinations_low = []
        with open('ressources/combinations_crime.csv') as fi:
            for line in fi.readlines():
                self.combinations_crime.append(tuple(line.strip().split(',')))
        with open('ressources/combinations_lowlife.csv') as fi:
            for line in fi.readlines():
                self.combinations_low.append(tuple(line.strip().split(',')))
        for fname in os.listdir(basepath):
            path = os.path.join(basepath, fname)
        try:
            splitResult = fname.split( " - " ) #split on scores
            self.doctype.append(splitResult[1])
            self.fromdate.append(splitResult[2])
            self.todate.append(splitResult[3])
        except IndexError:
            pass

    def get_models(self):

        ''' calling models'''

        models = {}
        for fname in os.listdir(basepath):
            path = os.path.join(basepath, fname)
            models['fname'] = gensim.models.Word2Vec.load(path)
            self.nmodel +=1
        yield models

    def get_scores(self):

        ''' calling similarity scores'''

        results = []
        for x in self.get_models():
            for pair in self.combinations_crime:
                try:
                    r = x['fname'].wv.similarity(pair[0],pair[1])
                    pair_1 = pair[0]
                    pair_2 = pair[1]
                except KeyError:
                    r = 0
                results.append({'pair': (pair[0],pair[1]),
                            'word2vec_score': r,
                            'doctype': self.doctype,
                            'fromdate': self.fromdate,
                            'todate': self.todate})
        return results


if __name__ == "__main__":

    logger = logging.getLogger()
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)


r = get_word2vec()
gensimscore = r.get_scores()

with open('gensim_scores_overtime/output.json',mode='w') as fo:
    fo.write('[')

    for result in gensimscore:
        print("this is the result:", result)
        fo.write(json.dumps(result))
        fo.write(',\n')
    fo.write('[]]')
