import csv
from prob_class import Problem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from difflib import SequenceMatcher
import operator
import math

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def getSimilarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def UniqueWords(words):
    uniqueWords = []
    [uniqueWords.append(x) for x in words if x not in uniqueWords]
    return uniqueWords


# validTags = ['dp', 'math', 'greedy', 'data structure', 'graph', 'string', 'geometry'
#                 , 'binary search', 'number theory', 'constructive algorithm', 
#                 'dfs', 'flows', 'sorting', 'brute force']

# validTags = {'dp':'dp', 'math':'math', 'greedy':'greedy', 'data structures':'data structures'
#             , 'implementation':'implementation', 'strings':'strings'
#             , 'sortings':'sortings', 'geometry':'geometry', 'number theory':'number theory'
#             , 'games':'game theory', 'trees':'trees', 'graphs':'graphs'
#             , 'combinatorics':'combinatorics', 'brute force':'implementation'
#             , 'binary search':'search', 'bitmasks':'dp', 'probabilities':'math'
#             , 'flows':'graphs', 'two pointers':'implementation'
#             , 'dfs':'graphs', 'bfs':'graphs', 'shortest paths':'graphs'
#             , 'chinese remainder theory':'number theory'
#             , 'suffix':'strings', 'constructive algorithms':'implementation'
#             , 'hashing':'hashing', 'divide and conquer':'divide and conquer'}

validTags = {}

# consideredCategories = ['math', 'dp', 'adhoc', 'greedy'
#                        , 'trees', 'graphs', 'segment trees'
#                        , 'combinatorics', 'search', 'geometry'
#                        , 'sortings', 'strings', 'implementation'
#                        , 'data structures', 'game theory']

consideredCategories = {'math': ['math', 'maths', 'advanced math', 'basic math', 'simple math', 'basic math', 'basic maths', 'mathematics'],
                        'dp':['dp+lcs', 'dpmgc', 'dp', 'digit dp', 'dp+bitmask', 'tree dp','bitmasking', 'bitset', 'dp+bitmask'],
                        'adhoc':['ad hoc','adhoc'],
                        'greedy':['greed algo', 'greedychxorr', 'greedy'],
                        'trees':['range tree', 'kd tree', 'link cut tree', 'fenwick tree', 'tree', 'binary tree', 'trees', 'segtree', 'segment trees', 'tree dp', 'suffix trees', 'splay tree', 'segment tree'],
                        'graphs':['graph', 'grap', 'graphs', 'basic graph', 'digraph', 'graph theory'],
                        'segment trees':['segment ', 'segment tre', 'segment tr', 'segment t', 'segment', 'seg', 'segtree', 'segme', 'segment trees', 'segment tree'],
                        'combinatorics':['combination', 'combinatorial', 'combinations', 'combinatorics'],
                        'search':['search', 'researching', 'binary search', 'binarysearch'],
                        'geometry':['geometry'],
                        'sortings':['mergesort', 'sorting'],
                        'strings':['string', 'array string', 'strin', 'string process', 'string parsing', 'string ha', 'strings'],
                        'implementation':['basic implement', 'implementation'],
                        'data structures':['data', 'data structure', 'datatypes'],
                        'game theory':['game theory', 'games', 'guessinggame', 'game'],
                        }

engine = create_engine('mysql+mysqldb://root:@localhost/data stage fyp')
conn = engine.connect()

Session = sessionmaker(bind=engine)
s = Session()

f = open('rare.txt', 'w')
probs = s.query(Problem)
rare = []
common = []
count = 1
for p in probs:
    tags = p.tag.split()
    temp = []
    for tag in tags:
        flag = '-' in tag or '_' in tag
        if flag:
            ts = tag.split('-' if '-' in tag else '_')
            s = ''
            for t in ts:
                s = s + t + ' '
            temp.append(s)
        else:
            temp.append(tag)

    tags = temp
    newTag = ''
    similarityDict = {}
    for tag in tags:
        tag = tag.strip()
        tag = tag.lower()
        for cat in consideredCategories:
            possibilites = consideredCategories[cat]
            for poss in possibilites:
                similarityDict[cat] = int(getSimilarity(poss, tag)*1000)

        sorted_tag = sorted(similarityDict.items(), key=operator.itemgetter(1))
        #print(sorted_tag)
        minTuple = sorted_tag[-1]
        # if not isclose(minTuple[1]- 0.6, 0.0, 0.05, 0.05):
        #     continue
        # if 'math' in tag:
        #     print(str(minTuple[1]) + ' mila ' + tag + ' ' + minTuple[0])
        if minTuple[1] < 450:
            #   print(str(minTuple[1]) + ' upar tha ' + tag + ' ' + minTuple[0])
            continue
        mapToTag = minTuple[0]
        try:
            listTags = validTags[mapToTag]
            listTags.append((tag, minTuple[1]))
            validTags[mapToTag] = listTags
            newTag = newTag + mapToTag + ' '
        except KeyError:
            validTags[mapToTag] = [(tag, minTuple[1])]

    #print(newTag)

    # p.modified_tags = newTag
    # s.commit()
    #print('{0} out of {1} {2} : {3}'.format(str(count), str(probs.count()), p.prob_code, str(newTag)))
    print(newTag)
    if newTag is '':
        rare.append(tags)
    count += 1

# sorted_rare = sorted(rare.items(), key=operator.itemgetter(1))
with open('newTagMap.txt', 'w') as f:
    f.write(str(validTags))
#print(validTags)
print(rare)
print(str(len(rare)))
# print('Following are rare tags: \n'+ str(sorted_rare))