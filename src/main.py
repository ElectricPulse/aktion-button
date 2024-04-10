import gpiozero
import threading
import sys
import args
import logic

def main():
    opts = args.processArgs(sys.argv[1:])

    if(opts == None):
        print('Invalid arguments', file=sys.stderr)
        return True

    config = logic.loadYaml('./config.yaml')

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

    driver = logic.init(opts.headful)
        
    if(logic.login(driver, username, password)):
        print("Couldn't login", file=sys.stderr)
        return True

    button = gpiozero.Button('GPIO4')
    led = gpiozero.LED('GPIO5')

    thread = threading.Thread(target=logic.monitorOutput, args=(driver,led))
    thread.start()

    logic.monitorInput(driver, button)

if(main()):
    exit(1)
