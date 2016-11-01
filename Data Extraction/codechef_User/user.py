class User:
	baseUrl = "https://www.codechef.com/users/"
	#ratingType = ['long', 'short', 'ltime']

	def __init__(uname, country, city, isStudent, sOrP, probs, prefLang, ratings, ranks):
		self.uname = uname
		self.url = baseUrl + uname

		self.country = country
		self.state = state
		
		self.city = city
		self.sOrP = sOrP
		
		self.probs = probs
		self.prefLang = prefLang

		self.ratings = ratings
		self.ranks = ranks

		self.isStudent = isStudent


