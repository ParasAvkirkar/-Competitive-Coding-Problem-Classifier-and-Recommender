
__author__ = 'Pranay'
from prob_class import Problem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv

engine = create_engine('mysql+pymysql://root:@localhost/data stage fyp')
conn = engine.connect()

Session = sessionmaker(bind=engine)
s = Session()

probs = s.query(Problem)

probCategory = {}
with open('category.csv', 'r') as f:
    reader = csv.reader(f)
    for line in reader:
        probCategory[line[0]] = line[2]

for p in probs:
    p.category = probCategory[p.prob_code]
    s.commit()
