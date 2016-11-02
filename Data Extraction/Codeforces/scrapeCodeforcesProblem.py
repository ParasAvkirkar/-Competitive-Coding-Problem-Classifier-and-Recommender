from HTMLParser import HTMLParser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from CodeforcesProblemPage import getCodeforcesProblem

import html
import pickle

current_progress = {'page':1, 'problem_no':0}

driver = webdriver.Chrome()
try:
	with open('current_progress.pickle', 'r+b') as f:
		current_progress = pickle.load(f)
		print 'Resuming Progress from page '+str(current_progress['page'])+' and problem no '+str(current_progress['problem_no'])
except Exception as e:
	print e
	print 'Starting problem collection'

count = current_progress['problem_no']
page_no = current_progress['page']
codeforcesProblemsLink="http://codeforces.com/problemset/page/"
while True:
	driver.get(codeforcesProblemsLink+str(page_no))

	print("Page successfully loaded")

	problemsTable = driver.find_element_by_class_name("datatable")
	problemList = problemsTable.find_elements_by_tag_name("tr")
	for problem in problemList[count:]:
		try:
			problemLink = problem.find_element_by_class_name("id")
			problemLink = problemLink.find_element_by_tag_name("a")
			problemId = problemLink.text
			problemLink = problemLink.get_attribute("href")
			
			print("Problem link extracted")

			p = getCodeforcesProblem(problemLink,problemId)
			if p:
				with open('codeforces/'+p.name, 'w+b') as f:
					pickle.dump(p, f)
				count = count + 1
				with open('current_progress.pickle', 'w+b') as f:
					pickle.dump({'page':page_no, 'problem_no':count}, f)
				print("Suceesfully extracted problem " + problemId + "  Count - " + str(count))

		except Exception as e:
			print("Table Header")
				#print(e)
	# nextPageLink = driver.find_elements_by_class_name("arrow")
	# for link in nextPageLink:
	# 	if link.text == HTMLParser().unescape('&rarr;'):
	# 		nextLink = link.get_attribute("href")
	# if nextLink == codeforcesProblemsLink:
	# 	break
	# else:
	# 	codeforcesProblemsLink = nextLink
	page_no += 1
	print codeforcesProblemsLink + str(page_no)
	count = 0
	print("Loading next page")

print("Extraction completed successfully " + str(count))
driver.close()
