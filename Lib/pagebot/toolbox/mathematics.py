# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     mathematics.py
#
import math
import operator
from pagebot.toolbox.units import point2D
from functools import reduce

def iround(value):
    return min(255, max(0, int(round(value*255.0))))

def to255(values):
    return [round(val * 255) for val in values]

def to100(values):
    return [round(val * 100) for val in values]
def lucasRange(a, z, n, minN=None, maxN=None):
    """Answers the range stem widths for interpolation, according to
    Lucas’ formula.

    http://www.lucasfonts.com/about/interpolation-theory/
    a = minStem
    z = maxStem
    n = number of interpolated stems, including the two masters
    minN = optional minimum value if normalizing, e.g. 0-1000
    maxN = optional maximum value if normalizing

    >>> lucasRange(32, 212, 8)
    [32, 42, 55, 72, 94, 124, 162, 212]
    >>> lucasRange(32, 212, 8, 0, 1000)
    [0, 55, 127, 222, 346, 508, 721, 1000]
    >>> lucasRange(32, 212, 8, 100, 200)
    [100, 106, 113, 122, 135, 151, 172, 200]
    """
    n = n - 2  # Correct for two masters
    i = []

    for x in range(n + 2):
        v = ((a ** (n + 1 - x)) * (z ** x)) ** (1.0 / (n + 1))
        if not None in (minN, maxN):
            v = (v - a) * (maxN - minN) / (z - a) + minN
        i.append(int(round(v)))
    return i

def intersection(p1, p2, p3, p4):
    """Returns 2D intersection point if it exists. Otherwise (None, None,
    None) is answered. Different from the RoboFont intersection tool, we
    intersect on infinite line lengths. See also:

    http://en.wikipedia.org/wiki/Line-line_intersection
    """
    x1, y1 = point2D(p1)
    x2, y2 = point2D(p2)
    x3, y3 = point2D(p3)
    x4, y4 = point2D(p4)

    d = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if d != 0:
        m1 = (x1*y2-y1*x2)
        m2 = (x3*y4-y3*x4)
        return (m1*(x3-x4) - m2*(x1-x2)) / d, (m1*(y3-y4) - m2*(y1-y2)) / d
    return None, None

def isBetween(p1, p2, p):
    """Checks if point is on line between line endpoints. Uses epsilon
    margin for float values, can be substituted by zero for integer
    values."""
    x1, y1 = point2D(p1)
    x2, y2 = point2D(p2)
    px, py = point2D(p)
    epsilon = 1e-6
    crossproduct = (py - y1) * (x2 - x1) - (px - x1) * (y2 - y1)
    if abs(crossproduct) > epsilon: return False   # (or != 0 if using integers)

    dotproduct = (px - x1) * (x2 - x1) + (py - y1)*(y2 - y1)
    if dotproduct < 0 : return False

    squaredlengthba = (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1)
    if dotproduct > squaredlengthba: return False

    return True

def squareDistance(p1, p2):
    """Answers the square of the distance for relative comparison and to
    save the time of the **sqrt**."""
    tx, ty = p2[0]-p1[0], p2[1]-p1[1]
    return tx*tx + ty*ty

def distance(p1, p2):
    """Answers the distance between the points."""
    return math.sqrt(squareDistance(p1, p2))

def point2Line(p1, p2, p):
    """Answers the distance from point *(px, py)* to line *((x1, y1), (x2,
    y2))*."""
    x1, y1 = point2D(p1)
    x2, y2 = point2D(p2)
    px, py = point2D(p)
    x, y = pointProjectedOnLine(p1, p2, p)
    tx, ty = px-x, py-y # Vector p1->p2
    return math.sqrt(tx*tx + ty*ty) # Length of p1->p2

def dotProduct(v1, v2):
    return reduce(operator.add, map(operator.mul, v1, v2))

def pointProjectedOnLine(p1, p2, p):
    """Answers the projected point **(px, py)** on line **((x1, y1), (x2,
    y2))**.  Answers **(x1, y1)** if there is not distance between the two
    points of the line."""
    # Line vector.
    x1, y1 = point2D(p1)
    x2, y2 = point2D(p2)
    px, py = point2D(p)

    tx, ty = float(x2 - x1), float(y2 - y1)
    v1 = (tx, ty)

    # Vector from line start to point.
    t1x, t1y = float(px - x1), float(py - y1)
    v2 = (t1x, t1y)

    # Square length of line to normalize.
    dd = tx*tx + ty*ty

    if dd == 0:
        return x1, y1

    dot = dotProduct(v1, v2)
    return  x1 + (dot * tx) / dd, y1 + (dot * ty) / dd

def insideCircle(dx, dy, r):
    """
    >>> insideCircle(1, 1, 5)
    True
    >>> insideCircle(3, 3, 3)
    False
    """
    assert r > 0

    if abs(dx) + abs(dy) <= r:
        return True
    if abs(dx) > r:
        return False
    if abs(dy) > r:
        return False
    if dx**2 + dy**2 <= r**2:
        return True

    return False

def isOdd(v):
    """
    >>> isOdd(1)
    True
    >>> isOdd(2)
    False
    """
    return v%2 != 0

def isEven(v):
    """
    import pagebot.toolbox.mathematics.*
    >>> isEven(2)
    True
    >>> isEven(1)
    False
    """
    return v%2 == 0

def scalexy(p, scaleP):
    return p[0] * scaleP[0], p[1] * scaleP[1]

def scalePointByVector(p, v):
    return p[0] * v[0], p[1] * v[1]

def vectorLength(v):
    return math.sqrt(v[0]**2 + v[1]**2)

@classmethod
def normalizedVector(p, length=1):
    """
    Normalize the vector @(x,y). The *length* defines
    the length of the normalized vector, default is @1@.
    ###    Freetype XXX: UNDOCUMENTED! It seems that it is possible to try   */
    ###    to normalize the vector (0,0).  Return immediately. */
    """
    if p[1] == 0:
        return math.copysign(length, p[0]), 0
    w = vectorLength(p)
    if w == 0:
        return None
    return 1.0 * p[0] * length / w, 1.0 * p[1] * length / w

def normalize(p, length=1):
    if p[1] == 0:
        return length, 0
    w = vectorLength(p)
    if w == 0:
        return None
    return 1.0 * p[0] * length / w

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
