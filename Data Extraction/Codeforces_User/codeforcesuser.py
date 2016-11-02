class CodeForcesUser:
	'Class representing users on Codeforces'

	def __init__(self, url, uname, name, country, city, organization, probs, ratings, rank):
		self.url = url
		self.uname = uname
		self.name = name

		self.organization = organization
		self.country = country
		self.city = city
		self.probs = probs

		self.ratings = ratings
		self.rank = rank


	def __str__(self):
		return self.uname + " " + self.name + " " + self.country + " " + self.city + " " + self.organization + " " + self.rank + " " + self.ratings

