from CodechefProblemPage import getCodechefProblem
from bs4 import BeautifulSoup
import requests
import pickle
from problems import Problem
import sys
sys.path.append("../DataBase")
import sqlDB

current_progress = {'section':0, 'problem_no':0}
codechefUrl = 'https://www.codechef.com'
codechefProblemUrl = 'https://www.codechef.com/problems/'
sections = ['easy', 'medium', 'hard']

try:
	with open('current_progress.pickle', 'r+b') as f:
		current_progress = pickle.load(f)
		print 'Resuming Progress from problem '+sections[current_progress['section']]+' and problem no '+str(current_progress['problem_no'])
except Exception as e:
	print e
	print 'Starting problem collection'

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