from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from CodeforcesProblemPage import getCodeforcesProblem

import html

count=0
driver = webdriver.Chrome()
codeforcesProblemsLink="http://codeforces.com/problemset/page/31"
while True:
	driver.get(codeforcesProblemsLink)

	print("Page successfully loaded")

	problemsTable = driver.find_element_by_class_name("datatable")
	problemList = problemsTable.find_elements_by_tag_name("tr")
	for problem in problemList:
		try:
			problemLink = problem.find_element_by_class_name("id")
			problemLink = problemLink.find_element_by_tag_name("a")
			problemId = problemLink.text
			problemLink = problemLink.get_attribute("href")
			
			print("Problem link extracted")

			getCodeforcesProblem(problemLink,problemId)
			count = count + 1

			print("Suceesfully extracted problem " + problemId + "  Count - " + str(count))

		except Exception as e:
				print("Table Header")
				#print(e)
	nextPageLink = driver.find_elements_by_class_name("arrow")
	for link in nextPageLink:
		if link.text == html.unescape('&rarr;'):
			nextLink = link.get_attribute("href")
	if nextLink == codeforcesProblemsLink:
		break
	else:
		codeforcesProblemsLink = nextLink

	print("Loading next page")

print("Extraction completed successfully " + str(count))
driver.close()
