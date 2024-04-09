import time
import sys
import attendance
from selenium.webdriver.common.by import By
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

def init(headful):
    options = webdriver.ChromeOptions()

    if(not headful):
        options.add_argument('headless')

    driver = webdriver.Chrome(options=options)
    driver.get('https://cloud.aktion.cz')
    time.sleep(1)

    return driver

def login(driver, username, password):
    try:
        usernameField = driver.find_element(By.ID, 'txtLogin_I')
        usernameField.send_keys(username)
        passwordField = driver.find_element(By.ID, 'txtPassword_I')
        passwordField.find_element(By.XPATH, '..').click()
        passwordField.send_keys(password)
        driver.find_element(By.ID, 'btnLogin').click()
        time.sleep(1)
    except Exception as err:
        print(err, file=sys.stderr)
        return True

    return False

def monitorOutput(driver, led):
    lastState = None

    while True:
        state = attendance.getAttendance(driver)

        if(state == None):
                print("Couldn't get last event")
                return True

        if(lastState != state):
            if(state):
                led.on()
            else:
                led.off()

            lastState = state

        time.sleep(1)

def monitorInput(driver, button):
    while True:
        button.wait_for_press()

        err = attendance.flipAttendance(driver)

        if(err):
            return True

    return False
