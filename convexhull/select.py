def leftmost(points):
    m = min(points, key = lambda point: point[0])[0]
    return [p for p in points if p[0] == m]

def rightmost(points):
    m = max(points, key = lambda point: point[0])[0]
    return [p for p in points if p[0] == m]

def bottommost(points):
    m = min(points, key = lambda point: point[1])[1]
    return [p for p in points if p[1] == m]

def topmost(points):
    m = max(points, key = lambda point: point[1])[1]
    return [p for p in points if p[1] == m]
