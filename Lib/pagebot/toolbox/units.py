#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
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
#     units # Basic contextual converter and interpretor
#
#     Absolute units
#     Millimeters MM = 0.0393701 * INCH
#     mm, Mm       Millimeters
#     cm, Cm       Centimeters
#     p, P         Picas 1/6"
#     pt, Pt       Points 1/72"
#     inch, Inch   Full inch
#
#     Relative units, using base and gutter as reference
#     em, Em       Relative to e.fontSize as base
#     perc, Perc   Relative to 100%
#     fr, Fr       Fraction columns for CSS-grid, without gutter
#     col, Col     Same as fr, using gutter. Works vertical as rows as well.
#     px, Px       Equal to points (for now)
#
#     Angle
#     radian       Radians angle
#     degrees      Degrees angle
#
import re, sys, math
from copy import copy

INCH = 72
MM = 0.0393701 * INCH # Millimeters as points. E.g. 3*MM --> 8.5039416 pt.

# Basic layout measures
U = 6 # Some basic unit grid to use as default.
EM_FONT_SIZE = U*2 # 12pt
BASELINE_GRID = U*2+3 # 2.5U = 15pt

from pagebot.toolbox.transformer import asNumberOrNone, asIntOrFloat, asFormatted

# P O I N T

def point3D(p=None):
    """Answers `p` as a 3D point. If it already is a list of 3 elements, then
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
    """Answers the 2D point from a 2D or 3D point.

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
    """Answers new 3D point, shifted by offset.

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
    """Answers the point as string of units. Ignore `z`-value if it renders to
    0.

    >>> point2S(pt(22.4, 33.5, 44.6))
    '22.4pt 33.5pt 44.6pt'
    >>> point2S(pt(33.6, 44.7))
    '33.6pt 44.7pt'
    """
    x, y, z = point3D(p)
    if z.rv:
        return '%s %s %s' % (x, y, z)
    return '%s %s' % (x, y)

def point2roundedS(p):
    """Answers the point as string of rounded units. Ignore `z`-value if it
    renders to 0.

    >>> point2roundedS(pt(22.4, 33.5, 44.6))
    '22 34 45'
    >>> point2roundedS(pt(33.6, 44.7))
    '34 45'
    """
    x, y, z = point3D(p)
    if z.rv:
        return '%d %d %d' % (x.rounded, y.rounded, z.rounded)
    return '%d %d' % (x.rounded, y.rounded)

def ru(u, *args, **kwargs):
    """Render to uu.ru or (u1.ru, u2.ru, ...) if uu is a list or tuple.
    If maker is defined, then use that to render towards.

    >>> ru(pt(100), pt(120)) # Absolute inits, nothing changes.
    (100pt, 120pt)
    >>> ru(pt(100), 121, (p(5), p(6), units('5"')), maker=pt) # All cast to pt
    (100pt, 121pt, (60pt, 72pt, 360pt))
    >>> ru(pt(60), 121, (p(5), p(6), units('5"')), maker=p) # Render units
    (5p, 121p, (5p, 6p, 30p))
    >>> ru(mm(10), mm(20), (mm(30), mm(40)), maker=mm) # Render units
    (10mm, 20mm, (30mm, 40mm))
    >>> ru(pt(60), 121, maker=p)
    (5p, 121p)
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
            uu = uu.ru
        return uu

def rv(u, *args, **kwargs):
    """Render to uu.rv or (u1.rv, u2.rv, ...) if uu is a list or tuple.
    If maker is defined, then use that to render towards.

    >>> rv(pt(100), pt(120)) # Absolute inits, nothing changes.
    (100, 120)
    >>> rv(pt(100), 121, (p(5), p(6), units('5"')), maker=pt) # All cast to pt
    (100, 121, (60, 72, 360))
    >>> rv(pt(60), 121, (p(5), p(6), units('5"')), maker=p) # Render units
    (5, 121, (5, 6, 30))
    >>> rv(mm(10), mm(20), (mm(30), mm(40)), maker=mm) # Render units
    (10, 20, (30, 40))
    >>> rv(pt(60), 121, maker=p)
    (5, 121)
    """
    if args:
        if not isinstance(u, (list, tuple)):
            u = [u]
        for arg in args:
            u.append(arg)

    if isinstance(u, (list, tuple)):
        ruu = []
        for uu in u:
            uu = rv(uu, **kwargs)
            ruu.append(uu)
        return tuple(ruu)

    uu = units(u, **kwargs)
    if uu is not None:
        uu = uu.rv
    return uu

def upt(u, *args, **kwargs):
    """Render to pt value(s). If values are a number, then answer it unchanged.

    >>> upt(50, pt(100), pt(120), (10, pt(20)))
    (50, 100, 120, (10, 20))
    >>> upt(None)
    0
    >>> upt(em(1.4), base=30) # Render to a fontSize
    42
    >>> upt(('20%', '30%', '40%'), base=300) # Render to a percentage base
    (60, 90, 120)
    """
    if args:
        if not isinstance(u, (list, tuple)):
            u = [u]
        else:
            u = list(u)
        for arg in args:
            u.append(arg)

    if isinstance(u, (list, tuple)):
        ruu = []
        for uu in u:
            uu = upt(uu, **kwargs)
            ruu.append(uu)
        return tuple(ruu)

    if u is None:
        return 0

    if isinstance(u, (int, float)):
        return u

    uu = units(u, **kwargs)
    if uu is not None:
        uu = uu.pt
    return uu

def isUnits(u, *args):
    """Answers is u (and all of the other items in the argument list)
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
    """Answers if u is an instance of Unit.

    >>> isUnit(pt(20))
    True
    >>> isUnit(pt(20, 21))
    False
    >>> isUnit(2)
    False
    """
    # isinstance(u, Unit) # Does not seem to work right for units created in other sources such as A4
    return hasattr(u, 'v') and hasattr(u, 'g') and hasattr(u, 'base')

def uRound(u, *args):
    """Answers the list with rounded units (and all of the other items in the argument list)
    are a Unit instance.

    >>> uRound(Em(2.3))
    2em
    >>> uRound(4.2)
    4pt
    >>> uRound(2, 2.4, pt(14.4), (20.9, pt(19.8)))
    [2pt, 2pt, 14pt, [21pt, 20pt]]
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
    """Answers the class of the Unit instance. Otherwise answer None.

    >>> u = Em(2)
    >>> classOf(u) is Em
    True
    """
    if isUnit(u):
        return u.__class__
    return None

