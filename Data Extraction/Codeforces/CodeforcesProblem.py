class CodeforcesProblem:
	'Class for representing problems'

	def __init__(self, problemId, name, url, tags, problemStatement, timelimit, memorylimit):
		self.id = id
		self.problemId = problemId
		self.name = name
		self.url = url
		self.tags = tags
		self.problemStatement = problemStatement
		self.timelimit = timelimit
		self.memorylimit = memorylimit

	def __str__(self):
		return "Problem name: " + self.name + " Problem tag: " + self.tags + " Problem url: "+self.url
	