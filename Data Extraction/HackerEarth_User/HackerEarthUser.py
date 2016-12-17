class HackerEarthUser:
	'Class representing users on HackerEarth'

	def __init__(self, url, uname, name, location, education, ratings, pref_lang, submissions):
		self.url = url
		self.uname = uname
		self.name = name

		self.location = location
		self.education = education
		self.submissions =submissions
		
		self.ratings = ratings
		
		self.pref_lang = pref_lang

	def __str__(self):
		return self.uname + " " + self.name + " " + self.location  + " " + self.education  + " " + self.ratings

"""class UserSubmission:
	
	def __init__(self, problemCode, noOfSubmissions, time):
		self.problemCode = problemCode
		self.noOfSubmissions = noOfSubmissions
		self.time = time

	def __str__(self):
		return "Problem code: " + self.problemCode + " No of submissions: " + str(self.noOfSubmissions) + " Time: "+str(self.time)
"""