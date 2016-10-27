from selenium import webdriver
from problems import Problem
from bs4 import BeautifulSoup
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


import requests


def getCodechefProblem(problemUrl):
	count = 0
	driver = webdriver.Chrome('C:\Users\Pranay\Downloads\Setups\Drivers\chromedriver.exe')
	#Get problem Name
	problemName = ''
	for c in problemUrl[::-1]:
		if c == '/':
			break
		problemName = problemName + c
	problemName = problemName[::-1]
	driver.get(problemUrl)
	print('reach problem page '+ problemUrl)
	try:
		problemText = ''
		#divProblem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "problem-page-complete")))

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
		
		prob = Problem(problemName, problemUrl, problemTags, problemText)
		# print(problemText)
		# print(prob)
		
		count = count + 1
		return prob
	except Exception as e:
			print('element not found')
			print(e)
			return None
	finally:
		driver.quit()