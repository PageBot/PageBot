# fonttoolbox.analyzers.pointcontextlist


## Functions

### Vertical
The Vertical class is a list of point contexts that share the same x-value
self.append, self.x, self.y, self.alternates, self.minYPoint, self.maxYPoint
### Diagonal
### PointContext
The PointContext instance is a Point wrapper, that also takes the 3 points previous
and next 3 points on the contour. The instance behaves like a normal point p, but
additional information is available as interpreted from the point context in relation 
to the neighbor points. The total of 6 points is derived
from the average construction of a serif, so it is possible to hold (and interpret) an 
entire serif sequence inside one point context.
### Horizontal
The Horizontal class is a list of point contexts that share the same y-value
self.append, self.x, self.y, self.alternates, self.minXPoint, self.maxXPoint.
### PointContextList
The PointContextList us a group of related PointContext instances that can be
queried and selected on their attributes.
