import cv2
from flask import Flask, Response, render_template,request

app = Flask(__name__, static_url_path="/static", static_folder='/home/drozdzal/Python/flask_trash/static')

class Camera:
    def __init__(self):
        self.is_stream_on = False
        self.camera_port = 0

    def check_stream(self):
        response=self.is_stream_on
        print(response)
        return response

    def turn_on_stream(self):
        self.is_stream_on = True
        #self.camera = cv2.VideoCapture("http://192.168.0.235:8080/video")
        self.camera = cv2.VideoCapture(0)
        print(self.is_stream_on)

    def get_frame(self):
  # this makes a web cam object        print(self.is_stream_on)
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

@app.route('/home',methods = ['POST', 'GET'])
def home():

    if request.method=="POST":
        position_x = request.form['position_x']
        position_y= request.form['position_y']
        yaw = request.form['yaw']
        print(position_x)
        print(position_y)
        print(yaw)


    return render_template("Home.html",mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_buffor')
def video_buffor():
    if obraz.check_stream():
        return Response(obraz.get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/turn_on_camera')
def turn_on_camera():
    print("cos  robie")
    obraz.turn_on_stream()
    return Response('OK')


@app.route('/turn_off_camera')
def turn_off_camera():
    obraz.release()
    return Response('OK')

#
# @app.route('/is_alive')
# def is_alive():
#     return Response('OK')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True, threaded=True)

# GET sending deta for client
# POST is geting data form server
#
