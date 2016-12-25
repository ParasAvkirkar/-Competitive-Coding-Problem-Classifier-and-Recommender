from prob_class import Problem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from nltk.corpus import stopwords

def create_word_features(words):
	# print words
	w = []
	for wrd in words.split():
		w.append(wrd)
	useful_words = [word for word in w if word not in
                       stopwords.words('english')]
	my_dict = ' '.join([word for word in useful_words])
	# print my_dict
	return my_dict

engine = create_engine('mysql+mysqldb://root:@localhost/data stage fyp')
conn = engine.connect()

Session = sessionmaker(bind=engine)
s = Session()

probs = s.query(Problem)

for p in probs:
    # print p.description
    try:
        p.description = create_word_features(p.description)
        print "success " + p.prob_code
        s.commit()
    except:
        print "failed " +p.prob_code

    # print desc
    # print