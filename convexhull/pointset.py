import pickle
import numpy as np
from collections import OrderedDict

class PointSet:

    def __init__(self, pts=[]):
        self.points  = pts

    def generate(self, size):
        x = np.round_(2500*np.random.random((size,)),2)
        y = np.round_(2500*np.random.random((size,)),2)
        no_dupes = OrderedDict()
        for p in zip(x, y):
            no_dupes.setdefault(p[:2], p)
        self.points = list(no_dupes.values())

    def save(self, filepath):
        with open(filepath, 'wb') as fp:
            pickle.dump(self.points, fp)

    def restore(self, filepath):
        with open (filepath, 'rb') as fp:
            self.points = pickle.load(fp)

    def compare(self, ps):
        me = set(self.points)
        them = set(ps.points)
        if (me - them) or (them - me):
            return False
        else:
            return True
