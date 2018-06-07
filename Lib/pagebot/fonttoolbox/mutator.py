#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#       from https://github.com/fonttools/fonttools/
#                                   blob/master/Lib/fontTools/varLib/mutator.py
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#    mutator.py
#
from fontTools.varLib.models import supportScalar, normalizeLocation
from fontTools.varLib import _DesignspaceAxis, _GetCoordinates
from fontTools.misc.fixedTools import floatToFixedToFloat
from fontTools.varLib.iup import iup_delta
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates

def glyphMutator(glyph, location, axes):
    u"""Answer the list of interpolated point, avoiding the need to make
    a new Variable Font etc. if we only need fast mutated points for a
    single glyph.

    >>> from pagebot.fonttoolbox.objects.font import findFont
    >>> vf = findFont('RobotoDelta-VF')
    >>> vf
    <Font RobotoDelta-VF>
    >>> coordinates = glyphMutator(vf['H'], dict(wght=210), vf.axes)
    >>> coordinates[0]
    (170.0, 0.0)
    """
    varFont = glyph.font.ttFont

    loc = normalizeLocation(location, axes)
    if 'avar' in varFont:
        maps = varFont['avar'].segments
        loc = {k:_DesignspaceAxis._map(v, maps[k]) for k,v in loc.items()}
    # Quantize to F2Dot14, to avoid surprise interpolations.
    loc = {k:floatToFixedToFloat(v, 14) for k,v in loc.items()}
    # Location is normalized now
    #log.info("Normalized location: %s", loc)

    #log.info("Mutating glyf/gvar tables")
    gvar = varFont['gvar']
    glyf = varFont['glyf']
    variations = gvar.variations[glyph.name]
    coordinates,_ = _GetCoordinates(varFont, glyph.name)
    origCoords, endPts = None, None
    for var in variations:
        scalar = supportScalar(loc, var.axes)
        if not scalar: continue
        delta = var.coordinates
        if None in delta:
            if origCoords is None:
                origCoords,control = _GetCoordinates(varFont, glyph.name)
                endPts = control[1] if control[0] >= 1 else list(range(len(control[1])))
            delta = iup_delta(delta, origCoords, endPts)
        coordinates += GlyphCoordinates(delta) * scalar
    return coordinates


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
