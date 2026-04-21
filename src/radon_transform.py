import numpy as np
from src.bresenham import bresenham
from src.emiters import emitter_pos
from src.detectors import detectors_pos


def get_sinogram(image, detectors_num, scans, span):
    """returns sinogram of image"""
    sinogram = np.zeros((scans, detectors_num)) #Początkowo pusty
    height, width = image.shape
    delta_alpha = 360.0 / scans #Długość kroku układu emiter detektory

    #Iteracja po wszystkich kątach
    for i in range(scans):
        angle = i * delta_alpha #Aktualny kąt

        #Pozycje emitera i detektorów
        xe, ye = emitter_pos(image, angle)
        detectors_positions = detectors_pos(image, angle, detectors_num, span)

        #Iteracja po detektorach
        for j, (xd, yd) in enumerate(detectors_positions):
            pixels = bresenham(xe, ye, xd, yd)
            line_sum = 0 #Suma intensywności promienia

            #Sumowanie wartości pikseli wzdłuź promienia
            for x, y in pixels:
                if 0 <= x < width and 0 <= y < height:
                    line_sum += image[y, x]

            #Normalizacja
            dx = abs(xd - xe)
            dy = abs(yd - ye)

            #Korekcja dyskretnej reprezentacji promienia
            length_factor = np.sqrt(dx ** 2 + dy ** 2) / max(dx, dy) if max(dx, dy) > 0 else 1.0

            center = width / 2.0
            #Wektory promienia
            v_cx, v_cy = center - xe, center - ye
            v_rx, v_ry = xd - xe, yd - ye

            #Długości wektorów
            len_c = np.sqrt(v_cx ** 2 + v_cy ** 2)
            len_r = np.sqrt(v_rx ** 2 + v_ry ** 2)

            #Domyślnie brak korekty kąta
            cos_gamma = 1.0
            if len_c > 0 and len_r > 0:
                # Iloczyn skalarny do wyliczenia kąta między wektorami
                cos_gamma = (v_cx * v_rx + v_cy * v_ry) / (len_c * len_r)

            #Zapis do sinogramu
            sinogram[i, j] = line_sum * length_factor * cos_gamma

    return sinogram


def inverse_radon(sinogram, image_shape, detectors_num, scans, span, return_history=False):
    """returns reconstructed image from sinogram"""
    height, width = image_shape
    reconstructed = np.zeros(image_shape) #Obraz zrekonstruowany początkowo pusty
    hits = np.zeros(image_shape) #Licznik trafień w piksel
    delta_alpha = 360.0 / scans #Krok układu

    #Jeżeli chcemy historię rekonstrukcji
    if return_history:
        history = np.zeros((scans, height, width))

    #Sztuczny obraz do wyznaczania geometrii
    dummy_image = np.zeros(image_shape)

    #Iteracja po kątach
    for i in range(scans):
        angle = i * delta_alpha

        xe, ye = emitter_pos(dummy_image, angle)
        detectors_positions = detectors_pos(dummy_image, angle, detectors_num, span)

        for j, (xd, yd) in enumerate(detectors_positions):
            pixels = bresenham(xe, ye, xd, yd)

            ray_value = sinogram[i, j] #Wartość promienia z sinogramu

            #Wsteczna projekcja
            for x, y in pixels:
                if 0 <= x < width and 0 <= y < height:
                    reconstructed[y, x] += ray_value
                    hits[y, x] += 1

        #Zapis historii
        if return_history:
            temp_hits = hits.copy()
            temp_hits[temp_hits == 0] = 1 #Bez dzielenia przez zero
            history[i] = reconstructed.copy() / temp_hits

    if return_history:
        #Usuwanie wartości ujemnych
        history = np.clip(history, 0, None)

        #Normalizacja
        for k in range(scans):
            #Usuwanie pikseli z małą liczbą trafień, powodujących szum
            history[k][hits < (scans * 0.05)] = 0.0
            #Usuwanie zbyt odstających pikseli
            p_max = np.percentile(history[k], 99.5)
            if p_max > 0:
                history[k] = (history[k] / p_max) * 255

        # Docinamy pojedyncze, odstające piksele, które po podzieleniu przez p_max przekroczyły 255
        history = np.clip(history, 0, 255)

        return history
    else:
        hits[hits == 0] = 1
        reconstructed = reconstructed / hits

        reconstructed = np.clip(reconstructed, 0, None)

        p_max = np.percentile(reconstructed, 99.5)

        if p_max > 0:
            reconstructed = (reconstructed / p_max) * 255

        reconstructed = np.clip(reconstructed, 0, 255)
        return reconstructed

