import numpy as np


def apply_filter(sinogram):
    """
    Filtruje sinogram przy użyciu precyzyjnej maski splotowej (Ram-Lak).
    """
    filtered_sinogram = np.zeros_like(sinogram)

    kernel_size = sinogram.shape[1]
    if kernel_size % 2 == 0:
        kernel_size -= 1

    center = kernel_size // 2
    kernel = np.zeros(kernel_size)

    # Generowanie matematycznego filtru Ram-Lak
    for i in range(kernel_size):
        if i == center:
            kernel[i] = 1.0  # Główny, centralny pik
        elif (i - center) % 2 != 0:
            # Ujemne wartości gasnące z kwadratem odległości (tylko dla nieparzystych)
            kernel[i] = -4.0 / (np.pi ** 2 * (i - center) ** 2)
        else:
            kernel[i] = 0.0  # Zera dla odległości parzystych

    # Wykonanie właściwego splotu na każdym wierszu sinogramu
    for i in range(sinogram.shape[0]):
        filtered_sinogram[i, :] = np.convolve(sinogram[i, :], kernel, mode='same')

    return filtered_sinogram