from ..select import leftmost
from ..select import rightmost
from ..select import bottommost
from ..select import topmost
from ..geometry import turn
from ..geometry import distance
import concurrent.futures
# from collections import OrderedDict

def _task(points, start, known):
    hull = []  #list of convex hull points
    candidate = None  # candiate point to add to CH
    i = 0  #index of last point in partial solution (ch)

    on_hull = start #last point added to the CH
                    # starting with known pt (leftmost)
    while True:
        hull.append(on_hull) #add candidate found last round to CH
        candidate = points[0]
        for point in points:
            if point == hull[i]:
                continue
            t = turn(hull[i], candidate, point)
            if (t < 0 or
                    (t == 0 and
                        distance(hull[i], point) > distance(hull[i], candidate))):
                candidate = point
        i += 1
        on_hull = candidate
        for k in known:
            if candidate[0] == k[0] and candidate[1] == k[1]:
                break
        else:
            continue
        break
    return hull

def ch(points, num_p=4):
    funcs = [leftmost, bottommost, rightmost, topmost]
    tie_break = [bottommost, rightmost, topmost, leftmost]
    min_sets = [f(points) for f in funcs]
    k = [f(m)[0] for f, m in list(zip(tie_break, min_sets))]
    collect = dict.fromkeys(k, [])
    known = list(collect)
    hull = []
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
