from ..geometry import turn
import concurrent.futures

def _task(points):
    hull = []
    for p in points:
        # While makes right turn or collinear
        while len(hull) >= 2 and turn(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)
    return hull

def ch(points):
    if len(points) <= 1:
        return points
    lower = []
    upper = []
    hull  = []
    points = sorted(points)

    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        l = {executor.submit(_task, points)}
        u = {executor.submit(_task, reversed(points))}
        for future in concurrent.futures.as_completed(l):
            lower = future.result()
        for future in concurrent.futures.as_completed(u):
            upper = future.result()

    hull.extend(lower[:-1])
    hull.extend(upper[:-1])

    return hull
