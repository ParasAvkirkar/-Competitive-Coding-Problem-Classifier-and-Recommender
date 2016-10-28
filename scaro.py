from selenium import webdriver
from problems import Problem
from bs4 import BeautifulSoup
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


from CodechefProblemPage import getCodechefProblem

import requests
import dryscrape



codechefUrl = 'https://www.codechef.com'
codechefProblemUrl = 'https://www.codechef.com/problems'
section = '/easy'


response = requests.get(codechefProblemUrl + section)
soup = BeautifulSoup(response.content, 'html.parser')

problemCollections = []
count = 0

problemRows = soup.find_all('tr')
driver = webdriver.Chrome()

for row in problemRows:
	problemName = ''
	# if(count > 2):
	# 	break
	if row.has_attr('class') and 'problemrow' in row['class']:
		allHrefTags = row.find_all('a')
		for a in allHrefTags:
			if a.has_attr('href') and 'problem' in a['href']:
				problemName = a.b.string
				
				# driver = webdriver.PhantomJS()
				# driver = webdriver.Firefox()
				# firefox_capabilities = DesiredCapabilities.FIREFOX
				# firefox_capabilities['marionette'] = True

				# driver = webdriver.Firefox(capabilities=firefox_capabilities)
				# drsiver = webdriver.Chrome()
				# driver.set_window_size(1120, 550)

				print('inside loop ' + codechefUrl + a['href'])
				prob = getCodechefProblem(codechefUrl + a['href'], driver)
				if prob == None:
					print('issue')
				else:
					print('not issue ' + str(count))
				count = count + 1
				problemCollections.append(prob)

				
driver.quit()				
for problem in problemCollections:
	print(problem)

