import cv2
import numpy as np
from math import sin, cos, pi, sqrt
import itertools


def rotx(angle):
    """ Returns a rotation matrix for the given angle about the X axis """
    return np.array(((1, 0, 0, 0),
                     (0, cos(angle), -sin(angle), 0),
                     (0, sin(angle), cos(angle), 0),
                     (0, 0, 0, 1)))


def roty(angle):
    """ Returns a rotation matrix for the given angle about the X axis """
    return np.array(((cos(angle), 0, sin(angle), 0),
                     (0, 1, 0, 0),
                     (-sin(angle), 0, cos(angle), 0),
                     (0, 0, 0, 1)))


def rotz(angle):
    """ Returns a rotation matrix for the given angle about the X axis """
    return np.array(((cos(angle), -sin(angle), 0, 0),
                     (sin(angle), cos(angle), 0, 0),
                     (0, 0, 1, 0),
                     (0, 0, 0, 1)))


def translate(translation):
    """ Returns a translation matrix for the given offset """
    x, y, z = translation
    return np.array(((1, 0, 0, x),
                     (0, 1, 0, y),
                     (0, 0, 1, z),
                     (0, 0, 0, 1)))


def get_plane_coordinates(camera_rotation, camera_position, f, x, y, z=0):
    direction = camera_rotation.dot(np.array([x, y, f]) / f)
    world_pos = camera_position - direction * ((camera_position[2]-z) / direction[2])
    return world_pos


def render(image, position, camera, f, color=(0,0,255)):
    height, width, _  = image.shape
    pos = np.ones(4)
    pos[:3] = position
    projected = np.linalg.inv(camera).dot(pos)
    projected = projected/projected[2] * f
    cv2.circle(image, (int(projected[0] + width/2), int(projected[1]+height/2)), 10, color, 3)
