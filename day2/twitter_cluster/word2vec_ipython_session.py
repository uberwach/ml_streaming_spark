# coding: utf-8
import gensim
model = gensim.models.Word2Vec.load_word2vec_format("wiki.en.text.vector", binary=False)
model.most_similar("king")
model.most_similar("berlin")
model.most_similar("university")
model.most_similar_cosmul("university")
model["king"]
model["king"] - model["man"] + model["woman"] - model["queen"] 
model["king"]
trump_tweet = "Just leaving Florida Big crowds of enthusiastic supporters lining the road that the FAKE NEWS media refuses to mention Very dishonest"
[word.lower_case() for word in trump_tweet.split(" ")]
[word.to_lower_case() for word in trump_tweet.split(" ")]
[word.to_lower() for word in trump_tweet.split(" ")]
"ABC".lower()
[word.lower() for word in trump_tweet.split(" ")]
vecs = [model[word.lower()] for word in trump_tweet.split(" ")]
vecs
type(vecs)
import numpy as np
np.sum(vecs) / len(vecs)
np.sum(vecs, axis=0) / len(vecs)
avg_vec = np.sum(vecs, axis=0) / len(vecs)
avg_vec.shape
model.similar_by_vector(avg_vec)
trump_tweet
stopwords = []
with open("stopwords_en.txt") as f:
    stopwords.append(f.read())
    
get_ipython().magic(u'pwd ')
with open("stopwords_en.txt") as f:
    stopwords.append(f.read())
    
stopwords
stopwords.split("\n")
stopwords[0].split("\n")
stopwords = stopwords[0].split("\n")
trump_tweet
filtered_tweet = [word.lower() for word in trump_tweet.split(" ") if word.lower() not in stopwords]
filtered_tweet
vecs = [model[word] for word in filtered_tweet]
avg_vec = np.sum(vecs, axis=0) / len(vecs)
model.similar_by_vector(avg_vec)
trump_tweet
model.similar_by_vector(avg_vec, 50)
