from time import sleep
from gpiozero import Button
import paho.mqtt.client as mqtt

broker_address = "192.168.1.200"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
client.connect(broker_address, 1883)
client.loop_start()

button = Button(21)
last_button = True
open_count = False
while True:
    x = 0
    time = 0
    while time<100:
        if button.is_pressed == False:
            x=x+1
        sleep(0.05)
        if x > 50:
            client.publish("BHL/FridgeAlarm/Alarm", "1", qos=1, retain=True)
            print('alarm')
            x = 0
            sleep(20)
        time = time + 1


    while True:
        if not button.is_pressed and last_button:
            client.publish("BHL/Fridge", "1", qos=1, retain=True)


        if button.is_pressed and not last_button:
            client.publish("BHL/Fridge", "0", qos=1, retain=True)
