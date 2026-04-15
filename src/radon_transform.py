import numpy as np
from src.bresenham import bresenham
from src.emiters import emitterPos
from src.detectors import detectorsPos


def get_sinogram(image, detectors_num, scans, span):
    sinogram = np.zeros((scans, detectors_num))
    height, width = image.shape
    delta_alpha = 360.0 / scans

    for i in range(scans):
        angle = i * delta_alpha

        xe, ye = emitterPos(image, angle)
        detectors_positions = detectorsPos(image, angle, detectors_num, span)

        for j, (xd, yd) in enumerate(detectors_positions):
            pixels = bresenham(xe, ye, xd, yd)
            line_sum = 0
            valid_pixels = 0

            for x, y in pixels:
                if 0 <= x < width and 0 <= y < height:
                    line_sum += image[y, x]
                    valid_pixels += 1

            if valid_pixels > 0:
                sinogram[i, j] = line_sum / valid_pixels

    return sinogram


def inverse_radon(sinogram, image_shape, detectors_num, scans, span):
    reconstructed = np.zeros(image_shape)
    hits = np.zeros(image_shape)
    height, width = image_shape
    delta_alpha = 360.0 / scans

    dummy_image = np.zeros(image_shape)

    for i in range(scans):
        angle = i * delta_alpha

        xe, ye = emitterPos(dummy_image, angle)
        detectors_positions = detectorsPos(dummy_image, angle, detectors_num, span)

        for j, (xd, yd) in enumerate(detectors_positions):
            pixels = bresenham(xe, ye, xd, yd)
            ray_value = sinogram[i, j]

            for x, y in pixels:
                if 0 <= x < width and 0 <= y < height:
                    reconstructed[y, x] += ray_value
                    hits[y, x] += 1

    hits[hits == 0] = 1
    reconstructed = reconstructed / hits

    if np.max(reconstructed) > 0:
        reconstructed = (reconstructed - np.min(reconstructed)) / (np.max(reconstructed) - np.min(reconstructed)) * 255

    return reconstructed