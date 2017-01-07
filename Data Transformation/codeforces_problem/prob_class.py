from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Problem(Base):
    __tablename__ = 'codeforces_problems'
    
    id = Column('id', Integer, primary_key = True)
    name = Column('name', String)
    problemId = Column('problemId', String)
    url = Column('url', String)
    description = Column('description', String)
    tags = Column('tags', String)
    modified_tags = Column('modified_tags', String)
    memorylimit = Column('memorylimit', String)
    difficulty = Column('difficulty', String)
    category = Column('category', String)
    timelimit = Column('timelimit', String)
    modified_description = Column('modified_description', String)

    def __repr__(self):
        return str(self.id) + " " + self.prob_code + " " + self.category
