import RPi.GPIO as GPIO
# import paho.mqtt.client as mqtt
# import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(2, GPIO.IN)

# broker_address = "192.168.1.200"
# client = mqtt.Client()
# client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
# client.on_message = on_message
# client.connect(broker_address, 1883)
# client.loop_start()

before = 0
now = 0
try:
    while True:
        now = GPIO.input(2)
        if now == 1 and before == 0:
            print(before, now, '\n alarm')
        else:
            print(before, now)
        before = GPIO.input(2)
except KeyboardInterrupt:
    print('Koniec')
