import numpy as np
from PIL import Image

def bresenham(x1, y1, x2, y2):
    """returns list of pixels contributing to line between (x1, y1) and (x2, y2)"""
    dir_x = 1 if x2 >= x1 else -1
    dir_y = 1 if y2 >= y1 else -1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    pixels = [(x1, y1)]
    if dx < dy:
        e = dy / 2
        for _ in range(dy):
            y1 += dir_y
            e -= dx
            if e < 0:
                x1 += dir_x
                e += dy
            pixels.append((x1, y1))
    else:
        e = dx / 2
        for _ in range(dx):
            x1 += dir_x
            e -= dy
            if e < 0:
                y1 += dir_y
                e += dx
            pixels.append((x1, y1))

    return pixels

def emitterPos(image, angle):
    """returns emitters position for the given angle"""
    radians = np.deg2rad(angle)
    r = img.shape[0] * np.sqrt(2) / 2
    center = int(img.shape[0] / 2)
    xe = int(r * np.cos(radians)) + center
    ye = int(r * np.sin(radians)) + center
    return xe, ye

def detectorsPos(image, angle, detectors, angle_range):
    """returns list of detectors positions for the given angle"""
    radians = np.deg2rad(angle)
    r = img.shape[0] * np.sqrt(2) / 2
    center = int(img.shape[0] / 2)
    theta = np.deg2rad(angle_range * 2)

    positions = []
    xd = int(r * np.cos(radians + np.pi - theta / 2)) + center
    yd = int(r * np.sin(radians + np.pi - theta / 2)) + center
    positions.append((xd, yd))

    for i in range(1, detectors - 1):
        xd = int(r * np.cos(radians + np.pi - theta / 2 + i * (theta / (detectors - 1)))) + center
        yd = int(r * np.sin(radians + np.pi - theta / 2 + i * (theta / (detectors - 1)))) + center
        positions.append((xd, yd))

    xd = int(r * np.cos(radians + np.pi + theta / 2)) + center
    yd = int(r * np.sin(radians + np.pi + theta / 2)) + center
    positions.append((xd, yd))
    return positions

image = Image.open("Kolo.jpg").convert("L")
img = np.array(image)

print(img.shape)
print(detectorsPos(img, 30, 10, 45))