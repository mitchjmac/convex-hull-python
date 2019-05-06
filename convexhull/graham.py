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


def _task_run(points, pid):
    return (pid, _graham(points))



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
    hull  = []
    points = sorted(points)

    # Spawn one process to find the upper and one to find the lower
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        half_hulls = {executor.submit(_task_run, x[0], x[1]):
                      x for x in zip([points,reversed(points)], range(2))}
        collect = dict.fromkeys(range(2), []) #dict to order subproblems
        for future in concurrent.futures.as_completed(half_hulls):
            data = future.result()
            collect[data[0]] = data[1]
        # Merge the upper and lower hulls
        for v in collect.values():
            hull.extend(v[:-1])

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
