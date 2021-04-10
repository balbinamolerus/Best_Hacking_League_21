from time import sleep
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

broker_address = "192.168.1.200"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
client.connect(broker_address, 1883)
client.loop_start()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.IN)

while True:
    now = GPIO.input(4)
    if now == 1 and before == 0:
        print('alarm')
    before = GPIO.input(4)