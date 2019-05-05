from ..select import leftmost
from ..select import rightmost
from ..select import bottommost
from ..select import topmost
from ..geometry import turn
from ..geometry import distance
import math
import concurrent.futures

def _merge(l, r):
    ret = []
    # Base case to merge 2 points, lowest y-coord first
    if len(l) == 1 and len(r) == 1:
        if l[0][1] < r[0][1]:
            ret.extend(l)
            ret.extend(r)
        else:
            ret.extend(r)
            ret.extend(l)
        return ret

    # Maintain order of sub hulls: start leftmost element -> counterclockwise
    while len(l) > 1 and l[0][0] > l[1][0]:
        rotate = l.pop(0)
        l.append(rotate)

    # Initialize variables used to find upper and lower tangents
    p = rightmost(l)         # set of points with rightmost x in left hull
    q = leftmost(r)          # set of points with leftmost x in right hull
    p_upp = topmost(p)[0]    # tie breakers in case of collinear points
    p_low = bottommost(p)[0]
    q_upp = topmost(q)[0]
    q_low = bottommost(q)[0]
    p_upp_i = l.index(p_upp) # index of the points on upper and lower tangents
    p_low_i = l.index(p_low)
    q_upp_i = r.index(q_upp)
    q_low_i = r.index(q_low)

    # computer upper tangent
    while True:
        p_prev = p_upp
        q_prev = q_upp
        # q_upp clockwise while left turn
        while True:
            cw_i = (q_upp_i-1) % len(r) # modulus to wrap around list
            t = turn(p_upp, q_upp, r[cw_i]) # z of cross product
            if ((t > 0) or #left turn
                    (t == 0 and #collinear points -> pick farthest point
                        distance(p_upp, r[cw_i]) > distance(p_upp, q_upp))):
                q_upp_i = cw_i
                q_upp = r[cw_i]
            else:
                break
        # p_upp counterclockwise while right turn
        while True:
            ccw_i = (p_upp_i+1) % len(l)
            t = turn(q_upp, p_upp, l[ccw_i])
            if ((t < 0) or #right turn
                    (t == 0 and
                        distance(q_upp, l[ccw_i]) > distance(q_upp, p_upp))):
                p_upp_i = ccw_i
                p_upp = l[ccw_i]
            else:
                break
        # if no tangents changed
        if p_upp == p_prev and q_upp == q_prev:
            break

    # computer lower tangent
    while True:
        p_prev = p_low
        q_prev = q_low
        # q_low counterclockwise while right turn
        while True:
            ccw_i = (q_low_i+1) % len(r)
            t = turn(p_low, q_low, r[ccw_i])
            if ((t < 0) or
                    (t == 0 and
                        distance(p_low, r[ccw_i]) > distance(p_low, q_low))):
                q_low_i = ccw_i
                q_low = r[ccw_i]
            else:
                break
        # p_low clockwise while left turn
        while True:
            cw_i = (p_low_i-1) % len(l)
            t = turn(q_low, p_low, l[cw_i])
            if ((t > 0) or
                    (t == 0 and
                        distance(q_low, l[cw_i]) > distance(q_low, p_low))):
                p_low_i = cw_i
                p_low = l[cw_i]
            else:
                break
        # if no tangents changed
        if p_low == p_prev and q_low == q_prev:
            break

    # Merge new hulls using found tangents
    ret.extend(l[0:p_low_i+1]) # append from leftmost in l hull until p_low ccw
    if q_upp_i < q_low_i: # handle case of index wraparound in *q* b/c modulus
        ret.extend(r[q_low_i:len(r)]) # essentially same as normal case below
        ret.extend(r[0:q_upp_i+1])    #  but the list representation is askew
    else: # no wraparound occured / normal case
        ret.extend(r[q_low_i:q_upp_i+1]) # append around right side of hull r
                                         #  ccw between tangent points
    if not p_low_i == p_upp_i: # filter case of single point in p
        if p_upp_i > p_low_i: # if no index wraparound in *p*
            ret.extend(l[p_upp_i:len(l)]) # append ccw from p_upp to l[0]

    return ret


def _divide_conquer(points):
    if len(points) == 1:
        return points
    left = _divide_conquer(points[:len(points)//2])
    right = _divide_conquer(points[len(points)//2:])
    return _merge(left, right)


def ch(points):
    if len(points) <= 1:
        return points
    points = sorted(points)
    return _divide_conquer(points)
