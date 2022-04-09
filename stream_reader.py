import subprocess as sp
import numpy as np
import threading


class StreamReader(threading.Thread):
    def __init__(self, url='http://192.168.85.50:8080/video', width=1280, height=720):
        super().__init__()
        self.width = width
        self.height = height
        self.image = np.zeros((self.height, self.width, 3))
        self.url = url
        self.pipe = sp.Popen(["ffmpeg",
                              "-i", self.url,
                              "-loglevel", "quiet",
                              "-an",
                              "-f", "image2pipe",
                              "-pix_fmt", "bgr24",
                              "-vcodec", "rawvideo", "-"],
                             stdin=sp.PIPE, stdout=sp.PIPE)

    def run(self):
        while True:
            try:
                raw_image = self.pipe.stdout.read(self.width * self.height * 3)
                self.image = np.frombuffer(raw_image, dtype=np.uint8).reshape((self.height, self.width, 3))
            except ValueError:
                self.pipe = sp.Popen(["ffmpeg",
                                      "-i", self.url,
                                      "-loglevel", "quiet",
                                      "-an",
                                      "-f", "image2pipe",
                                      "-pix_fmt", "bgr24",
                                      "-vcodec", "rawvideo", "-"],
                                     stdin=sp.PIPE, stdout=sp.PIPE)
