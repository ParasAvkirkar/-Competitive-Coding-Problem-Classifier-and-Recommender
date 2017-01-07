__author__ = 'Pranay'
import string
from prob_class import Problem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

printable = set(string.printable)

engine = create_engine('mysql+mysqldb://root:@localhost/data stage fyp')
conn = engine.connect()

Session = sessionmaker(bind=engine)
s = Session()

probs = s.query(Problem)

for p in probs:
    p.modified_description = filter(lambda x: x in printable, p.modified_description)
    s.commit()
    print p.modified_description