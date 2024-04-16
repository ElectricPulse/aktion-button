import time
import threading
import os
import sys
import args
import logic
import config
import utils
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
        
    print('Initializing')
    driver = logic.init(opts.headful, userConfig)
        
    exitEvent = threading.Event()
    lock = threading.Lock()

    print('Starting output handler')
    th1 = threading.Thread(
            target=utils.runThread,
            args=(logic.monitorOutput, (driver, config.io['led'], lock, userConfig), exitEvent)
        )
    th1.start()

    print('Starting input listener')
    th2 = threading.Thread(target=utils.runThread,
            args=(logic.monitorInput, (driver, config.io['button'], config.io['led'], config.io['leds'], lock, userConfig),
            exitEvent)
        )
    th2.start()

    while not exitEvent.is_set():
        time.sleep(1)

    print("Atleast one thread exited")
    print("Currently running", threading.active_count(), "threads")
    return 1

os._exit(main())
