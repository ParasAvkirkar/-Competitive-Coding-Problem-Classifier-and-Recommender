import MySQLdb

class UserSubmission:
	"""docstring for ClassName"""
	def __init__(self, problemCode, noOfSubmissions, date):
		self.problemCode = problemCode
		self.noOfSubmissions = noOfSubmissions
		self.date = date

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
