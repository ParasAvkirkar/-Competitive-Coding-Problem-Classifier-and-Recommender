import csv

from prob_class import Problem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from difflib import SequenceMatcher
import operator


# validTags = ['dp', 'math', 'greedy', 'data structure', 'graph', 'string', 'geometry'
#                 , 'binary search', 'number theory', 'constructive algorithm', 
#                 'dfs', 'flows', 'sorting', 'brute force']

validTags = {'dp':'dp', 'math':'math', 'greedy':'greedy', 'data structures':'data structures'
            , 'implementation':'implementation', 'strings':'strings'
            , 'sortings':'sortings', 'geometry':'geometry', 'number theory':'number theory'
            , 'games':'game theory', 'trees':'trees', 'graphs':'graphs'
            , 'combinatorics':'combinatorics', 'brute force':'implementation'
            , 'binary search':'search', 'bitmasks':'dp', 'probabilities':'math'
            , 'flows':'graphs', 'two pointers':'implementation'
            , 'dfs':'graphs', 'bfs':'graphs', 'shortest paths':'graphs'
            , 'chinese remainder theory':'number theory'
            , 'suffix':'strings', 'constructive algorithms':'implementation'
            , 'hashing':'hashing', 'divide and conquer':'divide and conquer'}

engine = create_engine('mysql+mysqldb://root:@localhost/data stage fyp')
conn = engine.connect()

Session = sessionmaker(bind=engine)
s = Session()


def UniqueWords(words):
    uniqueWords = []
    [uniqueWords.append(x) for x in words if x not in uniqueWords]
    return uniqueWords

probs = s.query(Problem)
rare = {}
common = []
count = 1
for p in probs:
    tags = p.tags.split()
    newTag = ''
    for tag in tags:
        tag = tag.strip()
        flag = True
        for vTag in validTags:
            if tag in vTag:
                newTag = newTag + validTags[vTag] + ' '
                flag = False
                break
        if flag: 
            try:
                rare[tag] = rare[tag] + 1
                #rare.append(tag)
            except KeyError:
                rare[tag] = 1
            #print(newTag + ' rare')
        else:
            common.append(tag)
            #print(newTag + ' common')
            
    newTag = ' '.join( UniqueWords(newTag.split() ))
    #print(newTag)

    p.modified_tags = newTag
    s.commit()
    print('{0} out of {1} {2} : {3}'.format(str(count), str(probs.count()), p.problemId, str(newTag)))
    count += 1

sorted_rare = sorted(rare.items(), key=operator.itemgetter(1))
print('Following are rare tags: \n'+ str(sorted_rare))