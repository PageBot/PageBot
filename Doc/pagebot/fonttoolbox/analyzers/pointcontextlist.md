# fonttoolbox.analyzers.pointcontextlist

### class Diagonal
### class Horizontal
The Horizontal class is a list of point contexts that share the same y-value
self.append, self.x, self.y, self.alternates, self.minXPoint, self.maxXPoint.
### class PointContext
The PointContext instance is a Point wrapper, that also takes the 3 points previous
and next 3 points on the contour. The instance behaves like a normal point p, but
additional information is available as interpreted from the point context in relation 
to the neighbor points. The total of 6 points is derived
from the average construction of a serif, so it is possible to hold (and interpret) an 
entire serif sequence inside one point context.
### class PointContextList
The PointContextList us a group of related PointContext instances that can be
queried and selected on their attributes.
### class Vertical
The Vertical class is a list of point contexts that share the same x-value
self.append, self.x, self.y, self.alternates, self.minYPoint, self.maxYPoint
### dict __builtins__
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
(key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
d = {}
for k, v in iterable:
d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
in the keyword argument list.  For example:  dict(one=1, two=2)
### __doc__
### str __file__
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### str __name__
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### str __package__
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
