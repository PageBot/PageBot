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
#     UseUnits.py
#
#     Implements basic intelligent spacing units with build-in conversions.
#
#     U N D E R  D E V E L O P M E N T
#     (Needs case testing when generating CSS)
#
INCH = 72
MM = 0.0393701 * INCH # Millimeters as points. E.g. 3*MM --> 8.5039416 pt.

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
        if isinstance(u, (int, float, long)):
            return self.__class__(u + self._v)
        assert u.absolute == self.absolute, "Cannot add relative and absolute values"
        return self.__class__(u.pt + self.pt) # Supports mm(2) + pt(4) + inch(3)
        
    def __sub__(self, u):
        if isinstance(u, self.__class__):
            return self.__class__(u._v - self._v)
        if isinstance(u, (int, float, long)):
            return self.__class__(u - self._v)
        assert u.absolute == self.absolute, "Cannot subtract relative and absolute values"
        return self.__class__(pt=u.pt - self.pt)
        
    def __div__(self, u):
        if isinstance(u, self.__class__):
            return self.__class__(u._v / self._v)
        if isinstance(u, (int, float, long)):
            return self.__class__(u / self._v)
        assert u.absolute == self.absolute, "Cannot divide relative and absolute values"
        return self.__class__(pt=u.pt / self.pt)
        
    def __mul__(self, u):
        if isinstance(u, self.__class__):
            return self.__class__(u._v * self._v)
        if isinstance(u, (int, float, long)):
            return self.__class__(u * self._v)
        assert u.absolute == self.absolute, "Cannot multiply relative and absolute values"
        return self.__class__(u=u.pt * self.pt)
        
class mm(Unit):

    def _get_u(self):
        return self._v / MM
    def _set_u(self, v):
        self._v = v * MM
    u = property(_get_u, _set_u)

class px(Unit):
    pass
        
class pt(Unit):
    pass

#   Relative  C S S  Units

class RelativeUnit(Unit):
    u"""Abstract class to avoid artihmetic between absolute and relative units.
    Needs absolute reference to convert to absolute units."""
    absolute = False # Cannot do arithmetic with absolute units.

    def _get_css(self):
        return str(self)
    css = property(_get_css)

class fr(RelativeUnit):
    u"""fractional units, used in CSS-grid. 
    https://gridbyexample.com/video/series-the-fr-unit/
    """
    pass
    
class em(RelativeUnit):
    u"""Em size is based on the current setting of the fontSize. 
    Used in CSS export."""
    pass

class perc(RelativeUnit):
    def __repr__(self):
        if isinstance(self._v, (int, long)):
            return '%d%%' % self._v
        return '%0.2f%%' % self._v



if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
