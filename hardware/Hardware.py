
import time
import serial

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.050)

count = 0
state = 0

ser.write('Strinas'.encode())

while 1:
    if(state == 0):
        while ser.in_waiting:
            data = ser.readline().decode("ascii")
            if(data == '1'):
                state = 1
                print("1 received")
                ser.write("1 received").encode()
            else:
                print("back to the start")
                ser.write("back to the start").encode()

    elif(state == 1):
        while ser.in_waiting:
            data = ser.readline().decode("ascii")
            if(data == '2'):
                state = 2;
                print("2 received")
                ser.write("2 received").encode()
            else:
                state = 0;
                print("back to the start")
                ser.write("back to the start").encode()

    elif(state == 2):
        while ser.in_waiting:
            data = ser.readline().decode("ascii")
            if(data == '3'):
                print("You win!")
                ser.write("You win!").encode()
                state = 0;
            else:
                state = 0;
                print("back to the start")
                ser.write("back to the start").encode()