import numpy as np
from src.bresenham import bresenham
from src.emiters import emitter_pos
from src.detectors import detectors_pos


def get_sinogram(image, detectors_num, scans, span):
    sinogram = np.zeros((scans, detectors_num))
    height, width = image.shape
    delta_alpha = 360.0 / scans

    for i in range(scans):
        angle = i * delta_alpha

        xe, ye = emitter_pos(image, angle)
        detectors_positions = detectors_pos(image, angle, detectors_num, span)

        for j, (xd, yd) in enumerate(detectors_positions):
            pixels = bresenham(xe, ye, xd, yd)
            line_sum = 0
            valid_pixels = 0

            for x, y in pixels:
                if 0 <= x < width and 0 <= y < height:
                    line_sum += image[y, x]
                    #valid_pixels += 1

            # if valid_pixels > 0:
            #     sinogram[i, j] = line_sum / valid_pixels

            sinogram[i, j] = line_sum

    return sinogram


def inverse_radon(sinogram, image_shape, detectors_num, scans, span, return_history=False):
    height, width = image_shape
    reconstructed = np.zeros(image_shape)
    hits = np.zeros(image_shape)
    delta_alpha = 360.0 / scans

    if return_history:
        history = np.zeros((scans, height, width))

    dummy_image = np.zeros(image_shape)

    for i in range(scans):
        angle = i * delta_alpha

        xe, ye = emitter_pos(dummy_image, angle)
        detectors_positions = detectors_pos(dummy_image, angle, detectors_num, span)

        for j, (xd, yd) in enumerate(detectors_positions):
            pixels = bresenham(xe, ye, xd, yd)
            ray_value = sinogram[i, j]

            for x, y in pixels:
                if 0 <= x < width and 0 <= y < height:
                    reconstructed[y, x] += ray_value
                    hits[y, x] += 1

        if return_history:
            # temp_hits = hits.copy()
            # temp_hits[temp_hits == 0] = 1
            history[i] = reconstructed.copy() #/ temp_hits

    if return_history:
        #global_min = np.min(history)
        history = np.clip(history, 0, None)
        # global_max = np.max(history)
        #
        # if global_max > 0:
        #     history = (history / global_max) * 255

        p_max = np.percentile(history, 99.5)

        if p_max > 0:
            history = (history / p_max) * 255

        # Docinamy pojedyncze, odstające piksele, które po podzieleniu przez p_max przekroczyły 255
        history = np.clip(history, 0, 255)

        return history
    else:
        # hits[hits == 0] = 1
        # reconstructed = reconstructed / hits


        # reconstructed = np.clip(reconstructed, 0, None)
        # if np.max(reconstructed) > 0:
        #     reconstructed = (reconstructed  / np.max(reconstructed)) * 255
        # return reconstructed

        reconstructed = np.clip(reconstructed, 0, None)

        p_max = np.percentile(reconstructed, 99.5)

        if p_max > 0:
            reconstructed = (reconstructed / p_max) * 255

        reconstructed = np.clip(reconstructed, 0, 255)
        return reconstructed
