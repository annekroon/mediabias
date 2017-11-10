#!/usr/bin/env python3
import inca
import gensim



def example_nu():
    docs = inca.core.search_utils.doctype_examples('nu')
    # per document

    teksten = [d['_source']['text'].split() for d in docs]
    m0 = gensim.models.Word2Vec(teksten, min_count=1)
    m0.most_similar(positive=['vliegramp'], negative=['Germanwings'])
    
    # per zin
    
    docs = inca.core.search_utils.doctype_examples('nu')
    docsjoined = " ".join([d['_source']['text'] for d in docs])
    sentences = [s.split() for s in docsjoined.split('.')]

    m1 = gensim.models.Word2Vec(sentences, min_count=1)
    m1.most_similar(positive=['vliegramp'], negative=['Germanwings'])



class example_telegraaf():

    def __init__(self):
        #docs = inca.core.database.scroll_query({
        #"query":{
        #    "match":{
        #        "doctype": "telegraaf (www)"
        #        }
        #}
        #})

        docs = inca.core.database.scroll_query(
            {
                  "query": {
                          "bool": {
                                    "filter": [
                                                { "match": { "doctype": "telegraaf (print)" }},
                                                { "range": { "publication_date": { "gte": "2014-01-01", "lt":"2014-02-01" }}}
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
    #example_nu()
    casus = example_telegraaf()
    m0 = casus.model
    print(m0.most_similar(positive=['buitenlandse'], negative=['media']))
    with open('/home/anne/word2vec_telegraaf2maanden', mode='wb') as fo: 
        m0.save(fo)
    print('Saved model')
    print("reopen it with m = gensim.models.Word2Vec.load('/home/anne/word2vec_telegraaf2maanden'")
