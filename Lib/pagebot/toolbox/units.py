#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     units.py
#
#     Implements basic intelligent spacing units with build-in conversions.
#
from pagebot.constants import MM
from pagebot.toolbox.transformer import asNumberOrNone

class Unit(object):
    u"""Base class for units, implementing most of the logic.

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
    """
    absolute = True
    def __init__(self, v):
        self._v = v or 0

    def _get_css(self):
        # Assuming that px == pt == class inits
        if int(round(u)) != self._v:
            return '%0.2fpx' % self.px
        return '%dpx' % self.px
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
    u"""Answer the mm instance. 

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
            if v.endswith('mm'):
                v = asNumberOrNone(v[:-2])
                if v is not None:
                    return cls(v)
        return None

    def asPt(self, _=None):
        return self._v * MM
    @classmethod
    def fromPt(cls, pt):
        return cls(pt / MM)

class px(Unit):
    u"""Answer the px (pixel) instance. 

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
    u"""pt is the base unit size of all PageBot measures. 

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
            if v.endswith('pt'):
                v = asNumberOrNone(v[:-2])
                if v is not None:
                    return cls(v)
        return None

    def asPt(self, factor=1):
        return self._v * factor
    @classmethod
    def fromPt(cls, pt, factor=1):
        return cls(pt / factor)

#   Relative Units (e.g. for use in CSS)

class RelativeUnit(Unit):
    u"""Abstract class to avoid artihmetic between absolute and relative units.
    Needs absolute reference to convert to absolute units."""
    absolute = False # Cannot do arithmetic with absolute units.

    def _get_css(self):
        return str(self)
    css = property(_get_css)

    def asPt(self, masterValue):
        u"""Answer the value in points, relative to the master value."""
        return self._v * masterValue
    @classmethod
    def fromPt(cls, pt, masterValue):
        return cls(pt / masterValue)

class fr(RelativeUnit):
    u"""fractional units, used in CSS-grid. 
    https://gridbyexample.com/video/series-the-fr-unit/

    >>> u = fr.make(0.35)
    >>> u
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
    u"""Em size is based on the current setting of the fontSize. 
    Used in CSS export.

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
    u"""Answer the relative percentage unit, if parsing as percentage (ending with % order "perc").

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
    >>> u.asPoints(500) # Answer percentage value relative to master value
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
            if v.endswith('perc'):
                v = asNumberOrNone(v[:-4])
                if v is not None:
                    return cls(v)
        return None

    def asPoints(self, masterValue):
        u"""Convert to points. Percentage has a different relative master calculation."""
        return self._v * masterValue / 100


    def asPt(self, masterValue):
        u"""Convert to points. Percentage has a different relative master calculation."""
        return self._v * masterValue / 100
    @classmethod
    def fromPt(cls, pt, masterValue):
        return cls(pt / masterValue * 100)

    def __repr__(self):
        if isinstance(self._v, int):
            return '%d%%' % self._v
        return '%0.2f%%' % self._v

UNIT_CLASSES = (mm, px, pt, fr, em, perc)

def getUnits(v):
    u"""If value is a string, then try to guess what type of units value is 
    and answer the right instance.

    >>> getUnits('100%')
    100%
    >>> getUnits('80  perc  ')
    80%
    >>> getUnits('12pt')
    12pt
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
    if isinstance(v, (int, float)):
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
