#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     units.py
#
#     Implements basic intelligent spacing units with build-in conversions.
#
#     units, Units # Basic contextual converter and interpretor
#
#     Absolute units
#     Millimeters MM = 0.0393701 * INCH
#     mm, Mm       Millimeters
#     p, P         Picas 1/6"
#     pt, Pt       Points 1/72"
#     inch, Inch
#
#     Relative units, using base and gutter as reference
#     em, Em       Relative to e.fontSize as base
#     perc, Perc   Relative to 100%
#     fr, Fr       Fraction columns for CSS-grid, without gutter
#     col, Col     Same as fr, using gutter. Works vertical as rows as well.
#     px, Px       Equal to points (for now)

from __future__ import division # Make integer division result in float.

import re
import sys
from copy import copy
from pagebot.toolbox.transformer import asNumberOrNone, asFormatted, asIntOrFloat

# max/max values for element sizes. Makes sure that elements dimensions never get 0
XXXL = sys.maxsize

INCH = 72
MM = 0.0393701 * INCH # Millimeters as points. E.g. 3*MM --> 8.5039416 pt.

# Basic layout measures
U = 6 # Some basic unit grid to use as default.
EM_FONT_SIZE = U*2 # 12pt
BASELINE_GRID = U*2+3 # 2.5U = 15pt

# P O I N T

def point3D(p=None):
    u"""Answers `p` as a 3D point. If it already is a list of 3 elements, then
    don't change and answer the original. If it's a smaller or larger
    list/tuple, then extend it.

    >>> point3D() # Default 3D origin
    (0pt, 0pt, 0pt)
    >>> point3D(pt(20, -40)) # Add z = pt(0)
    (20pt, -40pt, 0pt)
    >>> point3D(mm(30)) # One value defaults to x == y
    (30mm, 30mm, 0pt)
    >>> point3D(p(2,3,4,5)) # Trim tuple to 3 coordinates.
    (2p, 3p, 4p)
    """
    if not p: # None or zero.
        return pt(0, 0, 0) # Undefined 3D point as list.

    if isinstance(p, (list, tuple)):
        if len(p) > 3:
            p = p[:3]
        while len(p) < 3:
            p += (pt(0),) # Value undefined, add origin as z value.
        p = tuple(p)
    else:
        p = p, p, pt(0)

    return p

def point2D(p=None):
    u"""Answer the 2D point from a 2D or 3D point.

    >>> point2D() # Default 2D origin
    (0pt, 0pt)
    >>> point2D(pt(20, -40))
    (20pt, -40pt)
    >>> point2D(pt(20))
    (20pt, 20pt)
    >>> point2D(mm(2,3,4,5,6))
    (2mm, 3mm)
    """
    return point3D(p)[:2]

def pointOffset(point, offset):
    u"""Answer new 3D point, shifted by offset.

    Note that in normal usage the elements probably will be Unit instances.

    >>> pointOffset(pt(20, 30, 10), 12)
    (32pt, 42pt, 22pt)
    >>> pointOffset(p(20, 30, 40), pt(2, 3, 4))
    (20p2, 30p3, 40p4)
    >>> pointOffset(inch(12, 13), p(10))
    (13.67", 14.67", 120pt)
    >>> pointOffset(mm(12, 13), mm(100)) # Adding z = pt(0)
    (112mm, 113mm, 283.46pt)
    >>> pointOffset(mm(12, 13, 14), mm(100))
    (112mm, 113mm, 114mm)
    >>> pointOffset(pt(10, 20, 30), None) # None is interpreted as offset == 0
    (10pt, 20pt, 30pt)
    """
    if not offset:
        offset = pt(0, 0, 0)
    if not isinstance(offset, (tuple, list)):
        offset = (offset, offset, offset)
    point = point3D(point)
    offset = point3D(offset)
    assert isinstance(point, (tuple, list))
    #print(point[0], offset[0], point[1], offset[1], point[2], offset[2])
    return point[0] + offset[0], point[1] + offset[1], point[2] + offset[2]

def point2S(p):
    u"""Answer the point as string of units. Ignore `z`-value if it renders to
    0.

    >>> point2S(pt(22.4, 33.5, 44.6))
    '22.4pt 33.5pt 44.6pt'
    >>> point2S(pt(33.6, 44.7))
    '33.6pt 44.7pt'
    """
    x, y, z = point3D(p)
    if z.r:
        return '%s %s %s' % (x, y, z)
    return '%s %s' % (x, y)

def point2roundedS(p):
    u"""Answer the point as string of rounded units. Ignore `z`-value if it
    renders to 0.

    >>> point2roundedS(pt(22.4, 33.5, 44.6))
    '22 34 45'
    >>> point2roundedS(pt(33.6, 44.7))
    '34 45'
    """
    x, y, z = point3D(p)
    if z.r:
        return '%d %d %d' % (x.rounded, y.rounded, z.rounded)
    return '%d %d' % (x.rounded, y.rounded)

def ru(u, *args, **kwargs):
    u"""Render to uu.r or (u1.r, u2.r, ...) if uu is a list or tuple.
    If maker is defined, then use that to render towards.

    >>> ru(pt(100), pt(120))
    (100, 120)
    >>> ru(pt(100), 121, (p(5), p(6), units('5"')), maker=pt)
    (100, 121, (60, 72, 360))
    >>> ru(pt(60), 121, (p(5), p(6), units('5"')), maker=p) # Render units
    (5.0, 121, (5, 6, 30.0))
    >>> ru(mm(10), mm(20), (mm(30), mm(40)), maker=mm) # Render units
    (10, 20, (30, 40))
    """
    if args:
        if not isinstance(u, (list, tuple)):
            u = [u]
        for arg in args:
            u.append(arg)
    if isinstance(u, (list, tuple)):
        ruu = []
        for uu in u:
            uu = ru(uu, **kwargs)
            ruu.append(uu)
        return tuple(ruu)
    else:
        uu = units(u, **kwargs)
        if uu is not None:
            uu = uu.r
        return uu

def uv(u, *args, **kwargs):
    u"""Answer the clipped value of `u`. Otherwise use `u`. Convert to *int* if
    whole number.

    >>> uv(3)
    3
    >>> uv(Pt(10))
    10
    >>> uv(Em(2, min=10, max=20))
    10
    >>> units((pt(60), 121, (p(5), p(6), units('5"'))), maker=p) # units() creates then as P() instances.
    (5p, 121p, (5p, 6p, 30p))
    >>> uv(pt(60), 121, (p(5), p(6), units('5"')), maker=p) # Render units
    (5.0, 121, (5, 6, 30.0))
    """
    if args:
        if not isinstance(u, (list, tuple)):
            u = [u]
        for arg in args:
            u.append(arg)
    if isinstance(u, (list, tuple)):
        ruu = []
        for uu in u:
            uu = uv(uu, **kwargs)
            ruu.append(uu)
        return tuple(ruu)
    else:
        uu = units(u, **kwargs)
        if uu is not None:
            uu = uu.v
        return uu

def isUnits(u, *args):
    u"""Answer the boolean flag is u (and all of the other items in the argument list)
    are a Unit instance.

    >>> isUnits(Em(2))
    True
    >>> isUnits(2)
    False
    >>> isUnits(pt(1), pt(2), pt(3))
    True
    >>> isUnits(pt(1), pt(2), 3, pt(4))
    False
    """
    if args:
        if isinstance(u, (list, tuple)):
            u = list(u)
        else:
            u = [u]
        for arg in args:
            u.append(arg)
    if isUnit(u):
        return True
    if isinstance(u, (list, tuple)):
        for uu in u:
            if not isUnits(uu): # Can be nested tuples.
                return False
        return True
    return False

