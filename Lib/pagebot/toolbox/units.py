#!/usr/bin/env python
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
from pagebot.constants import MM, INCH
from pagebot.toolbox.transformer import asNumberOrNone

# Name and abbreviations
UNIT_PT = 'pt'
UNIT_MM = 'mm'
UNIT_PERC = 'perc'

class Unit(object):
    """Base class for units, implementing most of the logic.

        >>> mm(1)
        1mm
        >>> mm(10)*8
        80mm
        >>> fr(2) * fr(3)
        6fr
        >>> px(5) + 2
        7px
        >>> perc(12.4) + 4
        16.40%
        >>> # 3 + px(3) # Gives error. Reverse works
        >>> px(3) + 3
        6px
        >>> px(12) + px(10)
        22px
        >>> mm(10) + px(1)
        10.35mm
        >>> (mm(10) + mm(5)) * 2
        30mm
        >>> perc(20) + 8
        28%
        >>> inch(4), inch(4).asPt()
        (4", 288)
    """
    absolute = True
    def __init__(self, v):
        self._v = v or 0

    def _get_css(self):
        # Assuming that px == pt == class inits
        if int(round(self._v)) != self._v:
            return '%0.2fpx' % self.asPt()
        return '%dpx' % self.asPt()
    css = property(_get_css)

    def __repr__(self):
        if int(round(self._v)) != self._v:
            return '%0.2f%s' % (self._v, self.__class__.__name__)
        return '%d%s' % (self._v, self.__class__.__name__)

    def __eq__(self, u):
        if isinstance(u, self.__class__):
            return self._v == u._v
        assert self.absolute, "Cannot compare relative values %s == %s." % (self, u)
        if isinstance(u, (int, float)):
            return self._v == u
        assert u.absolute, "Cannot compare relative values %s == %s." % (self, u)
        return self.asPt() == u.asPt()

    def __ne__(self, u):
        if isinstance(u, self.__class__):
            return self._v != u._v
        assert self.absolute, "Cannot compare relative values %s != %s." % (self, u)
        if isinstance(u, (int, float)):
            return self._v != u
        assert u.absolute, "Cannot compare relative values %s != %s." % (self, u)
        return self.asPt() != u.asPt()

    def __le__(self, u):
        if isinstance(u, self.__class__):
            return self._v <= u._v
        assert self.absolute, "Cannot compare relative values %s <= %s." % (self, u)
        if isinstance(u, (int, float)):
            return self._v <= u
        assert u.absolute, "Cannot compare relative values %s <= %s." % (self, u)
        return self.asPt() <= u.asPt()

    def __lt__(self, u):
        if isinstance(u, self.__class__):
            return self._v < u._v
        assert self.absolute, "Cannot compare relative values %s < %s." % (self, u)
        if isinstance(u, (int, float)):
            return self._v < u
        assert u.absolute, "Cannot compare relative values %s < %s." % (self, u)
        return self.asPt() < u.asPt()

    def __ge__(self, u):
        if isinstance(u, self.__class__):
            return self._v >= u._v
        assert self.absolute, "Cannot compare relative values %s >= %s." % (self, u)
        if isinstance(u, (int, float)):
            return self._v >= u
        assert u.absolute, "Cannot compare relative values %s >= %s." % (self, u)
        return self.asPt() >= u.asPt()

    def __gt__(self, u):
        if isinstance(u, self.__class__):
            return self._v > u._v
        assert self.absolute, "Cannot compare relative values %s > %s." % (self, u)
        if isinstance(u, (int, float)):
            return self._v > u
        assert u.absolute, "Cannot compare relative values %s > %s." % (self, u)
        return self.asPt() > u.asPt()

    def __add__(self, u):
        if isinstance(u, self.__class__):
            return self.__class__(u._v + self._v)
        if isinstance(u, (int, float)):
            return self.__class__(self._v + u)
        assert u.absolute and self.absolute, "Cannot add relative values %s - %s" % (self, u)
        return self.__class__.fromPt(u.asPt() + self.asPt()) # Supports mm(2) + pt(4) + inch(3)

    def __sub__(self, u):
        if isinstance(u, self.__class__):
            return self.__class__(u._v - self._v)
        if isinstance(u, (int, float)):
            return self.__class__(self._v - u)
        assert u.absolute and self.absolute, "Cannot subtract relative values %s - %s" % (self, u)
        return self.__class__.fromPt(u.asPt() - self.asPt())

    def __div__(self, u):
        if isinstance(u, self.__class__):
            return self.__class__(u._v / self._v)
        if isinstance(u, (int, float)):
            return self.__class__(self._v / u)
        assert u.absolute and self.absolute, "Cannot divide relative values %s / %s" % (self, u)
        return self.__class__.fromPt(u.asPt() / self.asPt())

    def __mul__(self, u):
        if isinstance(u, self.__class__):
            return self.__class__(u._v * self._v)
        if isinstance(u, (int, float)):
            return self.__class__(self._v * u)
        assert u.absolute and self.absolute, "Cannot multiply relative values %s * %s" % (self, u)
        return self.__class__.fromPt(u.asPt() * self.asPt())

