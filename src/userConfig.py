import utils

def validateUserConfig(userConfig):
    #Test if config contains correct keys
    return False

def loadUserConfig():
    path = './config.yaml'

    userConfig = utils.loadYaml(path)

    if(userConfig == None):
        print('No user config at path', path, 'exists.', file=sys.stderr)
        return None

    if(validateUserConfig(userConfig)):
        print("Incorrectly formatted user config", file=sys.stderr)
        return None

    return userConfig

