from selenium import webdriver
from spojProblem import SpojProblem
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


import requests
import sys, os
import time
import re
import logging
import datetime


#driver = webdriver.Chrome('C:\Users\Pranay\Downloads\Setups\Drivers\chromedriver.exe')
# driver = webdriver.Chrome()
sys.path.append("../Utilities")
from driverUtil import getDriver
driver = getDriver()

logging.basicConfig(filename='exceptScenarios.log', level=logging.ERROR)

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
		print problemUrl
		print('reach problem page')

		#Getting tags of the problem
		problemTag = ''
		divTag = driver.find_element_by_id('problem-tags')
		aTags = divTag.find_elements_by_tag_name('a')
		for aTag in aTags:
			problemTag = problemTag + ' ' + aTag.text


		#Getting text of the problem
		problemText = ''
		divBody = driver.find_element_by_id('problem-body')
		all_children_by_xpath = divBody.find_elements_by_xpath(".//*")
		for child in all_children_by_xpath:
			problemText = problemText + ' ' + child.text

		#print(problemText)

		
		#Getting other infos of the problem
		addedBy = ''
		date = ''
		timelimit = ''
		source = ''
		memory = ''
		cluster = ''
		languages = ''
		tableInfo = driver.find_element_by_class_name('probleminfo')
		allRows = tableInfo.find_elements_by_tag_name('tr')
		for row in allRows:
			dataCells = row.find_elements_by_xpath(".//*")
			label = dataCells[0].text.lower()
			if('added' in label):
				addedBy = dataCells[1].text
			elif('date' in label):
				date = dataCells[1].text
			elif('time' in label):
				timelimit = dataCells[1].text
			elif('source' in label):
				source = dataCells[1].text
			elif('memory' in label):
				memory = dataCells[1].text
			elif('cluster' in label):
				cluster = dataCells[1].text
			elif('languages' in label):
				languages = dataCells[1].text					

		medianSubmissionSize = 0.0
		submissionSizes = []

		divContent = driver.find_element_by_id('content')
		statusUrl = ''
		aTags = divContent.find_elements_by_tag_name('a')
		for aTag in aTags:
			if 'status' in aTag.get_attribute('href'):
				statusUrl = aTag.get_attribute('href')
				break

		flag = True
		while flag:
			if statusUrl is not "":
				try:
					driver.get(statusUrl)
					# time.sleep(5)
					print 'got problem status page'
					titleTag = driver.find_element_by_tag_name('title')
					if 'error' in titleTag.text.lower():
						print 'got error page'
						return None
					else:
						
						#tableTag = driver.find_element_by_class_name('problems table newstatus')
						time.sleep(4)
						tableTag = driver.find_element_by_tag_name('table')
						bodyTag = tableTag.find_element_by_tag_name('tbody')
						allRowTags = bodyTag.find_elements_by_tag_name('tr')
						for rowTag in allRowTags:
							allDataTags = rowTag.find_elements_by_tag_name('td')
							if 'c++' in allDataTags[6].text.lower() and 'accepted' in allDataTags[3].text:
								#print re.sub("[^0-9, .]", "", allDataTags[5].text)
								submissionSizes.append(float(re.sub("[^0-9, .]", "", allDataTags[5].text)))

						paginationTag = driver.find_element_by_class_name('pagination')
						aTags = paginationTag.find_elements_by_tag_name('a')
						flag = False
						for aTag in aTags:
							if 'next' in aTag.text.lower():
								statusUrl = aTag.get_attribute('href')
								#driver.get(aTag.get_attribute('href'))

				except Exception as e:
					print 'exception raised while pulling status page'
					print(e)
					exc_type, exc_obj, exc_tb = sys.exc_info()
					print 'Exception at line '+ str(exc_tb.tb_lineno)
					logging.error('Time: {0} File: {1} Line: {2} Caused By: {3}'.format(datetime.datetime.now(), os.path.basename(__file__),
						exc_tb.tb_lineno, e))
					# logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
					# 		' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(e))
							
		if len(submissionSizes) == 0:
			print 'no c++ based submission sizes'
			return None
		submissionSizes.sort()
		medianSubmissionSize = submissionSizes[(len(submissionSizes) - 1)/2]
		# print(addedBy)
		# print(date)
		# print(timelimit)
		# print(source)
		# print(memory)
		# print(cluster)
		# print(languages)

		prob = SpojProblem(problemName, problemUrl, problemTag, problemText, addedBy, date, timelimit, source, memory, cluster, languages, medianSubmissionSize)
		print prob
		return prob
	except Exception as e:
		print('element not found')
		print(e)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print 'Exception at line '+ str(exc_tb.tb_lineno)
		logging.error('Time: {0} File: {1} Line: {2} Caused By: {3}'.format(datetime.datetime.now(), os.path.basename(__file__),
				exc_tb.tb_lineno, e))
		# logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
		# 		' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(e))
		with open('spoj/unsuccessful', 'a') as f:
			f.write(problemName+'\n')
		return None
	finally:
		pass
		#driver.quit()