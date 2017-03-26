import string
from nltk.corpus import stopwords
import re
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

def transform(desc):
    desc = removeNondecodableChars(desc)
    desc = minimizeDescription(desc)
    desc = removePunctuation(desc)
    desc = lemmatizeDescription(desc)
    # print 'Description Transformation Ended '
    return desc

printable = set(string.printable)

def removeNondecodableChars(desc):
    desc = filter(lambda x: x in printable, desc)
    return desc


def create_word_features(words):
    # print words
    w = []
    for wrd in words.split():
        w.append(wrd)
    useful_words = [word for word in w if word not in
                       stopwords.words('english')]
    my_dict = ' '.join([word for word in useful_words])
    # print my_dict
    return my_dict

def minimizeDescription(desc):
    desc = desc.replace('.', ' ')
    desc = desc.replace(',', ' ')
    desc = create_word_features(desc)
    return desc.lower()

punctuationSet = set(string.punctuation)

# regex = re.compile('[^a-zA-Z0-9]')
pattern = re.compile('([^\s\w]|_)+')


def removePunctuation(desc):
    desc = ''.join(ch for ch in desc if ch not in punctuationSet)
    desc = pattern.sub(' ', desc)
    return desc


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

def lemmatizeDescription(description):
    descriptionWords = description.split()
    wordNetLem = WordNetLemmatizer()
    newDesc = ''
    mapListTuples = pos_tag(description.split())
    for m in mapListTuples:
        try:
            l = list(m)
            word = l[0]
            typ = l[1]
            newDesc = newDesc + wordNetLem.lemmatize(str(word), get_wordnet_pos(str(typ)))
            newDesc = newDesc + ' '

            #print(str(word), str(typ))
        except Exception as e:
            pass
            # print(e)
    return newDesc
