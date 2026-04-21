import numpy as np



def detectors_pos(image, angle, detectors, angle_range):
    """returns list of detectors positions for the given angle"""
    radians = np.deg2rad(angle)
    r = image.shape[0] * np.sqrt(2) / 2
    center = int(image.shape[0] / 2)
    theta = np.deg2rad(angle_range)

    positions = []

    #pierwszy det
    xd = int(r * np.cos(radians + np.pi - theta / 2)) + center
    yd = int(r * np.sin(radians + np.pi - theta / 2)) + center
    positions.append((xd, yd))

    #środkowe det
    for i in range(1, detectors - 1):
        xd = int(r * np.cos(radians + np.pi - theta / 2 + i * (theta / (detectors - 1)))) + center
        yd = int(r * np.sin(radians + np.pi - theta / 2 + i * (theta / (detectors - 1)))) + center
        positions.append((xd, yd))

    #ostatni det
    xd = int(r * np.cos(radians + np.pi + theta / 2)) + center
    yd = int(r * np.sin(radians + np.pi + theta / 2)) + center
    positions.append((xd, yd))

    return positions