class SpojProblem:
	'Class for representing problems'

	def __init__(self, name, url, tags, description):
		self.id = id
		self.name = name
		self.url = url
		self.tags = tags
		self.description = description
		#self.process_description()

	def __str__(self):
		return "Problem name: " + self.name + " Problem tag: " + self.tags + " Problem url: "+self.url
		#return "Problem name: " + self.name + " Problem tag: " + self.tag

	