from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm
from sqlalchemy import Column, Integer, String, DateTime
import sys, pickle

sys.path.append('Utilities/')
from constants import categories, codechefDifficultyLevels

Base = declarative_base()


class Codechef_User(Base):
    __tablename__ = 'codechef_user'

    id = Column('id', Integer, primary_key=True)
    uname = Column('uname', String)
    country = Column('country', String)
    city = Column('city', String)
    is_student = Column('is_student', String)
    pref_lang = Column('pref_lang', String)

    rating_long = Column('rating_long', String)
    rating_short = Column('rating_short', String)
    rating_ltime = Column('rating_ltime', String)
    rank_long = Column('rank_long', String)
    rank_short = Column('rank_short', String)
    rank_ltime = Column('rank_ltime', String)

    total_solved = Column('total_solved', String)
    easy_solved = Column('easy_solved', String)
    medium_solved = Column('medium_solved', String)
    hard_solved = Column('hard_solved', String)
    challenge_solved = Column('challenge_solved', String)
    school_solved = Column('school_solved', String)
    unknown_solved = Column('unknown_solved', String)

    @orm.reconstructor
    def init_on_load(self):
        # A map for each user
        # It contains category as key, whose values is another map
        # This map has difficulty as key and value as list of attempts taken to solve that problem
        self.categoryDifficultyMap = {}
        self.user_level = 0.0
        self.solved_probs = {}
        self.failed_probs = {}
        self.recommendation_list = []
        self.problemMappings = {}

        for category in categories:
            #levelDict = {}
            self.categoryDifficultyMap[category] = {}
            for level in codechefDifficultyLevels:
                self.categoryDifficultyMap[category][level] = 0


    # Applicable only when categoryDifficultyMap is filled
    # Generally this method is expected to be called after building categoryDifficultyMap from database
    def calculate_user_level(self):
        for category in self.categoryDifficultyMap:
            levelDict = self.categoryDifficultyMap[category]
            for level in codechefDifficultyLevels:
                probs_solved_in_current_level = len(levelDict[level])
                self.user_level += probs_solved_in_current_level * codechefDifficultyLevels[level]

    def __repr__(self):
        return str(self.id) + " " + self.uname + " " + str(self.user_level)


class Codechef_User_Prob_Map(Base):
    __tablename__ = 'codechef_prob_user_diff_map'

    id = Column('id', Integer, primary_key=True)
    uname = Column('uname', String)
    prob_code = Column('prob_code', String)
    date = Column('date', DateTime)
    no_of_submissions = Column('no_of_submissions', String)
    difficulty = Column('difficulty', String)

    def __repr__(self):
        return str(self.id) + " " + self.uname + " " + self.prob_code
