def bresenham(x1,y1,x2,y2):
    dir_x = 1 if x1 < x2 else -1
    dir_y = 1 if y1 < y2 else -1

    dx = abs(x1-x2)
    dy = abs(y1-y2)

    pixels = []
    D = 2 * dy + dx
    while True:
        pixels.append((x1, y1))
        if x1 == x2 and y1 == y2:
            return pixels
        if D > 0:
            y1 += dir_y
            D = D + 2 * (dy - dx)
        else:
            D = D + 2 * dy
        x1 += dir_x

