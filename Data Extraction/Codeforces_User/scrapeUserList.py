from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from codeforcesuser import CodeForcesUser
import requests
import json
import pickle
import os, sys

sys.path.append("../Utilities")
from driverUtil import getDriver


if __name__ == '__main__':
	driver = getDriver()
	#nextPageUrl = 'http://codeforces.com/ratings/all/true'
	nextPageUrl = ''
	mainUrl = 'http://codeforces.com/ratings/page/'
	count = 0
	for i in range(31, 148):
		nextPageUrl = mainUrl + str(i)
		with open('texts/track.txt', 'w') as t:
			t.write(nextPageUrl + '\n')
			with open('texts/supuserList.txt', 'a') as f:
				driver.get(nextPageUrl)
				print(nextPageUrl)
				#dataTable = driver.find_element_by_class_name('datatable ratingsDatatable')
				dataTable = driver.find_element_by_xpath("//div[contains(@class, 'datatable ratingsDatatable')]")
				allATags = dataTable.find_elements_by_tag_name('a')
				for aTag in allATags:
					if '/profile/' in aTag.get_attribute('href'):
						#user = None
						f.write(aTag.text + '\n')
						count = count + 1
						print('count = ' + str(count) + ' ' + str(aTag.text))

