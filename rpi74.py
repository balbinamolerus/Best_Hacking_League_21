import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)

dioda = GPIO.PWM(12, 50)  # Nowa instancja PWM
wypelnienie = 0  # Wypełnienie sygnału PWM
dioda.start(wypelnienie)  # Uruchomienie sygnału PWM

try:
    while True:
        wypelnienie += 5
        if wypelnienie > 100:
            wypelnienie = 0
        dioda.ChangeDutyCycle(wypelnienie)  # Ustaw nową wartość wypełnienia
        time.sleep(0.05)
except KeyboardInterrupt:
    print('Koniec')

dioda.stop()
GPIO.cleanup()