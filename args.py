class Opts:
    def __init__(self):
        self.headful = False
        self.keepalive = False
        self.ask = True

def processArgs(args):
    opts = Opts()

    if(len(args) > 3):
        print('Invalid number of arguments', file=sys.stderr)
        return None

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

