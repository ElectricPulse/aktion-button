import time
import api
from selenium.webdriver.common.by import By
from selenium import webdriver
import selenium
import sys
import userio

def init(headful, userConfig):
    options = webdriver.ChromeOptions()

    if(not headful):
        options.add_argument('headless')

    driver = webdriver.Chrome(options=options)
    driver.get('https://cloud.aktion.cz')

    api.login(driver, userConfig)

    return driver

def monitorOutput(driver, led, lock, userConfig, exitEvent):
    lastState = None

    while not exitEvent.is_set():
        lock.acquire()
        state = api.getAttendance(driver, userConfig)
        lock.release()

        if(state == None):
            print("Couldn't get current attendance", file=sys.stderr)
            break

        api.displayAttendance(led, state)
        time.sleep(1)

def monitorInput(driver, button, led, leds, lock, userConfig, exitEvent):
    while not exitEvent.is_set():
        button.wait_for_press()

        progressThread = userio.startShowingProgress(leds, exitEvent)
        lock.acquire()
        err = api.flipAttendance(driver, led, userConfig)
        lock.release()
        userio.stopShowingProgress(progressThread)

        if(err):
            return True

    return False