def isUnit(u):
    u"""Answer the boolean flag if u is an instance of Unit.

    >>> isUnit(pt(20))
    True
    >>> isUnit(pt(20, 21))
    False
    >>> isUnit(2)
    False
    """
    # isinstance(u, Unit) # Does not seem to work right for units created in other sources such as A4
    return hasattr(u, '_v') and hasattr(u, 'base')

def uRound(u, *args):
    u"""Answer the list with rounded units (and all of the other items in the argument list)
    are a Unit instance.

    >>> uRound(Em(2.3))
    2em
    >>> uRound(4.2)
    4pt
    >>> uRound(2, 2.4, pt(14.5), (20.9, pt(19.8)))
    [2pt, 2pt, 15pt, [21pt, 20pt]]
    >>> uRound(pt(1.3), pt(2.4), pt(3.5))
    [1pt, 2pt, 4pt]
    >>> uRound(pt(1.000001), pt(2.44444449), 3, pt(mm(4)))
    [1pt, 2pt, 3pt, 11pt]
    """
    if args:
        if isinstance(u, (list, tuple)):
            u = list(u)
        else:
            u = [u]
        for arg in args:
            u.append(arg)
    if isUnit(u):
        u = u.rounded
    elif isinstance(u, (int, float)):
        u = pt(u).rounded
    elif isinstance(u, (list, tuple)):
        ruu = []
        for uu in u:
            ruu.append(uRound(uu)) # Can be nested tuples.
        u = ruu
    return u

def classOf(u):
    u"""Answer the class of the Unit instance. Otherwise answer None.

    >>> u = Em(2)
    >>> classOf(u) is Em
    True
    """
    if isUnit(u):
        return u.__class__
    return None

def uString(u, maker=None):
    u"""Answer the unit `u` as a string. In case it is not a Unit instance,
    convert to Unit first.

    >>> u = Em(2)
    >>> uString(u)
    '2em'
    >>> uString(2, fr) # Maker function works
    '2fr'
    >>> uString(2, Inch) # Unit class works
    '2"'
    """
    return str(units(u, maker))

us = uString # Convenience abbreviaion

