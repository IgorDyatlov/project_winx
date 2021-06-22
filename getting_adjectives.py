from pymystem3 import Mystem
import gensim
m = Mystem()

model = gensim.models.KeyedVectors.load_word2vec_format('winx.bin', binary=True)
model.init_sims(replace=True)

adjectives = set()

words = str(model.key_to_index).replace('{', '')
words = words.replace('}', '')
print(words[:100])
print(model.key_to_index)
for i in model.key_to_index:
    word = str(i)
    word = word.replace('{', '')
    word = word.replace('}', '')
    lemma = m.lemmatize(word)
    analyze = m.analyze(lemma[0])
    if 'analysis' in analyze[0]:
        try:
            pos = str(analyze[0]['analysis'][0]['gr']).split(',')[0]
            if pos == 'A':
                adjectives.add(str(analyze[0]['analysis'][0]['lex']))
        except IndexError:
            continue
print(adjectives)