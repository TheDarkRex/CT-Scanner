def bresenham(x1: int, y1: int, x2: int, y2: int) -> list:
    """Zwraca listę pikseli tworzących linię między (x1, y1) a (x2, y2)."""
    pixels = []

    # Obliczanie różnic bezwzględnych
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    # Ustalanie kierunku kroku
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    # Inicjalizacja błędu
    err = dx - dy

    while True:
        pixels.append((x1, y1))

        # Warunek zakończenia: dotarcie do punktu docelowego
        if x1 == x2 and y1 == y2:
            break

        # Podwojony błąd (eliminacja operacji zmiennoprzecinkowych)
        e2 = 2 * err

        # Korekta w osi X
        if e2 > -dy:
            err -= dy
            x1 += sx

        # Korekta w osi Y
        if e2 < dx:
            err += dx
            y1 += sy

    return pixels