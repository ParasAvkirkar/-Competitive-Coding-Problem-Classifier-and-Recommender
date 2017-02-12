from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Problem(Base):
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
