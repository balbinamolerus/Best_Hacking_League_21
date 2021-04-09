import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

import urllib

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(2, GPIO.IN)

broker_address = "192.168.1.200"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
client.connect(broker_address, 1883)
client.loop_start()

before = 0
now = 0
counter = 0
try:
    while True:
        now = GPIO.input(2)
        if now == 1 and before == 0:
            print('alarm')
            client.publish("BHL/FireAlarm/Alarm", "1", qos=1, retain=True)
        before = GPIO.input(2)

        # try:
        html = urllib.urlopen('http://192.168.1.82/')

        htmltext = html.read()
        print(htmltext)
        # except:
        #     print('error opening link')


except KeyboardInterrupt:
    print('Koniec')
