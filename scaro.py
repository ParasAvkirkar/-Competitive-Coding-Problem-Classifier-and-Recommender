from CodechefProblemPage import getCodechefProblem
from bs4 import BeautifulSoup

from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


from selenium import webdriver


import requests
import pickle
from problems import Problem

current_progress = {'section':0, 'problem_no':0}
codechefUrl = 'https://www.codechef.com'
codechefProblemUrl = 'https://www.codechef.com/problems'
section = '/easy'


response = requests.get(codechefProblemUrl + section)
soup = BeautifulSoup(response.content, 'html.parser')

problemCollections = []
count = 0

problemRows = soup.find_all('tr')
driver = webdriver.Chrome()

for row in problemRows:
	problemName = ''
	# if(count > 2):
	# 	break
	if row.has_attr('class') and 'problemrow' in row['class']:
		allHrefTags = row.find_all('a')
		for a in allHrefTags:
			if a.has_attr('href') and 'problem' in a['href']:
				problemName = a.b.string
				
				# driver = webdriver.PhantomJS()
				# driver = webdriver.Firefox()
				# firefox_capabilities = DesiredCapabilities.FIREFOX
				# firefox_capabilities['marionette'] = True

				# driver = webdriver.Firefox(capabilities=firefox_capabilities)
				# drsiver = webdriver.Chrome()
				# driver.set_window_size(1120, 550)

				print('inside loop ' + codechefUrl + a['href'])
				prob = getCodechefProblem(codechefUrl + a['href'], driver)
				if prob == None:
					print('issue')
				else:
					print('not issue ' + str(count))
				count = count + 1
				problemCollections.append(prob)

				
driver.quit()				
for problem in problemCollections:
	print(problem)


codechefProblemUrl = 'https://www.codechef.com/problems/'
sections = ['easy', 'medium', 'hard']

try:
	with open('current_progress.pickle', 'r+b') as f:
		current_progress = pickle.load(f)
		print('Resuming Progress from problem '+str(current_progress['problem_no'])+' ')
except Exception as e:
	print('Starting problem collection')

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
					p = getCodechefProblem(codechefUrl+a['href'])
					if p:
						with open('codechef/'+p.name, 'w+b') as f:
							pickle.dump(p, f)
							# f.write(p.__str__())
							# f.write(str(p.id)+'\t'+p.name+'\t'+p.url+'\t'+p.tags+'\t')#+p.description.encode('utf-8'))
							# f.write(p.description.encode('utf-8'))
						count+=1
						with open('current_progress.pickle', 'w+b') as f:
							pickle.dump({'section':sec_count, 'problem_no':count}, f)
	sec_count += 1
	with open('current_progress.pickle', 'w+b') as f:
		pickle.dump({'section':sec_count, 'problem_no':count}, f)

