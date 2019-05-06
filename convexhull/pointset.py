import pickle
import numpy as np
from collections import OrderedDict
import simplejson

class PointSet:

    def __init__(self, pts=[]):
        self.points  = pts

    def generate(self, size):
        x = np.round_(size*10*np.random.random((size,)),2)
        y = np.round_(size*10*np.random.random((size,)),2)
        no_dupes = OrderedDict()
        while True:
            for p in zip(x, y):
                no_dupes.setdefault(p[:2], p)
            num = len(no_dupes)
            if num == size:
                break
            else:
                gen = size - num
                x = np.round_(size*10*np.random.random((gen,)),2)
                y = np.round_(size*10*np.random.random((gen,)),2)
        self.points = list(no_dupes.values())

    def save(self, filepath):
        with open(filepath, 'w') as fp:
            simplejson.dump(self.points, fp)

    def load(self, filepath):
        with open (filepath, 'r') as fp:
            self.points = [tuple(l) for l in simplejson.load(fp)]

    def compare(self, ps):
        return self.points == ps.points
