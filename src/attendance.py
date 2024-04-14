import sys
import time
import logic
import config
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def displayAttendance(led, state):
    if(state):
        led.on()
    else:
        led.off()

def ensureLoaded(driver):
    btn1 = 'btn-primary'
    btn2 = 'btn-secondary'
    eventsList = "webtlasteventsbody"

    wait = WebDriverWait(driver, config.waitTimeout)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, btn1)))
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, btn2)))
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="webtlasteventsbody"]/*[2]')))

def reload(driver):
    driver.refresh()
    ensureLoaded(driver)

def getAttendance(driver):
    reload(driver)
    event = driver.find_element(By.XPATH, '//*[@id="webtlasteventsbody"]/*[2]')

    if(not event):
        return None

    html = event.get_attribute('innerHTML')

    if(html.find('Příchod') != -1):
        return True

    return False

def setAttendance(driver, state):
    reload(driver)
    className = 'btn-primary' if state else 'btn-secondary'
    button = driver.find_element(By.CLASS_NAME, className)
    button.click()
    confirm = driver.find_element(By.ID, 'ctl00_phContent_webterminal_popupWebTerminal_btnPotvrdit_CD')
    confirm.click()
    ensureLoaded(driver)

    return False

def flipAttendance(driver, led):
    state = getAttendance(driver)

    if(state == None):
        print("Couldn't get attendance state", file=sys.stderr)
        return True

    print("The last attendance state was", 'arrival' if state else 'departure')

    if(setAttendance(driver, not state)):
        print("Couldn't set attendance")
        return True

    newState = getAttendance(driver)

    if(newState == None):
        print("Couldn't get verifying attendance state", file=sys.stderr)
        return True

    if(state == newState):
        print("Action wasn't executed properly", file=sys.stderr)
        return True

    displayAttendance(led, newState)

    return False

