# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     point.py
#
import weakref
from pagebot.toolbox.transformer import point3D

class APoint(object):
    """Analyzer Point, used if addition information (like its type) needs to be stored.
    Otherwise just use the point2D() and point3D() which are simple tuples.

    >>> p = APoint(101, 303, True)
    >>> p.onCurve is False
    False
    >>> print(p)
    Pt(101,303,On)
    """

    def __init__(self, xy, onCurve=True, glyph=None, index=None):
        self.glyph = glyph # Set the weakref by property
        self.index = index # Index of this point in glyph.points
        self.p = point3D(xy)
        self.onCurve = bool(onCurve)

    def __getitem__(self, i):
        """Allow APoint to x and y attributes to be indexed like a point2D tuple."""
        return self.p[i]
    def __setitem__(self, i, value):
        self.p[i] = value
        # Update the changed point value in the glyph.
        glyph = self.glyph
        if glyph is not None and self.index is not None: # Still alive, then update x or y
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
        if glyph is not None and self.index is not None: # Still alive, then update value.
            glyph.flags[self.index] = bool(onCurve)
            glyph.dirty = True
    onCurve = property(_get_onCurve, _set_onCurve)

    def __sub__(self, p):
        return self.p[0] - p[0], self.p[1] - p[1]

    def __add__(self, p):
        return self.p[0] + p[0], self.p[1] + p[1]

    def __mul__(self, v):
        return self.p[0] * v, self.p[1] * v

    def __div__(self, v):
        return self.p[0] / v, self.p[1] / v

    def _get_x(self):
        return self.p[0]
    def _set_x(self, x):
        self[0] = x # Indirect by index, triggers the update of the glyph point data.
    x = property(_get_x, _set_x)

    def _get_y(self):
        return self.p[1]
    def _set_y(self, y):
        self[1] = y # Indirect by index, triggers the update of the glyph data.
    y = property(_get_y, _set_y)

    def _get_z(self):
        return self.p[2]
    def _set_z(self, z):
        self[2] = z # No equivalent in the glyph. Ignore.
    z = property(_get_z, _set_z)

    def _get_glyph(self):
        """Answer the parent glyph, if the weakref is still allive."""
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
        return 'Pt(%s,%s,%s)' % (self.x, self.y,{True:'On', False:'Off'}[self.onCurve])
