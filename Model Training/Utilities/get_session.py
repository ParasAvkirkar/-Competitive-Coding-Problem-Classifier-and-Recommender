from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_session():
	engine = create_engine('mysql+mysqldb://root:@localhost/data stage fyp')
	conn = engine.connect()

	Session = sessionmaker(bind=engine)
	s = Session()

	return s