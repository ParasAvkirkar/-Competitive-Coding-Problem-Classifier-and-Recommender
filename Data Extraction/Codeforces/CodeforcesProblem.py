import logging
import sys
import os
import datetime
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


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
		self.desription = problemStatement
		self.description = ""
		self.difficulty = 'Medium'
		self.category = tags
		self.process_description()
		logging.basicConfig(filename='exceptScenarios.log', level=logging.ERROR)

	def __str__(self):
		return "Problem name: " + self.name + " Problem tag: " + self.tags + " Problem url: "+self.url

	def process_description(self):
		try:			
			description_lines = self.desription.split('\n')
			# print(description_lines)
			description_lines = [line.strip() for line in description_lines]

			try:
				input_start = description_lines.index('Input')
			except ValueError:
				try:
					input_start = description_lines.index('Input :')
				except ValueError:
					try:
						input_start = description_lines.index('Input:')
					except ValueError:
						raise ValueError('Input not found')

					

			try:
				output_start = description_lines.index('Output')
			except ValueError:
				try:
					output_start = description_lines.index('Output :')
				except ValueError:
					try:
						output_start = description_lines.index('Output:')
					except ValueError:
						raise ValueError('Output not found')

			try:
				self.isExampleGiven = True
				example_start = description_lines.index('Examples')
			except ValueError:
				try:
					example_start = description_lines.index('Examples :')
				except ValueError:
					try:
						example_start = description_lines.index('Examples:')
					except ValueError:
						try:
							example_start = description_lines.index('Example')
						except ValueError:
							self.isExampleGiven = False
							raise ValueError('Example not found')

			self.statement = description_lines[:input_start]
			self.statement = ((self.create_word_features(self.statement)).replace('"', '')).replace("'", "")
			self.input = description_lines[input_start:output_start]
			self.input = ((self.create_word_features(self.input)).replace('"', '')).replace("'", "")
			self.output = description_lines[output_start:example_start]
			self.constraints = self.input
			# print self.input
			# print self.output

		except Exception as e:
			print(e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			print 'Exception at line '+ str(exc_tb.tb_lineno)
			logging.error('Time: {0} File: {1} Line: {2} ProblemUrl: {3} Caused By: {4}'.format(datetime.datetime.now(), os.path.basename(__file__),
								exc_tb.tb_lineno, self.url, e))
			# logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
			# 	' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(e))

	def create_word_features(self, words):
		useful_words = [word for word in words if word not in
                        stopwords.words('english')]
		my_dict = ' '.join([word for word in useful_words])
		return my_dict

def getProblemFromDescription(desciption):
	explanation_given = False
	if 'Explanation' in desciption:
		explanation_given = True
	problem = CodeforcesProblem('', '', '', '', desciption, '', '')
	problem.example_given = str(explanation_given)
	problem.description = problem.statement
	return problem