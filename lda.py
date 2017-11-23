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

    def __init__(self, doctype, fromdate,todate, num_topics, querystring):
        self.doctype = doctype
        self.fromdate = fromdate
        self.todate = todate
        self.query = {
                  "query": {
                      "bool":{
                          "must":{
                              "query_string" : {
                                  "default_field" : "text",
                                  "query" : querystring
                              }
                          },
                          "filter": [
                              { "match": { "_type": self.doctype}},
                              { "range": { "publication_date": { "gte": self.fromdate, "lt":self.todate }}}
                          ]
                      }
                }
            }


        self.documents = 0
        self.failed_document_reads = 0

        print('Start to build corpus')

        docs = list(self.get_docs())    # niet efficient, want alles in werkgeheugen, maar voor kleinere hoeveelheden data zou het moeten kunnen
        # print(docs[0])
        id2word_m1 = gensim.corpora.Dictionary(docs)                       # assign a token_id to each word
        id2word_m1.filter_extremes(no_below=5, no_above=0.5)
        ldacorpus = [id2word_m1.doc2bow(doc) for doc in docs]       # represent each speech by (token_id, token_count) tuples
        tfidfcorpus = gensim.models.TfidfModel(ldacorpus)

        print('Start to estimate model')
        lda_m1 = gensim.models.ldamodel.LdaModel(corpus=tfidfcorpus[ldacorpus],id2word=id2word_m1,num_topics=num_topics)
        
       
        print('Estimated model')
        print('\n\n\n\n\n')
        for t in lda_m1.print_topics(num_words=7):
            print(t)

        
        
    def get_docs(self):
        for d in inca.core.database.scroll_query(self.query):
            self.documents += 1
            doc_as_string = preprocess(d['_source']['text'])
            doc_as_list_of_words = doc_as_string.split()
            yield doc_as_list_of_words

'''
def train_and_save(fromdate,todate,doctype):
    filename = "{}word2vec-{}-{}-{}".format(PATH,doctype,fromdate,todate)
    
    casus = train_model(doctype,fromdate,todate)

    with open(filename, mode='wb') as fo: 
        casus.model.save(fo)
    print('Saved model')
    print("reopen it with m = gensim.models.Word2Vec.load('{}')".format(filename))
    
 ''' 

if __name__ == "__main__":
    
    logger = logging.getLogger()
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    '''
    train_and_save(fromdate = "2006-01-01", todate = "2016-01-01", doctype = "telegraaf (print)")
    train_and_save(fromdate = "2006-01-01", todate = "2016-01-01", doctype = "volkskrant (print)")
    train_and_save(fromdate = "2006-01-01", todate = "2016-01-01", doctype = "nrc (print)")
    train_and_save(fromdate = "2006-01-01", todate = "2016-01-01", doctype = "ad (print)")
    '''

    train_model(fromdate = "2006-01-01", todate = "2016-01-01", doctype = "ad (print)", num_topics=50, querystring = "buitenlander OR immigrant OR vluchteling OR allochtoon")
    
