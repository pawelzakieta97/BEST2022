import cv2
import numpy as np
import mediapipe as mp
import time
from stream_reader import StreamReader
from transformations import translate, rotz, rotx, roty, get_plane_coordinates

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils


class Pose:
    def __init__(self, landmarks, resolution=(480, 640), world_landmarks=None):
        self.landmarks = landmarks
        self.landmarks_px = []
        self.width = resolution[1]
        self.height = resolution[0]
        self.world_landmarks = world_landmarks

        for landmark in landmarks:
            self.landmarks_px.append(np.array([(landmark.x - 0.5) * self.width, (landmark.y - 0.5) * self.height]))

    def get_face_direction(self, camera_matrix=None, f=800):
        if self.landmarks[5].visibility > 0.9 and self.landmarks[2].visibility > 0.9:
            left_eye = np.array(self.landmarks[2])
            right_eye = np.array(self.landmarks[5])

            pass

    def get_world_position(self, camera_rotation, camera_position, f=1):
        valid_landmarks = [l.visibility>0.99 for l in self.landmarks]
        if not valid_landmarks:
            return None
        try:
            lowest_landmark = np.where(np.array(valid_landmarks))[0][-1]
        except:
            return None
        for i in range(27,32):
            if self.landmarks[i].visibility<0.8:
                continue
            return get_plane_coordinates(camera_rotation, camera_position, f,
                                     self.landmarks_px[i][0],
                                     self.landmarks_px[i][1])
        return None

    def get_length(self, idx1, idx2):
        pos1 = np.array([self.world_landmarks[idx1].x, self.world_landmarks[idx1].y, self.world_landmarks[idx1].z])
        pos2 = np.array([self.world_landmarks[idx2].x, self.world_landmarks[idx2].y, self.world_landmarks[idx2].z])
        return np.linalg.norm(pos2-pos1)

    def is_laying(self):
        thigh_length = self.get_length(24, 26)
        if self.world_landmarks[30].y - self.world_landmarks[0].y < 1.5 * thigh_length:
            return True
        return False

    def is_hand_raised(self):
        return self.world_landmarks[20].y < self.world_landmarks[0].y or self.world_landmarks[19].y < self.world_landmarks[0].y

class PoseReader:
    def __init__(self):
        self.mpPose = mp.solutions.pose
        self.pose = mpPose.Pose()
        self.mpDraw = mp.solutions.drawing_utils

    def detect(self, image_bgr, show=False):
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
        p = Pose(landmarks, image_bgr.shape, world_landmarks=world_landmarks)
        # print(landmarks[24])
        # print(p.get_face_direction())
        return p

if __name__ ==' __main__':
    pass
