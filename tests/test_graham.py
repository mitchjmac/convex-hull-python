from .context import convexhull
from convexhull import graham
from convexhull.pointset import PointSet
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# Low number of points
def low_points():
    in_points  = PointSet()
    correct    = PointSet()
    for i in range(0,4):
        inpath  = os.path.join(THIS_DIR, 'data/input/' + str(i) + 'p')
        outpath = os.path.join(THIS_DIR, 'data/output/' + str(i) + 'p')
        in_points.load(str(inpath))
        correct.load(str(outpath))
        seq_points = PointSet(graham.sequential(in_points.points))
        par_points = PointSet(graham.parallel(in_points.points))

        print(correct.compare(seq_points))
        print(correct.compare(par_points))
