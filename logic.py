import gpiozero
import os
import yaml
import time
import sys
from selenium import webdriver
import selenium

def loadYaml(path):
    try:
        file = open(path, 'r')
        data = yaml.load(file, Loader=yaml.FullLoader)
    except Exception as err:
        print(err, file=sys.stderr)
        data = None

    file.close()

    return data

def login(driver, username, password):
    try:
        time.sleep(1)
        usernameField = driver.find_element('id', 'txtLogin_I')
        usernameField.send_keys(username)
        passwordField = driver.find_element('id', 'txtPassword_I')
        passwordField.find_element_by_xpath('..').click()
        passwordField.send_keys(password)
        driver.find_element('id', 'btnLogin').click()
        time.sleep(2)
    except Exception as err:
        print(err, file=sys.stderr)
        return True

    return False

def getLastEvent(driver):
    try:
        events = driver.find_element('id', 'webtlasteventsbody')
        lastEvent = events.find_elements_by_xpath('.//*')[2]
        lastEventHTML = lastEvent.get_attribute('innerHTML')
    except Exception as err:
        print(err, file=sys.stderr)
        return None

    if(lastEventHTML.find('Příchod') != -1):
        return True

