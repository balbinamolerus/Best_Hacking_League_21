from time import sleep
from gpiozero import Button
import paho.mqtt.client as mqtt

broker_address = "192.168.1.200"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
client.connect(broker_address, 1883)
client.loop_start()

button = Button(21)

while True:
    x = 0
    time = 0
    while time<100:
        if button.is_pressed == False:
            x=x+1
        sleep(0.05)
        if x > 50:
            print('alarm')
            client.publish("BHL/FattyAlarm/Alarm", "1", qos=1, retain=True)
            x = 0
            sleep(20)
        time = time + 1

