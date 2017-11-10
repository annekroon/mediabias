#!/usr/bin/env python3
import inca
import gensim





class train_model():

    def __init__(self, doctype, fromdate,todate):
        self.doctype = doctype
        self.fromdate = fromdate
        self.todate = todate

        docs = inca.core.database.scroll_query(
            {
                  "query": {
                          "bool": {
                                    "filter": [
                                                { "match": { "doctype": self.doctype}},
                                                { "range": { "publication_date": { "gte": self.fromdate, "lt":self.todate }}}
                                              ]
                                  }
                        }
                }
            )
        
        self.sentences = []
        n=0
        errors = 0
        for d in docs:
            n+=1
            try:
                sentences_as_strings = d['_source']['text'].split('.')
                sentences_as_lists = [s.split() for s in sentences_as_strings]
                self.sentences.extend(sentences_as_lists)
            except:
                errors+=1
                continue
        print('Read {} sentences from {} documents. {} errors occured, probably because they did not contain any text'.format(len(self.sentences),n,errors)) 
        

        self.model = gensim.models.Word2Vec(self.sentences, min_count=1)

        print('Estimated Word2Vec model')


    
if __name__ == "__main__":

    fromdate = "2000-01-01"
    todate = "2016-01-01"
    doctype = "telegraaf (print)"

    path = "/mnt/elastic/"
    filename = "{}word2vec-{}-{}-{}".format(path,doctype,fromdate,todate)
    
    casus = train_model(doctype,fromdate,todate)

    with open(filename, mode='wb') as fo: 
        casus.model.save(fo)
    print('Saved model')
    print("reopen it with m = gensim.models.Word2Vec.load({})".format(filename))
