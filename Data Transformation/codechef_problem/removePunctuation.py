from prob_class import Problem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from nltk.corpus import stopwords
import string
import re

engine = create_engine('mysql+mysqldb://root:@localhost/data stage fyp')
conn = engine.connect()

Session = sessionmaker(bind=engine)
s = Session()

probs = s.query(Problem)

punctuationSet = set(string.punctuation)
# regex = re.compile('[^a-zA-Z0-9]')
pattern = re.compile('([^\s\w]|_)+')
count = 1
for p in probs:
	desc = p.modified_description
	desc = ''.join(ch for ch in desc if ch not in punctuationSet)
	desc = pattern.sub(' ', desc)
	p.modified_description = desc
	#print(p.modified_description)
	print('{0} out of {1} {2} '.format(str(count), str(probs.count()), p.prob_code))
	count = count + 1
	s.commit()
