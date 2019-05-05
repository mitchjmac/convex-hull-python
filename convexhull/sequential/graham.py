from ..geometry import turn

def ch(points):
    if len(points) <= 1:
        return points
    points = sorted(points)

    lower = []
    upper = []
    hull  = []

    # Lower hull
    for p in points:
        # While makes right turn or collinear
        while len(lower) >= 2 and turn(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    hull.extend(lower[:-1])

    # Upper hull
    for p in reversed(points):
        # While makes right turn or collinear
        while len(upper) >= 2 and turn(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    hull.extend(upper[:-1])

    return hull
