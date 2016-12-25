from prob_class import Problem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append('../../Data Extraction/codechef')
sys.path.append('../../Data Extraction/Utilities')

from CodechefProblemPage import getCodechefProblem

engine = create_engine('mysql+mysqldb://root:@localhost/data stage fyp')
conn = engine.connect()

Session = sessionmaker(bind=engine)
s = Session()

probs = s.query(Problem).filter(Problem.description == '')

for p in probs:
    prob = getCodechefProblem(p.url, p.difficulty)
    print p.prob_code
    p.description = prob.statement
    s.commit()