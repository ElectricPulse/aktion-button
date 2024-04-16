import sys
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

def login(driver, userConfig):
    ensureLoginLoaded(driver)

    usernameField = driver.find_element(By.ID, 'txtLogin_I')
    usernameField.send_keys(userConfig['username'])

    passwordField = driver.find_element(By.ID, 'txtPassword_I')
    passwordField.find_element(By.XPATH, '..').click()
    passwordField = driver.find_element(By.ID, 'txtPassword_I')
    passwordField.send_keys(userConfig['password'])
    driver.find_element(By.ID, 'btnLogin').click()

    ensureDashboardLoaded(driver)

def ensureLoginLoaded(driver):
    field1 = 'txtLogin_I'
    field2 = 'txtPassword_I'
    btn = 'btnLogin'

    wait = WebDriverWait(driver, config.waitTimeout)
    wait.until(EC.element_to_be_clickable((By.ID, field1)))
    wait.until(EC.presence_of_element_located((By.ID, field2)))
    wait.until(EC.element_to_be_clickable((By.ID, btn)))

def ensureDashboardLoaded(driver):
    btn1 = 'btn-primary'
    btn2 = 'btn-secondary'
    eventsList = "webtlasteventsbody"

    wait = WebDriverWait(driver, config.waitTimeout)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, btn1)))
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, btn2)))
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="webtlasteventsbody"]/*[2]')))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'terminal-timerCounter')))

def reload(driver, userConfig):
    print('In offline state, reloading', file=sys.stderr)
    driver.refresh()
    login(driver, userConfig)

def checkOffline(driver):
    statusElement = driver.find_element(By.CLASS_NAME, 'terminal-timerCounter')
    html = statusElement.get_attribute('innerHTML')
    offline = html.find('offline') != -1
    return offline

def getAttendance(driver, userConfig):
    if checkOffline(driver):
        reload(driver, userConfig)

    event = driver.find_element(By.XPATH, '//*[@id="webtlasteventsbody"]/*[2]')

    if(not event):
        return None

    html = event.get_attribute('innerHTML')

    if(html.find('Příchod') != -1):
        return True

    return False

def setAttendance(driver, state, userConfig):
    if checkOffline(driver):
        reload(driver, userConfig)

    className = 'btn-primary' if state else 'btn-secondary'
    button = driver.find_element(By.CLASS_NAME, className)
    button.click()
    confirm = driver.find_element(By.ID, 'ctl00_phContent_webterminal_popupWebTerminal_btnPotvrdit_CD')
    confirm.click()
    ensureDashboardLoaded(driver)

    return False

def flipAttendance(driver, led, userConfig):
    state = getAttendance(driver, userConfig)

    if(state == None):
        print("Couldn't get attendance state", file=sys.stderr)
        return True

    print("The last attendance state was", 'arrival' if state else 'departure')

    if(setAttendance(driver, not state, userConfig)):
        print("Couldn't set attendance")
        return True

    newState = getAttendance(driver, userConfig)

    if(newState == None):
        print("Couldn't get verifying attendance state", file=sys.stderr)
        return True

    if(state == newState):
        print("Action wasn't executed properly", file=sys.stderr)
        return True

    displayAttendance(led, newState)

    return False

