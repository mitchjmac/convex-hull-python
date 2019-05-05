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


def _task_split(points, pid, num_p, offset=0):
    if num_p > 1:
        if pid-offset < num_p/2:
            left = points[0:len(points)//2]
            return _task_split(left, pid, num_p/2, offset)
        else:
            right = points[len(points)//2:]
            return _task_split(right, pid, num_p/2, offset+(num_p/2))
    else:
        return (pid, _divide_conquer(points))


def _task_merge(left, right, pid):
    return (pid, _merge(left, right))


def ch(points, max_p=4):
    if len(points) <= 1:
        return points
    # Prep args
    points = sorted(points)
    num_p = 1 << (max_p.bit_length() - 1) # nearest power of 2 num processes
                                          #   leq max_p
    # Must run with at least num_p number of points
    while num_p > len(points):
        num_p //= 2

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_p) as executor:
        # Initial division of work between num_p processes
        # Will yield num_p sets of partially merged convex hulls
        mini_hulls = {executor.submit(_task_split, points, x, num_p):
                      x for x in range(num_p)}
        collect = dict.fromkeys(range(num_p), []) #dict to order subproblems
        for future in concurrent.futures.as_completed(mini_hulls):
            data = future.result()
            collect[data[0]] = data[1] #preserve order of convex hulls

        # Second division of work to merge the num_p partially merged hulls
        # Helpful to think of recursive tree:
        #   Initially, above, we had num_p processes, those results are merged
        #   by num_p/2 processes, and so on...
        # No easy way to chain futures through recursive calls, so simulating
        # the recursive tree
        merge_procs = [None] * (num_p - 1) #leaves-1 = num internal nodes
        to_merge = [None] * (num_p * 2 - 1) #store results after each merge
        # Get values from first division of work
        for k, v in collect.items():
            to_merge[k+num_p-1] = v
            # to_merge[v[0]] = v[1]
        # Spawn inital num_p/2 processes out of total num_p-1
        for x in range(num_p//2-1, num_p-1):
            merge_procs[x] = executor.submit(_task_merge, to_merge[2*x+1],
                                             to_merge[2*x+2], x)
        # Spawn the remaining processes
        while not to_merge[0]: #to_merge[0] is final result, so wait for it
            # Check for results from preceeding round of merges
            for p in merge_procs:
                #if children on tree are done executing
                if p and p.done() and not to_merge[p.result()[0]]:
                    to_merge[p.result()[0]] = p.result()[1]
            # Check if have both results from prior merge to start new merge
            for x in range(0,len(merge_procs)//2):
                if not merge_procs[x]: #if haven't already started process
                    if to_merge[2*x+1] and to_merge[2*x+2]:
                        merge_procs[x] = executor.submit(_task_merge,
                                                         to_merge[2*x+1],
                                                         to_merge[2*x+2], x)
    return to_merge[0]




