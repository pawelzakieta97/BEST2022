import cv2
import numpy as np
import mediapipe as mp
import time
from stream_reader import StreamReader
from transformations import translate, rotz, rotx, roty

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils


class Pose:
    def __init__(self, landmarks, resolution=(480, 640)):
        self.landmarks = landmarks
        self.landmarks_px = []
        self.width = resolution[1]
        self.height = resolution[0]

        for landmark in landmarks:
            self.landmarks_px.append(np.array([(landmark.x - 0.5) * self.width, (landmark.y - 0.5) * self.height]))

    def get_face_direction(self, camera_matrix=None, f=800):
        if self.landmarks[5].visibility > 0.9 and self.landmarks[2].visibility > 0.9:
            left_eye = np.array(self.landmarks[2])
            right_eye = np.array(self.landmarks[5])

            pass

    def get_world_position(self, camera_rotation, camera_position, f=1):
        # print(self.landmarks[0])
        foot_pos = np.array([self.landmarks_px[0][0], self.landmarks_px[0][1], f])
        # print(foot_pos)
        direction = camera_rotation.dot(foot_pos / f)
        world_pos = camera_position - direction * (camera_position[2]/direction[2])
        return world_pos


class PoseReader:
    def __init__(self):
        self.mpPose = mp.solutions.pose
        self.pose = mpPose.Pose()
        self.mpDraw = mp.solutions.drawing_utils

    def detect(self, image_bgr, show=True):
        # image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        results = pose.process(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB))
        if results.pose_landmarks is None:
            return None
        mpDraw.draw_landmarks(image_bgr, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        landmarks = []
        landmarks = [lm for lm in results.pose_landmarks.landmark]
        world_landmarks = [lm for lm in results.pose_world_landmarks.landmark]
        if show:
            cv2.imshow("Image", image_bgr)
            cv2.waitKey(1)
        p = Pose(landmarks, image_bgr.shape)
        # print(landmarks[24])
        # print(p.get_face_direction())
        return p

if __name__ ==' __main__':
    pass