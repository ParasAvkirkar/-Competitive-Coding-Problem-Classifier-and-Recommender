__author__ = 'Pranay'
import lemmatization, minimize_desc, remove_nondecodable_chars, removePunctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
 
def transform(desc):
    print 'Description Transformation Started: '
    desc = remove_nondecodable_chars.removeNondecodableChars(desc)
    desc = minimize_desc.minimizeDescription(desc)
    desc = removePunctuation.removePunctuation(desc)
    desc = lemmatization.lemmatizeDescription(desc)
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(desc)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    desc=' '.join(filtered_sentence)
    # print 'Description Transformation Ended '
    return desc
