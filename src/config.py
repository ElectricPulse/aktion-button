import gpiozero

#Internal
led1 = gpiozero.LED('GPIO6')
led2 = gpiozero.LED('GPIO13')
led3 = gpiozero.LED('GPIO19')

waitTimeout = 10000

io = {
    'button': gpiozero.Button('GPIO4'),
    'led': gpiozero.LED('GPIO5'),
    'leds': [led1, led2, led3]
}
