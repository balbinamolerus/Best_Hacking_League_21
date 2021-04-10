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
GPIO.setup(17, GPIO.IN)
GPIO.setup(2, GPIO.OUT)
while True:
    now = GPIO.input(17)
    sleep(1)
    if now == 0:
        print('alarm')
        GPIO.output(2, GPIO.LOW)
        sleep(15)
    else:
        GPIO.output(2, GPIO.HIGH)

