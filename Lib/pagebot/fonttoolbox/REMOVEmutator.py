#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#       from https://github.com/fonttools/fonttools/
#                                   blob/master/Lib/fontTools/varLib/mutator.py
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#    mutator.py
#
import os.path
from fontTools.misc.py23 import *
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.varLib import _GetCoordinates, _SetCoordinates

from fontTools.varLib.models import supportScalar, normalizeLocation
from pagebot.fonttoolbox.objects.font import Font
from pagebot.toolbox.transformer import path2FontName

def getMasterPath():
    """Answers the path to read master fonts. Default is at the same level as pagebot module.

    >>> getMasterPath().endswith('/Fonts/')
    True
    """
    #return '/'.join(pagebot.__file__.split('/')[:-2])+'/fonts/'
    from os.path import expanduser
    home = expanduser("~")
    return home + '/Fonts/'


def getInstancePath():
    """Answers the path to write instance fonts.

    >>> getInstancePath().endswith('/Fonts/_instances/')
    True
    """
    return getMasterPath() + '_instances/'


def _iup_segment(coords, rc1, rd1, rc2, rd2):
    # rc1 = reference coord 1
    # rd1 = reference delta 1
    out_arrays = [None, None]
    for j in 0,1:
        out_arrays[j] = out = []
        x1, x2, d1, d2 = rc1[j], rc2[j], rd1[j], rd2[j]


        if x1 == x2:
            n = len(coords)
            if d1 == d2:
                out.extend([d1]*n)
            else:
                out.extend([0]*n)
            continue

        if x1 > x2:
            x1, x2 = x2, x1
            d1, d2 = d2, d1

        # x1 < x2
        scale = (d2 - d1) / (x2 - x1)
        for pair in coords:
            x = pair[j]

            if x <= x1:
                d = d1
            elif x >= x2:
                d = d2
            else:
                # Interpolate
                d = d1 + (x - x1) * scale

            out.append(d)

    return zip(*out_arrays)


def _iup_contour(delta, coords):
    assert len(delta) == len(coords)
    if None not in delta:
        return delta

    n = len(delta)
    # indices of points with explicit deltas
    indices = [i for i,v in enumerate(delta) if v is not None]
    if not indices:
        # All deltas are None.  Return 0,0 for all.
        return [(0,0)]*n

    out = []
    it = iter(indices)
    start = next(it)
    if start != 0:
        # Initial segment that wraps around
        i1, i2, ri1, ri2 = 0, start, start, indices[-1]
        out.extend(_iup_segment(coords[i1:i2], coords[ri1], delta[ri1], coords[ri2], delta[ri2]))
    out.append(delta[start])
    for end in it:
        if end - start > 1:
            i1, i2, ri1, ri2 = start+1, end, start, end
            out.extend(_iup_segment(coords[i1:i2], coords[ri1], delta[ri1], coords[ri2], delta[ri2]))
        out.append(delta[end])
        start = end
    if start != n-1:
        # Final segment that wraps around
        i1, i2, ri1, ri2 = start+1, n, start, indices[0]
        out.extend(_iup_segment(coords[i1:i2], coords[ri1], delta[ri1], coords[ri2], delta[ri2]))

    assert len(delta) == len(out), (len(delta), len(out))
    return out


def _iup_delta(delta, coords, ends):
    assert sorted(ends) == ends and len(coords) == (ends[-1]+1 if ends else 0) + 4
    n = len(coords)
    ends = ends + [n-4, n-3, n-2, n-1]
    out = []
    start = 0
    for end in ends:
        end += 1
        contour = _iup_contour(delta[start:end], coords[start:end])
        out.extend(contour)
        start = end

    return out


