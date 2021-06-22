from gensim.models import word2vec, Word2Vec
import os
import re
import time
from pymystem3 import Mystem
from nltk.corpus import stopwords
from natasha import NewsMorphTagger, Doc, NewsEmbedding
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
m = Mystem()

outp = 'winx_mystem.txt'

data = word2vec.LineSentence(outp)
model_winx = Word2Vec(data, window=7, min_count=2)
model_winx.init_sims(replace=True)
model_path = 'winx.bin'
print("Saving model...")
model_winx.wv.save_word2vec_format(model_path, binary=True)


