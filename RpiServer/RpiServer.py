from flask import Flask, request
import time
import threading
from hardware.Hardware import hardware_setup

app = Flask(__name__)

mobile = hardware_setup()

@app.route('/')
def index():
  return "mobile platform remote control server online!"


@app.route('/drive', methods=['GET', 'POST'])
def drive_power():
    if request.method == 'POST':
        if mobile.is_busy:
            return "-1"
        args = request.args
        pwm_val=80
        mobile.wheelsForward()
        mobile.setPWM(pwm_val,pwm_val)
        mobile.is_busy = True
        time.sleep(float(args['power']))
        mobile.setPWM(0, 0)
        mobile.is_busy = False
        # ACTUALLY SET THE POWER
        return f"Setting drive power to {args['power']}"
    else:
        return str(mobile.drive_power)


@app.route('/turn', methods=['GET', 'POST'])
def steering_angle():
    if request.method == 'POST':
        if mobile.is_busy:
            return "-1"
        args = request.args
        pwm_val = 50
        angle = float(args['angle'])
        if angle>0:
            mobile.TurnLeft()
            mobile.setPWM(pwm_val, pwm_val)
            mobile.is_busy = True
            time.sleep(angle)
        elif angle<0:
            mobile.TurnRight()
            mobile.setPWM(pwm_val, pwm_val)
            mobile.is_busy = True
            time.sleep(-angle)
        mobile.setPWM(0, 0)
        mobile.is_busy = False
        # ACTUALLY SET THE POWER
        return "1"
    else:
        return "-1"



if __name__ == '__main__':
    app.debug = False
    app.run(host="0.0.0.0")