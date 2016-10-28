from selenium import webdriver
from problems import Problem
from bs4 import BeautifulSoup
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


import requests
import dryscrape


def getCodechefProblem(problemUrl, driver):
	#driver = webdriver.Chrome()
	#Get problem Name
	problemName = ''
	for c in problemUrl:
		if c == '/':
			break
		problemName = problemName + c
	problemName = problemName[::-1]

	driver.get(problemUrl)
	print('reach problem page '+ problemUrl)
	try:
		problemText = ''
		#divProblem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "problem-page-complete")))
		# wait = WebDriverWait(driver, 10)
		# wait.until(EC.presence_of_element_located((By.ID, "problem-page-complete")))

		divProblem = driver.find_element_by_id('problem-page-complete')					
		#print(str(divProblem))
		print('problem content got')
		all_children_by_xpath = divProblem.find_elements_by_xpath(".//*")
						
		for child in all_children_by_xpath:
			problemText = problemText + ' ' + child.text
		
		allHrefTags = driver.find_elements_by_tag_name('a')
		problemTags = ''
		for hrefTag in allHrefTags:
			if 'tag' in hrefTag.get_attribute('href'):
				problemTags = problemTags + ' ' + hrefTag.text
		
		prob = Problem(problemName, problemName, problemTags, problemText)
		# print(problemText)
		# print(prob)
	except Exception as e:
		print('element not found')
		print(e)
		prob = None
	else:
		pass
	finally:
		pass
		return prob