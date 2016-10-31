from selenium import webdriver
from user import User
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import requests


def fetch_user_list(start, driver):
	
	baseUrl = "http://www.spoj.com/ranks/users/start="
	userLink = baseUrl + str(start)

	driver.get(userLink)
	print('reach user list page '+ userLink)

	f = open('users_urls.txt', 'a')
	
	try:
		table = driver.find_element_by_class_name('table-condensed')
		for tr in table.find_elements_by_tag_name('tr'):
			# tds = tr.find_elements_by_tag_name('td')
			count = 1
			for td in tr.find_elements_by_tag_name('td'):
				if count == 3:
					a = td.find_element_by_tag_name('a')
					f.write(a.get_attribute('href') + '\n')
					# print (a.get_attribute('href'))
				count += 1	
	
	except Exception as e:
		print('element not found')
		print(e)
		prob = None
	else:
		pass
	finally:
		pass
	
	
	if start < 54000:
		fetch_user_list(start+100, driver)
		
	

driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
# fetch_user('anudeep2011', driver)
# fetch_user('sherlock_holms', driver)
fetch_user_list(0, driver)
# fetch_user('paragpachpute', driver)
# fetch_user('pranay0007', driver)
driver.close()