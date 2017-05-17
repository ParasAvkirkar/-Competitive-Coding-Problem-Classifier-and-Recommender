import string
from nltk.corpus import stopwords
import re
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.stem.porter import *
from stemming.porter2 import stem
import spacy


def transform(desc):
    desc = removeNondecodableChars(desc)
    desc = lemmatizeDescription(desc)
    desc = minimizeDescription(desc)
    desc = removePunctuation(desc)
    desc = stemming(desc)
    # print 'Description Transformation Ended '
    return desc


def new_transform(desc):
    desc = removeNondecodableChars(desc)
    desc = lemmatize_spacy(desc)
    desc = minimizeDescription(desc)
    desc = removePunctuation(desc)
    # desc = lemmatize_spacy(desc)
    desc = stemming(desc)

    return desc


def stemming(desc):
    stemmer = PorterStemmer()
    new_desc = ''
    for word in desc.split():
        new_desc = new_desc + stemmer.stem(word) + ' '

    return new_desc


def removeNondecodableChars(desc):
    printable = set(string.printable)
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


# regex = re.compile('[^a-zA-Z0-9]')


def removePunctuation(desc):
    punctuationSet = set(string.punctuation)
    pattern = re.compile('([^\s\w]|_)+')

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


def lemmatize_spacy(description):
    nlp = spacy.load('en')
    description = unicode(description)
    description = nlp(description)
    new_description = ''
    for token in description:
        if token.lemma_ != '-PRON-':
            new_description += token.lemma_ + ' '
        else:
            new_description += token.lower_ + ' '

    return new_description


def lemmatizeDescription(description):
    resultDescription = ''
    descriptionWords = description.split()
    for word in descriptionWords:
        wordNetLem = WordNetLemmatizer()
        newDesc = wordNetLem.lemmatize(str(word))
        newDesc += ' '
        resultDescription += newDesc
        mapListTuples = pos_tag(description.split())
        # for m in mapListTuples:
        #     try:
        #         l = list(m)
        #         # word = l[0]
        #         typ = l[1]
        #         # newDesc = wordNetLem.lemmatize(str(word), get_wordnet_pos(str(typ)))
        #         newDesc = wordNetLem.lemmatize(str(word))
        #         newDesc = newDesc + ' '
        #         resultDescription += newDesc
        #         #print(str(word), str(typ))
        #     except Exception as e:
        #         pass
        #         # print(e)
    return resultDescription


#
# s = 'chefland n city oneway roads city chef travel city road use unusual bike circumference front wheel number city yet circumference rear wheel n think circumference wheel broken equalspaced position front wheel position n1 rear wheel position n2 unit distance travel advance wheel position example chef travel distance wheel start position position front wheel leave mod n position rear wheel leave mod n furthermore chef bike fast road bumpy quite frequently least wheel touch ground happen turn bike need lubrication front rear wheel even rotate total number position travel road road give start city si end city ei distance front wheel travel fi distance rear wheel ri wheel start position begin chef trip travel sequence road i1 i2 ik front wheel position f fi1 fi2 fik mod n similarly rear wheel position r ri1 ri2 rik mod n1 chef want start end city ok start city chef also ok visit city once journey count destination chef also interested calculate number paths final position f r equal certain value number road traverse equal certain value us road twice count twice answer quite large need output answer mod'
s = 'saw'
print(transform(s))
