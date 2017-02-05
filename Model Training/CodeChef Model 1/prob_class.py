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
    modified_description = Column('modified_description', String)

    def __repr__(self):
        return str(self.id) + " " + self.prob_code + " " + self.category

class Codeforces_Problem(Base):
    __tablename__ = 'codeforces_problems'
    
    id = Column('id', Integer, primary_key = True)
    problemId = Column('problemId', Integer)
    name = Column('name', String)
    url = Column('url', String)
    description = Column('description', String)
    tags = Column('tags', String)
    time_limit = Column('timelimit', String)
    submission_size = Column('memorylimit', String)
    difficulty = Column('difficulty', String)
    category = Column('category', String)
    modified_description = Column('modified_description', String)
    modified_tags = Column('modified_tags', String)

    def __repr__(self):
        return str(self.id) + " " + self.prob_code + " " + self.category
