from .context import convexhull
from convexhull import dc
from convexhull.pointset import PointSet
import os
import numpy as np
from timeit import default_timer as timer

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
        seq_points = PointSet(dc.sequential(in_points.points))
        par_points = PointSet(dc.parallel(in_points.points))

        print(correct.compare(seq_points))
        print(correct.compare(par_points))

# Tests for correct answers / errors in cases with large numbers of points
def high_points(num_p):
    in_points  = PointSet()
    correct    = PointSet()

    for i in np.logspace(1,6,num=6-1+1,base=10,dtype='int'):
        inpath  = os.path.join(THIS_DIR, 'data/input/' + str(i) + 'p')
        outpath = os.path.join(THIS_DIR, 'data/output/' + str(i) + 'p')
        in_points.load(str(inpath))
        correct.load(str(outpath))
        seq_points = PointSet(dc.sequential(in_points.points))
        par_points = PointSet(dc.parallel(in_points.points, num_p))

        print(correct.compare(seq_points))
        print(correct.compare(par_points))


def test_time(num_p):
    in_points  = PointSet()
    for i in np.logspace(1,6,num=6-1+1,base=10,dtype='int'):
        inpath  = os.path.join(THIS_DIR, 'data/input/' + str(i) + 'p')
        in_points.load(str(inpath))
        # Sequential
        start = timer()
        seq_points = PointSet(dc.sequential(in_points.points))
        end = timer()
        print(end - start)
        # Concurrent
        start = timer()
        par_points = PointSet(dc.parallel(in_points.points, num_p))
        end = timer()
        print(end - start)
