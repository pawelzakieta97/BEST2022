import cv2
from flask import Flask, Response, render_template,request
from time import sleep
import requests

class Camera:
    def __init__(self):
        self.is_stream_on = True
        self.camera = cv2.VideoCapture('http://192.168.56.103:8080/video')
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
app = Flask(__name__, static_url_path="/static", static_folder='/home/pawel/BEST2022/web_server/static')


@app.route('/home',methods = ['POST', 'GET'])
def home():
    if request.method=="POST":
        item = request.form['item']
        position_x = request.form['position_x']
        position_y= request.form['position_y']
        if item == 'water':
            requests.get("http://192.168.56.76/get?input_servo1_value=1")
        elif item =='coffee':
                requests.get("http://192.168.56.76/get?input_servo2_value=1")

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

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=False, threaded=True)


