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
            print(e)
    return newDesc

if __name__ == "__main__":
    printable = set(string.printable)

    engine = create_engine('mysql+mysqldb://root:@localhost/data stage fyp')
    conn = engine.connect()

    Session = sessionmaker(bind=engine)
    s = Session()
    count = 1
    probs = s.query(Problem)
    wordNetLem = WordNetLemmatizer()
    for prob in probs:
        desc = prob.description
        descriptionWords = desc.split()

        newDesc = ''
        mapListTuples = pos_tag(desc.split())
        for m in mapListTuples:
            try:
                l = list(m)
                word = l[0]
                typ = l[1]
                newDesc = newDesc + wordNetLem.lemmatize(str(word), get_wordnet_pos(str(typ)))
                newDesc = newDesc + ' '
                #print(newDesc)
                #print(str(word), str(typ))
            except Exception as e:
                print(e)

        prob.description = newDesc
        s.commit()
        print('{0} out of {1} {2} '.format(str(count), str(probs.count()), prob.prob_code))
        count = count + 1
