__author__ = 'Pranay'
from bs4 import BeautifulSoup
import requests
import pickle
import os
import logging
import sys
import datetime
# import winsound
from itertools import izip
import csv

logging.basicConfig(filename='exceptScenarios.log', level=logging.ERROR)

current_progress = {'section':0, 'problem_no':0}
codechefUrl = 'https://www.codechef.com'
codechefProblemUrl = 'https://www.codechef.com/problems/'
sections = ['easy', 'medium', 'hard', 'school']

try:
	with open('current_progress_prob_code.pickle', 'r+b') as f:
		current_progress = pickle.load(f)
		print 'Resuming Progress from problem '+sections[current_progress['section']]+' and problem no '+str(current_progress['problem_no'])
except Exception as e:
	print(e)
	exc_type, exc_obj, exc_tb = sys.exc_info()
	print 'Exception at line '+ str(exc_tb.tb_lineno)
	logging.error('Time: {0} File: {1} Line: {2} Caused By: {3}'.format(datetime.datetime.now(), os.path.basename(__file__),
				exc_tb.tb_lineno, e))

print 'Starting problem collection'

prob_href = ''
try:
	sec_count = current_progress['section']
	codes = []
	diffs = []
	for section in sections[sec_count:]:
		response = requests.get(codechefProblemUrl + section)
		soup = BeautifulSoup(response.content, 'html.parser')
		count = current_progress['problem_no']
		problemCollections = []
		problemRows = soup.find_all("tr", { "class" : "problemrow" })
		for row in problemRows[count:]:
			codeAnchor = row.find('a',{'title':'Submit a solution to this problem.'})
			print sections[sec_count]+': '+codeAnchor.text
			codes.append(codeAnchor.text)
			diffs.append(sections[sec_count])
		sec_count = sec_count+1
		count = 0
		with open('current_progress_prob_code.pickle', 'w+b') as f:
			pickle.dump({'section':sec_count, 'problem_no':0}, f)

	with open('prob_diff.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerows(izip(codes, diffs))

except Exception as e:
	print(e)
	exc_type, exc_obj, exc_tb = sys.exc_info()
	print 'Exception at line '+ str(exc_tb.tb_lineno)
	logging.error('Time: {0} File: {1} Line: {2} Caused By: {3} Problem href: {4}'.format(datetime.datetime.now(), os.path.basename(__file__),
					exc_tb.tb_lineno, e, prob_href))
	# winsound.PlaySound("SystemExit", winsound.SND_ALIAS)