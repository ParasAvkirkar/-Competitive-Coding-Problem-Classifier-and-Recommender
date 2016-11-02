class User:
	baseUrl = "https://www.codechef.com/users/"
	#ratingType = ['long', 'short', 'ltime']

	def __init__(self, uname, country, city, isStudent, probs, prefLang, ratings, ranks):
		self.uname = uname
		self.url = self.baseUrl + uname

		self.country = country
		
		self.city = city
		self.isStudent = isStudent
		
		self.probs = probs
		self.prefLang = prefLang

		self.ratings = ratings
		self.ranks = ranks


