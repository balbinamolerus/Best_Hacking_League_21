from time import sleep
from gpiozero import MotionSensor


pir = MotionSensor(4)

while True:
  x=0
  t=0
  while t<1000:
    if pir.wait_for_motion()==True:
      x=x+1
    sleep(0.1)
    if x>10:
      print("ALARM")
      x=0
      print(t)


