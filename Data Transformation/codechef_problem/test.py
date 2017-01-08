import string
from prob_class import Problem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

s = 'chef likes problems geometry lot please help solve one problem find possible triangles integer sides radius inscribed circle also known incircle equal r two triangles said different least one different side lengths formally let two triangles t1 t2 let b c denote sides triangle t1  b  c similarly let e f denote sides triangle t2  e  f t1 said different t2 either  b  e c  f'

newDesc = ''
mapList = pos_tag(s.split())
#print(mapList)
wordNetLem = WordNetLemmatizer()
for m in mapList:
    try:
        l = list(m)
        word = l[0]
        typ = l[1]
        newDesc = newDesc + wordNetLem.lemmatize(str(word), get_wordnet_pos(str(typ)))
        newDesc = newDesc + ' '
        #print(newDesc)
        print(str(word), str(typ))
    except Exception as e:
        print(e)
