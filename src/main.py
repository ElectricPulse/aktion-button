import time
import threading
import sys
import args
import logic
import config
from userConfig import loadUserConfig

def main():
    opts = args.processArgs(sys.argv[1:])

    if(opts == None):
        print('Invalid arguments', file=sys.stderr)
        return True

    userConfig = loadUserConfig()

    if(userConfig == None):
        print("Couldn't load config", file=sys.stderr)
        return True
        
    print('Launching browser')
    driver = logic.init(opts.headful)
        
    print('Logging in')
    if(logic.login(driver, userConfig['username'], userConfig['password'])):
        print("Couldn't login", file=sys.stderr)
        return True

    lock = threading.Lock()

    print('Starting output handler')
    thread = threading.Thread(target=logic.monitorOutput, args=(driver, config.io['led'], lock))
    thread.start()

    print('Starting input listener')
    logic.monitorInput(driver, config.io['button'], config.io['led'], config.io['leds'], lock)

if(main()):
    exit(1)
