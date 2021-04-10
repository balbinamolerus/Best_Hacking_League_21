# importing libraries
import paho.mqtt.client as mqtt
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import threading
import RPi.GPIO as GPIO

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN)  # RFID
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(1, GPIO.OUT)
    GPIO.output(24, GPIO.LOW)  # CZERWONA
    GPIO.output(25, GPIO.LOW)  # YELLOW UPPER
    GPIO.output(8, GPIO.LOW)  # YELLOW MIDDLE
    GPIO.output(7, GPIO.LOW)  # YELLOW BOTTOM
    GPIO.output(1, GPIO.LOW)  # GREEN

    RFID_flag = 0
    Alarm = 0
    armed = 0;
    password = [1, 2, 3, 4]
    code = []
    txt = ''
    MoveAlarm = 0
    WaterAlarm = 0
    FireAlarm = 0
    FridgeAlarm = 0
    problem = 0

    # Bool, który decyduje, czy wysyłane są komunikaty po MQTT
    MQTT_publish = True


    def on_message(client, userdata, message):
        global MoveAlarm, WaterAlarm, FireAlarm
        if message.topic == "BHL/MoveDetected/Alarm":
            MoveAlarm = 1
        if message.topic == "BHL/FireAlarm/Alarm":
            FireAlarm = 1
        if message.topic == "BHL/WaterAlarm/Alarm":
            WaterAlarm = 1


    broker_address = "192.168.1.200"
    client = mqtt.Client("Control_Interface")
    client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
    client.on_message = on_message
    client.connect(broker_address, 1883)
    client.loop_start()
    client.subscribe([("BHL/MoveAlarm/Alarm", 1), ("BHL/FireAlarm/Alarm", 1), ("BHL/WaterAlarm/Alarm", 1),
                      ("BHL/MoveDetected/Alarm", 1)])


    def RFID_callback(channel):
        global RFID_flag
        RFID_flag = 1


    GPIO.add_event_detect(23, GPIO.FALLING, callback=RFID_callback, bouncetime=200)


    class AThread(QThread):

        def run(self):
            global armed, MoveAlarm, WaterAlarm, FireAlarm, Alarm, problem, RFID_flag
            while True:
                if RFID_flag == 1:
                    RFID_flag = 0
                    if armed == 1:
                        window.rfid()
                    elif armed == 0:
                        arm_alarm()

                if armed == 1 and MoveAlarm == 1 and Alarm == 0:
                    window.label.setStyleSheet("color: rgb(0, 0, 0);")
                    problem = 1
                    for t in range(5, -1, -1):
                        if RFID_flag == 1 or armed == 0:
                            problem = 0
                            break
                        if t == 0:
                            window.label.setStyleSheet("color: rgb(255, 0, 0);")
                            window.label.setText('ALARM'.format(t))
                            Alarm = 1
                            problem = 0
                            GPIO.output(24, GPIO.HIGH)  # CZERWONA
                            GPIO.output(25, GPIO.HIGH)  # YELLOW UPPER
                            GPIO.output(8, GPIO.HIGH)  # YELLOW MIDDLE
                            GPIO.output(7, GPIO.HIGH)  # YELLOW BOTTOM
                            GPIO.output(1, GPIO.HIGH)  # GREEN
                            if MQTT_publish == True:
                                client.publish("BHL/MoveAlarm/Alarm", "1")
                            break
                        if txt == '':
                            window.label.setText('Aktywacja alarmu za {}s'.format(t))
                        time.sleep(1)
                if WaterAlarm == 1:
                    GPIO.output(24, GPIO.LOW)  # CZERWONA
                    GPIO.output(25, GPIO.LOW)  # YELLOW UPPER
                    GPIO.output(8, GPIO.LOW)  # YELLOW MIDDLE
                    GPIO.output(7, GPIO.LOW)  # YELLOW BOTTOM
                    GPIO.output(1, GPIO.LOW)  # GREEN
                    armed = 1
                    while WaterAlarm:
                        if len(code) == 0:
                            GPIO.output(1, GPIO.LOW)
                            window.label.setStyleSheet("color: rgb(0, 0, 255);")
                            window.label.setText('UWAGA ZALANIE!')
                        time.sleep(1)
                        GPIO.output(7, GPIO.HIGH)  # YELLOW BOTTOM
                        time.sleep(1)
                        GPIO.output(7, GPIO.LOW)  # YELLOW BOTTOM
                        if armed == 0:
                            window.label.setStyleSheet("color: rgb(0, 255, 0);")
                            window.label.setText('Alarm rozbrojony')
                            GPIO.output(24, GPIO.LOW)  # CZERWONA
                            GPIO.output(25, GPIO.LOW)  # YELLOW UPPER
                            GPIO.output(8, GPIO.LOW)  # YELLOW MIDDLE
                            GPIO.output(7, GPIO.LOW)  # YELLOW BOTTOM
                            GPIO.output(1, GPIO.HIGH)  # GREEN
                        if RFID_flag == 1:
                            WaterAlarm = 0
                if FireAlarm == 1:
                    GPIO.output(24, GPIO.LOW)  # CZERWONA
                    GPIO.output(25, GPIO.LOW)  # YELLOW UPPER
                    GPIO.output(8, GPIO.LOW)  # YELLOW MIDDLE
                    GPIO.output(7, GPIO.LOW)  # YELLOW BOTTOM
                    GPIO.output(1, GPIO.LOW)  # GREEN
                    armed = 1
                    while FireAlarm == 1:
                        if len(code) == 0:
                            GPIO.output(1, GPIO.LOW)  # GREEN
                            window.label.setStyleSheet("color: rgb(255, 0, 0);")
                            window.label.setText('UWAGA POZAR!')
                        time.sleep(1)
                        GPIO.output(8, GPIO.HIGH)  # YELLOW MIDDLE
                        time.sleep(1)
                        GPIO.output(8, GPIO.LOW)  # YELLOW MIDDLE
                        if armed == 0:
                            window.label.setStyleSheet("color: rgb(0, 255, 0);")
                            window.label.setText('Alarm rozbrojony')
                            GPIO.output(24, GPIO.LOW)  # CZERWONA
                            GPIO.output(25, GPIO.LOW)  # YELLOW UPPER
                            GPIO.output(8, GPIO.LOW)  # YELLOW MIDDLE
                            GPIO.output(7, GPIO.LOW)  # YELLOW BOTTOM
                            GPIO.output(1, GPIO.HIGH)  # GREEN
                        if RFID_flag == 1:
                            FireAlarm = 0


    def clear_flags():
        global MoveAlarm, WaterAlarm, FireAlarm, Alarm, RFID_Flag
        problem = 0
        Alarm = 0
        MoveAlarm = 0
        WaterAlarm = 0
        FireAlarm = 0
        RFID_flag = 0
        GPIO.output(24, GPIO.LOW)  # CZERWONA
        GPIO.output(25, GPIO.LOW)  # YELLOW UPPER
        GPIO.output(8, GPIO.LOW)  # YELLOW MIDDLE
        GPIO.output(7, GPIO.LOW)  # YELLOW BOTTOM
        GPIO.output(1, GPIO.LOW)  # GREEN
        if MQTT_publish == True:
            client.publish("BHL/StopAlarm", "1")


    def arm_alarm():
        global code, txt, armed, RFID_flag
        window.label.setStyleSheet("color: rgb(255, 0, 0);")
        for t in range(6, -2, -2):
            if RFID_flag == 1:
                window.label.setStyleSheet("color: rgb(0, 255, 0);")
                window.label.setText('Przerwano uzbrajanie alarmu')
                time.sleep(2)
                break
            if t < 20:
                window.label.setText('Uzbrajanie alarmu {}s'.format(t + 1))
                GPIO.output(25, GPIO.HIGH)
                time.sleep(1)
            window.label.setText('Uzbrajanie alarmu {}s'.format(t))
            GPIO.output(25, GPIO.LOW)
            time.sleep(1)
        clear_flags()
        GPIO.output(25, GPIO.LOW)
        if RFID_flag == 1:
            RFID_flag = 0
            armed = 0
            clean_label()

        else:
            window.label.setText('Alarm uzbrojony')
            GPIO.output(24, GPIO.HIGH)
            GPIO.output(25, GPIO.LOW)
            GPIO.output(8, GPIO.LOW)
            GPIO.output(7, GPIO.LOW)
            GPIO.output(1, GPIO.LOW)
            armed = 1


    def clean_delay():
        global txt, code
        if problem == 0 and Alarm == 1:
            time.sleep(1)
            window.label.setStyleSheet("color: rgb(255, 0, 0);")
            window.label.setText('ALARM')
            GPIO.output(24, GPIO.HIGH)  # CZERWONA
            GPIO.output(25, GPIO.HIGH)  # YELLOW UPPER
            GPIO.output(8, GPIO.HIGH)  # YELLOW MIDDLE
            GPIO.output(7, GPIO.HIGH)  # YELLOW BOTTOM
            GPIO.output(1, GPIO.HIGH)  # GREEN
            code = []
            txt = ''
        else:
            GPIO.output(25, GPIO.LOW)  # YELLOW UPPER
            GPIO.output(8, GPIO.LOW)  # YELLOW MIDDLE
            GPIO.output(7, GPIO.HIGH)  # YELLOW BOTTOM
            GPIO.output(1, GPIO.LOW)  # GREEN
            time.sleep(0.5)
            code = []
            txt = ''
            GPIO.output(25, GPIO.LOW)  # YELLOW UPPER
            GPIO.output(8, GPIO.HIGH)  # YELLOW MIDDLE
            GPIO.output(7, GPIO.LOW)  # YELLOW BOTTOM
            time.sleep(0.5)
            GPIO.output(25, GPIO.HIGH)  # YELLOW UPPER
            GPIO.output(8, GPIO.LOW)  # YELLOW MIDDLE
            GPIO.output(7, GPIO.LOW)  # YELLOW BOTTOM
            time.sleep(0.5)
            GPIO.output(25, GPIO.LOW)  # YELLOW UPPER
            clean_label()


    def clean_label():
        global armed, Alarm, FireAlarm, WaterAlarm
        if armed == 1 and FireAlarm == 0 and WaterAlarm == 0 and problem == 0:
            window.label.setStyleSheet("color: rgb(255, 0, 0);")
            window.label.setText('Alarm uzbrojony')
            GPIO.output(24, GPIO.HIGH)
            GPIO.output(25, GPIO.LOW)  # YELLOW UPPER
            GPIO.output(8, GPIO.LOW)  # YELLOW MIDDLE
            GPIO.output(7, GPIO.LOW)  # YELLOW BOTTOM
            GPIO.output(1, GPIO.LOW)  # GREEN
        elif armed == 1 and Alarm == 1:
            window.label.setStyleSheet("color: rgb(255, 0, 0);")
            window.label.setText('ALARM')
            GPIO.output(24, GPIO.HIGH)  # CZERWONA
            GPIO.output(25, GPIO.HIGH)  # YELLOW UPPER
            GPIO.output(8, GPIO.HIGH)  # YELLOW MIDDLE
            GPIO.output(7, GPIO.HIGH)  # YELLOW BOTTOM
            GPIO.output(1, GPIO.HIGH)  # GREEN
        elif armed == 0:
            window.label.setStyleSheet("color: rgb(0, 255, 0);")
            Alarm = 0
            window.label.setStyleSheet("color: rgb(0, 255, 0);")
            window.label.setText('Alarm rozbrojony')
            clear_flags()
            GPIO.output(24, GPIO.LOW)  # CZERWONA
            GPIO.output(25, GPIO.LOW)  # YELLOW UPPER
            GPIO.output(8, GPIO.LOW)  # YELLOW MIDDLE
            GPIO.output(7, GPIO.LOW)  # YELLOW BOTTOM
            GPIO.output(1, GPIO.HIGH)  # GREEN


    def incorrect_code():
        global code, txt, armed
        window.label.setText('Kod niepoprawny')
        t1 = threading.Thread(target=clean_delay)
        t1.start()


    def correct_code():
        global code, txt, armed
        if armed == 1:
            code = []
            txt = ''
            armed = 0
            t1 = threading.Thread(target=clean_label)
            t1.start()
        elif armed == 0:
            code = []
            txt = ''
            t1 = threading.Thread(target=arm_alarm)
            t1.start()


    class Window(QMainWindow):

        def __init__(self):
            super().__init__()
            self.setWindowTitle("System alarmowy")
            self.setGeometry(100, 100, 620, 450)
            self.UiComponents()
            self.show()

            # method for widgets

        def UiComponents(self):
            self.label = QLabel(self)
            self.label.setGeometry(5, 5, 790, 80)
            self.label.setWordWrap(True)
            self.label.setStyleSheet("border : 2px solid black")
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setFont(QFont('Arial', 25))
            push1 = QPushButton("1", self)
            push1.setGeometry(230, 97, 110, 110)
            push2 = QPushButton("2", self)
            push2.setGeometry(345, 97, 110, 110)
            push3 = QPushButton("3", self)
            push3.setGeometry(460, 97, 110, 110)
            push4 = QPushButton("4", self)
            push4.setGeometry(230, 212, 110, 110)
            push5 = QPushButton("5", self)
            push5.setGeometry(345, 212, 110, 110)
            push6 = QPushButton("5", self)
            push6.setGeometry(460, 212, 110, 110)
            push7 = QPushButton("7", self)
            push7.setGeometry(230, 327, 110, 110)
            push8 = QPushButton("8", self)
            push8.setGeometry(345, 327, 110, 110)
            push9 = QPushButton("9", self)
            push9.setGeometry(460, 327, 110, 110)
            push1.clicked.connect(self.action1)
            push2.clicked.connect(self.action2)
            push3.clicked.connect(self.action3)
            push4.clicked.connect(self.action4)
            push5.clicked.connect(self.action5)
            push6.clicked.connect(self.action6)
            push7.clicked.connect(self.action7)
            push8.clicked.connect(self.action8)
            push9.clicked.connect(self.action9)

            self.showMaximized()

        def rfid(self):
            global code, txt, armed, Alarm
            Alarm = 0
            armed = 0
            code = []
            txt = ''
            clean_label()

        def action1(self):
            global code, txt
            code.append(1)
            self.label.setStyleSheet("color: rgb(0, 0, 0);")
            txt = txt + '*'
            if len(code) == 4:
                if (code == password):
                    correct_code()
                else:

                    incorrect_code()
            else:
                self.label.setText(txt)

        def action2(self):
            global code, txt
            code.append(2)
            self.label.setStyleSheet("color: rgb(0, 0, 0);")
            txt = txt + '*'
            if len(code) == 4:
                if (code == password):
                    correct_code()
                else:

                    incorrect_code()
            else:
                self.label.setText(txt)

        def action3(self):
            global code, txt
            code.append(3)
            self.label.setStyleSheet("color: rgb(0, 0, 0);")
            txt = txt + '*'
            if len(code) == 4:
                if (code == password):
                    correct_code()
                else:

                    incorrect_code()
            else:
                self.label.setText(txt)

        def action4(self):
            global code, txt
            code.append(4)
            self.label.setStyleSheet("color: rgb(0, 0, 0);")
            txt = txt + '*'
            if len(code) == 4:
                if (code == password):
                    correct_code()
                else:

                    incorrect_code()
            else:
                self.label.setText(txt)

        def action5(self):
            global code, txt
            code.append(5)
            self.label.setStyleSheet("color: rgb(0, 0, 0);")
            txt = txt + '*'
            if len(code) == 4:
                if (code == password):
                    correct_code()
                else:

                    incorrect_code()
            else:
                self.label.setText(txt)

        def action6(self):
            global code, txt
            code.append(6)
            self.label.setStyleSheet("color: rgb(0, 0, 0);")
            txt = txt + '*'
            if len(code) == 4:
                if (code == password):
                    correct_code()
                else:

                    incorrect_code()
            else:
                self.label.setText(txt)

        def action7(self):
            global code, txt
            code.append(7)
            self.label.setStyleSheet("color: rgb(0, 0, 0);")
            txt = txt + '*'
            if len(code) == 4:
                if (code == password):
                    correct_code()
                else:

                    incorrect_code()
            else:
                self.label.setText(txt)

        def action8(self):
            global code, txt
            code.append(8)
            self.label.setStyleSheet("color: rgb(0, 0, 0);")
            txt = txt + '*'
            if len(code) == 4:
                if (code == password):
                    correct_code()
                else:

                    incorrect_code()
            else:
                self.label.setText(txt)

        def action9(self):
            global code, txt
            code.append(9)
            self.label.setStyleSheet("color: rgb(0, 0, 0);")
            txt = txt + '*'
            if len(code) == 4:
                if (code == password):
                    correct_code()
                else:

                    incorrect_code()
            else:
                self.label.setText(txt)


    App = QApplication(sys.argv)
    window = Window()
    window.label.setStyleSheet("color: rgb(0, 255, 0);")
    window.label.setText('Alarm rozbrojony')
    clear_flags()
    GPIO.output(1, GPIO.HIGH)  # GREEN
    thread = AThread()
    thread.finished.connect(App.exit)
    thread.start()
    sys.exit(App.exec())
    # client.loop_stop() #stop the loop

except:
    print("Clean Program Exit")

finally:
    GPIO.cleanup()  # this ensures a clean exit

