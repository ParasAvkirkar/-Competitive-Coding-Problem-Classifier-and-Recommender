from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Problem(Base):
    __tablename__ = 'codeforces_problems'
    
    id = Column('id', Integer, primary_key = True)
    prob_code = Column('problemId', String)
    url = Column('url', String)
    description = Column('description', String)
    tag = Column('tags', String)
    # submission_size = Column('submission_size', String)
    # constraint = Column('constraint', String)
    example_given = 'True'
    difficulty = Column('difficulty', String)
    category = Column('category', String)
    time_limit = Column('timelimit', String)
    source_limit = Column('memorylimit', String)

    def __repr__(self):
        return str(self.id) + " " + self.prob_code + " " + self.category
