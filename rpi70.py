from time import sleep
from gpiozero import Button
import paho.mqtt.client as mqtt
import time

broker_address = "192.168.1.200"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
client.connect(broker_address, 1883)
client.loop_start()

button = Button(21)
last_button = True

open_count = False
fridge_alarm = False
starttime = time.time()
while True:
    # x = 0
    # time = 0
    # while time < 100:
    #     if button.is_pressed == False:
    #         x = x + 1
    #     sleep(0.05)
    #     if x > 50:
    #         client.publish("BHL/FridgeAlarm/Alarm", "1", qos=1, retain=True)
    #         print('alarm')
    #         x = 0
    #         sleep(20)
    #     time = time + 1

    while True:
        new_button = button.is_pressed
        if not new_button and last_button:
            client.publish("BHL/Fridge", "1", qos=1, retain=True)
            starttime = time.time()
            open_count = True

        if new_button and not last_button:
            client.publish("BHL/Fridge", "0", qos=1, retain=True)
            open_count = False

        if open_count and time.time() - starttime > 10:

            client.publish("BHL/FridgeAlarm/Alarm", "1", qos=1, retain=True)
            fridge_alarm = True

        if new_button and fridge_alarm:
            fridge_alarm = False
            client.publish("BHL/FridgeAlarm/Alarm", "0", qos=1, retain=True)


        last_button = new_button
