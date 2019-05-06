from .geometry import turn
import concurrent.futures

def _graham(points):
    """Finds upper or lower hull of the convex hull of a set of points

    Uses Graham Scan / Monotone Chaining to find either the upper or lower hull
    of the covex hull of a set of points.

    Args:
        points (list): The set of points to find the convex hull of

    Returns:
        list: The convex hull of the input points
    """
    hull = []
    for p in points:
        # While makes right turn or collinear
        while len(hull) >= 2 and turn(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)
    return hull

def parallel(points):
    """Finds the convex hull of a set of points

    Uses Graham Scan / Monotone Chaining to find the convex hull of a set of
    points. Uses two processes to find the upper and lower hulls in parallel.
    The set of points only includes the extreme points and points are ordered
    from the leftmost point (lowest x) then counterclockwise.

    Args:
        points (list): The set of points to find the convex hull of

    Returns:
        list: The convex hull of the points
    """
    if len(points) <= 1:
        return points
    lower = []
    upper = []
    hull  = []
    points = sorted(points)

    # Spawn one process to find the upper and one to find the lower
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        l = {executor.submit(_graham, points)}
        u = {executor.submit(_graham, reversed(points))}
        for future in concurrent.futures.as_completed(l):
            lower = future.result()
        for future in concurrent.futures.as_completed(u):
            upper = future.result()

    # Emrge the upper and lower hulls
    hull.extend(lower[:-1])
    hull.extend(upper[:-1])

    return hull

def sequential(points):
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

    hull  = []
    lower = _graham(points)
    upper = _graham(reversed(points))

    hull.extend(lower[:-1]) # Merge lower hull into result
    hull.extend(upper[:-1]) # Merge upper hull into result

    return hull