def generateInstance(variableFontPath, location, targetDirectory, normalize=False, force=False):

    instanceName = ""

    for k, v in sorted(location.items()):
        # TODO better way to normalize the location name to (0, 1000)
        v = min(v, 1000)
        v = max(v, 0)
        instanceName += "-%s%s" % (k, v)
    targetFileName = '.'.join(variableFontPath.split('/')[-1].split('.')[:-1]) + instanceName + '.ttf'

    if not targetDirectory.endswith('/'):
        targetDirectory += '/'
    if not os.path.exists(targetDirectory):
        os.makedirs(targetDirectory)
    outFile = targetDirectory + targetFileName

    if force or not os.path.exists(outFile):
        #print(location)
        #print("Loading variable font")
        varFont = TTFont(variableFontPath)

        fvar = varFont['fvar']
        axes = {a.axisTag:(a.minValue,a.defaultValue,a.maxValue) for a in fvar.axes}
        # TODO Apply avar
        # TODO Round to F2Dot14?
        loc = normalizeLocation(location, axes)
        # Location is normalized now
        #print("Normalized location:", loc, 'from', location)

        # Set the instance name IDs in the name table
        platforms=((1, 0, 0), (3, 1, 0x409)) # Macintosh and Windows
        for platformID, platEncID, langID in platforms:
            familyName = varFont['name'].getName(1, platformID, platEncID, langID) # 1 Font Family name
            if not familyName:
                continue
            familyName = familyName.toUnicode() # NameRecord to unicode string
            styleName = unicode(instanceName) # TODO make sure this works in any case
            fullFontName = " ".join([familyName, styleName])
            postscriptName = fullFontName.replace(" ", "-")
            varFont['name'].setName(styleName, 2, platformID, platEncID, langID) # 2 Font Subfamily name
            varFont['name'].setName(fullFontName, 4, platformID, platEncID, langID) # 4 Full font name
            varFont['name'].setName(postscriptName, 6, platformID, platEncID, langID) # 6 Postscript name for the font
            # Other important name IDs
            # 3 Unique font identifier (e.g. Version 0.000;NONE;Promise Bold Regular)
            # 25 Variables PostScript Name Prefix

        gvar = varFont['gvar']
        glyf = varFont['glyf']
        # get list of glyph names in gvar sorted by component depth
        glyphnames = sorted(
            gvar.variations.keys(),
            key=lambda name: (
                glyf[name].getCompositeMaxpValues(glyf).maxComponentDepth
                if glyf[name].isComposite() else 0,
                name))
        for glyphname in glyphnames:
            variations = gvar.variations[glyphname]
            coordinates,_ = _GetCoordinates(varFont, glyphname)
            origCoords, endPts = None, None
            for var in variations:
                scalar = supportScalar(loc, var.axes)#, ot=True)
                if not scalar: continue
                delta = var.coordinates
                if None in delta:
                    if origCoords is None:
                        origCoords,control = _GetCoordinates(varFont, glyphname)
                        endPts = control[1] if control[0] >= 1 else list(range(len(control[1])))
                    delta = _iup_delta(delta, origCoords, endPts)
                coordinates += GlyphCoordinates(delta) * scalar
            _SetCoordinates(varFont, glyphname, coordinates)

        #print("Removing variable tables")
        for tag in ('avar','cvar','fvar','gvar','HVAR','MVAR','VVAR','STAT'):
            if tag in varFont:
                del varFont[tag]

        #print("Saving instance font", outFile)
        varFont.save(outFile)

    # Installing the font in DrawBot. Answer font name and path.
    return outFile


def getVarFontInstance(fontOrPath, location, install=True, styleName=None, normalize=True):
    """The variablesFontPath refers to the file of the source variable font.
    The nLocation is dictionary axis locations of the instance with values between (0, 1000), e.g.
    dict(wght=0, wdth=1000) or values between  (0, 1), e.g. dict(wght=0.2, wdth=0.6).
    Set normalize to False if the values in location already are matching the axis min/max of the font.
    If there is a [opsz] Optical Size value defined, then store that information in the font.info.opticalSize.
    The optional *styleName* overwrites the *font.info.styleName* of the *ttFont* or the automatic
    location name."""
    if isinstance(fontOrPath, str):
        varFont = Font(fontOrPath, name=path2FontName(fontOrPath))
    else:
        varFont = fontOrPath
    fontPath = generateInstance(varFont.path, location, targetDirectory=getInstancePath(), normalize=normalize)
    # Answer the generated Variable Font instance. Add [opsz] value if is defined in the location, otherwise None.
    return Font(fontPath, install=install, opticalSize=location.get('opsz'), location=location, styleName=styleName)


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
