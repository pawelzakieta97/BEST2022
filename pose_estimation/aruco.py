import cv2
import cv2.aruco as aruco
import numpy as np
import math
from transformations import get_plane_coordinates, render


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


def detect_aruco_markers(image, camera_matrix, camera_distortion):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
    parameters = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=aruco_dict, parameters=parameters,
                                                 cameraMatrix=camera_matrix, distCoeff=camera_distortion)
    # cv2.aruco.drawDetectedMarkers(image, corners, ids)
    return corners, ids


def get_relative_aruco_transformation(corners, marker_size, camera_matrix, camera_distortion, image=None):
    ret = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)

    rvec, tvec = ret[0][0, 0, :], ret[1][0, 0, :]
    if image is not None:
        r = cv2.drawFrameAxes(image, camera_matrix, None, rvec, tvec, 0.1)
    aruco_transformation = np.eye(4)
    aruco_transformation[:3, :3] = cv2.Rodrigues(rvec)[0]
    aruco_transformation[:3, 3] = tvec
    return aruco_transformation


def get_relative_camera_transformation(corners, marker_size, camera_matrix, camera_distortion, image=None):
    aruco_transformation = get_relative_aruco_transformation(corners, marker_size, camera_matrix, camera_distortion,
                                                             image)
    camera_transformation = np.linalg.inv(aruco_transformation)

    return camera_transformation, aruco_transformation[2, 3]


def get_camera(image, map, marker_size, camera_matrix, distortion):
    reported_positions = []
    corners, detected_ids = detect_aruco_markers(image, camera_matrix, distortion)
    if not corners:
        return None
    detections = {id[0]: corner for id, corner in zip(detected_ids, corners)}
    for id, position in map.items():
        if id in detections.keys():
            camera_transformation, distance = get_relative_camera_transformation(detections[id], marker_size,
                                                                                 camera_matrix, distortion, image)
            camera_transformation[:3, 3] = camera_transformation[:3, 3] + position
            reported_positions.append((camera_transformation, distance))
    reported_positions = sorted(reported_positions, key=lambda x: x[1])

    if len(reported_positions) > 1:
        pass
        # print(f'diff:{reported_positions[0][0][:3, 3] - reported_positions[1][0][:3, 3]}')
    return reported_positions[0][0] if reported_positions else None


def get_robot(image, camera_transformation, camera_matrix, f, distortion, robot_id, robot_marker_size, h=0):
    corners, detected_ids = detect_aruco_markers(image, camera_matrix, distortion)
    if not corners:
        return None, None
    detections = {id[0]: corner for id, corner in zip(detected_ids, corners)}
    if robot_id not in detections:
        return None, None
    robot_transformation = get_relative_aruco_transformation(detections[robot_id], robot_marker_size,
                                                             camera_matrix, distortion, image)
    robot_transformation = np.dot(camera_transformation, robot_transformation)
    robot_forward = robot_transformation.dot(np.array([0, 1, 0, 1]))
    yaw = np.math.atan2(robot_forward[1], robot_forward[0])
    robot_px_coordinates = detections[robot_id][0].mean(axis=0)

    height, width, _ = image.shape
    robot_px_coordinates[0] = robot_px_coordinates[0] - width / 2
    robot_px_coordinates[1] = robot_px_coordinates[1] - height / 2

    position = get_plane_coordinates(camera_transformation[:3, :3],
                                     camera_transformation[:3, 3],
                                     f,
                                     robot_px_coordinates[0],
                                     robot_px_coordinates[1],
                                     z=h)
    return position, yaw
