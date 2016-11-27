import MySQLdb

class UserSubmission:
	"""docstring for ClassName"""
	def __init__(self, problemCode, noOfSubmissions, time):
		self.problemCode = problemCode
		self.noOfSubmissions = noOfSubmissions
		self.time = time

	def __str__(self):
		return "Problem code: " + self.problemCode + " No of submissions: " + str(self.noOfSubmissions) + " Time: "+str(self.time)

class User:
	baseUrl = "https://www.codechef.com/users/"
	#ratingType = ['long', 'short', 'ltime']

	def __init__(self, uname, country, city, isStudent, successSubmissions, prefLang, ratings, ranks):
		self.uname = uname
		self.url = self.baseUrl + uname

		self.country = country
		
		self.city = city
		self.isStudent = isStudent
		
		self.successSubmissions = successSubmissions
		self.prefLang = prefLang

		self.ratings = ratings
		self.ranks = ranks

	def __str__(self):
		return 'Username: '+self.uname+' Country: '+self.country+' City: '+self.city+' isStudent'+str(self.isStudent)
		+ ' Prefered Language: ' + self.prefLang + ' Ratings: '+self.ratings+' Ranks: '+self.ranks

	# def connect_db(self):
	# 	# Open database connection
	# 	ip = "localhost"
	# 	username = "root"
	# 	password = ""
	# 	db_name = "data stage fyp"
		
	# 	db = MySQLdb.connect(ip, username, password, db_name)
	# 	return db

	# def insert_db(self, uname, country, userCity, isStudent, problemsSolved, prefLang, rating, rank):
	# 	q = "INSERT INTO codechef_user VALUES ( " + "null, '" + uname + "', '" + country + "', '" + userCity + "', '" + str(isStudent) + "', '" + prefLang + "', '" + str(rating['Long']) + "', '" + str(rating['Short']) +"', '" + str(rating['LTime']) +"', '" + str(rank['Long']) +"', '"+ str(rank['Short']) +"', '" + str(rank['LTime']) + "')"
	# 	print q

	# 	db = self.connect_db()
	# 	# prepare a cursor object using cursor() method
	# 	cursor = db.cursor()

	# 	# execute SQL query using execute() method.
	# 	if cursor.execute(q) == 1:
	# 		db.commit()
	# 		print "Success DB"
	# 	else: print "Fail DB"	
			

