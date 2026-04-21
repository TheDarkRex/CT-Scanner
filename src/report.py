import numpy as np
import matplotlib.pyplot as plt
from radon_transform import get_sinogram, inverse_radon
from rmse import calculate_rmse



def get_rmse(image, detectors, scans, spans) -> list:
    results = []

    for detector in detectors:
        for scan in scans:
            for span in spans:
                sinogram = get_sinogram(image, detector, scan, span)
                reconstruction = inverse_radon(sinogram, image.shape, detector, scan, span, return_history=False)
                rmse = calculate_rmse(image, reconstruction)

                results.append(rmse)

    return results



def main():
    path = "../data/input/Shepp_logan.jpg"
    image = plt.imread(path)
    if len(image.shape) == 3:
        image = image[:, :, 0]
    image = image.astype(np.float64)

    # Zmienna liczba detektorów
    print(f"Zmienna liczba detektorów")
    detectors = [x for x in range(90, 810, 90)]
    results_det = get_rmse(image, detectors, [180], [180])

    for detector, result in zip(detectors, results_det):
        print(f"Liczba detektorów: {detector} -> RMSE: {result}")

    # Zmienna liczba skanów
    print(f"Zmienna liczba skanów")
    scans = [x for x in range(90, 810, 90)]
    results_scans = get_rmse(image, [180], scans, [180])

    for scan, result in zip(scans, results_scans):
        print(f"Liczba skanów: {scan} -> RMSE: {result}")

    # Zmienna rozpiętość wachlarza
    print(f"Zmienna rozpiętość wachlarza")
    spans = [x for x in range(45, 315, 45)]
    results_spans = get_rmse(image, [180], [180], spans)

    for span, result in zip(spans, results_spans):
        print(f"Rozpiętość wachlarza: {span} -> RMSE: {result}")

    # Wykres 1: Detektory
    plt.figure(figsize=(8, 6))
    plt.plot(detectors, results_det, marker='o', linestyle='-', color='blue')
    plt.title('Wpływ liczby detektorów na RMSE')
    plt.xlabel('Liczba detektorów')
    plt.ylabel('RMSE')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("wykres_rmse_detektory.png", dpi=300, bbox_inches='tight')

    # Wykres 2: Skany
    plt.figure(figsize=(8, 6))
    plt.plot(scans, results_scans, marker='o', linestyle='-', color='green')
    plt.title('Wpływ liczby skanów na RMSE')
    plt.xlabel('Liczba skanów')
    plt.ylabel('RMSE')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("wykres_rmse_skany.png", dpi=300, bbox_inches='tight')

    # Wykres 3: Rozpiętość wachlarza
    plt.figure(figsize=(8, 6))
    plt.plot(spans, results_spans, marker='o', linestyle='-', color='red')
    plt.title('Wpływ rozpiętości wachlarza na RMSE')
    plt.xlabel('Rozpiętość wachlarza (stopnie)')
    plt.ylabel('RMSE')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("wykres_rmse_wachlarz.png", dpi=300, bbox_inches='tight')

    plt.show()


if __name__ == "__main__":
    main()