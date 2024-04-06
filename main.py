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
        time.sleep(5)
        driver.find_element('id', 'txtLogin_I').send_keys(username)
        passwordField = driver.find_element('id', 'txtPassword_I_CLND')
        passwordField.click()
        passwordField.send_keys(password)
        time.sleep(10)
        #driver.find_element('id', 'btnLogin').click()
    except Exception as err:
        print(err, file=sys.stderr)
        return True

    return False

def run(headful):
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

    print(username)
    print(password)

    options = webdriver.ChromeOptions()

    if(not headful):
        options.add_argument('headless')

    driver = webdriver.Chrome(options=options)
    driver.get('https://cloud.aktion.cz')
    
    if(login(driver, username, password)):
        print("Couldn't login", file=sys.stderr)

class Opts:
    def __init__(self):
        self.headful = False
        self.keepalive = False

def processArgs(args):
    opts = Opts()

    for i in range(1, len(args)):
        match(sys.argv[i]):
                case 'headful':
                    opts.headful = True
                case 'keepalive':
                    opts.keepalive = True
                case _:
                    print('Invalid argument: ', sys.argv[i], file=sys.stderr)
                    return None
    return opts


def main():
    argc = len(sys.argv)
    
    if(argc < 4):
        opts = processArgs(sys.argv[1:])            
    else:
        print('Invalid number of arguments', file=sys.stderr)
        return True

    err = run(opts.headful)

    if(err):
        if(opts.keepalive):
            time.sleep(60)
        return True

    return False

if(main()):
    exit(1)
