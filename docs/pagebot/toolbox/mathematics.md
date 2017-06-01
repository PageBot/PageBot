# toolbox.mathematics


## Functions

### point2Line
Answers the distance from point <i>(px, py)</i> to line <i>((x1,
y1), (x2, y2))</i>.
### insideCircle
>>> insideCircle(1, 1, 5)
True
>>> insideCircle(3, 3, 3)
False
### dotProduct
### pointProjectedOnLine
Answers the projected point <b>(px, py)</b> on line <b>((x1, y1), (x2,
y2))</b>.  Answers <b>(x1, y1)</b> if there is not distance between the two
points of the line.
### normalize
### vectorLength
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
### squareDistance
Answers the square of the distance for relative comparison and to
save the time of the <b>sqrt</b>.
### test
### isEven
>>> isEven(2)
True
>>> isEven(1)
False
### isOdd
>>> isOdd(1)
True
>>> isOdd(2)
False
### intersection
Returns 2D intersection point if it exists. Otherwise (None, None,
None) is answered. Different from the RoboFont intersection tool, we
intersect on infinite line lengths. See also:

http://en.wikipedia.org/wiki/Line-line_intersection
### point2D
Answer the 2D origin as combination of p and offset.
### scalexy
### distance
Answers the distance between the points.
### isBetween
Checks if point is on line between line endpoints. Uses epsilon
margin for float values, can be substituted by zero for integer
values.
### scalePointByVector
### lucasRange
