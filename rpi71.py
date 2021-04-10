from time import sleep
from gpiozero import MotionSensor
import paho.mqtt.client as mqtt

broker_address = "192.168.1.200"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
client.connect(broker_address, 1883)
client.loop_start()

pir = MotionSensor(4)
lastvalue = False
while True:
  new_value=pir.wait_for_motion()
  if new_value and not lastvalue:
    print('alarm')
    client.publish("BHL/MoveDetected/Alarm", "1", qos=1, retain=True)
    sleep(3)
    lastvalue=new_value

