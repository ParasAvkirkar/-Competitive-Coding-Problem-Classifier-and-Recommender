from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from prob_class import Problem
from training_params import categories

engine = create_engine('mysql+mysqldb://root:@localhost/data stage fyp')
conn = engine.connect()

Session = sessionmaker(bind=engine)
s = Session()

probs = s.query(Problem)#.filter(Problem.category == 'dp' or)


#problist = [p for p in probs if p.category == 'dp' or p.category == 'graph']
problist = [p for p in probs if p.category in categories]
#print len(problist)
print(len(list(probs)))

def get_probs():
    return list(problist)


def getProbByCode(probCode):
	return [prob for prob in probs if probCode in prob.prob_code][0]