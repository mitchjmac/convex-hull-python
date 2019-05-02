def leftmost(points):
    p = min(points, key = lambda point: point[0])
    return p

def rightmost(points):
    p = max(points, key = lambda point: point[0])
    return p

def bottommost(points):
    p = min(points, key = lambda point: point[1])
    return p

def topmost(points):
    p = max(points, key = lambda point: point[1])
    return p
