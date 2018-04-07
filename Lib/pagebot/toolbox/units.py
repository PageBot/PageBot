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
#     U N D E R  D E V E L O P M E N T
#     (Needs case testing when generating CSS)
#
from pagebot.constants import MM
from pagebot.toolbox.transformer import asNumberOrNone

class Unit(object):
    u"""Base class for units, implementing most of the logic.

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
        >>> mm(12) + px(12)
        46.02mm
        >>> mm(12) + pt(5)
        39.02mm
        >>> perc(20) + 8
        28%
    """
    absolute = True
    def __init__(self, v=None, u=None):
        if v is not None: 
            self.u = v # Value is defined in this class units , convert internal to class units
        elif u is not None:
            self._v = u # Already in class units, keep value unchanged
        else:
            self._v = 0

    def _get_u(self): # Default px == pt == class units
        return self._v
    def _set_u(self, v):
        self._v = v or 0 # Assume that value is already class units
    u = property(_get_u, _set_u)

    pt = u

    def _get_css(self):
        # Assuming that px == pt == class inits
        u = self.u
        if int(round(u)) != self._v:
            return '%0.2fpx' % self._v
        return '%dpx' % self._v
    css = property(_get_css)
              
    def __repr__(self):
        u = self.u
        if int(round(u)) != u:
            return '%0.2f%s' % (u, self.__class__.__name__)
        return '%d%s' % (u, self.__class__.__name__)
   
    def __eq__(self, u):
        if isinstance(u, self.__class__):
            return self._v == u._v
        return self._v == u

    def __ne__(self, u):
        if isinstance(u, self.__class__):
            return self._v != u._v
        return self._v != u

    def __le__(self, u):
        if isinstance(u, self.__class__):
            return self._v <= u._v
        return self._v <= u

    def __lt__(self, u):
        if isinstance(u, self.__class__):
            return self._v < u._v
        return self._v < u

    def __ge__(self, u):
        if isinstance(u, self.__class__):
            return self._v >= u._v
        return self._v >= u

    def __gt__(self, u):
        if isinstance(u, self.__class__):
            return self._v > u._v
        return self._v > u

    def __add__(self, u):
        if isinstance(u, self.__class__):
            return self.__class__(u._v + self._v)
        if isinstance(u, (int, float)):
            return self.__class__(self._v + u)
        assert u.absolute == self.absolute, "Cannot add relative and absolute values"
        return self.__class__(u.pt + self.pt) # Supports mm(2) + pt(4) + inch(3)
        
    def __sub__(self, u):
        if isinstance(u, self.__class__):
            return self.__class__(u._v - self._v)
        if isinstance(u, (int, float)):
            return self.__class__(self._v - u)
        assert u.absolute == self.absolute, "Cannot subtract relative and absolute values"
        return self.__class__(pt=u.pt - self.pt)
        
    def __div__(self, u):
        if isinstance(u, self.__class__):
            return self.__class__(u._v / self._v)
        if isinstance(u, (int, float)):
            return self.__class__(self._v / u)
        assert u.absolute == self.absolute, "Cannot divide relative and absolute values"
        return self.__class__(pt=u.pt / self.pt)
        
    def __mul__(self, u):
        if isinstance(u, self.__class__):
            return self.__class__(u._v * self._v)
        if isinstance(u, (int, float)):
            return self.__class__(self._v * u)
        assert u.absolute == self.absolute, "Cannot multiply relative and absolute values"
        return self.__class__(u=u.pt * self.pt)
  
    def getValue(self, masterValue=None):
        u"""For non-relative values, answer the self._v unchanged."""
        return self._v

class mm(Unit):
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

    def _get_u(self):
        return self._v / MM
    def _set_u(self, v):
        self._v = v * MM
    u = property(_get_u, _set_u)

class px(Unit):
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
        
class pt(Unit):
    u"""pt is the base unit size of all PageBot measures. 

    >>> u = pt.make('0.4pt')
    >>> u
    0.40pt
    >>> u/2
    0.20pt
    >>> u-0.1
    0.30pt
    >>> u.getValue(100) # Answer fr value, relative to master value.
    0.4
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

#   Relative Units (e.g. for use in CSS)

class RelativeUnit(Unit):
    u"""Abstract class to avoid artihmetic between absolute and relative units.
    Needs absolute reference to convert to absolute units."""
    absolute = False # Cannot do arithmetic with absolute units.

    def _get_css(self):
        return str(self)
    css = property(_get_css)

    def getValue(self, masterValue):
        return self._v * masterValue

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
    >>> u.getValue(100) # Answer fr value, relative to master value.
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
    >>> u.getValue(12) # Answer em value, relative to master value.
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
    >>> u.getValue(500) # Answer percentage value relative to master value
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

    def getValue(self, masterValue):
        u"""Percentage has a different relative master calculation."""
        return self._v * masterValue / 100

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
    """
    for unitClass in UNIT_CLASSES:
        u = unitClass.make(v)
        if u is not None:
            return u
    return v


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
