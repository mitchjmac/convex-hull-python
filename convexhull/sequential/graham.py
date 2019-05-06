from ..geometry import turn

def ch(points):
    """Finds the convex hull of a set of points

    Uses Graham Scan / Monotone Chaining to find the convex hull of a set of
    points. The set of points only includes the extreme points and points are
    ordered from the leftmost point (lowest x) then counterclockwise.

    Args:
        points (list): The set of points to find the convex hull of

    Returns:
        list: The convex hull of the points
    """
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
    # Merge lower hull into result
    hull.extend(lower[:-1])

    # Upper hull
    for p in reversed(points):
        # While makes right turn or collinear
        while len(upper) >= 2 and turn(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    # Merge lower hull into result
    hull.extend(upper[:-1])

    return hull
