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

		self.process_description()

	def __str__(self):
		return "Problem name: " + self.name + " Problem tag: " + self.tags + " Problem url: "+self.url
		#return "Problem name: " + self.name + " Problem tag: " + self.tag

	def process_description(self):
		description_lines = self.description
		# print(description_lines)
		# description_lines = [line.strip() for line in description_lines]
		try:
			input_start = description_lines.index('Input')
			output_start = description_lines.index('Output')
			example_start = description_lines.index('Example')
		except ValueError:
			input_start = 0
			output_start = len(description_lines[0])
			example_start = len(description_lines[0])

		self.statement = description_lines[:input_start].split('\n')
		self.input = description_lines[input_start:output_start].split('\n')
		self.output = description_lines[output_start:example_start].split('\n')
		self.constraints = self.input
		print 'Statement'
		print self.statement
		print 'Input'
		print self.input
		print 'Output'
		print self.output