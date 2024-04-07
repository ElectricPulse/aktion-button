import pynput
import yaml
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

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

    if(lastEventHTML.find('Odchod') != -1):
        return False

    return None

def makeAction(driver, action):
    try:
        className = 'btn-primary' if action else 'btn-secondary'
        button = driver.find_element_by_class_name(className)
        button.click()
        confirm = driver.find_element('id', 'ctl00_phContent_webterminal_popupWebTerminal_btnPotvrdit_CD')
        confirm.click()
    except Exception as err:
        print(err, file=sys.stderr)
        return True

    return False

def run(headful, ask):
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

    options = webdriver.ChromeOptions()

    if(not headful):
        options.add_argument('headless')

    driver = webdriver.Chrome(options=options)
    driver.get('https://cloud.aktion.cz')
    
    if(login(driver, username, password)):
        print("Couldn't login", file=sys.stderr)
        return True

    event = getLastEvent(driver)

    if(event == None):
        print("Couldn't get last event", file=sys.stderr)
        return True

    print("The last event was", 'arrival' if event else 'departure')

    if(ask):
        res = input('Do you want to proceed to do the opposite action? (./y) ')

        if(res != 'y'):
            return False

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

class Opts:
    def __init__(self):
        self.headful = False
        self.keepalive = False
        self.ask = True

def processArgs(args):
    opts = Opts()

    for i in range(0, len(args)):
        match(args[i]):
                case 'headful':
                    opts.headful = True
                case 'keepalive':
                    opts.keepalive = True
                case '-y':
                    opts.ask = False
                case _:
                    print('Invalid argument: ', args[i], file=sys.stderr)
                    return None
    return opts


def app():
    argc = len(sys.argv)
    
    if(argc > 3):
        print('Invalid number of arguments', file=sys.stderr)
        return True

    opts = processArgs(sys.argv[1:])

    if(opts == None):
        print('Invalid arguments', file=sys.stderr)
        return True

    err = run(opts.headful, opts.ask)

    if(opts.keepalive):
        input('Press key to exit ')
    
    return err

def main():
    while True:
        c = keyboard.read_key()
        print(c)

if(main()):
    exit(1)
