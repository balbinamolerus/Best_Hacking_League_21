from time import sleep
from gpiozero import Button
import paho.mqtt.client as mqtt

broker_address = "192.168.1.200"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
client.connect(broker_address, 1883)
client.loop_start()

button = Button(4)
while True:
    if button.is_pressed==True:
        print("Alarm")