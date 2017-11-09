import inca
import gensim

docs = inca.core.search_utils.doctype_examples('nu')
teksten = [d['_source']['text'].split() for d in docs]
m0 = gensim.models.Word2Vec(teksten, min_count=1)
m0.most_similar(positive=['vliegramp'], negative=['Germanwings'])


# per zin

docs = inca.core.search_utils.doctype_examples('nu')
docsjoined = " ".join([d['_source']['text'] for d in docs])

sentences = [s.split() for s in docsjoined.split('.')]

m1 = gensim.models.Word2Vec(sentences, min_count=1)
m1.most_similar(positive=['vliegramp'], negative=['Germanwings'])
