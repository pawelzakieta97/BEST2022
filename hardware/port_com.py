# Import libraries
import RPi.GPIO as GPIO
import time

class hardware_setup():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11,GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        self.left_motor = GPIO.PWM(11,50)
        self.right_motor = GPIO.PWM(13, 50)
        self.left_motor.start(0)
        self.right_motor.start(0)
        print("Waiting for 2 seconds")
        time.sleep(2)

    def set_







#Let's move the servo!
print ("Rotating 180 degrees in 10 steps")

# Define variable duty
duty = 2

#right_motor.ChangeDutyCycle(duty)
#left_motor.ChangeDutyCycle(duty)

# Wait a couple of seconds
time.sleep(2)

# Turn back to 90 degrees
print ("Turning back to 90 degrees for 2 seconds")
servo1.ChangeDutyCycle(7)
servo2.ChangeDutyCycle(7)
servo3.ChangeDutyCycle(7)
time.sleep(2)


GPIO.cleanup()

