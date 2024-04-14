import time
import attendance
from selenium.webdriver.common.by import By
from selenium import webdriver
import selenium
import sys
import userio

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
        passwordField = driver.find_element(By.ID, 'txtPassword_I')
        passwordField.send_keys(password)
        driver.find_element(By.ID, 'btnLogin').click()
        attendance.ensureLoaded(driver)
    except Exception as err:
        print(err, file=sys.stderr)
        return True

    return False

def monitorOutput(driver, led, lock):
    lastState = None

    while True:
        lock.acquire()
        state = attendance.getAttendance(driver)
        lock.release()

        if(state == None):
            print("Couldn't get current attendance", file=sys.stderr)
            break

        attendance.displayAttendance(led, state)
        time.sleep(30)

def monitorInput(driver, button, led, leds, lock):
    while True:
        button.wait_for_press()

        progressThread = userio.startShowingProgress(leds)
        lock.acquire()
        err = attendance.flipAttendance(driver, led)
        lock.release()
        userio.stopShowingProgress(progressThread)

        if(err):
            return True

    return False
