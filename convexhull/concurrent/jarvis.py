from ..select import leftmost
from ..select import rightmost
from ..select import bottommost
from ..select import topmost
from ..geometry import turn
from ..geometry import distance
import concurrent.futures
from collections import OrderedDict

def _task(points, start, known):
    ch = []  #list of convex hull points
    candidate = None  # candiate point to add to CH
    i = 0  #index of last point in partial solution (ch)

    on_hull = start #last point added to the CH
                    # starting with known pt (leftmost)
    while True:
        ch.append(on_hull) #add candidate found last round to CH
        candidate = points[0]
        for point in points:
            if point == ch[i]:
                continue
            t = turn(ch[i], point, candidate)
            if (t < 1 or
                    (t == 0 and
                        distance(ch[i], point) > distance(ch[i], candidate))):
                candidate = point
        i += 1
        on_hull = candidate
        for k in known:
            if candidate[0] == k[0] and candidate[1] == k[1]:
                break
        else:
            continue
        break
    return ch


def jarvis(points, num_p=4):
    collect = {}
    ch = []
    funcs = [leftmost, bottommost, rightmost, topmost]
    known = list(dict.fromkeys([f(points) for f in funcs]))
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_p) as executor:
        hull_part = {executor.submit(_task, points, k, known): k for k in known}
        for k in known:
            collect[k] = []
        for future in concurrent.futures.as_completed(hull_part):
            data = future.result()
            collect[data[0]] = data
    for v in collect.values():
        ch.extend(v)
    return ch
