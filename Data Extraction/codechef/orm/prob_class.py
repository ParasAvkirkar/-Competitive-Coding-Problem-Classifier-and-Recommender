from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Problem(Base):
    __tablename__ = 'codechef_problem'
    
    id = Column('id', Integer, primary_key = True)
    prob_code = Column('prob_code', String)
    url = Column('url', String)
    description = Column('description', String)
    tag = Column('tag', String)
    submission_size = Column('submission_size', String)
    constraint = Column('constraint', String)
    example_given = Column('example_given', String)
    difficulty = Column('difficulty', String)
    category = Column('category', String)
    time_limit = Column('time_limit', String)
    source_limit = Column('source_limit', String)

    def __repr__(self):
        return str(self.id) + " " + self.prob_code + " " + self.category
