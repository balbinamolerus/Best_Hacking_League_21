import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time
import pygame
import urllib

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(2, GPIO.IN)

pygame.mixer.init()
pygame.mixer.music.load('alarm.mp3')
pygame.mixer.music.set_volume(0.5)


def on_message(client, userdata, message):
    if message.topic == "BHL/MoveAlarm/Alarm" or message.topic == "BHL/WaterAlarm/Alarm" or message.topic == "BHL/FireAlarm/Alarm":

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(loops=-1)

    if message.topic == "BHL/StopAlarm":

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()


broker_address = "192.168.1.200"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
client.connect(broker_address, 1883)
client.on_message = on_message
client.loop_start()
client.subscribe(
    [("BHL/MoveAlarm/Alarm", 1), ("BHL/FireAlarm/Alarm", 1), ("BHL/WaterAlarm/Alarm", 1), ("BHL/StopAlarm", 1)])
before = 0
now = 0
counter = 0
before_water = 0
now_water = 0
try:
    while True:
        now = GPIO.input(2)
        if now == 1 and before == 0:
            print('alarm')
            client.publish("BHL/FireAlarm/Alarm", "1", qos=1, retain=True)
        before = GPIO.input(2)

        # try:
        html = urllib.request.urlopen('http://192.168.1.82/')

        htmltext = html.read()
        now_water = int(htmltext.decode('utf-8'))

        # print(type(htmltext),htmltext)

        if now_water > 300 and before_water <= 300:
            print('water alarm')
            client.publish("BHL/WaterAlarm/Alarm", "1", qos=1, retain=True)
        # except:
        #     print('error opening link')
        before_water = now_water
        time.sleep(1)


except KeyboardInterrupt:
    print('Koniec')
