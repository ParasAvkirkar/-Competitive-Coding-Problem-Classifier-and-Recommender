from SpojProblemPage import getSpojProblem
from selenium import webdriver
from problems import Problem
from bs4 import BeautifulSoup
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


import requests
import time

from problems import Problem

current_progress = {'section':0, 'problem_no':0}
spojUrl = 'http://www.spoj.com'
spojProblemUrl = 'http://www.spoj.com/problems'
#sections = ['classical', 'challenge', 'partial', 'tutorial', 'riddle', 'basics']
sections = ['classical']

countProblems = 0
driver = webdriver.Chrome()
for section in sections:
	driver.get(spojProblemUrl + '/' + section)
	print(spojProblemUrl + '/' + section)
	# print(driver.text)
	# with open('temp.txt', 'w') as f:
	# 	f.write(driver.page_source.encode("utf-8"))
	# wait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "table-responsive")))
	#WebDriverWait(driver, 10).until(EC.presence_of_element_located(driver.find_element_by_name('td')))
	#time.sleep(10)
	tdTags = driver.find_elements_by_tag_name('td')

	for tdTag in tdTags:
		wait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
		aTags = tdTag.find_elements_by_tag_name('a')
		for aTag in aTags:
			if aTag is not None:
				if aTag.get_attribute('href') is not None and '/problems/' in aTag.get_attribute('href'):
					try:
					    # print "Page is ready!"
						prob = getSpojProblem(aTag.get_attribute('href'))
						countProblems = countProblems + 1
						if(prob is None):
							print('not successfull ' + str(countProblems))
						else:
							print('successfull ' + str(countProblems))
					except Exception as e:
					    print "exception in global scraping loop"
					    print(e)

driver.quit()