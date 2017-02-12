__author__ = 'Pranay'
import string
from prob_class import Problem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

printable = set(string.printable)

def removeNondecodableChars(desc):
    desc = filter(lambda x: x in printable, desc)
    return desc

if __name__ == "__main__":
    engine = create_engine('mysql+mysqldb://root:@localhost/data stage fyp')
    conn = engine.connect()

    Session = sessionmaker(bind=engine)
    s = Session()

    probs = s.query(Problem)
    count = 1
    for p in probs:
        p.modified_description = filter(lambda x: x in printable, p.modified_description)
        s.commit()
        #print p.modified_description
        print('{0} out of {1} {2} '.format(str(count), str(probs.count()), p.prob_code))
        count = count + 1