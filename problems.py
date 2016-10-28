class Problem:
	'Class for representing problems solved'

	def __init__(self, name, url, tags, description):
		self.id = id
		self.name = name
		self.url = url
		self.tags = tags
		self.description = description
		self.process_description()

	def __str__(self):
		return "Problem name: " + self.name + " Problem tag: " + self.tags + " Problem url: "+self.url
		#return "Problem name: " + self.name + " Problem tag: " + self.tag

	def process_description(self):
		description_lines = self.description.split('\n')
		print(description_lines)
		input_start = description_lines.index('Input')
		constraint_start = description_lines.index('Constraints')
		example_start = description_lines.index('Example')
		time_limit_start =  [i for i,word in enumerate(description_lines) if word.startswith('Time Limit:')][0]
		sources_limit_start =  [i for i,word in enumerate(description_lines) if word.startswith('Source Limit:')][0]
		lang_limit_start =  [i for i,word in enumerate(description_lines) if word.startswith('Languages:')][0]
		self.statement = description_lines[:input_start]
		self.input = description_lines[input_start:constraint_start]
		self.constraints = description_lines[constraint_start:example_start]
		self.time_limit = description_lines[time_limit_start:sources_limit_start]
		self.source_limit = description_lines[sources_limit_start:lang_limit_start]
		# print self.input
		# print self.constraints
		# print self.time_limit
		# print self.source_limit

