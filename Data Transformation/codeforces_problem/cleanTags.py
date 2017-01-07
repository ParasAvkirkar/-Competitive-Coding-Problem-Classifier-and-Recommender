import csv

__author__ = 'Pranay'
from prob_class import Problem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


validTags = ['dp', 'math', 'greedy', 'data structure', 'graph', 'string', 'geometry'
                , 'binary search', 'number theory', 'constructive algorithm', 
                'dfs', 'flows', 'sorting', 'brute force']

engine = create_engine('mysql+mysqldb://root:@localhost/data stage fyp')
conn = engine.connect()

Session = sessionmaker(bind=engine)
s = Session()


def UniqueWords(words):
    uniqueWords = []
    [uniqueWords.append(x) for x in words if x not in uniqueWords]
    return uniqueWords

probs = s.query(Problem)

for p in probs:
    tags = p.tags.split()

    newTag = ''
    for tag in tags:
        flag = False 

        for vTag in validTags:
            eachVTag = vTag.split()
            for e in eachVTag:
                if e in tag:
                    flag = True
                    break
            if flag:
                newTag = newTag + ' ' + vTag
                break
    if(newTag is not ''):
        newTag = ' '.join( UniqueWords(newTag.split() ))
        print(newTag)
    else:
        newTag = 'N/A'
    p.modified_tags = newTag
    s.commit()