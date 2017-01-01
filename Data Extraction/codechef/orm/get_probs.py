from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from prob_class import Problem

engine = create_engine('mysql+mysqldb://root:@localhost/data stage fyp')
conn = engine.connect()

Session = sessionmaker(bind=engine)
s = Session()

probs = s.query(Problem).filter()

problist = [p for p in probs]
print len(problist)

def get_probs():
    return problist


