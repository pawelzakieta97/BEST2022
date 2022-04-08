import cv2
import mediapipe as mp
import time
from stream_reader import StreamReader
from pose_reader import PoseReader
from transformations import *

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(-1)
pTime = 0
sr = StreamReader()
# sr.start()
pr = PoseReader()

camera_rotation = rotx(np.pi / 2)[:3, :3]
camera_position = np.array([0,0,1])
while True:
    res, img = cap.read()

    # img = sr.image
    # if img.max() == 0:
    #     continue
    # imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    p = pr.detect(image_bgr=img, show=True)
    if p:
        print(p.get_world_position(camera_rotation, camera_position, 800))
