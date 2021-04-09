from time import sleep
from gpiozero import MotionSensor


pir = MotionSensor(4)

while True:
  print(pir.wait_for_motion())
  sleep(0.1)
