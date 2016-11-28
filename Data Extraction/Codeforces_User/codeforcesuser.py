class CodeForcesUser:
	'Class representing users on Codeforces'

	def __init__(self, url, uname, name, country, city, organization, probs, submissions, ratings, rank, pref_lang):
		self.url = url
		self.uname = uname
		self.name = name

		self.organization = organization
		self.country = country
		self.city = city
		self.probs = probs
		self.submissions =submissions
		
		self.ratings = ratings
		self.rank = rank

		self.pref_lang = pref_lang

	def __str__(self):
		return self.uname + " " + self.name + " " + self.country + " " + self.city + " " + self.organization + " " + self.rank + " " + self.ratings

class UserSubmission:
	"""docstring for ClassName"""
	def __init__(self, problemCode, noOfSubmissions, time):
		self.problemCode = problemCode
		self.noOfSubmissions = noOfSubmissions
		self.time = time

	def __str__(self):
		return "Problem code: " + self.problemCode + " No of submissions: " + str(self.noOfSubmissions) + " Time: "+str(self.time)
