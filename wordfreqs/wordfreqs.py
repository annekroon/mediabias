#!/usr/bin/env python3
import inca
import gensim
import logging
import re

lettersanddotsonly = re.compile(r'[^a-zA-Z\.]')

PATH = "/mnt/elastic/"


def preprocess(s):
    s = s.lower().replace('!','.').replace('?','.')  # replace ! and ? by . for splitting sentences
    s = lettersanddotsonly.sub(' ',s)
    return s




def get_distance(doc, w1, w2):
    ''' returns a dict with the distance between two words in a given document'''

    words = doc.split()
    
    if w1 in words:
        position_w1 = words.index(w1)
    else:
        position_w1 = None

    
    if w2 in words:
        position_w2 = words.index(w2)
    else:
        position_w2 = None
        
        
    if position_w1 and position_w2:
        distance = abs(words.index(w2) - words.index(w1))
    else:
        distance = None
    
    return {'pair':(w1,w2),
            'distance':distance,
            'position_w1':position_w1,
            'position_w2':position_w2,
            'length':len(words)}




class cooc():

    def __init__(self, doctype, fromdate,todate):
        self.doctype = doctype
        self.fromdate = fromdate
        self.todate = todate
        self.query = {
                  "query": {
                          "bool": {
                                    "filter": [
                                                { "match": { "_type": self.doctype}},
                                                { "range": { "publication_date": { "gte": self.fromdate, "lt":self.todate }}}
                                              ]
                                  }
                        }
                }
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
        
      
        
    def get_documents(self):
        data = {}
        for d in inca.core.database.scroll_query(self.query):
            self.documents += 1
            try:
                data['text'] = preprocess(d['_source']['text'])
                data['doctype'] = d['_source']['doctype']
                data['publication_date'] = d['_source']['publication_date']
                yield data
            except:
                self.failed_document_reads +=1
                continue
                
    def distances_per_document(self)
        results = []
        for doc in self.get_documents():
            for pair in self.combinations_crime:
                    results.append({'distance': get_distance(doc['text'],pair[0],pair[1]),
                    'doctype':doc['doctype'],
                    'publication_date':doc['publication_date']})
        return results


def train_and_save(fromdate,todate,doctype):
    filename = "{}word2vec-{}-{}-{}".format(PATH,doctype,fromdate,todate)
    
    casus = cooc(doctype,fromdate,todate)

    with open(filename, mode='wb') as fo: 
        casus.model.save(fo)
    print('Saved model')
    print("reopen it with m = gensim.models.Word2Vec.load('{}')".format(filename))
    
    
if __name__ == "__main__":
    
    logger = logging.getLogger()
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)

    #train_and_save(fromdate = "2006-01-01", todate = "2016-01-01", doctype = "telegraaf (print)")
    #train_and_save(fromdate = "2006-01-01", todate = "2016-01-01", doctype = "volkskrant (print)")
    #train_and_save(fromdate = "2006-01-01", todate = "2016-01-01", doctype = "nrc (print)")
    #train_and_save(fromdate = "2006-01-01", todate = "2016-01-01", doctype = "ad (print)")
    casus = cooc(fromdate = "2016-01-01", todate = "2016-01-02", doctype = "telegraaf (print)")