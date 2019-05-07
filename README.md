# convex-hull-python

## Prerequisites
- Python 3
- Pip 3

## Install
```
git clone https://github.com/mitchjmac/convex-hull-python.git
```

```
cd convex-hull-python
```

```
pip3 install -r requirements.txt
```

## Running
### Interactive

Start python3 enviroment
```
python3
```

Import modules
```python
from convexhull import dc
from convexhull import graham
from convexhull import jarvis
from convexhull.pointset import PointSet
```

Generate test data
```python
p = PointSet()
p.generate(1000)
```

Run Algorithms
```python
dc.sequential(p.points)
dc.parallel(p.points, <num_processes>)

graham.sequential(p.points)
graham.parallel(p.points)

jarvis.sequential(p.points)
jarvis.parallel(p.points, <num_processes>)
```
Or
```python
q = PointSet(graham.sequential(p.points))
r = PointSet(jarvis.sequential(p.points))
q.compare(r)
```

### Using Test Modules
Import modules
```python
from convexhull import test_dc
from convexhull import test_graham
from convexhull import test_jarvis
```

Test low number of points [0,3]
```python
# True means found correct convex hull
# Outputs: for each test case
#   True/False for sequential
#   True/False for parallel
test_dc.low_points()
test_graham.low_points()
test_jarvis.low_points()
```

Test larger Sets of points [10,1000000,10x increment]
```python
# True means found correct convex hull
# Outputs: for each test case
#   True/False for sequential
#   True/False for parallel
test_dc.high_points(<num_processes>)
test_graham.high_points() #Runs with 2 processes
test_jarvis.high_points() #Runs with max 4 processes
```

Time Algorithms
```python
# Outputs: for each test case
#   Time for sequential in seconds
#   Time for parallel in seconds
test_dc.test_time(<num_processes>)
test_graham.test_time() #Runs with 2 processes
test_jarvis.test_time() #Runs with max 4 processes
```

To test on branch "big_test"
```python
from convexhull.pointset import PointSet
p = PointSet()
p.generate(10000000)
p.save('10000000p')
^D
```

```
cp 10000000p tests/data/input/
```

Then independently find the convex hull of that data set using a 3rd party program and save to tests/data/ouput/ in json format

Then run tests `high_points()` and `test_time()` like above


