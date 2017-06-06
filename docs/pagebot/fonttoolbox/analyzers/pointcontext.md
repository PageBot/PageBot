# fonttoolbox.analyzers.pointcontext


## Functions

### function point2Line
Answers the distance from point <i>(px, py)</i> to line <i>((x1,
y1), (x2, y2))</i>.
### function insideCircle
>>> insideCircle(1, 1, 5)
True
>>> insideCircle(3, 3, 3)
False
### function dotProduct
### function pointProjectedOnLine
Answers the projected point <b>(px, py)</b> on line <b>((x1, y1), (x2,
y2))</b>.  Answers <b>(x1, y1)</b> if there is not distance between the two
points of the line.
### function normalize
### function vectorLength
### normalizedVector
classmethod(function) -> method

Convert a function to be a class method.

A class method receives the class as implicit first argument,
just like an instance method receives the instance.
To declare a class method, use this idiom:

  class C:
  def f(cls, arg1, arg2, ...): ...
  f = classmethod(f)

It can be called either on the class (e.g. C.f()) or on an instance
(e.g. C().f()).  The instance is ignored except for its class.
If a class method is called for a derived class, the derived class
object is passed as the implied first argument.

Class methods are different than C++ or Java static methods.
If you want those, see the staticmethod builtin.
### function squareDistance
Answers the square of the distance for relative comparison and to
save the time of the <b>sqrt</b>.
### function test
### function isEven
>>> isEven(2)
True
>>> isEven(1)
False
### function isOdd
>>> isOdd(1)
True
>>> isOdd(2)
False
### function calculateAngle
Calculate the angle between points p1 and p2. Points can be either 2D or 3D 
point tuples or Point instances.
### function angleOfLines
Answer the angle difference (radials or default degrees) between p1-->p2 and q1-->q2.
### PointContext
The PointContext instance is a Point wrapper, that also takes the 3 points previous
and next 3 points on the contour. The instance behaves like a normal point p, but
additional information is available as interpreted from the point context in relation 
to the neighbor points. The total of 6 points is derived
from the average construction of a serif, so it is possible to hold (and interpret) an 
entire serif sequence inside one point context.
### function intersection
Returns 2D intersection point if it exists. Otherwise (None, None,
None) is answered. Different from the RoboFont intersection tool, we
intersect on infinite line lengths. See also:

http://en.wikipedia.org/wiki/Line-line_intersection
### function point2D
Answer the 2D origin as combination of p and offset.
### function scalexy
### function distance
Answers the distance between the points.
### Point
### function isBetween
Checks if point is on line between line endpoints. Uses epsilon
margin for float values, can be substituted by zero for integer
values.
### function scalePointByVector
### function lucasRange
Answers the range stem widths for interpolation, according to
Lucas’ formula.

http://www.lucasfonts.com/about/interpolation-theory/
a = minStem
z = maxStem
n = number of interpolated stems, including the two masters
minN = optional minimum value if normalizing, e.g. 0-1000
maxN = optional maximum value if normalizing

print Mathematics.lucasRange(32, 212, 8)
[32, 42, 55, 72, 94, 124, 162, 212]

print Mathematics.lucasRange(32, 212, 8, 0, 1000)
[0, 55, 127, 222, 346, 508, 721, 1000]

print Mathematics.lucasRange(32, 212, 8, 100, 200)
[100, 106, 113, 122, 135, 151, 172, 200]
