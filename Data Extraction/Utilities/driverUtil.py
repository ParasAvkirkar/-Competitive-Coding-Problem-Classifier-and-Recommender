__author__ = 'Pranay'

import os
import sys
import logging
import datetime

from selenium import webdriver

def getDriver():
    driver = None
    logging.basicConfig(filename='exceptScenarios.log', level=logging.ERROR)
    paths = ['', 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', 'C:\Users\Pranay\Downloads\Setups\Drivers\chromedriver.exe']
    i = 0
    while driver is None:
        try:
            print str(i)
            if paths[i] is '':
                driver = webdriver.Chrome()
            else:
                driver = webdriver.Chrome(paths[i])
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print 'Exception at line '+ str(exc_tb.tb_lineno)
            logging.error('Time: {0} File: {1} Line: {2} Caused By: {3}'.format(datetime.datetime.now(), os.path.basename(__file__),
                        exc_tb.tb_lineno, e))
            # logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
            #         ' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(e))
        i = i + 1
        if i >= len(paths):
            if driver is None:
                print 'driver not yet found'
            break
    return driver