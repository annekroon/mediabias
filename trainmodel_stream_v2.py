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


class train_model():

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
        self.model = gensim.models.Word2Vec(iter = 1, min_count=10)
        self.model.build_vocab(self.get_sentences_vocab())
        print('Build Word2Vec vocabulary')
        self.model.train(self.get_sentences_train(),total_examples=self.model.corpus_count, epochs=self.model.iter)
        print('Estimated Word2Vec model')

        
        
    def get_sentences_vocab(self):
        for d in inca.core.database.scroll_query(self.query):
            self.documents += 1
            try:
                sentences_as_strings = preprocess(d['_source']['text']).split('.')
                sentences_as_lists = [s.split() for s in sentences_as_strings]
                for sentence in sentences_as_lists:
                    yield sentence
            except:
                self.failed_document_reads +=1
                continue

    def get_sentences_train(self):
        for d in inca.core.database.scroll_query(self.query):
            try:
                sentences_as_strings = preprocess(d['_source']['text']).split('.')
                sentences_as_lists = [s.split() for s in sentences_as_strings]
                for sentence in sentences_as_lists:
                    yield sentence
            except:
                continue

        
        


def train_and_save(fromdate,todate,doctype):
    filename = "{}word2vec-{}-{}-{}".format(PATH,doctype,fromdate,todate)
    
    casus = train_model(doctype,fromdate,todate)

    with open(filename, mode='wb') as fo: 
        casus.model.save(fo)
    print('Saved model')
    print("reopen it with m = gensim.models.Word2Vec.load('{}')".format(filename))
    
    
if __name__ == "__main__":
    
    logger = logging.getLogger()
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)

    train_and_save(fromdate = "2006-01-01", todate = "2016-01-01", doctype = "telegraaf (print)")
    train_and_save(fromdate = "2006-01-01", todate = "2016-01-01", doctype = "volkskrant (print)")
    train_and_save(fromdate = "2006-01-01", todate = "2016-01-01", doctype = "nrc (print)")
    train_and_save(fromdate = "2006-01-01", todate = "2016-01-01", doctype = "ad (print)")
