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