class Unit(object):
    u"""Base class for units, implementing most of the logic.  Unit classes can
    be absolute (Pt, Px, Pica/P, Mm, Inch) and relative, which need the
    definintion of a base reference value (Perc, Fr) or em (Em).

        >>> mm(1)
        1mm
        >>> mm(10) * 8
        80mm
        >>> fr(2) * 3
        6fr
        >>> px(5) + 2
        7px
        >>> perc(20) + 8
        28%
        >>> perc(12.4) * 2
        24.8%
        >>> u = perc(15) + 5
        >>> u
        20%
        >>> u.base = pt(440)
        >>> u, u.r # Respectively: instance to str, rendered to u.base as 20% of pt(440)
        (20%, 88)
        >>> # 3 + px(3) # Gives error.
        >>> px(3) + 3
        6px
        >>> px(12) + px(10)
        22px
        >>> mm(10) + px(1)
        10.35mm
        >>> (mm(10) + mm(5)) * 2
        30mm
        >>> inch(4)
        4"
        >>> inch(4).pt # Convert inches to point value
        288
        >>> pt(inch(4)) # Convert inches to point unit
        288pt
        >>> isUnit(mm(2))
        True
        >>> isUnit(2)
        False
        >>> x, y = pt(100, 300) # Creating list of pt as batch
        >>> x.pt, y.pt
        (100, 300)
        >>> x, (y, z) = pt(100, (150, 300)) # Creating nested list of pt as batch
        >>> x.pt, y.pt, z.pt
        (100, 150, 300)
        >>> x, (y, z) = pt(100, (150, 300), min=200, max=250) # Creating nested list of pt as batch with generic min/max
        >>> x.pt, y.pt, z.pt
        (200, 200, 250)
        >>> u = units('100mm', min=10, max=30)
        >>> u._v, u.v, u.r, u # Respectively: Raw value, clipped to min/max, clipped and rendered (in case relative), clipped unit instance as str.
        (100, 30, 30, 30mm)
        >>> us(20) # Convert to unit string, default for number is pt
        '20pt'
        >>> us(pt(20)) # Value can be Unit instance
        '20pt'
        >>> us(20, mm) # Usage of a maker function (all lc)
        '20mm'
        >>> us(20, 'mm') # Or can be string name of maker function (caps or lc)
        '20mm'
        >>> us(20, 'MM') # Or can be string name of maker function (caps or lc)
        '20mm'
        >>> us(20, Mm) # Or can be real class (initial cap)
        '20mm'
    """
    BASE = None # Default "base reference for relative units. Unused None for absolute units."

    isAbsolute = True
    isRelative = False
    isEm = False

    def __init__(self, v=0, base=None, g=0, min=None, max=None):
        assert isinstance(v, (int, float)) # Otherwise do a cast first as pt(otherUnit)
        self._v = v
        # Base can be a unit value, ot a dictionary, where self.UNIT is the key.
        # This way units(...) can decide on the type of unit, where the base has multiple entries.
        if base is None:
            base = self.BASE
        self.base = base # Default base value for reference by relative units.
        self.g = g # Default gutter for reference by relative units. Ignored by absolute units.
        self.min = min # Used when rendered towards pt or clipped.
        self.max = max

    def _get_min(self):
        return self._min
    def _set_min(self, min):
        if isinstance(min, str):
            min = units(min)
        if isUnit(min):
            min = min.pt
        if min is None:
            min = -XXXL
        self._min = min
    min = property(_get_min, _set_min)

    def _get_max(self):
        return self._max
    def _set_max(self, max):
        if isinstance(max, str):
            max = units(max)
        if isUnit(max):
            max = max.pt
        if max is None:
            max = XXXL
        self._max = max
    max = property(_get_max, _set_max)

    def _get_name(self):
        u"""Answer the unit name.

        >>> pt(123).name
        'Pt'
        >>> mm(234).name
        'Mm'
        """
        return self.__class__.__name__
    name = property(_get_name)

    def _get_rounded(self):
        u"""Answer a new instance of self with rounded value.
        Note that we are rounding the self.v here, not the rendered result.

        >>> u = pt(12.2)
        >>> ru = u.rounded # Create new pt-unit
        >>> u, ru # Did not change original u
        (12.2pt, 12pt)
        """
        u = copy(self)
        u._v = int(round(self.r))
        return u
    rounded = property(_get_rounded)

    def __repr__(self):
        v = asIntOrFloat(self.v) # Clip to min/max.
        if isinstance(v, int):
            return '%d%s' % (v, self.name.lower())
        return '%s%s' % (asFormatted(v), self.name.lower())

    def _get_pt(self):
        u"""Answer the clipped value in *pt*. Base value for absolute unit
        values is ignored.

        >>> p(1).pt
        12
        >>> pt(1), pt(1).pt # Render value cast to pt
        (1pt, 1)
        >>> 10 + inch(1).pt + 8 # Rendered to a pt-units, so 10 and 8 behave as pt numbers.
        90
        >>> (10 + inch(1) + 8).pt # Using reversed __radd__, then rendered and cast to pt-unit.
        1368
        >>> 2 * pt(4).p # Rendered and cast to picas
        8
        >>> mm(1).pt
        2.8346472
        >>> inch(1).pt
        72
        """
        return asIntOrFloat(self.r * self.PT_FACTOR) # Factor to points
    def _set_pt(self, v):
        self._v = v / self.PT_FACTOR
    pt = property(_get_pt, _set_pt)

    def _get_px(self):
        u"""Answers the clipped value in *px*. Base value for absolute unit values
        is ignored.

        >>> p(1).px
        12
        >>> px(1), px(1).pt
        (1px, 1)
        >>> 10 + inch(1).pt + 8 # Rendered to a number
        90
        >>> mm(1).pt
        2.8346472
        """
        return asIntOrFloat(px(self.pt).v)
    px = property(_get_px)

    def _get_inch(self):
        return inch(self.pt).v
    inch = property(_get_inch)

    def _get_p(self):
        return p(self.pt).v
    p = property(_get_p)

    def _get_v(self):
        u"""Answers the raw unit value, clipped to the self.min and self.max
        local values. For absolute inits u.v and u.r are identical. For
        relative units u.v answers the clipped value and u.r answers the value
        rendered by u.base.

        >>> u = Inch(2)
        >>> u.v
        2
        >>> u.min = 10
        >>> u.max = 20
        >>> u.v
        10
        """
        return min(self.max, max(self.min, self._v))
    def _set_v(self, v):
        u"""Set the raw unit value.

        >>> u = Inch(2)
        >>> u.v = 3
        >>> u, u.v
        (3", 3)
        """
        self._v = v
    v = property(_get_v, _set_v)
    r = property(_get_v) # Read only

    def __int__(self):
        u"""Answers self as rounded int, rendered and converted to points.

        >>> int(pt(20.2))
        20
        """
        return int(round(self.pt))

    def __float__(self):
        u"""Answers self as float, rendered and converted to points.

        >>> float(pt(20.2))
        20.2
        """
        return self.pt

    def __coerce__(self, v):
        u"""Converts to type of v.

        >>> '%dpoints' % pt(10)
        '10points'
        """
        if isinstance(v, (int, float)):
            return self, pt(v)
        return self, units(v)

    def __abs__(self):
        u"""Answers an absolute-value copy of self.

        >>> abs(units('-10pt'))
        10pt
        >>> abs(mm(-1000))
        1000mm
        >>> abs(-pt(2))
        2pt
        """
        u = copy(self)
        u.v = abs(u.v)
        return u

    def __eq__(self, u):
        u"""Answers the boolean result how self compares to rendered u.

        >>> u = pt(20)
        >>> u == 20
        True
        >>> u == 21
        False
        >>> u == pt(20) # Compare with different instance
        True
        >>> u == mm(20)
        False
        >>> u == []
        False
        """
        if isinstance(u, (int, float)): # One is a scalar, just compare with rendered value
            return self.r == u
        if isUnit(u):
            if isinstance(u, self.__class__):
                return self.r == u.r # Same class, compare rendered result may differe from base or min/max)
            return self.pt == u.pt # Incompatible unit types, compare via points
        return False

    def __ne__(self, u):
        u"""Answers the boolean result how self compares to rendered u.

        >>> u = pt(20)
        >>> u != 20
        False
        >>> u != 21
        True
        >>> u != pt(20) # Compare with different unit instances of same class
        False
        >>> u != mm(20) # Compare with unit instance of different class.
        True
        >>> u != [] # All other situations are not matching
        True
        """
        if isinstance(u, (int, float)): # One is a scalar, just compare
            return self.r != u
        if isUnit(u):
            if isinstance(u, self.__class__):
                return self.r != u.r
            return self.pt != u.pt # Incompatible unit types, compare via points
        return True

    def __le__(self, u):
        u"""Answers the boolean result how self compares to rendered u.

        >>> u = pt(20)
        >>> u <= 20
        True
        >>> u <= 19
        False
        >>> u <= pt(20) # Compare with different unit instances of same class
        True
        >>> u <= mm(20) # Compare with unit instance of different class.
        True
        >>> u <= mm(2) # Compare with unit instance of different class.
        False
        >>> u <= [] # All other situations are not matching
        False
        """
        if isinstance(u, (int, float)): # One is a scalar, just compare
            return self.r <= u
        if isUnit(u):
            if isinstance(u, self.__class__):
                return self.r <= u.r
            return self.pt <= u.pt # Incompatible unit types, compare via points
        return False

    def __lt__(self, u):
        u"""Answers the boolean result how self compares to rendered u.

        >>> u = pt(20)
        >>> u < 21
        True
        >>> u < 20
        False
        >>> u < pt(21) # Compare with different unit instances of same class
        True
        >>> u < mm(20) # Compare with unit instance of different class.
        True
        >>> u < mm(2) # Compare with unit instance of different class.
        False
        >>> u < [] # All other situations are not matching
        False
        """
        if isinstance(u, (int, float)): # One is a scalar, just compare
            return self.r < u
        if isUnit(u):
            if isinstance(u, self.__class__):
                return self.r < u.r
            return self.pt < u.pt # Incompatible unit types, compare via points
        return False

    def __ge__(self, u):
        u"""Answers the boolean result how self compares to rendered u.

        >>> u = pt(20)
        >>> u >= 20
        True
        >>> u >= 21
        False
        >>> u >= pt(20) # Compare with different unit instances of same class
        True
        >>> u >= mm(2) # Compare with unit instance of different class.
        True
        >>> u >= mm(200) # Compare with unit instance of different class.
        False
        >>> u >= [] # All other situations are not matching
        False
        """
        if isinstance(u, (int, float)): # One is a scalar, just compare
            return self.r >= u
        if isUnit(u):
            if isinstance(u, self.__class__):
                return self.r >= u.r
            return self.pt >= u.pt # Incompatible unit types, compare via points
        return False

    def __gt__(self, u):
        u"""Answers the boolean result how self compares to rendered u.

        >>> u = pt(20)
        >>> u > 19
        True
        >>> u > 20
        False
        >>> u > pt(19) # Compare with different unit instances of same class
        True
        >>> u > mm(2) # Compare with unit instance of different class.
        True
        >>> u > mm(200) # Compare with unit instance of different class.
        False
        >>> u > [] # All other situations are not matching
        False
        """
        if isinstance(u, (int, float)): # One is a scalar, just compare
            return self.r > u
        if isUnit(u):
            if isinstance(u, self.__class__):
                return self.r > u.r
            return self.pt > u.pt # Incompatible unit types, compare via points
        return False

    def __add__(self, u):
        u"""Adds self to `u`, creating a new Unit instance with the same type
        as self.

        >>> u = units('10pt')
        >>> u + 20 # Create a new Unit instance of the same type
        30pt
        >>> u + mm(10) # Add another type of unit
        38.35pt
        >>> u = p(2)
        >>> u + 1, u + pt(1) # Numbers are interpeted as adding picas. Otherwise use pt(1)
        (3p, 2p1)
        >>> 10 + pt(10) # Thanks to implementation of __radd__ the reverse also works.
        20pt
        """
        u0 = copy(self) # Keep values of self
        if isinstance(u, (int, float)): # One is a scalar, just add
            u0.v += u
        elif u0.__class__ == u.__class__:
            u0.v += u.v # Same class, just add
        elif isUnit(u):
            u0.pt += u.pt # Adding units, calculate via points
        else:
            raise ValueError('Cannot add "%s" to "%s"' % (self, u))
        return u0

    __radd__ = __add__

    def __sub__(self, u):
        u"""Subtracts `u` from self, creating a new Unit instance with the same
        type as self.

        >>> u = units('50pt')
        >>> u - 20 # Create a new Unit instance of the same type
        30pt
        >>> u - mm(10) # Subtract another type of unit
        21.65pt
        """
        u0 = copy(self) # Keep values of self
        if isinstance(u, (int, float)): # One is a scalar, just subtract
            u0.v -= u
        elif u0.__class__ == u.__class__:
            u0.v -= u.v # Same class, just subtract
        elif isUnit(u):
            u0.pt -= u.pt # Subtracting units, calculate via points
        else:
            raise ValueError('Cannot subtract "%s" from "%s"' % (u, self))
        return u0

    def __rsub__(self, u):
        u"""Subtract in reversed order.

        >>> 30 - pt(10) # Thanks to implementation of __rsub__ the reverse also works.
        20pt
        """
        return -self + u

    def __div__(self, u):
        u"""Divide self by u, creating a new Unit instance with the same type
        as self.  Unit / Unit creates a float number.

        >>> u = units('60pt')
        >>> u / 2 # Create a new Unit instance of the same type
        30pt
        >>> asFormatted(u / mm(1.5)) # Unit / Unit create ratio float number
        '14.11'
        >>> u / units('120pt') # Unit / Unit create a float ratio number.
        0.5
        """
        u0 = copy(self) # Keep values of self
        if isinstance(u, (int, float)): # One is a scalar, just divide
            assert u, ('Zero division "%s/%s"' % (u0, u))
            u0.v /= u
        elif isUnit(u):
            upt = u.pt
            assert upt, ('Zero division "%s/%s"' % (u0, u))
            u0 = u0.pt / upt # Dividing units, create ratio float number.
        else:
            raise ValueError('Cannot divide "%s" by "%s"' % (u0, u))
        return u0

    __truediv__ = __div__

    def __rtruediv__(self, u):
        u"""Dividing non-unit by unit is not supported.

        >>> (2 / pt(20)) is None
        True
        """
        #raise ValueError('Cannot divide non-unit "%s" by unit "%s"' % (u, self))
        return None

    __itruediv__ = __rtruediv__

    def __mul__(self, u):
        u"""Multiply self by u, creating a new Unit instance with the same type
        as self. Units can only be multiplied by numbers. Unit * Unit raises a
        ValueError.

        >>> u = units('60pt')
        >>> u / 2 # Create a new Unit instance of the same type
        30pt
        >>> asFormatted(u / mm(1.5)) # Unit / Unit create ratio float number
        '14.11'
        >>> u / units('120pt') # Unit / Unit create a float ratio number.
        0.5
        >>> 10 * mm(10) # Thanks to implementation of __rmul__ the reverse also works.
        100mm
        """
        u0 = copy(self) # Keep values of self
        if isinstance(u, (int, float)): # One is a scalar, just multiply
            u0.v *= u
        elif isUnit(u) and u.isEm:
            u0.base = u.r
            u0 = u0.r
        else:
            raise ValueError('Cannot multiply "%s" by "%s"' % (u0, u))
        return u0

    __rmul__ = __mul__

    def __neg__(self):
        u"""Reverse sign of self, answer as copied unit.

        >>> -pt(-20)
        20pt
        >>> -pt(20) - pt(10)
        -30pt
        """
        u = copy(self) # Keep values of self
        u.v = -self._v
        return u

