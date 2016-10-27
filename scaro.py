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



codechefUrl = 'https://www.codechef.com'
codechefProblemUrl = 'https://www.codechef.com/problems/'
section = 'easy'


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
				# driver = webdriver.Chrome()
				# driver.set_window_size(1120, 550)

				driver.get(codechefUrl + a['href'])
				print('reach problem page '+a['href'])
				
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

					print('count ' + str(count))
					
					prob = Problem(problemName, codechefUrl + a['href'], problemTags, problemText)
					# print(problemText)
					# print(prob)
					problemCollections.append(prob)
					count = count + 1
				except Exception as e:
					print('element not found')
					print(e)
				else:
					pass
				finally:
					pass
					#driver.quit()
				

driver.quit()				
for problem in problemCollections:
	print(problem)

