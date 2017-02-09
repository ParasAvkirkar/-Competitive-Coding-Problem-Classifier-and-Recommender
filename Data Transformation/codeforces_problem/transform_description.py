__author__ = 'Pranay'
import lemmatization, minimize_desc, remove_nondecodable_chars, removePunctuation

def transform(desc):
    desc = remove_nondecodable_chars.removeNondecodableChars(desc)
    desc = minimize_desc.minimizeDescription(desc)
    desc = removePunctuation.removePunctuation(desc)
    desc = lemmatization.lemmatizeDescription(desc)
    return desc