#   Mm

def mm(v, *args, **kwargs):
    u = None
    minV = kwargs.get('min')
    maxV = kwargs.get('max')
    if args: # If there are more arguments, bind them together in a list.
        v = [v]+list(args)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v:
            u.append(mm(uv, min=minV, max=maxV))
        u = tuple(u)
    elif isinstance(v, (int, float)):
        u = Mm(v, min=minV, max=maxV)
    elif isUnit(v):
        u = Mm(min=minV, max=maxV) # New Mm and convert via pt
        u.pt = v.pt
    elif isinstance(v, str):
        v = v.strip().lower()
        if v.endswith(Mm.UNIT):
            v = asNumberOrNone(v[:-2])
            if v is not None:
                u = Mm(v, min=minV, max=maxV)
        else: # Something else, try again.
            u = mm(units(v), min=minV, max=maxV)
    return u

class Mm(Unit):
    u"""Answer the mm instance.

    >>> u = Mm(210)
    >>> u
    210mm
    >>> u = mm('297mm') # A4
    >>> u
    297mm
    >>> u/2
    148.5mm
    >>> u-100
    197mm
    >>> u+100
    397mm
    >>> u.v # Raw value of the Unit instance
    297
    >>> isinstance(u.v, (int, float))
    True
    >>> pt(u).rounded # Rounded A4 --> pts
    842pt
    >>> mm(10, 11, 12) # Multiple arguments create a list of tuple mm
    (10mm, 11mm, 12mm)
    >>> mm((10, 11, 12, 13)) # Arguments can be submitted as list or tuple
    (10mm, 11mm, 12mm, 13mm)
    >>> mm(pt(5), p(6), '3"') # Arguments can be a list of other units types.
    (1.76mm, 25.4mm, 76.2mm)
    """
    PT_FACTOR = MM # mm <---> points
    UNIT = 'mm'

    def _get_mm(self):
        u"""No transformation or casting, just answer the self.v value.

        >>> mm(5).mm
        5
        >>> 10 * mm(5).mm
        50
        """
        return asIntOrFloat(self.v)
    mm = property(_get_mm)

#   Pt

def pt(v, *args, **kwargs):
    u = None
    minV = kwargs.get('min')
    maxV = kwargs.get('max')
    if args: # If there are more arguments, bind them together in a list.
        v = [v]+list(args)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v:
            u.append(pt(uv, min=minV, max=maxV))
        u = tuple(u)
    elif isinstance(v, (int, float)): # Simple value as input, use class
        u = Pt(v, min=minV, max=maxV)
    elif isUnit(v): # It's already a Unit instance, convert via points.
        u = Pt(v.pt, min=minV, max=maxV)
    elif isinstance(v, str): # Value is a string, interpret from unit extension.
        v = v.strip().lower()
        if v.endswith(Pt.UNIT):
            v = asNumberOrNone(v[:-2])
            if v is not None:
                u = Pt(v, min=minV, max=maxV)
        else: # Something else, recursively try again.
            u = pt(units(v), min=minV, max=maxV)
    return u

class Pt(Unit):
    u"""pt is the base unit size of all PageBot measures.

    >>> Pt(6) # Create directly as class, only takes numbers or Unit instances
    6pt
    >>> pt(6) # Create through interpreting values (int, float, Unit, str)
    6pt
    >>> pt('6pt')
    6pt
    >>> u = units('6pt') # unit function auto-detects matching unit class.
    >>> u
    6pt
    >>> u/2
    3pt
    >>> u-1
    5pt
    >>> pt(12).pt
    12
    >>> u = pt(12)
    >>> u.pt = 120
    >>> u
    120pt
    >>> pt(10, 11, 12) # Multiple arguments create a list of tuple pt
    (10pt, 11pt, 12pt)
    >>> pt((10, 11, 12, 13)) # Arguments can be submitted as list or tuple
    (10pt, 11pt, 12pt, 13pt)
    >>> pt(mm(5), p(6)) # Arguments can be a list of other units types.
    (14.17pt, 72pt)
    >>> pt('11"', '12"') # Arguments interpreted from other unit type string.
    (792pt, 864pt)
    >>> pt(10, 12, 13, (20, 21)) # Nested lists, created nested list of pt
    (10pt, 12pt, 13pt, (20pt, 21pt))
    """
    PT_FACTOR = 1 # pt <--> pt factor
    UNIT = 'pt'

    def _get_pt(self):
        u"""No transformation or casting. Just answer the self.v.

        >>> pt(12).pt
        12
        """
        return asIntOrFloat(self.v)
    def _set_pt(self, v):
        self.v = v
    pt = property(_get_pt, _set_pt)

