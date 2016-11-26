from SpojProblemPage import getSpojProblem
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


import requests
import time
import pickle

current_progress = {'section':0, 'problem_no':0}
spojUrl = 'http://www.spoj.com'
spojProblemUrl = 'http://www.spoj.com/problems'
sections = ['classical', 'challenge', 'partial', 'tutorial', 'riddle', 'basics']
# sections = ['classical']

try:
	with open('current_progress.pickle', 'r+b') as f:
		current_progress = pickle.load(f)
		print 'Resuming Progress from problem '+sections[current_progress['section']]+' and problem no '+str(current_progress['problem_no'])
except Exception as e:
	print e
	print 'Starting problem collection'

sec_count = current_progress['section']


#driver = webdriver.Chrome('C:\Users\Pranay\Downloads\Setups\Drivers\chromedriver.exe')
driver = webdriver.Chrome()
nextPageUrl = ''
for section in sections[sec_count:]:
	nextPageUrl = spojProblemUrl + '/' + section
	#driver.get(spojProblemUrl + '/' + section)
	# with open('temp.txt', 'w') as f:
	# 	f.write(driver.page_source.encode("utf-8"))
	# wait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "table-responsive")))
	#WebDriverWait(driver, 10).until(EC.presence_of_element_located(driver.find_element_by_name('td')))
	#time.sleep(10)
	print(nextPageUrl)
	while nextPageUrl is not "":
		driver.get(nextPageUrl)
		pagerTags = driver.find_elements_by_class_name('pager_link')
		for tag in pagerTags:
			if 'next' in tag.text.lower():
				nextPageUrl = tag.get_attribute('href')
				break

		print(nextPageUrl)
		tdTags = driver.find_elements_by_tag_name('td')
		count = current_progress['problem_no']
		for tdTag in tdTags[count:]:
			wait = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
			aTags = tdTag.find_elements_by_tag_name('a')
			for aTag in aTags:
				if aTag is not None:
					if aTag.get_attribute('href') is not None and '/problems/' in aTag.get_attribute('href'):
						try:
							# print "Page is ready!"
							prob = getSpojProblem(aTag.get_attribute('href'))
							count = count + 1
							if(prob is None):
								print('not successfull ' + str(count))
							else:
								print('successfull ' + str(count))
								with open('spoj/'+prob.name, 'w+b') as f:
									pickle.dump(prob, f)
									# f.write(p.__str__())
									# f.write(str(p.id)+'\t'+p.name+'\t'+p.url+'\t'+p.tags+'\t')#+p.description.encode('utf-8'))
									# f.write(p.description.encode('utf-8'))
								count+=1
								with open('current_progress.pickle', 'w+b') as f:
									pickle.dump({'section':sec_count, 'problem_no':count}, f)
						except Exception as e:
							print "exception in global scraping loop"
							print(e)
		sec_count += 1
		count = 0
		with open('current_progress.pickle', 'w+b') as f:
			pickle.dump({'section':sec_count, 'problem_no':0}, f)

driver.quit()