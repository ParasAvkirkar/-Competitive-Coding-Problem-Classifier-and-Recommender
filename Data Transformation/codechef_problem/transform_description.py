__author__ = 'Pranay'
import lemmatization, minimize_desc, remove_nondecodable_chars, removePunctuation

def transform(desc):
    print 'Description Transformation Started: '
    desc = remove_nondecodable_chars.removeNondecodableChars(desc)
    desc = minimize_desc.minimizeDescription(desc)
    desc = removePunctuation.removePunctuation(desc)
    desc = lemmatization.lemmatizeDescription(desc)
    print desc
    return desc
