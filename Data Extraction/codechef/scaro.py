from CodechefProblemPage import getCodechefProblem
from bs4 import BeautifulSoup
import requests
import pickle
from problems import Problem
import os
import logging
import sys
import datetime
import winsound
sys.path.append("../DataBase")
import sqlDB

logging.basicConfig(filename='exceptScenarios.log', level=logging.ERROR)

current_progress = {'section':0, 'problem_no':0}
codechefUrl = 'https://www.codechef.com'
codechefProblemUrl = 'https://www.codechef.com/problems/'
sections = ['easy', 'medium', 'hard', 'school']

try:
	with open('current_progress.pickle', 'r+b') as f:
		current_progress = pickle.load(f)
		print 'Resuming Progress from problem '+sections[current_progress['section']]+' and problem no '+str(current_progress['problem_no'])
except Exception as e:
	print(e)
	exc_type, exc_obj, exc_tb = sys.exc_info()
	print 'Exception at line '+ str(exc_tb.tb_lineno)
	logging.error('Time: {0} File: {1} Line: {2} Caused By: {3}'.format(datetime.datetime.now(), os.path.basename(__file__),
				exc_tb.tb_lineno, e))
	# logging.error('Time: {0} File: {1} Line: {2} Caused By: {3}'.format(datetime.datetime.now(), os.path.basename(__file__),
	# 				exc_tb.tb_lineno, e))
	# logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
	# 	' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(e))

print 'Starting problem collection'

prob_href = ''
try:
	sec_count = current_progress['section']

	for section in sections[sec_count:]:
		response = requests.get(codechefProblemUrl + section)
		soup = BeautifulSoup(response.content, 'html.parser')
		count = current_progress['problem_no']
		problemCollections = []
		problemRows = soup.find_all('tr')
		for row in problemRows[count:]:
			if row.has_attr('class') and 'problemrow' in row['class']:
				allHrefTags = row.find_all('a')
				for a in allHrefTags:
					if a.has_attr('href') and 'problem' in a['href']:
						prob_href = a['href']
						p = getCodechefProblem(codechefUrl+a['href'], sections[current_progress['section']])
						if p:
							sqlDB.insert_problem_db('codechef_problem', p.name, p.url, p.statement, p.tags, p.difficulty, p.category,
													p.submission_size, p.constraints, p.time_limit, p.source_limit, p.example_given)
							# with open('codechef/'+p.name, 'w+b') as f:
							# 	pickle.dump(p, f)
								# f.write(p.__str__())
								# f.write(str(p.id)+'\t'+p.name+'\t'+p.url+'\t'+p.tags+'\t')#+p.description.encode('utf-8'))
								# f.write(p.description.encode('utf-8'))
							count+=1
							with open('current_progress.pickle', 'w+b') as f:
								pickle.dump({'section':sec_count, 'problem_no':count}, f)
		sec_count += 1
		count = 0
		with open('current_progress.pickle', 'w+b') as f:
			pickle.dump({'section':sec_count, 'problem_no':0}, f)
except Exception as e:
	print(e)
	exc_type, exc_obj, exc_tb = sys.exc_info()
	print 'Exception at line '+ str(exc_tb.tb_lineno)
	logging.error('Time: {0} File: {1} Line: {2} Caused By: {3} Problem href: {4}'.format(datetime.datetime.now(), os.path.basename(__file__),
					exc_tb.tb_lineno, e, prob_href))
	winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
	# logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
	# 	' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(e))