#   P(ica)

def p(v, *args, **kwargs):
    u"""Create a new instance of P, using v as source value. In case v is already
    a Unit instance, then convert to that P needs, through the amount of points.

    >>> p(20)
    20p
    >>> p('20p6')
    20p6
    >>> p(pt(72)), p(pt(73)), p(pt(73.5)), p(pt(73.55)), p(pt(73.555))
    (6p, 6p1, 6p1.5, 6p1.55, 6p1.56)
    >>> p('0p1000')
    83p4
    >>> p(mm(3)) # Argument can be another Unit instance.
    0p8.5
    >>> p(123.88)
    123p10.56
    >>> p(inch(1))
    6p
    >>> p(inch(1.5))
    9p
    >>> p(inch(1.6))
    9p7.2
    >>> p(pt(36)) # 12
    3p
    >>> pica(20)
    20p
    >>> units('p6')
    0p6
    >>> p(10, 11, 12) # Multiple arguments create a list of tuple p
    (10p, 11p, 12p)
    >>> p((10, 11, 12, 13)) # Arguments can be submitted as list or tuple
    (10p, 11p, 12p, 13p)
    >>> p(mm(5), pt(24), inch(5)) # Arguments can be a list of other units types.
    (1p2.17, 2p, 30p)
    >>> p('10pt', '1"', '1.5"', units('1.5"')+3) # Arguments can be a list of other units types.
    (0p10, 6p, 9p, 27p)
    >>> p(10, 12, 13, (20, 21)) # Nested lists, created nested list of p
    (10p, 12p, 13p, (20p, 21p))
    """
    u = None
    minV = kwargs.get('min')
    maxV = kwargs.get('max')
    if args: # If there are more arguments, bind them together in a list.
        v = [v]+list(args)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v:
            u.append(p(uv, min=minV, max=maxV))
        u = tuple(u)
    elif isinstance(v, (int, float)):
        u = P(v, min=minV, max=maxV)
    elif isUnit(v):
        u = P(min=minV, max=maxV) # Make new Pica and convert via pt
        u.pt = v.pt
    elif isinstance(v, str):
        v = v.strip().lower().replace('pica', P.UNIT)
        if not 'pt' in v: # Hack to avoid confusion with '10pt')
            vv = VALUE_PICA.findall(v)
            if vv:
                v0 = asNumberOrNone(vv[0][0] or '0')
                v1 = asNumberOrNone(vv[0][1][1:] or '0')
                if v0 is not None and v1 is not None:
                    u = P(min=minV, max=maxV)
                    u.pt = v0*P.PT_FACTOR+v1
            else:
                u = p(units(v, min=minV, max=maxV))
        else: # Something else, recursively try again.
            u = p(units(v), min=minV, max=maxV)
    return u

