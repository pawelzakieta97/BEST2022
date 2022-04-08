import cv2
import cv2.aruco as aruco
import numpy as np


def rvec_to_yaw(rvec):
    """
    Convert rotation vector to yaw

    """

    rvec = np.asarray(rvec, dtype=np.float64)
    rmat = cv2.Rodrigues(rvec)[0]

    sy = np.sqrt(rmat[0, 0] * rmat[0, 0] + rmat[1, 0] * rmat[1, 0])
    if sy < 1e-6:
        x = np.arctan2(-rmat[1, 2], rmat[1, 1])
        y = np.arctan2(-rmat[2, 0], sy)
        z = 0
    else:
        x = np.arctan2(rmat[2, 1], rmat[2, 2])
        y = np.arctan2(-rmat[2, 0], sy)
        z = np.arctan2(rmat[1, 0], rmat[0, 0])

    roll, pitch, yaw = np.rad2deg([y, x, z])
    return yaw
def calculate_aruco(image,camera_matrix,camera_distortion,aruco_id,marker_size):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
    parameters = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=aruco_dict, parameters=parameters,
                                                 cameraMatrix=camera_matrix, distCoeff=camera_distortion)
    if ids is not None and ids[0] == aruco_id:
        ret = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)

        rvec, tvec = ret[0][0, 0, :], ret[1][0, 0, :]
        r = cv2.drawFrameAxes(image, camera_matrix, None, rvec, tvec, 0.1)
        rotation_matrix = np.array([[0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 1]],
                                   dtype=float)
        cv2.aruco.drawDetectedMarkers(image, corners, ids)
        return tvec, rvec

camera_matrix=np.loadtxt('camera.txt', delimiter=',')
width = 1280
height = 720
f = width / 53 * 43
camera_matrix = np.array([
    [f, 0, width / 2],
    [0, f, height / 2],
    [0, 0, 1]
])
camera_distorition=np.loadtxt('distortion.txt', delimiter=',')

while 1:
    camera=cv2.VideoCapture("http://192.168.43.70:8080/video")
    _,frame=camera.read()
    print(calculate_aruco(frame,camera_matrix,camera_distorition,0,0.50))
    cv2.imshow("okno",frame)
    cv2.waitKey(1)



