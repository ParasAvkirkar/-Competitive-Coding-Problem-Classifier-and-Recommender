from selenium import webdriver
from problems import Problem
from bs4 import BeautifulSoup
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import re
import requests
import sys, os
import time

driver = webdriver.Chrome()

#driver = webdriver.Chrome('C:\Users\Pranay\Downloads\Setups\Drivers\chromedriver.exe')
def getCodechefProblem(problemUrl):
	count = 0
	# driver = webdriver.Chrome('C:\Users\Pranay\Downloads\Setups\Drivers\chromedriver.exe')
	# submissionPageQuery = "?sort_by=All&sorting_order=asc&language=All&status=15&handle=&Submit=GO"
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
		divProblem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "problem-page-complete")))

		divProblem = driver.find_element_by_id('problem-page-complete')					
		
		print('problem content got')
		all_children_by_xpath = divProblem.find_elements_by_xpath(".//*")
						
		for child in all_children_by_xpath:
			problemText = problemText + ' ' + child.text
		
		allHrefTags = driver.find_elements_by_tag_name('a')
		problemTags = ''
		for hrefTag in allHrefTags:
			if 'tag' in hrefTag.get_attribute('href'):
				problemTags = problemTags + ' ' + hrefTag.text
		
		medianSubmissionSize = 0.0
		submissionSizes = []
		totalSub = 0

		successDiv = driver.find_element_by_id('success-submissions')
		plusButton = successDiv.find_element_by_tag_name('button')
		plusButton.click()
		
		flag = True
		while flag:
			tableTag = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "dataTable")))
			tableTag = driver.find_element_by_class_name('dataTable')
			bodyTag = tableTag.find_element_by_tag_name('tbody')
			allRowTags = bodyTag.find_elements_by_tag_name('tr')
			for rowTag in allRowTags:
				if len(submissionSizes) >= 100:
					flag = False
					break
		
				allDataTags = rowTag.find_elements_by_tag_name('td')
				if len(allDataTags) > 3:
					if "c++" in allDataTags[3].text.lower():
			 			totalSub = totalSub + 1
			 			submissionSizes.append(float(re.sub("[^0-9, .]", "", allDataTags[2].text)))
			 			totalSub = totalSub + 1
			 			
			successDiv = driver.find_element_by_id('success-submissions')
			aTags = successDiv.find_elements_by_tag_name('a')
			if aTags is None:
				break				
			
			flag = False
			#print 'searching onclick for next'	
			for aTag in aTags:
				try:
					onclickAttr = aTag.get_attribute('onclick')
					if onclickAttr is not None and 'next' in onclickAttr:
						flag = True
						#print 'clicking next button'
						aTag.click()
						time.sleep(2)
						break
				except Exception as e:
					print e
					exc_type, exc_obj, exc_tb = sys.exc_info()
					print exc_tb.tb_lineno
					onclickAttr = None

		
		submissionSizes.sort()
		medianSubmissionSize = submissionSizes[(len(submissionSizes) - 1)/2]
		print str(medianSubmissionSize) + " median submission size"
		
		prob = Problem(problemName, problemUrl, problemTags, problemText, medianSubmissionSize)
		count = count + 1
		return prob
	except Exception as e:
			print('Exception raised')
			print(e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			print exc_tb.tb_lineno
			with open('codechef/unscuccessful', 'a') as f:
				f.write(problemName+'\n')
			return None
