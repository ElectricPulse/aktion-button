import gpiozero
import threading
import args
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
        time.sleep(3)
        usernameField = driver.find_element('id', 'txtLogin_I')
        usernameField.send_keys(username)
        passwordField = driver.find_element('id', 'txtPassword_I')
        passwordField.find_element('xpath', '..').click()
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
        lastEvent = events.find_elements('xpath', './/*')[2]
        lastEventHTML = lastEvent.get_attribute('innerHTML')
    except Exception as err:
        print(err, file=sys.stderr)
        return None

    if(lastEventHTML.find('Příchod') != -1):
        return True

    if(lastEventHTML.find('Odchod') != -1):
        return False

    return None

def makeAction(driver, action):
    try:
        className = 'btn-primary' if action else 'btn-secondary'
        button = driver.find_element('class', className)
        button.click()
        confirm = driver.find_element('id', 'ctl00_phContent_webterminal_popupWebTerminal_btnPotvrdit_CD')
        confirm.click()
    except Exception as err:
        print(err, file=sys.stderr)
        return True

    return False

def init(headful):
    options = webdriver.ChromeOptions()

    if(not headful):
        options.add_argument('headless')

    driver = webdriver.Chrome(options=options)
    driver.get('https://cloud.aktion.cz')

    return driver

def run(driver):
    event = getLastEvent(driver)

    if(event == None):
        print("Couldn't get last event", file=sys.stderr)
        return True

    print("The last event was", 'arrival' if event else 'departure')

    if(makeAction(driver, not event)):
        print("Couldn't make action")
        return True

    time.sleep(2)

    newEvent = getLastEvent(driver)

    if(newEvent == None):
        print("Couldn't get last event", file=sys.stderr)
        return True

    if(event == newEvent):
        print("Action wasn't executed properly", file=sys.stderr)
        return True

    return False

def checkDeviceExists(id):
    path = '/sys/bus/usb/devices/' + id + '/driver'
    return os.path.exists(path)

def monitorOutput(driver, led):
    lastState = None

    while True:
        state = getLastEvent(driver)

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

        err = run(driver)

        if(err):
            return True

    return False

def main():
    opts = args.processArgs(sys.argv[1:])

    if(opts == None):
        print('Invalid arguments', file=sys.stderr)
        return True

    driver = init(opts.headful)

    config = loadYaml('./config.yaml')

    if(config == None):
        print("Couldn't load config", file=sys.stderr)
        return True

    try:
        username = config['username']
        password = config['password']
    except KeyError as err:
        print('Missing key', err)
        print('Invalid config', file=sys.stderr)
        return True
        
    if(login(driver, username, password)):
        print("Couldn't login", file=sys.stderr)
        return True


    button = gpiozero.Button('GPIO4')
    led = gpiozero.LED('GPIO5')

    thread = threading.Thread(target=monitorOutput, args=(driver,led))
    thread.start()

    monitorInput(driver, button)

if(main()):
    exit(1)
