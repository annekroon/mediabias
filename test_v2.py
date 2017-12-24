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

basepath = "../../trained_models/2000_2016/"

#for fname in os.listdir(basepath):
#    path = os.path.join(basepath, fname)
#    print(path)
#    model[fname] = gensim.models.Word2Vec.load(path)

class get_word2vec():

    def __init__(self, doctype, fromdate,todate):
        self.doctype = doctype
        self.fromdate = fromdate
        self.todate = todate
        self.combinations_crime = []
        self.combinations_low = []
        with open('../ressources/combinations_crime.csv') as fi:
            for line in fi.readlines():
                self.combinations_crime.append(tuple(line.strip().split(',')))
        with open('../ressources/combinations_lowlife.csv') as fi:
            for line in fi.readlines():
                self.combinations_low.append(tuple(line.strip().split(',')))

def get_models(self):
    model = {}
    for fname in os.listdir(basepath):
        path = os.path.join(basepath, fname)
        model[fname] = gensim.models.Word2Vec.load(path)
        self.models += 1
        yield models

def scores(self):
    for model in self.get_models():
        for pair in self.combinations_crime:
            try:
                r = model[fname].wv.similarity(pair[0],pair[1])
                print("first r", resultaat)
            except KeyError:
                r = 0
                print("secondr", resultaat)
                results.append({'word2vec': r,
                                'doctype': doc['doctype'],
                                'publication_date':doc['publication_date']})
        yield results

def open_models(fromdate, todate, doctype)
    filename = "{}word2vec-{}-{}-{}".format(PATH,doctype,fromdate,todate)

if __name__ == "__main__":

    logger = logging.getLogger()
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)


    open_models()

d = scores()
print(d)

for pair in pairs_crim:
    try:
        resultaat = model[fname].wv.similarity(pair[0],pair[1])
        print("first r", resultaat)
    except KeyError:
        resultaat = 0
            print("secondr", resultaat)




#    resultaat_nrc = mnrc.wv.similarity(pair[0],pair[1])

    scores_crim[pair] = {'telegraaf': resultaat_tel}


    if os.path.isdir(path):
        # skip directories
        continue

source = "/Users/admin/surfdrive/Werk/projects/17_mediabias/trained_models/2000_2016/"
model[x] = (gensim.models.Word2Vec.load([x for x in os.listdir(source)]

archives = [x for x in os.listdir(source)]
print(archives)


models = {}
for x in archives:

    print(x)

path_to_models = '/Users/admin/surfdrive/Werk/projects/17_mediabias/trained_models/2000_2016/'
models = gensim.models.Word2Vec.load(path_to_models + "telegraaf", path_to_models + "ad")
print(models)
for e in models:
    print(e)
print("datatype", type(models))


with io.open(infile, 'r', encoding='utf8') as fin:
    for f in fin:
        print(fin)

model = gensim.models.Word2Vec.load(path_to_models + "telegraaf")

models = [item for sublist in json.load(open('../wordfreqs/output.json')) for item in sublist]

with open("/Users/admin/surfdrive/Werk/projects/17_mediabias/trained_models/2000_2016/ad") as fi:
    for line in fi:
        print(line)

path_to_models = "/Users/admin/surfdrive/Werk/projects/17_mediabias/trained_models/2000_2016/"
for e in path_to_models:
    print(e)



with open('../ressources/combinations_crime.csv') as fi:
            for line in fi.readlines():
                self.combinations_crime.append(tuple(line.strip().split(',')))

d = get_distance(doc['text'],pair[0],pair[1])

mtel = []
for e in path_to_models:
    print(e)


def preprocess(s):
    s = s.lower().replace('!','.').replace('?','.')  # replace ! and ? by . for splitting sentences
    s = lettersanddotsonly.sub(' ',s)
    return s


class word2vec():

    def __init__(self):
        self.documents = 0
        self.failed_document_reads = 0
        self.combinations_crime = []
        self.combinations_low = []
        with open('../ressources/combinations_crime.csv') as fi:
            for line in fi.readlines():
                self.combinations_crime.append(tuple(line.strip().split(',')))
        with open('../ressources/combinations_lowlife.csv') as fi:
            for line in fi.readlines():
                self.combinations_low.append(tuple(line.strip().split(',')))

    def scores(self):
        scores_crime = {}
        scores_low = {}
        for m in models:
            self.documents += 1
            try:
                data['text'] = preprocess(d['_source']['text'])
                data['doctype'] = d['_source']['doctype']
                data['publication_date'] = d['_source']['publication_date']
                yield data
            except:
                self.failed_document_reads +=1
                continue

    def distances_per_document(self):
        for doc in self.get_documents():
            results = []
            for pair in self.combinations_crime:
                d = get_distance(doc['text'],pair[0],pair[1])
                if d['distance']:
                    results.append({'distance': d,
                                    'doctype':doc['doctype'],
                                    'publication_date':doc['publication_date']})
            yield results



if __name__ == "__main__":

    logger = logging.getLogger()
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)


    casus = cooc(fromdate = "2016-01-01", todate = "2016-01-05", doctype = "telegraaf (print)")

    distgen = casus.distances_per_document()

    with open('output.json',mode='w') as fo:
        fo.write('[')

        for result in distgen:
            if len(result)>0:
                print(result)
                fo.write(json.dumps(result))
                fo.write(',\n')
        fo.write('[]]')
