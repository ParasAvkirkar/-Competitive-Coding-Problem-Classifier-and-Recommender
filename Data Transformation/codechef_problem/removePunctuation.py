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
pattern = re.compile('[^a-zA-Z0-9]+')
# pattern = re.compile('([^\s\w]|_)+')
count = 1

# sample = 'know potato first food ever grown space ? today big day chef crum called make potato dishes people valley food got angry knowing someone said potatoes thick started making thin crisp ! (and thus invented potato chips :) ) n persons sitting row ( numbered 0 n-1 ) given array v v[i] village number ith person r rounds po serves potato chips group people sitting continuously (a sub-array) shifu worried round k people village served potato chips others may protest leads disruption outer peace estimate damage round wants know many distinct villages k people served round'
# print sample
# sample = pattern.sub(' ', sample)
# print sample


for p in probs:
	desc = p.modified_description
	desc = ''.join(ch for ch in desc if ch not in punctuationSet)
	desc = pattern.sub(' ', desc)

	# print p.modified_description
	
	p.modified_description = desc
	# print(p.modified_description)
	
	print('{0} out of {1} {2} '.format(str(count), str(probs.count()), p.prob_code))
	# print
	count = count + 1
	s.commit()
