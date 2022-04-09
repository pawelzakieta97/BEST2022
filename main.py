import datetime

import cv2
import numpy as np

from human_pose.pose_reader import PoseReader
from pose_estimation.aruco import get_camera, get_robot
from stream_reader import StreamReader
from transformations import render
from raspberry_controller import RaspberryController
from playsound import playsound


def call_for_help():
    print("DZOWNIE PO POGOTOWIE")
    playsound('./calling.wav')


def instruct():
    print("INFORMOWANIE O OPCJACH")
    playsound('./inform.wav')


def disarm_call_for_help():
    print("NOT CALLING FOR HELP")
    playsound('./disarm.wav')


def kawusia_delivered():
    print("KAWUSIA DELIVERED")
    playsound("./kawusia.wav")


def water_delivered():
    print("WATER DELIVERED")
    playsound("./water.wav")


if __name__ == '__main__':
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
        if robot_pos is not None and robot_yaw is not None:
            pass
            # print(f'pos:{robot_pos}\trobot_yaw: {robot_yaw}')
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
        if state == 'idle':
            if camera_transformation is not None and robot_pos is not None and p is not None:
                if p.is_laying():
                    state = 'following'
                    robot_set_pos = p.get_world_position(camera_transformation[:3, :3],
                                                         camera_transformation[:3, 3], f)

                if help_start is not None and datetime.datetime.now() - help_start < help_timeout:
                    continue
                if p.is_left_hand_raised():

                    state = 'delivering_kawusia'
                    robot_set_pos = p.get_world_position(camera_transformation[:3, :3],
                                                         camera_transformation[:3, 3], f)

                if p.is_right_hand_raised():
                    state = 'delivering_water'
                    robot_set_pos = p.get_world_position(camera_transformation[:3, :3],
                                                         camera_transformation[:3, 3], f)

        elif state == 'following':
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
