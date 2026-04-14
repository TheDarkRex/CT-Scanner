def bresenham(x0, y0, x1, y1):
    dx = x0 - x1
    dy = y0 - y1

    pixels = []
    D = 2 * dy + dx
    while True:
        pixels.append((x0, y0))
        if x0 == x1 and y0 == y1:
            return pixels
        if D > 0:
            y0 += 1
            D = D + 2 * (dy - dx)
        else:
            D = D + 2 * dy
        x1 += 1

