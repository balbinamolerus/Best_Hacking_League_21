from time import sleep
from gpiozero import MotionSensor

def detectIntruders():
  pir.wait_for_motion()
  print('Intruder Alert!')
  sleep(5)

pir = MotionSensor(2)

while True:
  detectIntruders()