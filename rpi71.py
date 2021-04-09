from time import sleep
from gpiozero import MotionSensor
import paho.mqtt.client as mqtt

broker_address = "192.168.1.200"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
client.connect(broker_address, 1883)
client.loop_start()

pir = MotionSensor(4)

while True:
  x=0
  t=0
  while t<50:
    if pir.wait_for_motion()==True:
      x=x+1
    sleep(0.1)
    if x>20:
      print('alarm')
      client.publish("BHL/MoveAlarm/Alarm", "1", qos=1, retain=True)
      x=0
      print(t)
      sleep(10)
    t=t+1


