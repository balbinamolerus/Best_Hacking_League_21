import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(2, GPIO.IN)

try:
    while True:
        print(GPIO.input(2))
except KeyboardInterrupt:
    print('Koniec')
