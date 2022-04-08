import subprocess as sp
import numpy as np
import cv2

url = 'http://192.168.85.50:8080/video'

pipe = sp.Popen(["ffmpeg",
                 "-i", url,
                 "-loglevel", "quiet",
                 "-an",
                 "-f", "image2pipe",
                 "-pix_fmt", "bgr24",
                 "-vcodec", "rawvideo", "-"],
                stdin=sp.PIPE, stdout=sp.PIPE)

while True:
    width = 1920
    height = 1080
    raw_image = pipe.stdout.read(width * height * 3)
    image = np.frombuffer(raw_image, dtype=np.uint8).reshape((height, width, 3))
    cv2.imshow("xyz", image)
    if cv2.waitKey(5) == 27:
        break