class mm(Unit):
    """Answer the mm instance.

    >>> u = mm.make(210)
    >>> u
    210mm
    >>> u = mm.make('297mm') # A4
    >>> u
    297mm
    >>> u/2
    148mm
    >>> u-100
    197mm
    >>> u+100
    397mm
    >>> u._v
    297
    >>> round(u.asPt()) # Rounded A4 --> pts
    842.0
    """

    @classmethod
    def make(cls, v):
        if isinstance(v, (int, float)):
            return cls(v)
        if isinstance(v, str):
            v = v.strip().lower()
            if v.endswith(UNIT_MM):
                v = asNumberOrNone(v[:-2])
                if v is not None:
                    return cls(v)
        return None

    def asPt(self, factor=MM):
        return self._v * factor
    @classmethod
    def fromPt(cls, pt, factor=MM):
        return cls(pt / factor)

class px(Unit):
    """Answer the px (pixel) instance.

    >>> u = px.make(0.2)
    >>> u
    0.20px
    >>> u = px.make('0.4px')
    >>> u
    0.40px
    >>> u/2
    0.20px
    >>> u-0.1
    0.30px
    >>> u.asPt(100) # Answer px value, relative to master value.
    40.0
    """

    @classmethod
    def make(cls, v):
        if isinstance(v, (int, float)):
            return cls(v)
        if isinstance(v, str):
            v = v.strip().lower()
            if v.endswith('px'):
                v = asNumberOrNone(v[:-2])
                if v is not None:
                    return cls(v)
        return None

    def asPt(self, factor=1):
        return self._v * factor
    @classmethod
    def fromPt(cls, pt, factor=1):
        return cls(pt / factor)

class pt(Unit):
    """pt is the base unit size of all PageBot measures.

    >>> u = pt.make(0.4)
    >>> u
    0.40pt
    >>> u = pt.make('0.4pt')
    >>> u
    0.40pt
    >>> u/2
    0.20pt
    >>> u-0.1
    0.30pt
    >>> u.asPt(100) # Answer pt value, relative to master value.
    40.0
    """
    @classmethod
    def make(cls, v):
        if isinstance(v, (int, float)):
            return cls(v)
        if isinstance(v, str):
            v = v.strip().lower()
            if v.endswith(UNIT_PT):
                v = asNumberOrNone(v[:-2])
                if v is not None:
                    return cls(v)
        return None

    def asPt(self, factor=1):
        return self._v * factor
    @classmethod
    def fromPt(cls, pt, factor=1):
        return cls(pt / factor)

class inch(Unit):
    """inch 72 * the base unit size of all PageBot measures.

    >>> getUnits('0.4"')
    0.40"
    >>> inch(0.4)
    0.40"
    >>> inch.make('0.4"')
    0.40"
    >>> u = inch.make('0.4inch')
    >>> u
    0.40"
    >>> u/2
    0.20"
    >>> u-0.1
    0.30"
    >>> u.asPt(100) # Answer pt value, relative to master value.
    40.0
    """
    @classmethod
    def make(cls, v):
        if isinstance(v, (int, float)):
            return cls(v)
        if isinstance(v, str):
            v = v.strip().lower()
            if v.endswith('"'):
                v = asNumberOrNone(v[:-1])
                if v is not None:
                    return cls(v)
            elif v.endswith('inch'):
                v = asNumberOrNone(v[:-4])
                if v is not None:
                    return cls(v)
        return None

    def asPt(self, factor=INCH):
        return self._v * factor
    @classmethod
    def fromPt(cls, pt, factor=INCH):
        return cls(pt / factor)

    def __repr__(self):
        if isinstance(self._v, int):
            return '%d"' % self._v
        return '%0.2f"' % self._v

