import cv2
import numpy as np

from human_pose.pose_reader import PoseReader
from pose_estimation.aruco import get_camera, get_robot
from stream_reader import StreamReader
from transformations import render

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
    sr = StreamReader(url="http://192.168.56.103:8080/video", height=height, width=width)
    sr.start()
    robot_pos = None
    robot_yaw = None
    while 1:
        # _, frame = camera.read()
        frame = sr.image
        if frame.max() == 0:
            continue
        camera_transformation = get_camera(frame,
                                           map,
                                           marker_size=0.17,
                                           camera_matrix=camera_matrix,
                                           distortion=None)
        if camera_transformation is not None:
            robot_pos, robot_yaw = get_robot(frame, camera_transformation, camera_matrix, f, None, 4, 0.085)
        if robot_pos is not None and robot_yaw is not None:
            print(f'pos:{robot_pos}\trobot_yaw: {robot_yaw}')
        if camera_transformation is not None:
            for p in workspace:
                render(frame, p, camera_transformation, f)
            if robot_pos is not None:
                render(frame, robot_pos, camera_transformation, f, color=(255,0,0))
        p = None
        # p = pr.detect(image_bgr=frame, show=True)
        if p and camera_transformation is not None:
            print(p.get_world_position(camera_transformation[:3, :3],
                                       camera_transformation[:3, 3], f))
        cv2.imshow("okno", frame)
        cv2.waitKey(1)
