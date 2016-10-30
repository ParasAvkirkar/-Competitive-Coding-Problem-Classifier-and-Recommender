class SpojUser:
	def __init__(uname, country, probs, ratings, ranks):
		self.uname = uname
		self.url = baseUrl + uname

		self.country = country
		self.probs = probs

		self.ratings = ratings
		self.ranks = ranks


