from HTMLParser import HTMLParser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from CodeforcesProblemPage import getCodeforcesProblem
from HTMLParser import HTMLParser

import pickle

current_progress = {'link':"http://codeforces.com/problemset/", 'problem_no':0, 'total_problems':0}

h = HTMLParser()
driver = webdriver.Chrome()
try:
	with open('current_progress.pickle', 'r+b') as f:
		current_progress = pickle.load(f)
		print 'Resuming Progress from page '+str(current_progress['link'])+' and problem no '+str(current_progress['problem_no'])
except Exception as e:
	print e
	print 'Starting problem collection'

page_count = current_progress['problem_no']
global_count = current_progress['total_problems']
codeforcesProblemsLink = current_progress['link']
while True:
	driver.get(codeforcesProblemsLink)

	print("Page successfully loaded")

	problemsTable = driver.find_element_by_class_name("datatable")
	problemList = problemsTable.find_elements_by_tag_name("tr")
	for problem in problemList[page_count:]:
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
				global_count = global_count + 1
				page_count = page_count +1
				with open('current_progress.pickle', 'w+b') as f:
					pickle.dump({'link':codeforcesProblemsLink, 'problem_no':page_count, 'total_problems':global_count}, f)
				print("Suceesfully extracted problem " + problemId + "  Count - " + str(global_count))

		except Exception as e:
			print("Table Header")
				#print(e)
	nextPageLink = driver.find_elements_by_class_name("arrow")
	for link in nextPageLink:
		if link.text == HTMLParser().unescape('&rarr;'):
			nextLink = link.get_attribute("href")
	if nextLink == codeforcesProblemsLink:
		break
	else:
		codeforcesProblemsLink = nextLink
	page_count = 0
	print("Loading next page")

print("Extraction completed successfully " + str(global_count))
driver.close()
