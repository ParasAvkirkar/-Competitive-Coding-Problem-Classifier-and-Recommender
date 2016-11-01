from selenium import webdriver
from spojProblem import SpojProblem
from bs4 import BeautifulSoup
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


import requests


#driver = webdriver.Chrome('C:\Users\Pranay\Downloads\Setups\Drivers\chromedriver.exe')
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

		#Getting tags of the problem
		problemTag = ''
		divTags = driver.find_element_by_id('problem-tags')
		aTags = divTags.find_elements_by_tag_name('a')
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
		time = ''
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
				time = dataCells[1].text
			elif('source' in label):
				source = dataCells[1].text
			elif('memory' in label):
				memory = dataCells[1].text
			elif('cluster' in label):
				cluster = dataCells[1].text
			elif('languages' in label):
				languages = dataCells[1].text					

		print(addedBy)
		print(date)
		print(time)
		print(source)
		print(memory)
		print(cluster)
		print(languages)

		prob = SpojProblem(problemName, problemUrl, problemTag, problemText, addedBy, date, time, source, memory, cluster, languages)
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