#   Relative Units (e.g. for use in CSS)

class RelativeUnit(Unit):
    """Abstract class to avoid artihmetic between absolute and relative units.
    Needs absolute reference to convert to absolute units."""
    absolute = False # Cannot do arithmetic with absolute units.

    def _get_css(self):
        return str(self)
    css = property(_get_css)

    def asPt(self, masterValue):
        """Answer the value in points, relative to the master value."""
        return self._v * masterValue
    @classmethod
    def fromPt(cls, pt, masterValue):
        return cls(pt / masterValue)

class fr(RelativeUnit):
    """fractional units, used in CSS-grid.
    https://gridbyexample.com/video/series-the-fr-unit/

    >>> getUnits('0.35fr')
    0.35fr
    >>> fr.make(0.35)
    0.35fr
    >>> u = fr.make('0.4fr')
    >>> u
    0.40fr
    >>> u/2
    0.20fr
    >>> u-0.1
    0.30fr
    >>> u.asPt(100) # Answer fr value as points, relative to master value.
    40.0
    """
    @classmethod
    def make(cls, v):
        if isinstance(v, (int, float)):
            return cls(v)
        if isinstance(v, str):
            v = v.strip().lower()
            if v.endswith('fr'):
                v = asNumberOrNone(v[:-2])
                if v is not None:
                    return cls(v)
        return None

class em(RelativeUnit):
    """Em size is based on the current setting of the fontSize.
    Used in CSS export.

    >>> getUnits('10em')
    10em
    >>> em.make(10)
    10em
    >>> u = em.make('10em')
    >>> u
    10em
    >>> u/2
    5em
    >>> u-8
    2em
    >>> u.asPt(12) # Answer em value in points, relative to master value.
    120
    """
    @classmethod
    def make(cls, v):
        if isinstance(v, (int, float)):
            return cls(v)
        if isinstance(v, str):
            v = v.strip().lower()
            if v.endswith('em'):
                v = asNumberOrNone(v[:-2])
                if v is not None:
                    return cls(v)
        return None

class perc(RelativeUnit):
    """Answer the relative percentage unit, if parsing as percentage (ending with % order "perc").

    >>> getUnits('100%')
    100%
    >>> perc.make(100)
    100%
    >>> u = perc.make('100%')
    >>> u
    100%
    >>> u/2
    50%
    >>> u/10*2
    20%
    >>> u-30.5
    69.50%
    >>> u = perc.make('66%')
    >>> u.asPt(500) # Answer percentage value relative to master value
    330
    """
    @classmethod
    def make(cls, v):
        if isinstance(v, (int, float)):
            return cls(v)
        if isinstance(v, str):
            v = v.strip().lower()
            if v.endswith('%'):
                v = asNumberOrNone(v[:-1])
                if v is not None:
                    return cls(v)
            elif v.endswith(UNIT_PERC):
                v = asNumberOrNone(v[:-4])
                if v is not None:
                    return cls(v)
        return None

    def asPt(self, masterValue):
        """Convert to points. Percentage has a different relative master calculation."""
        return self._v * masterValue / 100
    @classmethod
    def fromPt(cls, pt, masterValue):
        return cls(pt / masterValue * 100)

    def __repr__(self):
        if isinstance(self._v, int):
            return '%d%%' % self._v
        return '%0.2f%%' % self._v

UNIT_CLASSES = (mm, px, pt, inch, fr, em, perc)

def getUnits(v):
    """If value is a string, then try to guess what type of units value is
    and answer the right instance.

    >>> getUnits('100%')
    100%
    >>> getUnits('80  perc  ')
    80%
    >>> getUnits('12pt')
    12pt
    >>> getUnits('10"')
    10"
    >>> getUnits('10 inch  ')
    10"
    >>> getUnits('140mm')
    140mm
    >>> getUnits('30pt')
    30pt
    >>> getUnits('1.4em')
    1.40em
    >>> getUnits(0.33)
    0.33
    >>> getUnits('SomethingElse')
    'SomethingElse'
    """
    if v is None or isinstance(v, (int, float)):
        return v
    for unitClass in UNIT_CLASSES:
        u = unitClass.make(v)
        if u is not None:
            return u
    return v

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
