from ..select import leftmost
from ..select import bottommost
from ..geometry import turn
from ..geometry import distance

def ch(points):
    """Finds the convex hull of a set of points.

    Find the convex hull of a set of points using Jarvis March. The set of
    points only includes the extreme points and points are ordered from the
    leftmost point (lowest x) then counterclockwise.

    Args:
        points (list): The input set of poitns to find the convex hull of

    Returns:
        list: The convex hull of the set of points
    """
    hull = []  #list of convex hull points
    candidate = None  #candiate point to add to CH
    i = 0  #index of last point in partial solution (ch)

    lm = leftmost(points)  #last point added to the CH
                            # starting with known pt (leftmost)
    on_hull = bottommost(lm)[0]

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
        if candidate[0] == hull[0][0] and candidate[1] == hull[0][1]:
            break
    return hull
