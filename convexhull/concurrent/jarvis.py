from ..select import leftmost
from ..select import rightmost
from ..select import bottommost
from ..select import topmost
from ..geometry import turn
from ..geometry import distance
import concurrent.futures

def _task(points, start, known):
    """Runs Jarvis March to find a portion of the convex hull of a set of points

    This function is called from a subprocess. Finds the portion of a convex
    hull of the input set of points between start and the first encountered
    point in known.

    Args:
        points (list): Input set of point to find convex hull of
        start ((float, float)): The starting point
        known (list): Known points on convex hull to stop serching at (where
        another process started at)

    Returns:
        list: The partial convex hull of the set of points
    """
    hull = []  #list of convex hull points
    candidate = None  # candiate point to add to CH
    i = 0  #index of last point in partial solution (ch)

    on_hull = start #last point added to the CH
                    # starting with known pt (leftmost)
    while True:
        hull.append(on_hull) # add candidate found last round to CH
        candidate = points[0]
        for point in points:
            if point == hull[i]:
                continue
            t = turn(hull[i], candidate, point)
            if (t < 0 or # if left turn
                    (t == 0 and # if collinear and farther points
                        distance(hull[i], point) > distance(hull[i], candidate))):
                candidate = point
        i += 1
        on_hull = candidate
        # Return when encounter the first point in known
        for k in known:
            if candidate[0] == k[0] and candidate[1] == k[1]:
                break
        else:
            continue
        break
    return hull

def ch(points, num_p=4):
    """Finds the convex hull of a set of points.

    Find the convex hull of a set of points. Uses 2-4 processes to find portions
    of the convex hull in parallel. Finds 2-4 known points on the hull and then
    starts processes to scan counterclocwise. The set of points only includes
    the extreme points and points are ordered from the leftmost point (lowest x)
    then counterclockwise.

    Args:
        points (list): The input set of poitns to find the convex hull of
        num_p (int, optional): Tme max number of subprocesses to spawn

    Returns:
        list: The convex hull of the set of points
    """
    funcs = [leftmost, bottommost, rightmost, topmost]
    tie_break = [bottommost, rightmost, topmost, leftmost]
    # Find set of points farthest to the bottom, right, top, left
    min_sets = [f(points) for f in funcs]
    # Tiebreak for collinear points
    k = [f(m)[0] for f, m in list(zip(tie_break, min_sets))]
    collect = dict.fromkeys(k, []) # dict used to order results from processes
    known = list(collect)
    hull = []
    # For each point in the known points on the hull spawn processes
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_p) as executor:
        hull_part = {executor.submit(_task, points, k, known): k for k in known}
        for k in known:
            collect[k] = []
        for future in concurrent.futures.as_completed(hull_part):
            data = future.result()
            collect[data[0]] = data
    for v in collect.values():
        hull.extend(v)
    return hull
