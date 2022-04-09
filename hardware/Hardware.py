# Import libraries
import RPi.GPIO as GPIO
import time
from mpu6050 import mpu6050
import threading
import numpy as np
import time

class hardware_setup():
    def __init__(self):
        self.initialize_all()
        #self.gyro_integer=0
        #self.calibrate_gyro()
        self.is_busy = False

    def initialize_all(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(29, GPIO.OUT)
        GPIO.setup(31, GPIO.OUT)
        GPIO.setup(33, GPIO.OUT)
        GPIO.setup(35, GPIO.OUT)
        self.left_motor = GPIO.PWM(11, 50)
        self.right_motor = GPIO.PWM(13, 50)
        self.left_motor.start(0)
        self.right_motor.start(0)
        #self.sensor = mpu6050(0x68)
        #print("Waiting for 2 seconds")
        time.sleep(2)
    def wheelsForward(self):
        GPIO.output(29, 1)
        GPIO.output(31, 0)
        GPIO.output(33, 1)
        GPIO.output(35, 0)

    def TurnLeft(self):
        GPIO.output(29, 0)
        GPIO.output(31, 1)
        GPIO.output(33, 1)
        GPIO.output(35, 0)

    def TurnRight(self):
        GPIO.output(29, 1)
        GPIO.output(31, 0)
        GPIO.output(33, 0)
        GPIO.output(35, 1)

    def setPWM(self,left,right):
        self.right_motor.ChangeDutyCycle(right)
        self.left_motor.ChangeDutyCycle(left)

    def calibrate_gyro(self):
        gyro=[]
        start = time.time()
        while (time.time()-start)<2:
            gyro.append(self.sensor.get_gyro_data()['z'])
        gyro=np.array(gyro)
        gyro=gyro.mean()
        self.mean_gyro=gyro


    def integer_gyro_data(self):
        while 1:
            start = time.time()
            reading = self.sensor.get_gyro_data()['z'] - self.mean_gyro
            # print(self.sensor.get_gyro_data()['z'])
            self.gyro_integer+=reading * (time.time() - start)

    def work_in_progress(self):
        gyro_thread=threading.Thread(target=self.integer_gyro_data)
        main_process=threading.Thread(target=self.decision_process)
        gyro_thread.start()
        main_process.start()
        gyro_thread.join()
        main_process.join()

    def decision_process(self):
        while 1:
            pass

if __name__ == "__main__":
    Hardware=hardware_setup()
    Hardware.work_in_progress()



