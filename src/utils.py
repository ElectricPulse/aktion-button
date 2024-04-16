import yaml
import sys

def loadYaml(path):
    try:
        file = open(path, 'r')
        data = yaml.load(file, Loader=yaml.FullLoader)
    except Exception as err:
        print(err, file=sys.stderr)
        data = None

    file.close()

    return data

def runThread(func, args, exitEvent):
    try:
        func(*args, exitEvent)
    except Exception as err:
        print("Error in thread: ", err, file=sys.stderr)
    finally:
        exitEvent.set()


