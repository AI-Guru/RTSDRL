import math
import numpy as np

def vector_from_angle_and_length(angle, length):
    vector = (length * math.sin(angle), length * math.cos(angle))
    vector = np.array(vector)
    return vector


def polar_coordinates(x, y):
    angle = math.atan2(x, y)
    if angle < 0.0:
        angle += 2.0 * math.pi
    length = math.sqrt(x**2 + y**2)
    return angle, length


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
