"""Word2Vec example"""
import gensim

#  training on 11515802065 raw words (9337059807 effective words) took 20035.8s, 466018 effective words/s
model = gensim.models.Word2Vec.load_word2vec_format("wiki.en.text.vector", binary=False)


print model.most_similar("queen")
