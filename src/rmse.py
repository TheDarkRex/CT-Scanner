import numpy as np


def calculate_rmse(original_image, reconstructed_image):
    """Calculates the root mean squared error (RMSE) between two images"""
    orig_norm = original_image.astype(np.float32) / 255.0
    rec_norm = reconstructed_image.astype(np.float32) / 255.0

    mse = np.mean((orig_norm - rec_norm) ** 2)
    rmse = np.sqrt(mse)
    return rmse