import csv

__author__ = 'Pranay'
from prob_class import Problem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

tag_map = {
}

# with open('tag_map.csv','wb') as f:
#     w = csv.writer(f)
#     for category in tag_map:
#         w.writerow([category]+tag_map[category])

with open('tag_map.csv','rb') as f:
    r = list(csv.reader(f))
    for row in r:
        tag_map[row[0]] = [code for code in row[1:]]

print tag_map

engine = create_engine('mysql+mysqldb://root:@localhost/data stage fyp')
conn = engine.connect()

Session = sessionmaker(bind=engine)
s = Session()

probs = s.query(Problem)

for p in probs:
    tags = p.tag.split()
    print tags
    f = False
    for category in tag_map:
        f = False
        for code in tag_map[category]:
            for tag in tags:
                f = f or (code in tag)
        if f:
            p.category = category
            break
    if not f:
        p.category = 'N/A'
    s.commit()