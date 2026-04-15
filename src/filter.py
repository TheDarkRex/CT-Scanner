import numpy as np


def apply_filter(sinogram):
    filtered_sinogram = np.zeros_like(sinogram)
    kernel = np.array([-0.125, -0.25, 0.75, -0.25, -0.125])

    for i in range(sinogram.shape[0]):
        filtered_sinogram[i, :] = np.convolve(sinogram[i, :], kernel, mode='same')

    filtered_sinogram = np.clip(filtered_sinogram, 0, None)
    return filtered_sinogram