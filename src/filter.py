import numpy as np


def apply_filter(sinogram):
    """
    filtruje sinogram przy użyciu maski splotowej Ram-Lak
    """
    filtered_sinogram = np.zeros_like(sinogram)

    kernel_size = sinogram.shape[1]
    if kernel_size % 2 == 0:
        kernel_size -= 1

    center = kernel_size // 2
    kernel = np.zeros(kernel_size)

    # Filtr Ram-Lak
    for i in range(kernel_size):
        if i == center:
            kernel[i] = 1.0  # Główny, centralny pik
        elif (i - center) % 2 != 0:
            # Ujemne wartości gasnące z kwadratem odległości (tylko dla nieparzystych)
            kernel[i] = -4.0 / (np.pi ** 2 * (i - center) ** 2)

    pad_width = kernel_size // 2
    # Dla każdego wiersza sinogramu
    for i in range(sinogram.shape[0]):
        # Dopełnienie wartością brzegową lub zerami
        padded_row = np.pad(sinogram[i, :], pad_width, mode='edge')
        # Splot
        convolved = np.convolve(padded_row, kernel, mode='same')
        # Przycięcie do oryginalnego rozmiaru
        filtered_sinogram[i, :] = convolved[pad_width:-pad_width]

    return filtered_sinogram