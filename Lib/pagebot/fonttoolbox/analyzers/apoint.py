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
#     apoint.py
#
import weakref

class APoint:
    """Analyzer Point, used if addition information (like its type) needs to be
    stored. Otherwise just use the point2D() and point3D() which are simple
    tuples.
    Note that the values are plain numbers in font.info.unitsPerEm, not PabeBot units.

    >>> p = APoint((101, 303), True)
    >>> p.onCurve is False
    False
    >>> print(p)
    APoint(101,303,On)
    """

    def __init__(self, xyz, onCurve=True, glyph=None, index=None):
        self.glyph = glyph # Set the weakref by property
        self.index = index # Index of this point in glyph.points
        self.p = list(xyz or [])
        while len(self.p) < 3:
            self.p.append(0)
        self.onCurve = bool(onCurve)

    def __getitem__(self, i):
        u"""Allow APoint to x and y attributes to be indexed like a point2D tuple.

        >>> ap = APoint((100, 200))
        >>> ap, ap[0], ap[1]
        (APoint(100,200,On), 100, 200)
        """
        return self.p[i]

    def __setitem__(self, i, value):
        u"""Allow APoint to x and y attributes to be indexed like a point2D or point3D tuple.

        >>> ap = APoint((100, 200))
        >>> ap[1] = 222
        >>> ap, ap[0], ap[1]
        (APoint(100,222,On), 100, 222)
        """
        self.p[i] = value

        # Update the changed point value in the glyph.
        glyph = self.glyph
        if glyph is not None and self.index is not None: # Glyph still alive? Then update x or y
            x, y = glyph.coordinates[self.index]
            if i == 0:
                glyph.coordinates[self.index] = value, y
            elif i == 1:
                glyph.coordinates[self.index] = x, value
            # Ignore setting of z
            glyph.dirty = True

    def _get_onCurve(self):
        return self._onCurve
    def _set_onCurve(self, onCurve):
        self._onCurve = onCurve
        # Update the changed point value in the glyph.
        glyph = self.glyph
        if glyph is not None and self.index is not None: # Still alive, then update glyph points too.
            glyph.flags[self.index] = bool(onCurve)
            glyph.dirty = True
    onCurve = property(_get_onCurve, _set_onCurve)

    def __lt__(self, p):
        u"""Compare the points.

        >>> APoint((100, 200)) < APoint((200, 300))
        True
        >>> APoint((100, 200)) < APoint((100, 300))
        True
        >>> APoint((100, 200)) < APoint((100, 200))
        False
        """
        return self.p < p.p

    def __le__(self, p):
        u"""Compare the points.

        >>> APoint((100, 200)) <= APoint((200, 300))
        True
        >>> APoint((100, 200)) <= APoint((100, 300))
        True
        >>> APoint((100, 200)) <= APoint((100, 200))
        True
        >>> APoint((100, 200)) <= APoint((100, 199))
        False
        """
        return self.p <= p.p

    def __gt__(self, p):
        u"""Compare the points.

        >>> APoint((200, 100)) > APoint((100, 300))
        True
        >>> APoint((200, 200)) > APoint((200, 100))
        True
        >>> APoint((200, 100)) > APoint((200, 99))
        True
        >>> APoint((200, 100)) > APoint((200, 100))
        False
        """
        return self.p > p.p

    def __ge__(self, p):
        u"""Compare the points.

        >>> APoint((200, 100)) >= APoint((100, 300))
        True
        >>> APoint((200, 200)) >= APoint((200, 100))
        True
        >>> APoint((200, 100)) >= APoint((200, 100))
        True
        >>> APoint((200, 100)) >= APoint((200, 101))
        False
        """
        return self.p >= p.p

    def __sub__(self, p):
        u"""Subtract the points. Result is a point3D tuple.

        >>> APoint((200, 500)) - APoint((100, 300))
        (100, 200, 0)
        >>> APoint((200, 500, 10)) - APoint((100, 300))
        (100, 200, 10)
        >>> APoint((200, 500, 10)) - APoint((-100, -300, -100))
        (300, 800, 110)
        """
        return self.p[0] - p[0], self.p[1] - p[1], self.p[2] - p[2]

    def __add__(self, p):
        u"""Add the points. Result is a point3D tuple.

        >>> APoint((200, 500)) + APoint((100, 300))
        (300, 800, 0)
        >>> APoint((200, 500, 10)) + APoint((100, 300))
        (300, 800, 10)
        >>> APoint((200, 500, 10)) + APoint((-100, -300, -100))
        (100, 200, -90)
        """
        return self.p[0] + p[0], self.p[1] + p[1], self.p[2] + p[2]

    def __mul__(self, v):
        u"""Multiply the point by a scalar. Result is a point3D tuple.

        >>> APoint((200, 500)) * 2
        (400, 1000, 0)
        >>> APoint((200, 500, 10)) * 2
        (400, 1000, 20)
        """
        assert isinstance(v, (int, float))
        return self.p[0] * v, self.p[1] * v, self.p[2] * v

    def __div__(self, v):
        u"""Divide the point by a scalar. Result is a point3D tuple.

        >>> APoint((200, 500)) / 2
        (100, 250, 0)
        >>> APoint((200, 500, 10)) / 2
        (100, 250, 5)
        """
        assert isinstance(v, (int, float))
        return int(round(self.p[0] / v)), int(round(self.p[1] / v)), int(round(self.p[2] / v))

    __truediv__ = __div__

    def _get_x(self):
        u"""APoint.x property. Using indexed addressing of self.p to trigger
        Glyph point update.

        >>> ap = APoint((200, 500))
        >>> ap.x = 100
        >>> ap, ap.x
        (APoint(100,500,On), 100)
        """
        return self.p[0]
    def _set_x(self, x):
        self[0] = x # Indirect by index, triggers the update of the glyph point data.
    x = property(_get_x, _set_x)

    def _get_y(self):
        u"""APoint.y property. Using indexed addressing of self.p to trigger
        Glyph point update.

        >>> ap = APoint((200, 500))
        >>> ap.y = 100
        >>> ap, ap.y
        (APoint(200,100,On), 100)
        """
        return self.p[1]
    def _set_y(self, y):
        self[1] = y # Indirect by index, triggers the update of the glyph data.
    y = property(_get_y, _set_y)

    def _get_z(self):
        u"""APoint.z property. Not really used by the analyzers, it is there
        for compatibility reasons, as all positions in PageBot are 3D.

        >>> ap = APoint((200, 500, 700))
        >>> ap.z = 100
        >>> ap, ap.z
        (APoint(200,500,100,On), 100)
        """
        return self.p[2]
    def _set_z(self, z):
        self[2] = z # No equivalent in the glyph. Ignore.
    z = property(_get_z, _set_z)

    def _get_glyph(self):
        """Answers the parent glyph, if the weakref is still allive."""
        if self._glyph is not None:
            return self._glyph()
        return None
    def _set_glyph(self, glyph):
        if glyph is not None:
            self._glyph = weakref.ref(glyph)
        else:
            self._glyph = None
    glyph = property(_get_glyph, _set_glyph)

    def __repr__(self):
        s = '%s(%s,%s' % (self.__class__.__name__, self.x, self.y)
        if int(self.z):
            s += ',%s' % int(self.z)
        return s + ',%s)' % ({True:'On', False:'Off'}[self.onCurve])

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
