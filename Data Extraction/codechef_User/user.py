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
		return 'Username: '+self.uname+' Country: '+self.country+' City: '+self.city+' isStudent'+str(self.isStudent)\
		+ ' Prefered Language: ' + self.prefLang + ' Ratings: '+self.ratings+' Ranks: '+self.ranks

			
