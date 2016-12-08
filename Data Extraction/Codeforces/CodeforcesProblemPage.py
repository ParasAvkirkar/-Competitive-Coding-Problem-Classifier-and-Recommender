from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from CodeforcesProblem import CodeforcesProblem

import re, sys
import os
import logging
import datetime

sys.path.append("../Utilities")
from driverUtil import getDriver

driver = getDriver()
logging.basicConfig(filename='exceptScenarios.log', level=logging.ERROR)

def getCodeforcesProblem(problemUrl,problemId):
	
	try:
		driver.get(problemUrl)
		search = re.search('[a-zA-Z]', problemId)
		pos = search.start()
		problemId = problemId[:pos] + '/' + problemId[pos:]

		titleTag = driver.find_element_by_class_name("title")
		problemName = titleTag.text
		
		timeLimitTag = driver.find_element_by_class_name("time-limit")
		timelimit = timeLimitTag.text[19:]
		
		memoryLimitTag = driver.find_element_by_class_name("memory-limit")
		memorylimit = memoryLimitTag.text[21:]
		
		problemTags=''
		tagsList = driver.find_elements_by_class_name("tag-box")
		for tag in tagsList:
			problemTags = problemTags + tag.text + ' '

		problemStatementTag = driver.find_element_by_class_name("problem-statement")
		problemStatement = problemStatementTag.text
		
		print(problemId)
		# print(problemName)
		# print(problemUrl)
		# print(problemTags)
		# print(problemStatement)
		# print(timelimit)
		# print(memorylimit)

		problem = CodeforcesProblem(problemId, problemName, problemUrl, problemTags, problemStatement, timelimit, memorylimit)
		return problem
	except Exception as e:
		print(e)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print 'Exception at line '+ str(exc_tb.tb_lineno)
		logging.error('Time: {0} File: {1} Line: {2} ProblemUrl: {3} Caused By: {4}'.format(datetime.datetime.now(), os.path.basename(__file__),
								exc_tb.tb_lineno, problemUrl, e))
		# logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
		# 		' :Line Number: '+ str(exc_tb.tb_lineno) + ' :Problem Id: '+ str(problemId) +' :Caused By: ' + str(e))
		return None