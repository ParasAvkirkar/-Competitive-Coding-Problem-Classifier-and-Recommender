from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Integrated_Problem(Base):
    __tablename__ = 'problem'
    
    id = Column('id', Integer)
    platform = Column('platform', String)
    prob_code = Column('prob_code', String, primary_key=True)
    url = Column('url', String)
    description = Column('description', String)
    tags = Column('tags', String)
    sub_size = Column('sub_size', String)
    difficulty = Column('difficulty', String)
    category = Column('category', String)
    time_limit = Column('time_limit', String)
    memory_limit = Column('memory_limit', String)
    modified_description = Column('modified_description', String)

    def __repr__(self):
        return str(self.id) + " " + self.prob_code + " " + self.category


class Codechef_Problem(Base):
    __tablename__ = 'codechef_problem'

    id = Column('id', Integer, primary_key=True)
    prob_code = Column('prob_code', String)
    url = Column('url', String)
    description = Column('description', String)
    tags = Column('tag', String)
    sub_size = Column('submission_size', String)
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

    id = Column('id', Integer, primary_key=True)
    prob_code = Column('problemId', Integer)
    name = Column('name', String)
    url = Column('url', String)
    description = Column('description', String)
    tags = Column('tags', String)
    time_limit = Column('timelimit', String)
    sub_size = Column('memorylimit', String)
    difficulty = Column('difficulty', String)
    category = Column('category', String)
    modified_description = Column('modified_description', String)
    modified_tags = Column('modified_tags', String)

    def __repr__(self):
        return str(self.id) + " " + self.prob_code + " " + self.category
