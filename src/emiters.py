import numpy as np
from PIL import Image


def emitterPos(image, angle):
    """returns emitters position for the given angle"""
    radians = np.deg2rad(angle)
    r = image.shape[0] * np.sqrt(2) / 2
    center = int(image.shape[0] / 2)
    xe = int(r * np.cos(radians)) + center
    ye = int(r * np.sin(radians)) + center
    return xe, ye