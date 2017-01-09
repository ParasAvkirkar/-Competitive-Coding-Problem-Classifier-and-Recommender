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

# s """chef advocate go green initiative 
#     today n trees planted row outside restaurant today height i-th tree hi 
#     feet trees grow rate mi feet per day chef knows trees look beautiful form
#      zig-zag sequence trees said zig-zag sequence heights tree first increases decreases 
#     alternates decreasing/increasing respectively formally trees said 
#     zig-zag sequence one following two conditions holds h1 < h2 > h3 < h4 h1 > h2 < h3 > h4 
#     chef wants know intervals time heights trees form zig-zag sequence"""

#  t = """
#         submissions problem available read problems statements 
#         mandarin chinese russian vietnamese well today planned day 
#         tor thik ayvaks wedding kark infatuated ayvak offers play 
#         game thik whosoever wins get marry ayvak ayvak values games chance 
#         things life agrees kark sets n grid (n rows columns) labelled left right 
#         top bottom consecutively numbers 1 m*n 1 top left corner m*n bottom
#          right corner example labelled 3 6 grid looks follows: kark already 
#         painted k unit squares grid heart next thik randomly picks rectangle sides
#          grid lines positive area valid rectangle equal probability chosen 
#         three distinct possibilities thiks rectangle 3 6 grid shown below: nine 
#         different rectangles 2 2 grid shown below: thiks rectangle contains least half hearts 
#         thik gets marry ayvak otherwise kark marry ayvak kark wants know 
#         whether advantage wants know expected value number hearts randomly chosen 
#         rectangle cover im sure good heart please cover job"""   
s ="chef advocate go green initiative today n trees planted row outside restaurant today height i-th tree hi feet trees grow rate mi feet per day chef knows trees look beautiful form zig-zag sequence trees said zig-zag sequence heights tree first increases decreases alternates decreasing/increasing respectively formally trees said zig-zag sequence one following two conditions holds h1 < h2 > h3 < h4 h1 > h2 < h3 > h4 chef wants know intervals time heights trees form zig-zag sequence"
t =" submissions problem available read problems statements mandarin chinese russian vietnamese well today planned day tor thik ayvaks wedding kark infatuated ayvak offers play game thik whosoever wins get marry ayvak ayvak values games chance things life agrees kark sets n grid (n rows columns) labelled left right top bottom consecutively numbers 1 m*n 1 top left corner m*n bottom right corner example labelled 3 6 grid looks follows: kark already painted k unit squares grid heart next thik randomly picks rectangle sides grid lines positive area valid rectangle equal probability chosen three distinct possibilities thiks rectangle 3 6 grid shown below: nine different rectangles 2 2 grid shown below: thiks rectangle contains least half hearts thik gets marry ayvak otherwise kark marry ayvak kark wants know whether advantage wants know expected value number hearts randomly chosen rectangle cover im sure good heart please cover job"

s = s + t

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
