class SpojProblem:
	'Class for representing problems'

	def __init__(self, name, url, tags, description, addedBy, date, timelimit, sourcelimit, memorylimit, cluster, languages):
		self.id = id
		self.name = name
		self.url = url
		self.tags = tags
		self.description = description
		self.addedBy = addedBy
		self.date = date
		self.timelimit = timelimit
		self.sourcelimit = sourcelimit
		self.memorylimit = memorylimit
		self.cluster = cluster
		self.languages = languages

		#self.process_description()

	def __str__(self):
		return "Problem name: " + self.name + " Problem tag: " + self.tags + " Problem url: "+self.url
		#return "Problem name: " + self.name + " Problem tag: " + self.tag

	