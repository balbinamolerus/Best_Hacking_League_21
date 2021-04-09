# import RPi.GPIO as GPIO
# import paho.mqtt.client as mqtt
# import sys
# import adafruit_dht
# import time
# import board
# import urllib
#
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
#
# broker_address = "192.168.1.200"
# client = mqtt.Client()
# client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
# client.connect(broker_address, 1883)
# client.loop_start()
#
# dht_device = adafruit_dht.DHT11(board.D4)
#
# # sensor_args = { '11': Adafruit_DHT.DHT11,
# #                 '22': Adafruit_DHT.DHT22,
# #                 '2302': Adafruit_DHT.AM2302 }
# # if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
# #     sensor = sensor_args[sys.argv[1]]
# #     pin = sys.argv[2]
# # else:
# #     print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
# #     print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
# #     sys.exit(1)
#
#
# try:
#     while True:
#         temperature = dht_device.temperature
#         humidity = dht_device.humidity
#         if humidity is not None and temperature is not None:
#             print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
#         else:
#             print('Failed to get reading. Try again!')
#             sys.exit(1)
#         if humidity>70:
#             client.publish("BHL/HumidityAlarm/Alarm", "1", qos=1, retain=True)
#         time.sleep(1)
#
# except KeyboardInterrupt:
#     print('Koniec')


import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)

dioda = GPIO.PWM(12, 5000)  # Nowa instancja PWM
wypelnienie = 0  # Wypełnienie sygnału PWM
dioda.start(wypelnienie)  # Uruchomienie sygnału PWM

try:
    while True:
        wypelnienie += 1
        if wypelnienie > 100:
            wypelnienie = 0
        dioda.ChangeDutyCycle(wypelnienie)  # Ustaw nową wartość wypełnienia
        time.sleep(0.05)
except KeyboardInterrupt:
    print('Koniec')

dioda.stop()
GPIO.cleanup()
