from .context import convexhull
from convexhull import jarvis
from convexhull.pointset import PointSet
import os
import numpy as np

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# Tests for correct answers / errors in cases with low numbers of points
def low_points():
    in_points  = PointSet()
    correct    = PointSet()
    for i in range(0,4):
        inpath  = os.path.join(THIS_DIR, 'data/input/' + str(i) + 'p')
        outpath = os.path.join(THIS_DIR, 'data/output/' + str(i) + 'p')
        in_points.load(str(inpath))
        correct.load(str(outpath))
        seq_points = PointSet(jarvis.sequential(in_points.points))
        par_points = PointSet(jarvis.parallel(in_points.points))

        print(correct.compare(seq_points))
        print(correct.compare(par_points))


# Tests for correct answers / errors in cases with large numbers of points
def high_points():
    in_points  = PointSet()
    correct    = PointSet()

    for i in np.logspace(1,6,num=6-1+1,base=10,dtype='int'):
        inpath  = os.path.join(THIS_DIR, 'data/input/' + str(i) + 'p')
        outpath = os.path.join(THIS_DIR, 'data/output/' + str(i) + 'p')
        in_points.load(str(inpath))
        correct.load(str(outpath))
        seq_points = PointSet(jarvis.sequential(in_points.points))
        par_points = PointSet(jarvis.parallel(in_points.points))

        print(correct.compare(seq_points))
        print(correct.compare(par_points))


def test_time():
    in_points  = PointSet()
    for i in np.logspace(1,6,num=6-1+1,base=10,dtype='int'):
        inpath  = os.path.join(THIS_DIR, 'data/input/' + str(i) + 'p')
        in_points.load(str(inpath))
        start = timer()
        seq_points = PointSet(jarvis.sequential(in_points.points))
        end = timer()
        print(end - start)
        start = timer()
        end = timer()
        print(end - start)
        par_points = PointSet(jarvis.parallel(in_points.points))
        start = timer()
        end = timer()
        print(end - start)
