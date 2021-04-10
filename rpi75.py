from time import sleep
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

broker_address = "192.168.1.200"
client = mqtt.Client("Control_Interface")
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
client.on_message = on_message
client.connect(broker_address, 1883)
client.loop_start()
client.subscribe([("BHL/MoveAlarm/Alarm", 1)])

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.IN)
GPIO.setup(2, GPIO.OUT)
while True:
    now = GPIO.input(17)
    sleep(0.2)
    if now == 0 or client.on_message.topic == "BHL/MoveAlarm/Alarm"=="BHL/MoveAlarm/Alarm":
        print('alarm')
        GPIO.output(2, GPIO.LOW)
    else:
        GPIO.output(2, GPIO.HIGH)

