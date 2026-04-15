def bresenham(x1, y1, x2, y2):
    """returns list of pixels contributing to line between (x1, y1) and (x2, y2)"""
    dir_x = 1 if x2 >= x1 else -1
    dir_y = 1 if y2 >= y1 else -1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    pixels = [(x1, y1)]
    if dx < dy:
        e = dy / 2
        for _ in range(dy):
            y1 += dir_y
            e -= dx
            if e < 0:
                x1 += dir_x
                e += dy
            pixels.append((x1, y1))
    else:
        e = dx / 2
        for _ in range(dx):
            x1 += dir_x
            e -= dy
            if e < 0:
                y1 += dir_y
                e += dx
            pixels.append((x1, y1))

    return pixels