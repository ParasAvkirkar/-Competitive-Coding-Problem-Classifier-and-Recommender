from HTMLParser import HTMLParser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from CodeforcesProblemPage import getCodeforcesProblem
from HTMLParser import HTMLParser

import pickle
import sys
import os
import datetime
import logging
sys.path.append("../Utilities")
from driverUtil import getDriver
sys.path.append("../DataBase")
import sqlDB


current_progress = {'link':"http://codeforces.com/problemset/", 'problem_no':0, 'total_problems':0}
logging.basicConfig(filename='exceptScenarios.log', level=logging.ERROR)

h = HTMLParser()
driver = getDriver()
try:
	with open('current_progress.pickle', 'r+b') as f:
		current_progress = pickle.load(f)
		print 'Resuming Progress from page '+str(current_progress['link'])+' and problem no '+str(current_progress['problem_no'])
except Exception as e:
	print(e)
	exc_type, exc_obj, exc_tb = sys.exc_info()
	print 'Exception at line '+ str(exc_tb.tb_lineno)
	logging.error('Time: {0} File: {1} Line: {2} Caused By: {3}'.format(datetime.datetime.now(), os.path.basename(__file__),
								exc_tb.tb_lineno, e))
	# logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
	# 		' :Line Number: '+ str(exc_tb.tb_lineno) + ' :Caused By: ' + str(e))
	
try:
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
					# with open('codeforces/'+p.name, 'w+b') as f:
					# 	pickle.dump(p, f)
					sqlDB.insert_problem_db('codeforces_problem', p.name, p.url, p.problemStatement, p.tags, p.difficulty, p.category,
													'', p.constraints, p.timelimit, '50000', p.isExampleGiven)
					global_count = global_count + 1
					page_count = page_count + 1
					with open('current_progress.pickle', 'w+b') as f:
						pickle.dump({'link':codeforcesProblemsLink, 'problem_no':page_count, 'total_problems':global_count}, f)
					print("Suceesfully extracted problem " + problemId + "  Count - " + str(global_count))

			except Exception as e:
				if page_count != 0 :
					print(e)
					exc_type, exc_obj, exc_tb = sys.exc_info()
					print 'Exception at line ' + str(exc_tb.tb_lineno)
					logging.error('Time: {0} File: {1} Line: {2} ProblemsListPageUrl: {3} ProblemUrl: {4} Caused By: {5}'.format(datetime.datetime.now(), os.path.basename(__file__),
						exc_tb.tb_lineno, codeforcesProblemsLink, problemLink, e))
				# logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
				# 	+ ' :Problem Link: '+ str(codeforcesProblemsLink) +' :Line Number: '+ str(exc_tb.tb_lineno) + ' :Caused By: ' + str(e))

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
except Exception as e:
	print(e)
	exc_type, exc_obj, exc_tb = sys.exc_info()
	print 'Exception at line '+ str(exc_tb.tb_lineno)
	logging.error('Time: {0} File: {1} Line: {2} ProblemsListPageUrl: {3} Caused By: {4}'.format(datetime.datetime.now(), os.path.basename(__file__),
		exc_tb.tb_lineno, codeforcesProblemsLink, e))
	# logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
	# 		' :Line Number: '+ str(exc_tb.tb_lineno) + ' :Caused By: ' + str(e))
