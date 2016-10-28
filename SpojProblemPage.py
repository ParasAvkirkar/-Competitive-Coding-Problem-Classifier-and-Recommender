from selenium import webdriver
from spojProblem import SpojProblem
from bs4 import BeautifulSoup
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


import requests


driver = webdriver.Chrome()
def getSpojProblem(problemUrl):
	
	#driver = webdriver.Chrome('C:\Users\Pranay\Downloads\Setups\Drivers\chromedriver.exe')

	#Get problem Name
	problemName = ''
	for c in problemUrl[::-1]:
		if c == '/':
			break
		problemName = problemName + c
	problemName = problemName[::-1]
	
	try:
		
		driver.get(problemUrl)
		print('reach problem page')

		problemTag = ''
		divTags = driver.find_element_by_id('problem-tags')
		aTags = divTags.find_elements_by_tag_name('a')
		for aTag in aTags:
			problemTag = problemTag + ' ' + aTag.text

		problemText = ''
		divBody = driver.find_element_by_id('problem-body')
		all_children_by_xpath = divBody.find_elements_by_xpath(".//*")
		for child in all_children_by_xpath:
			problemText = problemText + ' ' + child.text

		prob = SpojProblem(problemName, problemUrl, problemTag, problemText)
		print(problemText)

		
		return prob
	except Exception as e:
			print('element not found')
			print(e)
			with open('spoj/unscuccessful', 'a') as f:
				f.write(problemName+'\n')
			return None
	finally:
		pass
		#driver.quit()