import sys, os
sys.path.append('../Utilities')

from prob_class import Problem
from get_session import get_session

def get_probs():
	s = get_session()
	probs = s.query(Problem).filter()

	problist = [p for p in probs]
	print len(problist)
    
	return problist

def get_probs_without_category_NA():
	s = get_session()
	probs = s.query(Problem).filter()

	problist = [p for p in probs if p.category != 'N/A']
	print len(problist)
    
	return problist

if __name__ == '__main__':
	get_probs_without_category_NA()