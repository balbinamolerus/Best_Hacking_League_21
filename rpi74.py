import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

# import pygame


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.OUT)

Alarm = False
Brightness = 0


# pygame.mixer.init()
# pygame.mixer.music.load('alarm.mp3')
# pygame.mixer.music.set_volume(1.0)


def on_message(client, userdata, message):
    global Alarm, Brightness
    if message.topic == "BHL/MoveAlarm/Alarm" or message.topic == "BHL/WaterAlarm/Alarm" or message.topic == "BHL/FireAlarm/Alarm":
        Alarm = True


    if message.topic == "BHL/StopAlarm":
        Alarm = False

    if message.topic == "BHL/LED/setOn":
        if str(message.payload.decode("utf-8")) == "0":
            Brightness = 0
        if str(message.payload.decode("utf-8")) == "1" and not Brightness:
            Brightness = 100

    if message.topic == "BHL/LED/setBrightness":
        Brightness = int(message.payload.decode("utf-8"))


broker_address = "192.168.1.200"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
client.on_message = on_message
client.connect(broker_address, 1883)
client.loop_start()

client.subscribe(
    [("BHL/MoveAlarm/Alarm", 1), ("BHL/FireAlarm/Alarm", 1), ("BHL/WaterAlarm/Alarm", 1), ("BHL/StopAlarm", 1),
     ("BHL/LED/setOn", 1), ("BHL/LED/setBrightness", 1)])

dioda = GPIO.PWM(21, 980)  # Nowa instancja PWM
wypelnienienew = 0  # Wypełnienie sygnału PWM
wypelnienieold = 0
dioda.start(wypelnienienew)  # Uruchomienie sygnału PWM

updown = True
wypelnienie = 0
oldBrightness = 0
counter = 0


last_temperature = 100
last_humidity = 100

#client.publish("BHL/temperature", str(last_temperature), qos=1, retain=True)
#client.publish("BHL/humidity", str(last_humidity), qos=1, retain=True)


try:
    while True:
        if Alarm:
            if updown == True:
                dioda.ChangeDutyCycle(wypelnienie)
                wypelnienie = wypelnienie + 2
                if wypelnienie == 100:
                    updown = False
            else:
                dioda.ChangeDutyCycle(wypelnienie)
                wypelnienie = wypelnienie - 2
                if wypelnienie == 2:
                    updown = True

        else:
            if Brightness != oldBrightness:
                dioda.ChangeDutyCycle(Brightness)
                client.publish("BHL/LED/getBrightness", str(Brightness), qos=1, retain=True)
                if Brightness:
                    client.publish("BHL/LED/getOn", "1", qos=1, retain=True)
                else:
                    client.publish("BHL/LED/getOn", "0", qos=1, retain=True)
                oldBrightness = Brightness


        time.sleep(0.01)

except KeyboardInterrupt:
    print('Koniec')

dioda.stop()
GPIO.cleanup()
