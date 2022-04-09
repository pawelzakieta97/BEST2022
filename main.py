import datetime
import threading

import cv2
import numpy as np

from human_pose.pose_reader import PoseReader
from pose_estimation.aruco import get_camera, get_robot
from stream_reader import StreamReader
from transformations import render
from raspberry_controller import RaspberryController
from playsound import playsound

import cv2
from flask import Flask, Response, render_template,request
from time import sleep
import requests

class Camera:
    def __init__(self):
        self.is_stream_on = True
        self.camera = cv2.VideoCapture(0)

    def check_stream(self):
        return self.is_stream_on

    def get_frame(self):
        while self.is_stream_on:
            ret,frame = self.camera.read()
            imgencode = cv2.imencode('.png', frame)[1]
            stringData = imgencode.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: text/plain\r\n\r\n' + stringData + b'\r\n')

    def release(self):
        self.is_stream_on = False
        print(self.is_stream_on)
        self.camera.release()

global obraz
obraz=Camera()
app = Flask(__name__, static_url_path="/static", static_folder='/home/pawel/BEST2022/web_server/static', template_folder='/home/pawel/BEST2022/web_server/templates')


def call_for_help():
    print("DZOWNIE PO POGOTOWIE")
    playsound('./calling.mp3')


def instruct():
    print("INFORMOWANIE O OPCJACH")
    playsound('./instruct.mp3')


def disarm_call_for_help():
    print("NOT CALLING FOR HELP")
    playsound('./disarm.mp3')


def kawusia_delivered():
    print("KAWUSIA DELIVERED")
    playsound("./kawusia.mp3")


def water_delivered():
    print("WATER DELIVERED")
    playsound("./water.mp3")


pr = PoseReader()
map = {
    0: np.array([0, 0, 0]),
    1: np.array([0, 0.3, 0])
}
scale = 0.3
workspace = [np.array([0, 0, 0]),
             np.array([0, scale, 0]),
             np.array([scale, scale, 0]),
             np.array([scale, 0, 0])]
# camera_matrix = np.loadtxt('camera.txt', delimiter=',')
width = 1280
height = 720
f = width / 53 * 43
camera_matrix = np.array([
    [f, 0, width / 2],
    [0, f, height / 2],
    [0, 0, 1]
])
# camera_distorition = np.loadtxt('distortion.txt', delimiter=',')
camera = cv2.VideoCapture("http://192.168.56.103:8080/video")
robot_url = "0.0.0.0:5000"
sr = StreamReader(url="http://192.168.56.103:8080/video", height=height, width=width)
sr.start()
robot_pos = None
robot_yaw = None
camera_transformation = None
person_position = None
rc = RaspberryController('http://raspberrypi.local:5000')
robot_set_pos = map[0]
max_distance = 0.5
state = 'idle'
help_start = None
handrise_timeout = datetime.timedelta(seconds=10)
help_timeout = datetime.timedelta(seconds=30)

