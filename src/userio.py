import threading
import time

def loopLeds(leds):
    t = threading.currentThread()
    i = 0

    while getattr(t, 'do_run', True):
        leds[i].on()
        time.sleep(0.3)
        leds[i].off()
        i += 1
        if(i == len(leds)):
            i = 0

def startShowingProgress(leds):
    thread = threading.Thread(target=loopLeds, args=(leds,))
    thread.start()
    return thread

def stopShowingProgress(thread):
    thread.do_run = False

