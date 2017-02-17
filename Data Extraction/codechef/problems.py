from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk.classify.util

import sys
import os
import logging
import datetime

class Problem:
	'Class for representing problems solved'

	def __init__(self, name, url, tags, description, difficulty, submission_size):
		self.id = id
		self.name = name
		self.url = url
		self.tags = tags
		self.description = description
		self.process_description()
		self.difficulty = difficulty
		if difficulty == 'unknown':
			self.difficulty = 'medium'
		self.submission_size = submission_size
		if difficulty == 'hard':
			self.example_given = False
		self.example_given = True
		self.category = self.tags
		logging.basicConfig(filename='exceptScenarios.log', level=logging.ERROR)

	def __str__(self):
		return "Problem name: " + self.name + " Problem tag: " + self.tags + " Problem url: "+self.url + " Submission Size: "+ str(self.submission_size)
		#return "Problem name: " + self.name + " Problem tag: " + self.tag

	def process_description(self):
		try:
			description_lines = self.description.split('\n')
			#print(description_lines)
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
						try:
							input_start = description_lines.index('INPUT FORMAT')
						except ValueError:
							try:
								input_start = description_lines.index('INPUT:')
							except ValueError:
								try:
									input_start = description_lines.index('Input format')
								except ValueError:
									try:
										input_start = description_lines.index('Input Format')
									except ValueError:
										try:
											input_start = description_lines.index('Input Description')
										except ValueError:
											input_start = description_lines.index('Input format:')



			try:
				example_start = description_lines.index('Example')
			except ValueError:
				try:
					example_start = description_lines.index('Example:')
				except ValueError:
					try:
						example_start = description_lines.index('Example :')
					except ValueError:
						try:
							example_start = description_lines.index('Example 1')
						except:
							example_start = -1
							

			try:
				constraint_start = description_lines.index('Constraints')
			except ValueError:
				try:
					constraint_start = description_lines.index('Constraints :')
				except ValueError:
					try:
						constraint_start = [i for i,word in enumerate(description_lines) if word.startswith('Constraints and Subtasks')][0]
					except:
						try:
							constraint_start = description_lines.index('Constraints:')
						except:
							try:
								constraint_start = description_lines.index('CONSTRAINTS')
							except:
								try:
									constraint_start = description_lines.index('CONSTRAINTS:')
								except:
									constraint_start = example_start	# means constraints not given


			time_limit_start =  [i for i,word in enumerate(description_lines) if word.startswith('Time Limit:')][0]
			sources_limit_start =  [i for i,word in enumerate(description_lines) if word.startswith('Source Limit:')][0]
			lang_limit_start =  [i for i,word in enumerate(description_lines) if word.startswith('Languages:')][0]
			self.statement = description_lines[:input_start]
			self.statement = ((self.create_word_features(self.statement)).replace('"', '')).replace("'", "")
			self.input = description_lines[input_start:constraint_start]
			self.input = ((self.create_word_features(self.input)).replace('"', '')).replace("'", "")
			self.constraints = description_lines[constraint_start:example_start]
			self.constraints = ((self.create_word_features(self.constraints)).replace('"', '')).replace("'", "")
			self.time_limit = description_lines[time_limit_start:sources_limit_start]
			self.source_limit = description_lines[sources_limit_start:lang_limit_start]
			sl = self.source_limit[0]
			self.source_limit = (sl[sl.index(':')+1:sl.index('B')]).strip()
			tl = self.time_limit[0]
			self.time_limit = (tl[tl.index(':')+1:tl.index('s')]).strip()
			# print self.description
			# print self.input
			# print self.constraints
			# print self.time_limit
			# print self.source_limit
		except Exception as e:
			print(e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			print 'Exception at line '+ str(exc_tb.tb_lineno)
			logging.error('Time: {0} File: {1} Line: {2} Caused By: {3}  Problem Name: {4}'.format(datetime.datetime.now(), os.path.basename(__file__),
						exc_tb.tb_lineno, e, self.name))
			# logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
			# 		' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(e))


	def create_word_features(self, words):
		# print words
		w = []
		for line in words:
			for wrd in line.split():
				w.append(wrd)
		useful_words = [word for word in w if word not in
                        stopwords.words('english')]
		my_dict = ' '.join([word for word in useful_words])
		# print my_dict
		return my_dict

def getProblemFromDescription(desciption):
	explanation_given = False
	if 'Explanation' in desciption:
		explanation_given = True
	problem = Problem('', '', '', desciption, '', '')
	problem.example_given = str(explanation_given)
	problem.description = problem.statement
	return problem