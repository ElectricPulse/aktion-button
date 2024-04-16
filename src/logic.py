import time
import api
from selenium.webdriver.common.by import By
from selenium import webdriver
import selenium
import sys
import userio

def init(headful, username, password):
    options = webdriver.ChromeOptions()

    if(not headful):
        options.add_argument('headless')

    driver = webdriver.Chrome(options=options)
    driver.get('https://cloud.aktion.cz')

    api.login(driver, username, password)

    return driver

def monitorOutput(driver, led, lock, exitEvent):
    lastState = None

    while not exitEvent.is_set():
        lock.acquire()
        state = api.getAttendance(driver)
        lock.release()

        if(state == None):
            print("Couldn't get current attendance", file=sys.stderr)
            break

        api.displayAttendance(led, state)
        time.sleep(1)

def monitorInput(driver, button, led, leds, lock, exitEvent):
    while not exitEvent.is_set():
        button.wait_for_press()

        progressThread = userio.startShowingProgress(leds, exitEvent)
        lock.acquire()
        err = api.flipAttendance(driver, led)
        lock.release()
        userio.stopShowingProgress(progressThread)

        if(err):
            return True

    return False
