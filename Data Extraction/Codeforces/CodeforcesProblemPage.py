from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from CodeforcesProblem import CodeforcesProblem

import re

driver = webdriver.Chrome()

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
		print('ERROR')
		print(e)
		with open('codeforces/error', 'a') as f:
			f.write(problemName+'\n')
		return None