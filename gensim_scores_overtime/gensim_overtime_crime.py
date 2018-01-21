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
import pandas as pd

basepath = "../../trained_data/all"

class word2vec_analyzer():
    '''This class provides a Bias Analyzer for Word2Vec models.'''

    def __init__(self):
        self.nmodel = 0
        self.combinations_crime = []
        self.combinations_low = []
        with open('../ressources/combinations_crime.csv') as fi:
            for line in fi.readlines():
                self.combinations_crime.append(tuple(line.strip().split(',')))
        with open('../ressources/combinations_lowlife.csv') as fi:
            for line in fi.readlines():
                self.combinations_low.append(tuple(line.strip().split(',')))
        logger.info("Created analyzer with {} combinations for crime and {} combinations for low life".format(
            len(self.combinations_crime), len(self.combinations_low)))


    def get_model(self):
        '''yields a dict with one item. key is the filename, value the gensim model'''
        filenames = [e for e in os.listdir(basepath) if not e.startswith('.')]

        for fname in filenames:
            model = {}
            path = os.path.join(basepath, fname)
            model['gensimmodel'] = gensim.models.Word2Vec.load(path)
            model['filename'] = fname
            splitResult = fname.split( "_" ) #split on scores
            model['doctype'] = splitResult[1]
            model['fromdate'] = splitResult[2]
            model['todate'] = splitResult[3]
            self.nmodel +=1
            yield model

    def get_scores(self):
        results = []
        for model in self.get_model():
            logger.info("Retrieving similarity scores from model {} ...".format(model['filename']))
            for pair in self.combinations_crime:
                try:
                    r = model['gensimmodel'].wv.similarity(pair[0],pair[1])
                    pair_1 = pair[0]
                    pair_2 = pair[1]
                except KeyError:
                    r = 0
                results.append({'pair': (pair[0],pair[1]),
                            'word2vec_score_crim': r,
                            'doctype': model['doctype'],
                            'fromdate': model['fromdate'],
                            'todate': model['todate']})
        return results


if __name__ == "__main__":

    logger = logging.getLogger()
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)

    print("\n\n\nInitiate Analyzer for my dataset\n\n\n")
    myanalyzer = word2vec_analyzer()
    print("\n\n\nCalculate bias scores\n\n\n")
    gensimscore = myanalyzer.get_scores()

    print("\n\n\nSave results\n\n\n")
    with open('../../r_analyses/mediabias/gensim_overtime/output_all_crime.json',mode='w') as fo:
        fo.write('[')

        for result in gensimscore:
            #print("this is the result:", result)
            fo.write(json.dumps(result))
            fo.write(',\n')
        fo.write('[]]')

    df = pd.DataFrame.from_dict(gensimscore)
    print('Created dataframe')
    # print(df)
    df.to_csv('../../r_analyses/mediabias/gensim_overtime/output_all_crime.csv')