@app.route('/home',methods = ['POST', 'GET'])
def home():
    if request.method == "POST":
        item = request.form['item']
        position_x = request.form['position_x']
        position_y= request.form['position_y']
        if item == 'water':
            requests.get("http://172.20.10.11/get?input_servo1_value=1")
        elif item =='coffee':
                requests.get("http://172.20.10.11/get?input_servo2_value=1")

        sleep(5)
        ###tutaj nawigacja do x i y
        print(f"Chce do x={position_x} oraz y={position_y}")
        ###

    return render_template("Home.html",mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_buffor')
def video_buffor():
    if obraz.check_stream():
        return Response(obraz.get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response('Stream_off')

@app.route('/camera_off')
def turn_off_camera():
    obraz.release()
    return Response('OK')

rc.enable = False
if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='localhost', port=5000, debug=False, use_reloader=False)).start()
    while 1:
        # _, frame = camera.read()
        frame = sr.image
        if frame.max() == 0:
            continue

        new_camera_transformation = get_camera(frame,
                                               map,
                                               marker_size=0.17,
                                               camera_matrix=camera_matrix,
                                               distortion=None)
        if new_camera_transformation is not None:
            camera_transformation = new_camera_transformation
        if camera_transformation is not None:
            robot_pos, robot_yaw = get_robot(frame, camera_transformation, camera_matrix, f, None, 4, 0.085, h=0.15)
        if camera_transformation is not None:
            for p in workspace:
                render(frame, p, camera_transformation, f)
            if robot_pos is not None:
                render(frame, robot_pos, camera_transformation, f, color=(255, 0, 0))
        # p = None
        p = pr.detect(image_bgr=frame, show=False)
        if p and camera_transformation is not None:
            person_position = p.get_world_position(camera_transformation[:3, :3],
                                                   camera_transformation[:3, 3], f)
            if person_position is not None:
                render(frame, person_position, camera_transformation, f, color=(0, 255, 0))

        # STATE AUTOMATA
        print(f"CURRENT STATE: {state}")
        if state == 'idle':
            if camera_transformation is not None and robot_pos is not None and p is not None:
                if p.is_laying():
                    person_position = p.get_world_position(camera_transformation[:3, :3],
                                                         camera_transformation[:3, 3], f)
                    if person_position is not None:
                        robot_set_pos = person_position
                        state = 'following'

                if help_start is not None and datetime.datetime.now() - help_start < help_timeout:
                    continue
                if p.is_left_hand_raised():
                    person_position = p.get_world_position(camera_transformation[:3, :3],
                                                           camera_transformation[:3, 3], f)
                    if person_position is not None:
                        robot_set_pos = person_position
                        state = 'delivering_kawusia'
                        rc.drive(1)

                if p.is_right_hand_raised():
                    person_position = p.get_world_position(camera_transformation[:3, :3],
                                                           camera_transformation[:3, 3], f)
                    if person_position is not None:
                        robot_set_pos = person_position
                        state = 'delivering_water'
                        rc.drive(1)

        elif state == 'following':
            render(frame, person_position, camera_transformation, f, color=(0, 0, 0), thickness=5, radius=15)
            # if person_position is not None:
            #     robot_set_pos = person_position
            if camera_transformation is not None and robot_pos is not None:
                robot2pos = robot_set_pos - robot_pos
                if np.linalg.norm(robot2pos) < max_distance:
                    state = 'offering_help'
                    help_start = datetime.datetime.now()
                else:
                    required_yaw = np.math.atan2(robot2pos[1], robot2pos[0])
                    yaw_change = required_yaw - robot_yaw
                    if yaw_change < -np.pi:
                        yaw_change += 2 * np.pi
                    if yaw_change > np.pi:
                        yaw_change -= 2 * np.pi
                    print(yaw_change)
                    if abs(yaw_change) > np.pi / 6:
                        rc.turn(-yaw_change / 8)
                        pass
                    else:
                        pass
                        rc.drive(0.2)
        elif state == 'offering_help':
            # TODO: play "do u need help boomer?"
            if datetime.datetime.now() - help_start > handrise_timeout:
                call_for_help()
                state = 'idle'
            if p is not None:
                if not p.is_laying() or p.is_hand_raised():
                    disarm_call_for_help()
                    state = 'idle'

        elif state == 'delivering_kawusia':
            # if person_position is not None:
            #     robot_set_pos = person_position
            render(frame, robot_set_pos, camera_transformation, f, color=(0, 50, 50), thickness=5, radius=15)

            if camera_transformation is not None and robot_pos is not None:
                robot2pos = robot_set_pos - robot_pos
                if np.linalg.norm(robot2pos) < max_distance:
                    kawusia_delivered()
                    state = 'idle'
                else:
                    required_yaw = np.math.atan2(robot2pos[1], robot2pos[0])
                    yaw_change = required_yaw - robot_yaw
                    if yaw_change < -np.pi:
                        yaw_change += 2 * np.pi
                    if yaw_change > np.pi:
                        yaw_change -= 2 * np.pi
                    print(yaw_change)
                    if abs(yaw_change) > np.pi / 6:
                        rc.turn(-yaw_change / 8)
                        pass
                    else:
                        pass
                        rc.drive(0.2)

        elif state == 'delivering_water':
            render(frame, robot_set_pos, camera_transformation, f, color=(50, 0, 0), thickness=5, radius=15)

            if camera_transformation is not None and robot_pos is not None:
                robot2pos = robot_set_pos - robot_pos
                if np.linalg.norm(robot2pos) < max_distance:
                    water_delivered()
                    state = 'idle'
                else:
                    required_yaw = np.math.atan2(robot2pos[1], robot2pos[0])
                    yaw_change = required_yaw - robot_yaw
                    if yaw_change < -np.pi:
                        yaw_change += 2 * np.pi
                    if yaw_change > np.pi:
                        yaw_change -= 2 * np.pi
                    print(yaw_change)
                    if abs(yaw_change) > np.pi / 6:
                        rc.turn(-yaw_change / 8)
                        pass
                    else:
                        pass
                        rc.drive(0.2)
        cv2.imshow("okno", frame)
        cv2.waitKey(1)