class P(Unit):
    u"""P (pica) class.

    >>> u = P(2)
    >>> u.v
    2
    >>> u = p(1)
    >>> u, u+2, u+pt(2), u+pt(100), u*5, u/2
    (1p, 3p, 1p2, 9p4, 5p, 0p6)
    >>> p('2.8p')
    2p9.6
    """
    PT_FACTOR = 12  # 12 points = 1p
    UNIT = 'p'

    def _get_p(self):
        u"""No transforming or casting, just answer the self.v.

        >>> p(5).p
        5
        """
        return asIntOrFloat(self.v)
    p = property(_get_p)

    def __repr__(self):
        v0 = int(self.v * self.PT_FACTOR // self.PT_FACTOR)
        v1 = asIntOrFloat((self.v - v0) * self.PT_FACTOR)
        if v1:
            if isinstance(v1, int):
                return '%dp%d' % (v0, v1)
            return '%dp%s' % (v0, asFormatted(v1))
        return '%dp' % v0

Pica = P
pica = p

#   Inch

def inch(v, *args, **kwargs):
    u = None
    minV = kwargs.get('min')
    maxV = kwargs.get('max')
    if args: # If there are more arguments, bind them together in a list.
        v = [v]+list(args)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v:
            u.append(inch(uv))
        u = tuple(u)
    elif isinstance(v, (int, float)):
        return Inch(v, min=minV, max=maxV)
    elif isUnit(v):
        u = Inch(min=minV, max=maxV) # New Inch and convert via pt
        u.pt = v.pt
    elif isinstance(v, str):
        v = v.strip().lower()
        if v.endswith(Inch.UNITC): # "-character
            v = asNumberOrNone(v[:-1])
            if v is not None:
                u = Inch(v, min=minV, max=maxV)
        elif v.endswith(Inch.UNIT):
            v = asNumberOrNone(v[:-4])
            if v is not None:
                u = Inch(v, min=minV, max=maxV)
        else: # Something else, recursively try again.
            u = inch(units(v), min=minV, max=maxV)
    return u

class Inch(Unit):
    u"""Inch 72 * the base unit size of all PageBot measures.

    >>> units('0.4"')
    0.40"
    >>> Inch(0.4)
    0.40"
    >>> inch('0.4"')
    0.40"
    >>> u = units('0.4inch')
    >>> u
    0.40"
    >>> u*2
    0.80"
    >>> u/2
    0.20"
    >>> u-0.1
    0.30"
    >>> inch(10, 11, 12) # Multiple arguments create a list of tuple inch
    (10", 11", 12")
    >>> inch((10, 11, 12, 13)) # Arguments can be submitted as list or tuple
    (10", 11", 12", 13")
    >>> inch(mm(5), pt(24), px(5)) # Arguments can be a list of other units types.
    (0.20", 0.33", 0.07")
    >>> inch('10pt', '11mm') # Arguments can interprete from strings of other units types.
    (0.14", 0.43")
    """
    PT_FACTOR = INCH # 72pt = 1"
    UNIT = 'inch' # Alternative is "
    UNITC = '"'

    def _get_inch(self):
        u"""No transforming or casting, just answer the self.v.

        >>> inch(6).inch
        6
        >>> inch(7.0).inch
        7
        """
        return asIntOrFloat(self.v)
    inch = property(_get_inch)

    def __repr__(self):
        v = asIntOrFloat(self.v)
        if isinstance(v, int):
            return '%d%s' % (self._v, self.UNITC)
        return '%0.2f%s' % (self._v, self.UNITC)

class Formula(Unit):
    u"""Unit class that contains a sequence of other units and rules how to apply them.
    This gives users the opportunity to combine absolute and relative measures.
    The API of a Formula instance is the same as with normal units.

    TODO: More rules to be added. Usage of labelled self.units dictionary.
    TODO: The Formula needs more thinking

    >>> f = Formula(f='addAll', units=[pt(10), pt(22)])
    >>> f.f
    'addAll'
    """
    PT_FACTOR = 1 # Formulas behave as points by default, but that can be changed.
    UNIT = 'f'

    def __init__(self, v=0, base=None, g=0, min=None, f=None, max=None, units=None):
        Unit.__init__(self, v=v, base=base, g=g, min=min, max=max)
        self.f = f
        if units is None:
            units = {}
        self.units = units # Key is id, value is unit

    def addAll(self):
        result = None
        for unitId, unit in self.units.items():
            if result is None:
                result = copy(unit)
            else:
                result += unit
        return result


#   Relative Units (e.g. for use in CSS)

class RelativeUnit(Unit):
    u"""Abstract class to avoid artihmetic between absolute and relative units.
    Needs absolute reference to convert to absolute units.

    >>> u = units('12%')
    >>>
    """
    BASE = 1 # Default "base reference for relative units."
    GUTTER = U*2 # Used as default gutter measure for Col units.
    BASE_KEY = 'base' # Key in optional base of relative units.
    isAbsolute = False # Cannot do arithmetic with absolute Unit instances.
    isRelative = True

    def _get_r(self):
        u"""Answer the rendered clipped value of self, clipped to the self.min and self.max local values.
        The value is based on the type of self. For absolute units the result of u.v and u.r is identical.
        For relative units u.v answers the clipped value and u.r answers the value rendered by self.base.
        self.base can be another unit or a dictionary of base values.

        >>> u = Inch(2)
        >>> u.v
        2
        >>> u.min = 10
        >>> u.max = 20
        >>> u.v
        10
        """
        return asIntOrFloat(self.base * self.v / self.BASE)
    r = property(_get_r)

    def _get_pt(self):
        u"""Answer the rendered value in pt.

        >>> u = fr(2, base=12)
        >>> u, u.pt
        (2fr, 6)
        >>> u = p(12)
        >>> u.pt
        144
        """
        return asIntOrFloat(pt(self.r).v) # Clip rendered value to min/max and cast to points
    pt = property(_get_pt)

    def _get_mm(self):
        u"""Answer the rendered value in mm.

        >>> u = fr(2, base=mm(10))
        >>> u, u.mm, mm(u)
        (2fr, 5, 5mm)
        """
        return asIntOrFloat(mm(self.r).v) # Clip rendered value to min/max and cast to mm
    mm = property(_get_mm)

    def _get_p(self):
        u"""Answer the rendered value in picas.

        >>> u = fr(2, base=p(12))
        >>> u, u.p
        (2fr, 6)
        >>> u = units('75%', base=p(72))
        >>> u, u.p, p(u)
        (75%, 54, 54p)
        """
        return asIntOrFloat(p(self.r).v) # Clip rendered value to min/max and factor to mm
    p = property(_get_p)

    def _get_inch(self):
        u"""Answer the rendered value in inch.

        >>> fr(2, base='4"').inch
        2
        >>> fr(2, base=inch(10)).inch
        5
        >>> units('25%', base=inch(10)).inch
        2.5
        """
        return asIntOrFloat(inch(self.r).v) # Clip rendered value to min/max and factor to mm
    inch = property(_get_inch)

    def _get_base(self):
        u"""Optional base value as reference for relative units. Save as Unit instance.

        >>> u = perc('10%', base=300)
        >>> u, u.base, u.r
        (10%, 300pt, 30)
        >>> u = units('20%', base=mm(200))
        >>> u, u.base, u.r
        (20%, 200mm, 40mm)
        >>> u.base
        200mm
        >>> u.pt, u.r, u.v # Value in pt of 20% of 200pt
        (113.385888, 40mm, 20)
        >>> u = units('5em', base=dict(em=pt(12), perc=pt(50)))
        >>> u.pt # Rendered to base selection pt(12)
        60
        >>> u = units('25%', base='36p')
        >>> u, u.base, u.v, u.r, u.p, u.pt, u.inch
        (25%, 36p, 25, 9p, 9, 108, 1.5)
        """
        if isinstance(self._base, dict):
            return self._base[self.BASE_KEY]
        return self._base
    def _set_base(self, base):
        if isinstance(base, dict):
            assert self.BASE_KEY in base
        elif not isinstance(base, dict) and not isUnit(base):
            base = units(base)
        self._base = base
    base = property(_get_base, _set_base)

    def _get_g(self):
        u"""Optional gutter value as reference for relative units. Save as Unit instance.

        >>> u = col(0.25, base=mm(200), g=mm(8))
        >>> u.base
        200mm
        >>> u.mm # (200 + 8)/4 - 8 --> 44 + 8 + 44 + 8 + 44 + 8 + 44 = 200
        44
        >>> from pagebot.constants import A4
        >>> margin = 15
        >>> u = col(0.5, base=A4[0]-2*margin, g=mm(8))
        >>> u, u.r
        (0.5col, 86mm)
        """
        return self._g
    def _set_g(self, g):
        if not isUnit(g):
            g = units(g)
        self._g = g
    g = property(_get_g, _set_g)

#   Px

def px(v, *args, **kwargs):
    u = None
    base = kwargs.get('base', Px.BASE)
    g = kwargs.get('g', 0) # Not used by Px
    minV = kwargs.get('min')
    maxV = kwargs.get('max')
    if args: # If there are more arguments, bind them together in a list.
        v = [v]+list(args)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v:
            u.append(px(uv, base=base, g=g, min=minV, max=maxV))
        u = tuple(u)
    elif isinstance(v, (int, float, RelativeUnit)):
        u = Px(v, base=base, g=g, min=minV, max=maxV)
    elif isinstance(v, str):
        v = v.strip().lower()
        if v.endswith(Px.UNIT):
            v = asNumberOrNone(v[:-2])
            if v is not None:
                u = Px(v, base=base, g=g, min=minV, max=maxV)
        else: # Something else, recursively try again
            u = units(v, base=base, g=g, min=minV, max=maxV)
            assert isinstance(u, Px) # Only makes sense for relative if the same.
    return u

class Px(RelativeUnit):
    u"""Answer the px (pixel) instance.

    >>> Px(12) # Direct creation of class instance, only for (int, float, Unit)
    12px
    >>> px(12) # Through creator function
    12px
    >>> px('12px') # Through creator function, strings are interpreted (int, float, Unit, str)
    12px
    >>> u = units('12px')
    >>> u
    12px
    >>> u/2 # Math on Unit create new Unit instance of same type.
    6px
    >>> u-1
    11px
    >>> u.pt # Answer pt value, assuming here an 1:1 conversion
    12
    """
    PT_FACTOR = 1 # This may not always be 1:1 to points.
    UNIT = 'px'

    def _get_px(self):
        u"""No transforming or casting, just answer the self.v.

        >>> px(23).px
        23
        """
        return asIntOrFloat(self.v)
    px = property(_get_px)

#   Fr

def fr(v, *args, **kwargs):
    u = None
    base = kwargs.get('base', Fr.BASE)
    g = kwargs.get('g', 0) # Not used by Fr
    minV = kwargs.get('min')
    maxV = kwargs.get('max')
    if args: # If there are more arguments, bind them together in a list.
        v = [v]+list(args)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v:
            u.append(fr(uv, base=base, g=g, min=minV, max=maxV))
        u = tuple(u)
    elif isinstance(v, (int, float, RelativeUnit)):
        u = Fr(v, base=base, g=g, min=minV, max=maxV)
    elif isinstance(v, str):
        v = v.strip().lower()
        if v.endswith(Fr.UNIT):
            v = asNumberOrNone(v[:-2])
            if v is not None:
                u = Fr(v, base=base, g=g, min=minV, max=maxV)
        else: # Something else, recursively try again
            u = units(v, base=base, g=g, min=minV, max=maxV)
            assert isinstance(u, Fr) # Only makes sense for relative if the same.
    return u

class Fr(RelativeUnit):
    u"""fractional units, used in CSS-grid.
    https://gridbyexample.com/video/series-the-fr-unit/

    >>> units('5fr')
    5fr
    >>> fr(5)
    5fr
    >>> u = units('4fr', base=100)
    >>> u.isEm, u.isRelative
    (False, True)
    >>> u
    4fr
    >>> u/2
    2fr
    >>> u-0.5
    3.5fr
    >>> u.base = 100
    >>> u, pt(u) # Answer fr value as points, relative to base master value.
    (4fr, 25pt)
    """
    UNIT = 'fr'

    def _get_r(self):
        u"""Answer the rendered clipped value, clipped to the self.min and self.max local values.
        For absolute inits u.v and u.r are identical.
        For relative units u.v answers the clipped value and u.r answers the value rendered by self.base
        self.base can be a unit or a number.

        >>> u = Fr(2)
        >>> u.v
        2
        >>> u.min = 10
        >>> u.max = 20
        >>> u.v
        10
        """
        return asIntOrFloat(self.base / self.v)
    r = property(_get_r)

#   Col

def col(v, *args, **kwargs):
    u = None
    base = kwargs.get('base', Col.BASE)
    g = kwargs.get('g', Col.GUTTER)
    minV = kwargs.get('min')
    maxV = kwargs.get('max')
    if args: # If there are more arguments, bind them together in a list.
        v = [v]+list(args)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v:
            u.append(col(uv, base=base, g=g, min=minV, max=maxV))
        u = tuple(u)
    elif isinstance(v, (int, float, RelativeUnit)):
        u = Col(v, base=base, g=g, min=minV, max=maxV)
    elif isinstance(v, str):
        v = v.strip().lower()
        if v.endswith(Col.UNIT):
            v = asNumberOrNone(v[:-3])
            if v is not None:
                u = Col(v, base=base, g=g, min=minV, max=maxV)
        else: # Something else, recursively try again
            u = units(v, base=base, g=g, min=minV, max=maxV)
            assert isinstance(u, Col) # Only makes sense for relative if the same.
    return u

class Col(RelativeUnit):
    u"""Fraction of a width, including gutter calculation. Reverse of Fr.
    Gutter is default Col.GUTTER

    >>> units('0.25col')
    0.25col
    >>> col(1/2)
    0.5col
    >>> u = units('0.5col', base=100, g=8)
    >>> u.isEm, u.isRelative
    (False, True)
    >>> u
    0.5col
    >>> u/2
    0.25col
    >>> u-0.3
    0.2col
    >>> u.base = 500 # With of the column
    >>> u.g = 8
    >>> u, pt(u) # Answer col value as points, relative to base master value and gutter.
    (0.5col, 246pt)
    """
    UNIT = 'col'

    def _get_r(self):
        u"""Answer the rendered clipped value, clipped to the self.min and self.max local values.
        For absolute inits u.v and u.r are identical.
        For relative units u.v answers the clipped value and u.r answers the value rendered by self.base
        self.base can be a unit or a number.
        self.g can be a unit or a number

        >>> u = Col(1/2, base=mm(100), g=mm(4))
        >>> u.v
        0.5
        >>> u.r # (100 + 4)/2 - 4
        48mm
        """
        return asIntOrFloat((self.base + self.g) * self.v - self.g) # Calculate the fraction of base, reduced by gutter
    r = property(_get_r)

#   Em

def em(v, *args, **kwargs):
    u = None
    base = kwargs.get('base', EM_FONT_SIZE)
    g = kwargs.get('g', 0) # Default not used by Em
    minV = kwargs.get('min')
    maxV = kwargs.get('max')
    if args: # If there are more arguments, bind them together in a list.
        v = [v]+list(args)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v: # Recursively append
            u.append(em(uv, base=base, g=g, min=minV, max=maxV))
        u = tuple(u)
    elif isinstance(v, (int, float, RelativeUnit)):
        u = Em(v, base=base, g=g, min=minV, max=maxV)
    elif isinstance(v, str):
        v = v.strip().lower()
        if v.endswith(Em.UNIT):
            v = asNumberOrNone(v[:-2])
            if v is not None:
                u = Em(v, base=base, g=g, min=minV, max=maxV)
        else: # Something else, recursively try again
            u = units(v, base=base, g=g, min=minV, max=maxV)
            assert isinstance(u, Em) # Only makes sense for relative if the same.
    return u

class Em(RelativeUnit):
    u"""Em size is based on the current setting of the fontSize.
    Used in CSS export.

    >>> units('10em')
    10em
    >>> Em(10)
    10em
    >>> u = units('10em')
    >>> u.isEm and u.isRelative
    True
    >>> u
    10em
    >>> u/2
    5em
    >>> u-8
    2em
    >>> u.base = 12 # Caller can set the base reference value
    >>> pt(u)
    120pt
    >>> u.base = 24
    >>> pt(u)
    240pt
    >>> em(1, 2, 3, 4)
    (1em, 2em, 3em, 4em)
    """
    isEm = True
    UNIT = 'em'
    BASE_KEY = 'em' # Key in optional base of relative units.

    def _get_pt(self):
        u"""Answer the rendered value in pt. Base value for absolute unit values is ignored.
        self.base can be a unit or a number.

        >>> u = units('10em', base=12)
        >>> u, u.r # Answer the rendered value
        (10em, 120)
        >>> u.base = 8 # Alter the base em.
        >>> u # Full representation
        10em
        >>> u.base # Defined base for the em (often set in pt units)
        8pt
        >>> u.v # Clipped value of u._v
        10
        >>> u.r # Render to Pt instance
        80
        >>> u.pt # Render to points number
        80
        """
        return asIntOrFloat(pt(self.base * self.v).v) # Clip to min/max and factor to points
    def _set_pt(self, v):
        self._v = v / self.base
    pt = property(_get_pt, _set_pt)

#   Perc

def perc(v, *args, **kwargs):
    u"""Convert value v to a Perc instance or list or Perc instances.

    >>> u = perc(12, base=200)
    >>> u, u.base, u.v, u.r # Value and rendered value
    (12%, 200pt, 12, 24)
    >>> perc('10%', '11%', '12%', '13%') # Convert series of arguments to a list of Perc instances.
    (10%, 11%, 12%, 13%)
    """
    u = None
    base = kwargs.get('base')
    g = kwargs.get('g', 0) # Default not used by Perc
    minV = kwargs.get('min')
    maxV = kwargs.get('max')
    if args: # If there are more arguments, bind them together in a list.
        if not isinstance(v, (tuple, list)):
            v = [v]
        for arg in args:
            v.append(arg)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v:
            u.append(perc(uv, base=base, g=g, min=minV, max=maxV))
        u = tuple(u)
    elif isinstance(v, (int, float, RelativeUnit)):
        u = Perc(v, base=base, g=g, min=minV, max=maxV)
    elif isinstance(v, str):
        v = v.strip().lower()
        if v.endswith(Perc.UNITC): # %-character
            v = asNumberOrNone(v[:-1])
            if v is not None:
                u = Perc(v, base=base, g=g, min=minV, max=maxV)
        elif v.endswith(Perc.UNIT):
            v = asNumberOrNone(v[:-4])
            if v is not None:
                u = Perc(v, base=base, g=g, min=minV, max=maxV)
        else: # Something else, recursively try again
            u = units(v, base=base, g=g, min=minV, max=maxV)
            assert isinstance(u, Perc) # Only makes sense for relative if the same.
    return u

class Perc(RelativeUnit):
    u"""Answer the relative percentage unit, if parsing as percentage (ending with % order "perc").

    >>> units('100%')
    100%
    >>> perc(100) # Using the maker function
    100%
    >>> Perc(100) # Directly using the class constructor (no checking on validity of attributes done)
    100%
    >>> u = perc('100%')
    >>> u, u.r # Default base is 100pt
    (100%, 100)
    >>> u/2, (u/2).v, (u/2).r # Render to base of 100pt
    (50%, 50.0, 50)
    >>> u/10*2
    20%
    >>> u+21
    121%
    >>> u-30+0.51
    70.51%
    >>> units('66%', base=500).r # Render value towards base unit
    330
    >>> units('66%', base=mm(500)).r # Render value towards base unit
    330mm
    >>> Perc(1.2) + 1.2
    2.4%
    """
    BASE = 100 # Default "base reference for relative units."
    UNIT = 'perc'
    UNITC = '%'

    def __repr__(self):
        v = asIntOrFloat(self.v) # Clip to min/max
        if isinstance(v, int):
            return u'%d%%' % v
        return u'%s%%' % asFormatted(v)

    def _get_pt(self):
        u"""Answer the rendered value in pt. Base value for absolute unit values is ignored.

        >>> u = units('10%', base=120)
        >>> u, pt(u)
        (10%, 12pt)
        >>> u.pt # Render to point int value
        12
        """
        return asIntOrFloat(self.base.pt * self.v / self.BASE) # Clip to min/max and factor to points
    def _set_pt(self, v):
        self._v = v / self.base.pt * self.BASE
    pt = property(_get_pt)

UNIT_MAKERS = dict(px=px, pt=pt, mm=mm, inch=inch, p=p, pica=pica, em=em, fr=fr, col=col, perc=perc)
MAKER_UNITS = dict([[maker, unit] for unit, maker in UNIT_MAKERS.items()])
MAKERS = set((pt, px, mm, inch, p, em, fr, col, perc))
CLASS_MAKERS = {Pt:pt, Px:px, Mm:mm, Inch:inch, P:p, Pica:pica, Em:em, Fr:fr, Col:col, Perc:perc}

VALUE_UNIT = re.compile('[ \t]*([0-9.-]*)[ \t]*([a-zA-Z"%]*)[ \t]*')
UNIT_VALUE = re.compile('[ \t]*([a-zA-Z"%]*)[ \t]*([0-9.-]*)[ \t]*')
VALUE_PICA = re.compile('[ \t]*([0-9.-]*)[ \t]*(p[0-9.]*)[ \t]*')

def value2Maker(v):
    u"""Find maker function best matching v. If no unit/maker/class name can be found,
    then assume it is pt() requested. Answer the pair of (value, unitName).
    Otherwise answer None.

    >>> value2Maker('123pt') == pt
    True
    >>> value2Maker('123px') == px
    True
    >>> value2Maker('123') == pt
    True
    >>> value2Maker('123.45fr') == fr
    True
    >>> value2Maker('pt') == pt
    True
    >>> value2Maker(pt) == pt
    True
    >>> value2Maker(Pt) == pt
    True
    >>> value2Maker(Inch) == inch
    True
    >>> value2Maker(Col) == col
    True
    """
    maker = None
    if isinstance(v, (int, float)):
        maker = pt
    elif v in UNIT_MAKERS:
        maker = UNIT_MAKERS[v]
    elif v in CLASS_MAKERS:
        maker = CLASS_MAKERS[v]
    elif v in MAKERS:
        maker = v
    elif isUnit(v):
        maker = UNIT_MAKERS[V.UNIT]
    elif isinstance(v, str):
        v = v.lower()
        if v in UNIT_MAKERS:
            maker = UNIT_MAKERS[v]
        else:
            value, unit = VALUE_UNIT.findall(v)[0]
            if not value:
                unit, value = UNIT_VALUE.findall(v)[0]
            if value:
                if not unit:
                    unit = Pt.UNIT
                elif unit == Inch.UNITC: # '"'
                    unit = Inch.UNIT
                elif unit == Perc.UNITC: # '%'
                    unit = Perc.UNIT
            if unit in UNIT_MAKERS:
                maker = UNIT_MAKERS[unit]
    return maker

def units(v, maker=None, g=None, base=None, min=None, max=None, default=None):
    u"""If value is a string, then try to guess what type of units value is
    and answer the right instance. Answer None if not valid transformation could be done.

    >>> units('100%')
    100%
    >>> units('   80  perc  ') # Spaced are trimmed.
    80%
    >>> units('12pt')
    12pt
    >>> units('10"')
    10"
    >>> units('10 inch  ') # Trim any white space.
    10"
    >>> units('140mm')
    140mm
    >>> units('30pt')
    30pt
    >>> units('1.4em')
    1.4em
    >>> units('0.5col')
    0.5col
    >>> units(mm(5), default=0)
    5mm
    >>> units(mm('xyz'), default=pt(13)) # Use default if value cannot be evaluated.
    13pt
    >>> units(10, maker=p) # All types of makers work: method, name, class
    10p
    >>> units(10, maker='p')
    10p
    >>> units(10, maker=P)
    10p
    >>> units(12) # Default for plain number is pt if no class defined.
    12pt
    >>> units('SomethingElse') is None
    True
    >>> units('12pt', 'mm') # Altering maker units converts.
    4.23mm
    >>> units(mm(12), pt) # Casting to another unit type
    34.02pt
    >>> u1 = units('10pt')
    >>> u1 is units(u1) # Creates copy of u1
    False
    >>> uu = pt(0), 12, (pt(13), pt(14))
    >>> units(uu) # Create a recursive list of units
    (0pt, 12pt, (13pt, 14pt))
    """
    if isinstance(v, (list, tuple)):
        uu = []
        for vv in v:
            uu.append(units(vv, maker=maker, g=g, base=base, min=min, max=max))
        return tuple(uu)

    u = default
    makerF = value2Maker(maker)
    assert maker is None or makerF in MAKERS, ('Cannot find unit maker for "%s"' % maker)

    if isUnit(v):
        u = copy(v) # Make sure to copy, avoiding overwriting local values of units.
        if maker is not None:
            u = makerF(u, g=g, base=base, min=min, max=max)
    elif v is not None:
        # Plain values are interpreted as point Units
        if makerF is None:
            makerF = value2Maker(v)
        # makerF is now supposed to be a maker or real Unit class, use it
        if makerF:
            u = makerF(v, g=g, base=base, min=min, max=max)

    # In case we got a valid unit, then try to set the paremeters if not None.
    if u is not None:
        if base is not None: # Base can be unit or number.
            u.base = base # Recursive force base to be unit instance
        if g is not None: # Optional gutter can be unit or number
            u.g = g # Recursive force gutter to be unit instance.

    if u is None and default is not None:
        u = units(default, g=g, base=base, min=min, max=max)
    return u # If possible to create, answer u. Otherwise result is None


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
