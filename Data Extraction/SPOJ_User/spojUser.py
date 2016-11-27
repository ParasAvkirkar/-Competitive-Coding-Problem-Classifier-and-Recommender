class SubmissionDetails:
	def __init__(self, problemCode, noOfSubmissions, time):
		self.problemCode = problemCode
		self.noOfSubmissions = noOfSubmissions
		self.time = time

class SpojUser:
	def __init__(self, url, uname, country, submissionDetails, ratings, ranks):
		self.url = url
		self.uname = uname
		#self.name = name

		self.country = country
		self.submissionDetails = submissionDetails

		self.ratings = ratings
		self.ranks = ranks

	def __str__(self):
		return 'Username: '+ self.uname + ' Country: ' + self.country + ' Ratings: ' + self.ratings + ' Ranks: ' + self.ranks