def uString(u, maker=None):
    """Answers the unit `u` as a string. In case it is not a Unit instance,
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

class Unit:
    """Base class for units, implementing most of the logic.  Unit classes can
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
        >>> u, u.ru, u.rv # Respectively: instance to str, rendered to u.base as 20% of pt(440)
        (20%, 88pt, 88)
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
        >>> u = units('100mm')
        >>> u.v, u.ru # Respectively: Raw value, rendered (in case relative)
        (100, 100mm)
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

    def __init__(self, v=0, base=None, g=0):
        assert isinstance(v, (int, float)) # Otherwise do a cast first as pt(otherUnit)
        self.v = v
        # Base can be a unit value, ot a dictionary, where self.UNIT is the key.
        # This way units(...) can decide on the type of unit, where the base has multiple entries.
        if base is None:
            base = self.BASE
        self.base = base # Default base value for reference by relative units.
        self.g = g # Default gutter for reference by relative units. Ignored by absolute units.

    def _get_name(self):
        """Answers the unit name.

        >>> pt(123).name
        'Pt'
        >>> mm(234).name
        'Mm'
        """
        return self.__class__.__name__
    name = property(_get_name)

    def _get_rounded(self):
        """Answers a new instance of self with rounded value.
        Note that we are rounding the self.v here, not the rendered result.

        >>> u = pt(12.2)
        >>> u, u.v, u.rv # Stored as float value
        (12.2pt, 12.2, 12.2)
        >>> ru = u.rounded # Create new pt-unit
        >>> u, ru, ru.v, ru.rv # Did not change original u
        (12.2pt, 12pt, 12, 12)
        """
        u = copy(self)
        u.v = int(round(self.v))
        return u
    rounded = property(_get_rounded)

    def __repr__(self):
        v = asIntOrFloat(self.v)
        if isinstance(v, int):
            return '%d%s' % (v, self.name.lower())
        return '%s%s' % (asFormatted(v), self.name.lower())

    def asNormalizedJSON(self):
        """Answer self as normalized JSON-compatible dict.

        >>> d = pt(200).asNormalizedJSON()
        >>> d['class_'], d['v'], d['base']
        ('Pt', 200, 'None')
        >>> d = em(200, base=24).asNormalizedJSON()
        >>> d['class_'], d['v'], d['base']['v']
        ('Em', 200, 24)
        """
        from pagebot.toolbox.transformer import asNormalizedJSON
        return dict(class_=self.__class__.__name__, v=self.v, base=asNormalizedJSON(self.base), g=self.g)

    def _get_pt(self):
        """Answers the value in *pt*. Base value for absolute unit
        values is ignored.

        >>> p(1).pt
        12
        >>> pt(1), pt(1).pt # Render value cast to pt
        (1pt, 1)
        >>> 10 + inch(1).pt + 8 # Rendered to a pt-units, so 10 and 8 behave as pt numbers.
        90
        >>> (10 + inch(1) + 8).pt # Using reversed __radd__, then rendered and cast to pt-unit.
        1368
        >>> mm(1).pt
        2.8346472
        >>> inch(1).pt
        72
        """
        return asIntOrFloat(self.rv * self.PT_FACTOR) # Factor to points
    def _set_pt(self, v):
        self.v = v / self.PT_FACTOR
    pt = property(_get_pt, _set_pt)

    def _get_px(self):
        """Answers the value in *px*. Base value for absolute unit values
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
        u"""Answers the rendered value, translated to inch via pt.

        >>> u = pt(72)
        >>> u.pt, u.inch
        (72, 1)
        >>> int(round(cm(2.54).inch))
        1
        """
        return asIntOrFloat(self.pt/Inch.PT_FACTOR)
    inch = property(_get_inch)

    def _get_p(self):
        u"""Answers the rendered value, translated to Pica via pt.

        >>> 2 * pt(12).p # Rendered and cast to picas
        2
        >>> inch(5).p
        30
        """
        return asIntOrFloat(self.pt/P.PT_FACTOR)
    p = property(_get_p)

    def _get_cm(self):
        u"""Answers the rendered value, translated to cm via pt.

        >>> int(round(pt(595).cm)) # Rendered and cast to cm
        21
        >>> inch(5).cm == pt(5*72).cm
        True
        >>> mm(50).cm
        5
        """
        return asIntOrFloat(self.pt/Cm.PT_FACTOR)
    cm = property(_get_cm)

    def _get_mm(self):
        u"""Answers the rendered value, translated to mm via pt.

        >>> int(round(4 * pt(12).mm)) # Rendered and cast to picas
        17
        >>> int(round(inch(5).mm))
        127
        >>> cm(5).mm
        50
        """
        return asIntOrFloat(self.pt/Mm.PT_FACTOR)
    mm = property(_get_mm)

    def _get_rv(self):
        """Answers the rendered unit value for absolute values.

        >>> u = Inch(2)
        >>> u.rv
        2
        """
        return asIntOrFloat(self.v)
    def _set_rv(self, v):
        """Set the raw unit value, same as self.v = v for absolute values.

        >>> u = Inch(2)
        >>> u.rv = 3
        >>> u.v
        3
        """
        self.v = v
    rv = property(_get_rv, _set_rv)

    def _get_ru(self):
        u"""For absolute units the rendering toward units is just a copy of self.

        >>> u = inch(3)
        >>> u.ru, u == u.ru, u is u.ru
        (3", True, False)
        """
        return copy(self)
    ru = property(_get_ru)

    def __int__(self):
        """Answers self as rounded int, rendered and converted to points.

        >>> int(pt(20.2))
        20
        """
        return asIntOrFloat(round(self.pt))

    def __float__(self):
        """Answers self as float, rendered and converted to points.

        >>> float(pt(20.2))
        20.2
        """
        return float(self.pt)

    def __round__(self):
        """Answers the rounded self as value.

        >>> u = pt(12.4)
        >>> u.rounded
        12pt
        >>> round(u)
        12pt
        >>> u = pt(12.51)
        >>> u.rounded
        13pt
        >>> round(u)
        13pt
        """
        return self.rounded

    def __bool__(self):
        u"""Answers the boolean representation of self, if self.rv renders to 0.

        >>> bool(pt(0))
        False
        >>> bool(pt(100))
        True
        """
        return bool(self.rv)

    def __coerce__(self, v):
        """Converts to type of v.

        >>> '%dpoints' % pt(10)
        '10points'
        """
        if isinstance(v, (int, float)):
            return self, pt(v)
        return self, units(v)

    def __abs__(self):
        """Answers an absolute-value copy of self.

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
        """Answers the boolean result how self compares to rendered u.

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
            return self.rv == u
        if isUnit(u):
            if isinstance(u, self.__class__):
                return self.rv == u.rv # Same class, compare rendered result may differe from base)
            return self.pt == u.pt # Incompatible unit types, compare via points
        return False

    def __ne__(self, u):
        """Answers the boolean result how self compares to rendered u.

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
            return self.rv != u
        if isUnit(u):
            if isinstance(u, self.__class__):
                return self.rv != u.rv
            return self.pt != u.pt # Incompatible unit types, compare via points
        return True

    def __le__(self, u):
        """Answers the boolean result how self compares to rendered u.

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
            return self.rv <= u
        if isUnit(u):
            if isinstance(u, self.__class__):
                return self.rv <= u.rv
            return self.pt <= u.pt # Incompatible unit types, compare via points
        return False

    def __lt__(self, u):
        """Answers the boolean result how self compares to rendered u.

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
            return self.rv < u
        if isUnit(u):
            if isinstance(u, self.__class__):
                return self.rv < u.rv
            return self.pt < u.pt # Incompatible unit types, compare via points
        return False

    def __ge__(self, u):
        """Answers the boolean result how self compares to rendered u.

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
            return self.rv >= u
        if isUnit(u):
            if isinstance(u, self.__class__):
                return self.rv >= u.rv
            return self.pt >= u.pt # Incompatible unit types, compare via points
        return False

    def __gt__(self, u):
        """Answers the boolean result how self compares to rendered u.

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
            return self.rv > u
        if isUnit(u):
            if isinstance(u, self.__class__):
                return self.rv > u.rv
            return self.pt > u.pt # Incompatible unit types, compare via points
        return False

    def __add__(self, u):
        """Adds self to `u`, creating a new Unit instance with the same type
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
        >>> p(1) + pt(12) + '1p6'
        3p6

        """
        u0 = copy(self) # Keep values of self
        if isinstance(u, str):
            u = units(u)
            if u is None:
                raise ValueError('Cannot add "%s" to "%s"' % (self, u))
        if isinstance(u, (int, float)): # One is a scalar, just add
            u0.v += u
        elif u0.__class__ == u.__class__:
            u0.v += u.v # Same class, just add.
        elif isUnit(u):
            u0.pt += u.pt # Adding units, calculate via points
        else:
            raise ValueError('Cannot add "%s" to "%s"' % (self, u))
        return u0

    __radd__ = __add__

    def __sub__(self, u):
        """Subtracts `u` from self, creating a new Unit instance with the same
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
            u0.v -= u.v # Same class, just subtract.
        elif isUnit(u):
            u0.pt -= u.pt # Subtracting units, calculate via points
        else:
            raise ValueError('Cannot subtract "%s" from "%s"' % (u, self))
        return u0

    def __rsub__(self, u):
        """Subtract in reversed order.

        >>> 30 - pt(10) # Thanks to implementation of __rsub__ the reverse also works.
        20pt
        """
        return -self + u

    def __div__(self, u):
        """Divide self by u, creating a new Unit instance with the same type
        as self.  Unit / Unit creates a float number.

        >>> u = units('60pt')
        >>> u / 2 # Create a new Unit instance of the same type
        30pt
        >>> asFormatted(u / mm(1.5)) # Unit / Unit create ratio float number
        '14.11'
        >>> u / units('120pt') # Unit / Unit create a float ratio number.
        0.5
        >>> pt(10)/pt(5)
        2.0
        """
        u0 = copy(self) # Keep values of self
        if isinstance(u, (int, float)): # One is a scalar, just divide
            assert u, ('Zero division "%s/%s"' % (u0, u))
            u0.v /= u # Just divide.
        elif isUnit(u):
            upt = u.pt
            assert upt, ('Zero division "%s/%s"' % (u0, u))
            u0 = u0.pt / upt # Dividing units, create ratio float number.
        else:
            raise ValueError('Cannot divide "%s" by "%s"' % (u0, u))
        return u0

    __itruediv__ = __truediv__ = __div__

    def __rdiv__(self, u):
        """Dividing non-unit creates a copy of self with value u/self.v

        >>> 200 / pt(20)
        10pt
        >>> 185.0 / pt(20)
        9.25pt
        """
        u0 = copy(self)
        if not self.v:
            raise ValueError('Cannot divide "%s" by "%s"' % (u, self.v))
        u0.v = u / self.v
        return u0

    __rtruediv__ = __rdiv__

    def __mul__(self, u):
        """Multiply self by u, creating a new Unit instance with the same type
        as self. Units can only be multiplied by numbers. Unit * Unit raises a
        ValueError.

        >>> u = units('60pt')
        >>> u * 2 # Create a new Unit instance of the same type
        120pt
        >>> 10 * mm(10) # Thanks to implementation of __rmul__ the reverse also works.
        100mm
        >>> pt(100) * 0.8
        80pt
        """
        u0 = copy(self) # Keep original values of self
        if isinstance(u, (int, float)): # One is a scalar, just multiply
            u0.v *= u # Just multiply
        elif isUnit(u) and u.isEm:
            u0.base = u.r
            u0 = u0.r
        else:
            raise ValueError('Cannot multiply "%s" by "%s" of class %s' % (u0, u, u.__class__.__name__))
        return u0

    # Order of multiplication doesn't matter, except for the resulting unit type.
    __rmul__ = __mul__

    def __neg__(self):
        """Reverse sign of self, answer as copied unit.

        >>> -pt(-20)
        20pt
        >>> -pt(20) - pt(10)
        -30pt
        """
        u = copy(self) # Keep values of self
        u.v = -self.v
        return u

    def byBase(self, base):
        """Not implemented for non-relative units"""
        raise ValueError('Cannot calculate non-relative "%s" unit "%s" by base "%s" ' % (self.__class__.__name__, self.v, base))

#   Mm

def mm(v, *args, **kwargs):
    u = None
    if args: # If there are more arguments, bind them together in a list.
        v = [v]+list(args)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v:
            u.append(mm(uv))
        u = tuple(u)
    elif isinstance(v, (int, float)):
        u = Mm(v)
    elif isUnit(v):
        u = Mm() # New Mm and convert via pt
        u.pt = v.pt
    elif isinstance(v, str):
        v = v.strip().lower()
        if v.endswith(Mm.UNIT):
            v = asNumberOrNone(v[:-2])
            if v is not None:
                u = Mm(v)
        else: # Something else, try again.
            u = mm(units(v))
    return u

class Mm(Unit):
    """Answers the mm instance.

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
        """Just answer the self.rv value.

        >>> mm(5).mm
        5
        >>> 10 * mm(5).mm
        50
        """
        return self.rv
    mm = property(_get_mm)

#   Cm

def cm(v, *args, **kwargs):
    u = None
    if args: # If there are more arguments, bind them together in a list.
        v = [v]+list(args)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v:
            u.append(cm(uv))
        u = tuple(u)
    elif isinstance(v, (int, float)):
        u = Cm(v)
    elif isUnit(v):
        u = Cm() # New Cm and convert via pt
        u.pt = v.pt
    elif isinstance(v, str):
        v = v.strip().lower()
        if v.endswith(Cm.UNIT):
            v = asNumberOrNone(v[:-2])
            if v is not None:
                u = Cm(v)
        else: # Something else, try again.
            u = cm(units(v))
    return u

class Cm(Unit):
    """Answers the mm instance.

    >>> u = Cm(210)
    >>> u
    210cm
    >>> u = cm('29.7cm') # A4
    >>> u
    29.7cm
    >>> u/2
    14.85cm
    >>> u-10
    19.7cm
    >>> u+10
    39.7cm
    >>> u.v # Raw value of the Unit instance
    29.7
    >>> isinstance(u.v, (int, float))
    True
    >>> pt(u).rounded # Rounded A4 --> pts
    842pt
    >>> cm(10, 11, 12) # Multiple arguments create a list of tuple mm
    (10cm, 11cm, 12cm)
    >>> cm((10, 11, 12, 13)) # Arguments can be submitted as list or tuple
    (10cm, 11cm, 12cm, 13cm)
    >>> cm(pt(50), p(6), '3"') # Arguments can be a list of other units types.
    (1.76cm, 2.54cm, 7.62cm)
    """
    PT_FACTOR = MM*10 # mm <---> points
    UNIT = 'cm'

    def _get_cm(self):
        """Just answer the self.rv value.

        >>> cm(5).cm
        5
        >>> 10 * cm(5).cm
        50
        """
        return self.rv
    cm = property(_get_cm)

#   Pt

def pt(v, *args, **kwargs):
    u = None

    if args: # If there are more arguments, bind them together in a list.
        v = [v]+list(args)

    if isinstance(v, (tuple, list)):
        u = []
        for uv in v:
            u.append(pt(uv))
        u = tuple(u)

    elif isinstance(v, (int, float)): # Simple value as input, use class
        u = Pt(v)
    elif isUnit(v): # It's already a Unit instance, convert via points.
        u = Pt(v.pt)
    elif isinstance(v, str): # Value is a string, interpret from unit extension.
        v = v.strip().lower()
        if v.endswith(Pt.UNIT):
            v = asNumberOrNone(v[:-2])
            if v is not None:
                u = Pt(asIntOrFloat(v))
        else: # Something else, recursively try again, force to pt.
            u = pt(units(v))

    return u

class Pt(Unit):
    """pt is the base unit size of all PageBot measures.

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
        """Just answer the self.rv.

        >>> pt(12).pt
        12
        """
        return self.rv
    def _set_pt(self, v):
        self.v = v
    pt = property(_get_pt, _set_pt)

#   P(ica)

def p(v, *args, **kwargs):
    """Create a new instance of P, using v as source value. In case v is already
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
    if args: # If there are more arguments, bind them together in a list.
        v = [v]+list(args)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v:
            u.append(p(uv))
        u = tuple(u)
    elif isinstance(v, (int, float)):
        u = P(v)
    elif isUnit(v):
        u = P() # Make new Pica and convert via pt
        u.pt = v.pt
    elif isinstance(v, str):
        v = v.strip().lower().replace('pica', P.UNIT)
        if not 'pt' in v: # Hack to avoid confusion with '10pt')
            vv = VALUE_PICA.findall(v)
            if vv:
                v0 = asNumberOrNone(vv[0][0] or '0')
                v1 = asNumberOrNone(vv[0][1][1:] or '0')
                if v0 is not None and v1 is not None:
                    u = P()
                    u.pt = v0*P.PT_FACTOR+v1
            else:
                u = p(units(v))
        else: # Something else, recursively try again.
            u = p(units(v))
    return u

class P(Unit):
    """P (pica) class.

    >>> u = P(2)
    >>> u.v, u.rv # Same value for absolute values
    (2, 2)
    >>> u = p(1)
    >>> u, u+2, u+pt(2), u+pt(100), u*5, u/2
    (1p, 3p, 1p2, 9p4, 5p, 0p6)
    >>> p('2.5p') # Fraction of pica, not points. Translates to 2p6
    2p6
    """
    PT_FACTOR = 12  # 12 points = 1p
    UNIT = 'p'

    def _get_p(self):
        """No transforming or casting, just answer the self.v.

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
    if args: # If there are more arguments, bind them together in a list.
        v = [v]+list(args)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v:
            u.append(inch(uv))
        u = tuple(u)
    elif isinstance(v, (int, float)):
        return Inch(v)
    elif isUnit(v):
        u = Inch() # New Inch and convert via pt
        u.pt = v.pt
    elif isinstance(v, str):
        v = v.strip().lower()
        if v.endswith(Inch.UNITC): # "-character
            v = asNumberOrNone(v[:-1])
            if v is not None:
                u = Inch(v)
        elif v.endswith(Inch.UNIT):
            v = asNumberOrNone(v[:-4])
            if v is not None:
                u = Inch(v)
        else: # Something else, recursively try again.
            u = inch(units(v))
    return u

class Inch(Unit):
    """Inch 72 * the base unit size of all PageBot measures.

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
        """No transforming or casting, just answer the self.rv.

        >>> inch(6).inch
        6
        >>> inch(7.0).inch
        7
        """
        return self.rv
    inch = property(_get_inch)

    def __repr__(self):
        v = asIntOrFloat(self.v)
        if isinstance(v, int):
            return '%d%s' % (v, self.UNITC)
        return '%0.2f%s' % (v, self.UNITC)

class Formula(Unit):
    """Unit class that contains a sequence of other units and rules how to apply them.
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

    def __init__(self, v=0, base=None, g=0, f=None, units=None):
        Unit.__init__(self, v=v, base=base, g=g)
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
    """Abstract class to avoid artihmetic between absolute and relative units.
    Needs absolute reference to convert to absolute units.

    >>> u = units('12%')
    >>>
    """
    BASE = 1 # Default "base reference for relative units."
    GUTTER = U*2 # Used as default gutter measure for Col units.
    BASE_KEY = 'base' # Key in optional base of relative units.
    isAbsolute = False # Cannot do arithmetic with absolute Unit instances.
    isRelative = True

    def _get_rv(self):
        """Answers the rendered value of self.
        The value is based on the type of self. For absolute units the result of u.v and u.r is identical.
        For relative units u.v answers the value and u.r answers the value rendered by self.base.
        self.base can be another unit or a dictionary of base unit values.

        >>> u = Inch(2)
        >>> u.v, u.rv
        (2, 2)
        """
        return asIntOrFloat((self.base * self.v / self.BASE).rv)
    rv = property(_get_rv)

    def _get_ru(self):
        """Answers the rendered value of self, by units type of self.base.
        For absolute units the result of u.v and u.r is identical.
        For relative units u.v answers the value and u.r answers the value rendered by self.base.
        self.base can be another unit or a dictionary of base values.

        >>> uBase = Inch(24)
        >>> uBase
        24"
        >>> u = perc(20, base=uBase)
        >>> u, u.v, u.ru, u.rv
        (20%, 20, 4.80", 4.8)
        """
        return self.base * self.v / self.BASE
    ru = property(_get_ru)

    def _get_pt(self):
        """Answers the rendered value in pt.

        >>> u = fr(2, base=12)
        >>> u, u.pt
        (2fr, 6)
        >>> u = p(12)
        >>> u.pt
        144
        """
        return asIntOrFloat(pt(self.ru).rv) # Render value and cast to points
    pt = property(_get_pt)

    def _get_mm(self):
        """Answers the rendered value in mm.

        >>> u = fr(2, base=mm(10))
        >>> u, u.mm, mm(u)
        (2fr, 5, 5mm)
        """
        return asIntOrFloat(mm(self.ru).rv) # Rendered value and cast to mm
    mm = property(_get_mm)

    def _get_p(self):
        """Answers the rendered value in picas.

        >>> u = fr(2, base=p(12))
        >>> u, u.p
        (2fr, 6)
        >>> u = units('75%', base=p(72))
        >>> u, u.p, p(u)
        (75%, 54, 54p)
        """
        return asIntOrFloat(p(self.ru).rv) # Rendered value and factor to mm
    p = property(_get_p)

    def _get_inch(self):
        """Answers the rendered value in inch.

        >>> fr(2, base='4"').inch
        2
        >>> fr(2, base=inch(10)).inch
        5
        >>> units('25%', base=inch(10)).inch
        2.5
        """
        return asIntOrFloat(inch(self.ru).rv) # Rendered value and factor to mm
    inch = property(_get_inch)

    def _get_base(self):
        """Optional base value as reference for relative units. Save as Unit instance.

        >>> u = perc('10%', base=300)
        >>> u, u.base, u.ru, u.rv, u.v
        (10%, 300pt, 30pt, 30, 10)
        >>> u = units('20%', base=mm(200))
        >>> u, u.base, u.ru, u.rv, u.v # unit, base of %, rendered unit, rendered value
        (20%, 200mm, 40mm, 40, 20)
        >>> u.pt, u.rv, u.ru, u.v # Value in pt of 20% of 200pt
        (113.385888, 40, 40mm, 20)
        >>> u = units('5em', base=dict(em=pt(12), perc=pt(50)))
        >>> u.pt # Rendered to base selection pt(12)
        60
        >>> u = units('25%', base='36p')
        >>> u, u.base, u.v, u.rv, u.ru, u.p, u.pt, u.inch
        (25%, 36p, 25, 9, 9p, 9, 108, 1.5)
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

    def byBase(self, base):
        """Answer the rendered value with base instead of self._base)

        >>> u = em(1.4, base=20)
        >>> u.base
        20pt
        >>> u.pt
        28
        >>> u.byBase(100)
        140.0
        """
        return base * self.v

    def _get_g(self):
        """Optional gutter value as reference for relative units. Save as Unit instance.

        >>> u = col(0.25, base=mm(200), g=mm(6))
        >>> u.base, u.g # Show unit base and gutter
        (200mm, 6mm)
        >>> u.g = mm(8) # Set gutter
        >>> #FIX u.mm # (200 + 8)/4 - 8 --> 44 + 8 + 44 + 8 + 44 + 8 + 44 = 200
        44
        >>> from pagebot.constants import A4
        >>> margin = 15
        >>> u = col(0.5, base=A4[0]-2*margin, g=mm(8))
        >>> u, u.ru, u.rv
        (0.5col, 90mm, 86mm)
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
    if args: # If there are more arguments, bind them together in a list.
        v = [v]+list(args)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v:
            u.append(px(uv, base=base, g=g))
        u = tuple(u)
    elif isinstance(v, (int, float, RelativeUnit)):
        u = Px(v, base=base, g=g)
    elif isinstance(v, str):
        v = v.strip().lower()
        if v.endswith(Px.UNIT):
            v = asNumberOrNone(v[:-2])
            if v is not None:
                u = Px(v, base=base, g=g)
        else: # Something else, recursively try again
            u = units(v, base=base, g=g)
            assert isinstance(u, Px) # Only makes sense for relative if the same.
    return u

class Px(RelativeUnit):
    """Answers the px (pixel) instance.

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
        """No transforming or casting, just answer the self.v.

        >>> px(23).px
        23
        """
        return self.rv
    px = property(_get_px)

#   Fr

def fr(v, *args, **kwargs):
    """Fractional units, used in CSS-grid.

    >>> u = fr(3, base=300)
    >>> u, u.rv, upt(u)
    (3fr, 100, 100)
    """
    u = None
    base = kwargs.get('base', Fr.BASE)
    g = kwargs.get('g', 0) # Not used by Fr
    if args: # If there are more arguments, bind them together in a list.
        v = [v]+list(args)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v:
            u.append(fr(uv, base=base, g=g))
        u = tuple(u)
    elif isinstance(v, (int, float, RelativeUnit)):
        u = Fr(v, base=base, g=g)
    elif isinstance(v, str):
        v = v.strip().lower()
        if v.endswith(Fr.UNIT):
            v = asNumberOrNone(v[:-2])
            if v is not None:
                u = Fr(v, base=base, g=g)
        else: # Something else, recursively try again
            u = units(v, base=base, g=g)
            assert isinstance(u, Fr) # Only makes sense for relative if the same.
    return u

class Fr(RelativeUnit):
    """Fractional units, used in CSS-grid.
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

    def _get_rv(self):
        """Answers the rendered value.
        For absolute inits u.v and u.rv are identical.
        For relative units u.v answers the value and u.r answers the value rendered by self.base
        self.base can be a unit or a number.

        >>> u = Fr(2, base=mm(10))
        >>> u.v, u.rv, u.ru, u.mm
        (2, 5mm, 5mm, 5)
        >>> u = Fr(4, base=100)
        >>> u.v, u.rv, u.ru, u.pt
        (4, 25, 25pt, 25)
        """
        return asIntOrFloat(self.base / self.v)
    rv = property(_get_rv)

    def _get_ru(self):
        """Answers the rendered unit.
        For absolute inits u and u.ru are identical.
        For relative units u.rv answers the value and u.ru answers the value rendered by self.base
        self.base can be a unit or a number.

        >>> u = Fr(2, base=mm(10))
        >>> u.v, u.rv, u.ru, u.mm
        (2, 5mm, 5mm, 5)
        >>> u = Fr(4, base=100)
        >>> u.v, u.rv, u.ru, u.pt
        (4, 25, 25pt, 25)
        """
        return self.base / self.v
    ru = property(_get_ru)

#   Col

def col(v, *args, **kwargs):
    u = None
    base = kwargs.get('base', Col.BASE)
    g = kwargs.get('g', Col.GUTTER)
    if args: # If there are more arguments, bind them together in a list.
        v = [v]+list(args)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v:
            u.append(col(uv, base=base, g=g))
        u = tuple(u)
    elif isinstance(v, (int, float, RelativeUnit)):
        u = Col(v, base=base, g=g)
    elif isinstance(v, str):
        v = v.strip().lower()
        if v.endswith(Col.UNIT):
            v = asNumberOrNone(v[:-3])
            if v is not None:
                u = Col(v, base=base, g=g)
        else: # Something else, recursively try again
            u = units(v, base=base, g=g)
            assert isinstance(u, Col) # Only makes sense for relative if the same.
    return u

class Col(RelativeUnit):
    """Fraction of a width, including gutter calculation. Reverse of Fr.
    Gutter is default Col.GUTTER

    >>> u = col(1/4, base=mm(200), g=mm(6)) # Width of 1/4 width column.
    >>> u.base, u.g # Show unit base and gutter
    (200mm, 6mm)
    >>> u.g = mm(8) # Set gutter
    >>> #FIX u.mm # (200 + 8)/4 - 8 --> 44 + 8 + 44 + 8 + 44 + 8 + 44 = 200
    44
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
    >>> u, pt(u) # TODO: CHECK ANSWER. Answer col value as points, relative to base master value and gutter.
    (0.5col, 250pt)
    """
    UNIT = 'col'

    def _get_rv(self):
        """Answers the rendered value.
        For absolute inits u.v and u.r are identical.
        For relative units u.v answers the value and u.r answers the value rendered by self.base
        self.base can be a unit or a number.
        self.g can be a unit or a number

        >>> u = Col(1/2, base=mm(100), g=mm(4))
        >>> u.v, u.rv # (100 + 4)/2 - 4
        (0.5, 48mm)
        """
        return asIntOrFloat((self.base + self.g) * self.v - self.g) # Calculate the fraction of base, reduced by gutter
    rv = property(_get_rv)

#   Em

def em(v, *args, **kwargs):
    u = None
    base = kwargs.get('base', EM_FONT_SIZE)
    g = kwargs.get('g', 0) # Default not used by Em
    if args: # If there are more arguments, bind them together in a list.
        v = [v]+list(args)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v: # Recursively append
            u.append(em(uv, base=base, g=g))
        u = tuple(u)
    elif isinstance(v, (int, float, RelativeUnit)):
        u = Em(v, base=base, g=g)
    elif isinstance(v, str):
        v = v.strip().lower()
        if v.endswith(Em.UNIT):
            v = asNumberOrNone(v[:-2])
            if v is not None:
                u = Em(v, base=base, g=g)
        else: # Something else, recursively try again
            u = units(v, base=base, g=g)
            assert isinstance(u, Em) # Only makes sense for relative if the same.
    return u

class Em(RelativeUnit):
    """Em size is based on the current setting of the fontSize.
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
        """Answers the rendered value in pt. Base value for absolute unit values is ignored.
        self.base can be a unit or a number.

        >>> u = units('10em', base=12)
        >>> u, u.rv # Answer the rendered value
        (10em, 120)
        >>> u.base = 8 # Alter the base em.
        >>> u # Full representation
        10em
        >>> u.base # Defined base for the em (often set in pt units)
        8pt
        >>> u.v # Raw stored value
        10
        >>> u.rv # Render to Pt value
        80
        >>> u.ru # Render to Pt instance
        80pt
        >>> u.pt # Render to points numbe value
        80
        """
        return asIntOrFloat(pt(self.base * self.v).v) # Render and factor to points
    def _set_pt(self, v):
        self.v = v / self.base
    pt = property(_get_pt, _set_pt)

#   Perc

def perc(v, *args, **kwargs):
    """Convert value v to a Perc instance or list or Perc instances.

    >>> u = perc(20, base=pt(440))
    >>> u, u.ru, u.rv, u.v
    (20%, 88pt, 88, 20)
    >>> u = perc(12, base=240)
    >>> perc('10%', '11%', '12%', '13%') # Convert series of arguments to a list of Perc instances.
    (10%, 11%, 12%, 13%)
    """
    u = None
    base = kwargs.get('base')
    g = kwargs.get('g', 0) # Default not used by Perc
    if args: # If there are more arguments, bind them together in a list.
        if not isinstance(v, (tuple, list)):
            v = [v]
        for arg in args:
            v.append(arg)
    if isinstance(v, (tuple, list)):
        u = []
        for uv in v:
            u.append(perc(uv, base=base, g=g))
        u = tuple(u)
    elif isinstance(v, (int, float, RelativeUnit)):
        u = Perc(v, base=base, g=g)
    elif isinstance(v, str):
        v = v.strip().lower()
        if v.endswith(Perc.UNITC): # %-character
            v = asNumberOrNone(v[:-1])
            if v is not None:
                u = Perc(v, base=base, g=g)
        elif v.endswith(Perc.UNIT):
            v = asNumberOrNone(v[:-4])
            if v is not None:
                u = Perc(v, base=base, g=g)
        else: # Something else, recursively try again
            u = units(v, base=base, g=g)
            assert isinstance(u, Perc) # Only makes sense for relative if the same.
    return u

class Perc(RelativeUnit):
    """Answers the relative percentage unit, if parsing as percentage (ending with % order "perc").

    >>> units('100%')
    100%
    >>> perc(100) # Using the maker function
    100%
    >>> Perc(100) # Directly using the class constructor (no checking on validity of attributes done)
    100%
    >>> u = perc('100%')
    >>> u, u.ru, u.rv # Default base is 100pt
    (100%, 100pt, 100)
    >>> u/2, (u/2).v, (u/2).rv, (u/2).ru # Render to base of 100pt
    (50%, 50.0, 50, 50pt)
    >>> u/10*2
    20%
    >>> u+21
    121%
    >>> u-30+0.51
    70.51%
    >>> units('66%', base=500).rv # Render value towards base unit
    330
    >>> rv('66%', base=mm(500)) # Render value towards base unit
    330
    >>> units('66%', base=500).ru # Render towards base unit
    330pt
    >>> ru('66%', base=mm(500)) # Render unit towards base unit
    330mm
    >>> Perc(1.2) + 1.2
    2.4%
    """
    BASE = 100 # Default "base reference for relative units."
    UNIT = 'perc'
    UNITC = '%'

    def byBase(self, base):
        """Answer the rendered value with base instead of self._base)

        >>> u = perc(28, base=300)
        >>> u.base
        300pt
        >>> u.pt
        84
        >>> u.byBase(200)
        56.0
        """
        return base * self.v / 100

    def __repr__(self):
        v = asIntOrFloat(self.v)
        if isinstance(v, int):
            return u'%d%%' % v
        return u'%s%%' % asFormatted(v)

    def _get_pt(self):
        """Answers the rendered value in pt. Base value for absolute unit values is ignored.

        >>> u = units('10%', base=120)
        >>> u, pt(u)
        (10%, 12pt)
        >>> u.pt # Render to point int value
        12
        """
        return asIntOrFloat(self.base.pt * self.v / self.BASE) # Render and factor to points
    def _set_pt(self, v):
        self.v = v / self.base.pt * self.BASE
    pt = property(_get_pt)

UNIT_MAKERS = dict(px=px, pt=pt, mm=mm, inch=inch, p=p, pica=pica, em=em, fr=fr, col=col, perc=perc)
MAKER_UNITS = {maker: unit for unit, maker in UNIT_MAKERS.items()}
MAKERS = set((pt, px, mm, inch, p, em, fr, col, perc))
CLASS_MAKERS = {Pt:pt, Px:px, Mm:mm, Inch:inch, P:p, Pica:pica, Em:em, Fr:fr, Col:col, Perc:perc}

VALUE_UNIT = re.compile('[ \t]*([0-9.-]*)[ \t]*([a-zA-Z"%]*)[ \t]*')
UNIT_VALUE = re.compile('[ \t]*([a-zA-Z"%]*)[ \t]*([0-9.-]*)[ \t]*')
VALUE_PICA = re.compile('[ \t]*([0-9.-]*)[ \t]*(p[0-9.]*)[ \t]*')

def value2Maker(v):
    """Find maker function best matching v. If no unit/maker/class name can be
    found, then assume it is pt() requested. Answer the pair of (value,
    unitName). Otherwise answer None.

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
        maker = UNIT_MAKERS[v.UNIT]

    elif isinstance(v, str):
        v = v.lower()
        if v in UNIT_MAKERS:
            maker = UNIT_MAKERS[v]
        else:
            value, unitType = VALUE_UNIT.findall(v)[0]

            if not value:
                unitType, value = UNIT_VALUE.findall(v)[0]

            if value:
                if not unitType:
                    unitType = Pt.UNIT
                elif unitType == Inch.UNITC: # '"'
                    unitType = Inch.UNIT
                elif unitType == Perc.UNITC: # '%'
                    unitType = Perc.UNIT

            maker = UNIT_MAKERS.get(unitType, maker)
    return maker

def units(v, maker=None, g=None, base=None, default=None):
    """If value is a string, then try to guess what type of units value is and
    answer the right instance. Answer None if not valid transformation could be
    done.

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
            uu.append(units(vv, maker=maker, g=g, base=base))
        return tuple(uu)

    u = default
    makerF = value2Maker(maker)
    assert maker is None or makerF in MAKERS, ('Cannot find unit maker for "%s"' % maker)

    if isUnit(v):
        u = copy(v) # Make sure to copy, avoiding overwriting local values of units.
        if maker is not None:
            u = makerF(u, g=g, base=base)
    elif v is not None:
        # Plain values are interpreted as point Units
        if makerF is None:
            makerF = value2Maker(v)
        # makerF is now supposed to be a maker or real Unit class, use it
        if makerF:
            u = makerF(v, g=g, base=base)

    # In case we got a valid unit, then try to set the paremeters if not None.
    if u is not None:
        if base is not None: # Base can be unit or number.
            u.base = base # Recursive force base to be unit instance
        if g is not None: # Optional gutter can be unit or number
            u.g = g # Recursive force gutter to be unit instance.

    if u is None and default is not None:
        u = units(default, g=g, base=base)
    return u # If possible to create, answer u. Otherwise result is None

# Automatic angle conversion between degrees and radians.

def asin(v):
    """Answers a Radians instance, using math.asin(v)

    >>> a = degrees(0)
    >>> asin(a.sin)
    0rad
    >>> a = degrees(45)
    >>> abs(asin(a.sin) - 0.25) < 0.01
    True
    >>> a = degrees(90)
    >>> asin(a.sin)
    0.5rad
    >>> a = degrees(-90)
    >>> asin(a.sin)
    -0.5rad
    """
    return radians(math.asin(v)/math.pi)

def acos(v):
    """Answers a Radians instance, using math.acos(v)

    >>> a = degrees(0)
    >>> acos(a.cos)
    0.5rad
    >>> a = degrees(180)
    >>> acos(a.cos).degrees
    -90
    """
    return radians(math.asin(v)/math.pi)

def atan(v):
    """Answers a Radians instance, using math.atan(v)

    >>> a = degrees(0)
    >>> atan(a.tan)
    0rad
    >>> a = degrees(45)
    >>> atan(a.tan).degrees
    45
    """
    return radians(math.atan(v)/math.pi)

def atan2(v1, v2):
    """Answers a Radians instance, using math.atan2(v1, v2)

    >>> atan2(1, 1).degrees
    45
    >>> atan2(100, -100).degrees
    135
    >>> atan2(-100, 100).degrees
    -45
    """
    return radians(math.atan2(v1, v2)/math.pi)

class Angle:

    def __init__(self, angle):
        if isinstance(angle, float):
            if angle == round(angle):
                angle = int(angle)
        self.angle = angle

    def asNormalizedJSON(self):
        """Answer self as normalized JSON-compatible dict.

        >>> d = pt(200).asNormalizedJSON()
        >>> d['class_'], d['v'], d['base']
        ('Pt', 200, 'None')
        >>> d = em(200, base=24).asNormalizedJSON()
        >>> d['class_'], d['v'], d['base']['v']
        ('Em', 200, 24)
        """
        return dict(class_=self.__class__.__name__, angle=self.angle or 0)

    def __add__(self, angle):
        """Add two angles, using degrees as intermedia value.

        >>> degrees(45) + 5
        50deg
        >>> degrees(45) + radians(0.5)
        135deg
        >>> radians(0.5) + degrees(45)
        0.75rad
        >>> 5 + degrees(45)
        50deg
        """
        angle = self.angle + self.asValue(angle)
        if angle == round(angle):
            angle = int(angle)
        return self.__class__(angle) # Answer new Degrees instance

    __radd__ = __add__ # Additions work in both directions.

    def __sub__(self, angle):
        """Subtract two angles or angle and value, using degrees as intermedia value.

        >>> degrees(45) - 5
        40deg
        >>> degrees(45) - radians(0.5)
        -45deg
        >>> radians(0.5) - degrees(45)
        0.25rad
        """
        angle = self.angle - self.asValue(angle)
        if angle == round(angle):
            angle = int(angle)
        return self.__class__(angle) # Answer new instance

    def __rsub__(self, angle):
        """Reverse subtract value and angle, using degrees as intermedia value.

        >>> 5 - degrees(45)
        -40deg
        >>> 1 - radians(0.5)
        0.5rad
        """
        angle = self.asValue(angle) - self.angle
        if angle == round(angle):
            angle = int(angle)
        return self.__class__(angle) # Answer new instance

    def __mul__(self, factor):
        """Multiply the angle with a factor. Answer a new instance of the same type.

        >>> degrees(45) * 2
        90deg
        >>> degrees(45) * 0.5
        22.5deg
        >>> 3 * degrees(45)
        135deg
        """
        assert isinstance(factor, (int, float))
        angle = self.angle * factor
        if angle == round(angle):
            angle = int(angle)
        return self.__class__(angle)

    __rmul__ = __mul__ # Multiplications work in both directions

    def __div__(self, factor):
        """Divide the angle by a factor. Answer a new instance of the same type.

        >>> degrees(80) / 2
        40deg
        >>> degrees(45) / 0.5
        90deg
        >>> radians(0.5) / 2
        0.25rad
        """
        assert isinstance(factor, (int, float))
        angle = self.angle / factor
        if angle == round(angle):
            angle = int(angle)
        return self.__class__(angle)

    __truediv__ = __div__

    def __floordiv__(self, factor):
        """Fllor-divide the angle by a factor. Answer a new instance of the same type.

        >>> degrees(45) // 2
        22deg
        >>> degrees(45) // 0.5
        90deg
        >>> radians(2.2) // 2
        1rad
        """
        assert isinstance(factor, (int, float))
        return self.__class__(self.angle // factor)

    __itruediv__ = __floordiv__

    def __le__(self, a):
        """Test if self is less or equal to angle a or value a.

        >>> degrees(90) <= degrees(30)
        False
        >>> degrees(30) <= 90
        True
        >>> degrees(30) <= 30
        True
        >>> radians(0.5) <= radians(0.75)
        True
        >>> radians(0.25) <= 0.1
        False
        """
        if isinstance(a, Angle):
            return self.degrees <= a.degrees
        return self.angle <= a

    def __lt__(self, a):
        """Test if self is less than angle a or value a.

        >>> degrees(90) < degrees(30)
        False
        >>> degrees(30) < 90
        True
        >>> radians(0.5) < radians(0.75)
        True
        >>> radians(0.25) < 0.1
        False
        """
        if isinstance(a, Angle):
            return self.degrees < a.degrees
        return self.angle < a

    def __ge__(self, a):
        """Test if self is greater or equal to angle a or value a.

        >>> degrees(90) >= degrees(30)
        True
        >>> degrees(30) >= 90
        False
        >>> degrees(30) >= 30
        True
        >>> radians(0.5) >= radians(0.75)
        False
        >>> radians(0.25) >= 0.1
        True
        """
        if isinstance(a, Angle):
            return self.degrees >= a.degrees
        return self.angle >= a

    def __gt__(self, a):
        """Test if self is greater than angle a or value a.

        >>> degrees(90) > degrees(30)
        True
        >>> degrees(30) > 90
        False
        >>> degrees(30) > 30
        False
        >>> radians(0.5) > radians(0.75)
        False
        >>> radians(0.25) > 0.1
        True
        """
        if isinstance(a, Angle):
            return self.degrees > a.degrees
        return self.angle > a

    def __ne__(self, a):
        """Test if self not equal to angle a or value a.

        >>> degrees(90) != degrees(30)
        True
        >>> degrees(30) != 90
        True
        >>> degrees(30) != 30
        False
        >>> radians(0.5) != radians(0.75)
        True
        >>> radians(0.25) != 0.1
        True
        >>> radians(0.25) != 0.25
        False
        """
        if isinstance(a, Angle):
            return self.degrees != a.degrees
        return self.angle != a

    def __eq__(self, a):
        """Test if self not equal to angle a or value a.

        >>> degrees(90) == degrees(30)
        False
        >>> degrees(90) == degrees(90)
        True
        >>> degrees(90) == radians(0.5)
        True
        >>> degrees(30) == 90
        False
        >>> degrees(30) == 30
        True
        >>> radians(0.5) == radians(0.75)
        False
        >>> radians(0.25) == 0.1
        False
        >>> radians(0.25) == 0.25
        True
        """
        if isinstance(a, Angle):
            return self.degrees == a.degrees
        return self.angle == a

    def __neg__(self):
        """Reverse sign of self, answer as copied unit.

        >>> a = degrees(90)
        >>> -a
        -90deg
        >>> a = radians(0.5)
        >>> -a
        -0.5rad
        """
        return self.__class__(-self.angle)

    def __abs__(self):
        """Answers the absolute value as new instance.

        >>> a = degrees(-30)
        >>> abs(a)
        30deg
        >>> a = radians(-0.5)
        >>> abs(a)
        0.5rad
        """
        return self.__class__(abs(self.angle))


    def __int__(self):
        """Answers self as rounded int, rendered and converted to points.

        >>> int(degrees(30.5))
        30
        >>> float(radians(1))
        1.0
        """
        return int(self.angle)

    def __float__(self):
        """Answers self as float, rendered and converted to points.

        >>> float(degrees(30))
        30.0
        >>> float(radians(2))
        2.0
        """
        return float(self.angle)

    def __round__(self):
        """Answers the rounded self as value.

        >>> round(degrees(30.5))
        30deg
        """
        return self.__class__(round(self.angle))

    def __bool__(self):
        return bool(self.angle)

    # Math angle functions as properties

    def _get_sin(self):
        """Answers the math.sin(self) of this angle.
        See also asin(v) above, that answers an Angle instance.

        >>> degrees(0).sin
        0.0
        >>> degrees(90).sin
        1.0
        >>> degrees(45).sin == radians(0.25).sin
        True
        >>> degrees(-15).sin + radians(1/12).sin < 0.0001
        True
        >>> radians(8).sin < 1
        True
        """
        return math.sin(math.pi*self.radians)
    sin = property(_get_sin)

    def _get_cos(self):
        """Answers the math.cos(self) of this angle.
        See also acos(v) above, that answers an Angle instance.

        >>> degrees(0).cos
        1.0
        >>> degrees(90).cos < 1
        True
        >>> degrees(45).cos == radians(0.25).cos
        True
        >>> degrees(-15).cos - radians(1/12).cos
        0.0
        >>> radians(8).cos
        1.0
        """
        return math.cos(math.pi*self.radians)
    cos = property(_get_cos)

    def _get_tan(self):
        """Answers the math.tan(self) of this angle.
        See also atan2(v1, v2) above, that answers an Angle instance.

        >>> degrees(0).tan
        0.0
        >>> degrees(90).tan == radians(0.5).tan # Large number, instead of infinity?
        True
        >>> degrees(45).tan == radians(0.25).tan
        True
        >>> degrees(-15).tan + radians(1/12).tan < 1
        True
        >>> radians(8).tan < 1
        True
        """
        return math.tan(math.pi*self.radians)
    tan = property(_get_tan)

class Degrees(Angle):
    """Store the value as degrees.

    >>> from math import pi
    >>> a = degrees(30)
    >>> a
    30deg
    >>> a.degrees
    30
    >>> a = degrees(90)
    >>> a.degrees, a.radians
    (90, 0.5)
    >>> a + 30 - 15
    105deg
    >>> 20 + a # Reverse addition casts the number into degree value
    110deg
    >>> 120 - a
    30deg
    >>> a/2 # Create integer value for whole angles
    45deg
    >>> a/2.4
    37.5deg
    >>> a//3
    30deg
    """
    def __repr__(self):
        return '%sdeg' % self.angle

    def asValue(self, angle):
        u"""Answers the value of angle of the same type as self.

        >>> degrees(30).asValue(60)
        60
        >>> degrees(30).asValue(degrees(15))
        15
        >>> degrees(30).asValue(radians(0.5))
        90
        """
        if isinstance(angle, Angle):
            return angle.degrees
        return angle or 0

    def _get_degrees(self):
        return self.angle
    degrees = property(_get_degrees)

    def _get_radians(self):
        return math.radians(self.angle/math.pi)
    radians = property(_get_radians)

def degrees(angle):
    if isinstance(angle, Angle):
        angle = angle.degrees
    return Degrees(angle)

class Radians(Angle):
    """Store the value as radians factor to math.pi, so 0.5*pi is stored in self.angle as 0.5

    >>> from math import pi
    >>> a = radians(0.75)
    >>> a
    0.75rad
    >>> a.degrees, a.radians
    (135, 0.75)
    >>> a = radians(0)
    >>> a.degrees, a.radians
    (0, 0)
    >>> a = radians(0.5) # Add numbers in the context of the angle type.
    >>> a + 0.5 - 0.25
    0.75rad
    >>> 20 + a # Reverse addition casts the number into degree value
    20.5rad
    >>> 1.5 - a
    1rad
    >>> a/2 # Create integer value for whole angles
    0.25rad
    >>> -a
    -0.5rad
    """
    def __repr__(self):
        return '%srad' % self.angle

    def asValue(self, angle):
        u"""Answers the value of angle of the same type as self.

        >>> radians(0.5).asValue(0.75)
        0.75
        >>> radians(30).asValue(radians(0.33))
        0.33
        >>> radians(30).asValue(degrees(45))
        0.25
        """
        if isinstance(angle, Angle):
            return angle.radians
        return angle or 0

    def _get_degrees(self):
        angle = math.degrees(math.pi*self.angle)
        if angle == round(angle):
            angle = int(angle)
        return angle
    degrees = property(_get_degrees)

    def _get_radians(self):
        angle = self.angle
        if angle == round(angle):
            angle = int(angle)
        return angle
    radians = property(_get_radians)

def radians(angle):
    if isinstance(angle, Angle):
        angle = angle.radians.angle
    return Radians(angle)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
