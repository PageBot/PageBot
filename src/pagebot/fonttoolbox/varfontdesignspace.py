# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#       from https://github.com/fonttools/fonttools/blob/master/Lib/fontTools/varLib/mutator.py
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     varfontdesignspace.py
#
from __future__ import division

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph as TTGlyph, GlyphCoordinates
from fontTools.varLib.models import VariationModel, supportScalar, normalizeLocation
from fontTools.varLib import _GetCoordinates

# Copied from from tnbits.compilers.f5.ttfTools import getBestCmap
def getBestCmap(font, cmapPreferences=((3, 10), (3, 1), (0, 3))):
    """Return a unicode -> glyphName dictionary from the 'best' unicode cmap that the font
    contains. In order of preference, the font will be searched for cmaps 3,10, 3,1 and 0,3.

        >>> from fontTools.ttLib import TTFont
        >>> from tnTestFonts import getFontPath
        >>> path = getFontPath("CusterRE-RegularS2.ttf")
        >>> font = TTFont(path)
        >>> cmap = getBestCmap(font)
        >>> len(cmap)
        248
        >>> max(cmap)
        64258
        >>> path = getFontPath("ProW6.otf")
        >>> font = TTFont(path)
        >>> cmap = getBestCmap(font)
        >>> len(cmap)
        13641
        >>> print hex(max(cmap))  # if result > 0xffff then it must have been a 3,10 cmap
        0x2f9f4
        >>> getBestCmap(font, cmapPreferences=[(123, 456)])
        Traceback (most recent call last):
            ...
        ValueError: None of the requested cmap subtables were found
    """
    cmapTable = font["cmap"]
    for platformID, platEncID in cmapPreferences:
        cmapSubtable = cmapTable.getcmap(platformID, platEncID)
        if cmapSubtable is not None:
            #print platformID, platEncID
            return cmapSubtable.cmap
    raise ValueError("None of the requested cmap subtables were found")

# Copied from tnbits.toolparts.buildvariations.designspacemodel import DesignSpaceBase, Axis
class DesignSpaceBase(object):

    def __init__(self, axes):
        assert len(axes) == len(set(a.tag for a in axes)), "Axis tags must be unique"
        self.axes = axes

    def getOutline(self, glyphName, location, penFactory):
        """Create an outline for the requested glyph and location, using
        penFactory to construct a pen. It will be called with a glyphSet argument.
        Return the path/pen, a centerPt and a size as a 3-tuple.
        """
        # XXX it needs to be seen whether the center + size thing actually works.
        # Maybe a rectangle (not necessarily the bounding box) works better.
        raise NotImplementedError()

    def getGlyphName(self, charCode):
        """Return the glyph name associated with charCode (a Unicode code point).
        Should return '.notdef' if the character is not defined."""
        raise NotImplementedError()


class Axis(object):

    def __init__(self, name, minValue, defaultValue, maxValue, tag=None):
        self.name = name
        self.minValue = minValue
        self.defaultValue = defaultValue
        self.maxValue = maxValue
        self.tag = tag or name

    def normalizeValue(self, value):
        # This normalizes the value to be between 0 and 1, so this is not the
        # same as the normalized value in a variation font. This is purely to
        # calculate slider settings.
        return (value - self.minValue) / (self.maxValue - self.minValue)

def setCoordinates(glyph, coord, glyfTable):
    # Handle phantom points for (left, right, top, bottom) positions.
    assert len(coord) >= 4
    if not hasattr(glyph, 'xMin'):
        glyph.recalcBounds(glyfTable)
    leftSideX = coord[-4][0]
    rightSideX = coord[-3][0]
    topSideY = coord[-2][1]
    bottomSideY = coord[-1][1]

    for _ in range(4):
        del coord[-1]

    if glyph.isComposite():
        assert len(coord) == len(glyph.components)
        for p,comp in zip(coord, glyph.components):
            if hasattr(comp, 'x'):
                comp.x,comp.y = p
    elif glyph.numberOfContours is 0:
        assert len(coord) == 0
    else:
        assert len(coord) == len(glyph.coordinates)
        glyph.coordinates = coord

    glyph.recalcBounds(glyfTable)

    horizontalAdvanceWidth = rightSideX - leftSideX
    leftSideBearing = glyph.xMin - leftSideX
    return horizontalAdvanceWidth, leftSideBearing
    # XXX Handle vertical
    # XXX Remove the round when https://github.com/behdad/fonttools/issues/593 is fixed
    # font["hmtx"].metrics[glyphName] = int(round(horizontalAdvanceWidth)), int(round(leftSideBearing))


class TTVarFontGlyphSet(object):

    def __init__(self, font):
        self._ttFont = font
        self._axes = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in font['fvar'].axes}
        self.setLocation({})
    
    def setLocation(self, location):
        self.location = normalizeLocation(location, self._axes)

    def keys(self):
        return list(self._ttFont['glyf'].keys())

    def has_key(self, glyphName):
        return glyphName in self._ttFont['glyf']
    __contains__ = has_key

    def __getitem__(self, glyphName):
        return TTVarGlyph(self._ttFont, glyphName, self.location)

    def get(self, glyphName, default=None):
        try:
            return self[glyphName]
        except KeyError:
            return default


class TTVarGlyph(object):

    def __init__(self, ttFont, glyphName, location):
        self._ttFont = ttFont
        self._glyphName = glyphName
        self._location = location
        self.width, self.lsb = ttFont['hmtx'][glyphName]

    @staticmethod
    def _copyGlyph(glyph, glyfTable):
        glyph = TTGlyph(glyph.compile(glyfTable))
        glyph.expand(glyfTable)
        return glyph

    def draw(self, pen):
        glyph = self._ttFont['glyf'][self._glyphName]
        glyph = self._copyGlyph(glyph, self._ttFont['glyf'])

        variations = self._ttFont['gvar'].variations[self._glyphName]
        coordinates, _ = _GetCoordinates(self._ttFont, self._glyphName)
        for var in variations:
            scalar = supportScalar(self._location, var.axes)
            if not scalar:
                continue
            # print(var.coordinates)
            if None in var.coordinates:
                print("warning: replacing missing deltas with (0, 0)")
            deltas = GlyphCoordinates([pt or (0, 0) for pt in var.coordinates])
            coordinates += deltas * scalar

        horizontalAdvanceWidth, leftSideBearing = setCoordinates(glyph, coordinates, self._ttFont['glyf'])
        self.width = horizontalAdvanceWidth
        glyph.draw(pen, self._ttFont['glyf'])  # XXX offset based on lsb


class TTVarFontDesignSpace(DesignSpaceBase):

    @classmethod
    def fromVarFontPath(cls, path):
        ttFont = TTFont(path, lazy=True)
        return cls(ttFont)

    def __init__(self, ttFont):
        self.ttFont = ttFont
        self.cmap = getBestCmap(ttFont)
        axes = []
        fvar = self.ttFont["fvar"]
        for a in fvar.axes:
            nameRecord = self.ttFont["name"].getName(a.axisNameID, 3, 1)
            if nameRecord is None:
                nameRecord = self.ttFont["name"].getName(a.axisNameID, 1, 0)
            name = nameRecord.toUnicode()
            axes.append(Axis(name, a.minValue, a.defaultValue, a.maxValue, a.axisTag))

        super(TTVarFontDesignSpace, self).__init__(axes)
        self.glyphSet = TTVarFontGlyphSet(ttFont)

    def getGlyphName(self, charCode):
        return self.cmap.get(charCode, ".notdef")

    def getOutline(self, glyphName, location, penFactory):
        pen = penFactory(self.glyphSet)
        self.glyphSet.setLocation(location)
        if glyphName in self.glyphSet:
            varGlyph = self.glyphSet[glyphName]
        else:
            varGlyph = self.glyphSet[".notdef"]
        varGlyph.draw(pen)
        os2 = self.ttFont["OS/2"]
        if hasattr(os2, "sxHeight"):
            xHeight = os2.sxHeight
            capHeight = os2.sCapHeight
        else:
            capHeight = self.ttFont["hhea"].ascent
            xHeight = 0.7 * self.ttFont["hhea"].ascent  # XXX
        centerPoint = (varGlyph.width / 2, xHeight / 2)
        size = capHeight
        return pen, centerPoint, size


if __name__ == "__main__":

    class DesignSpaceExplorerTest(object):

        def __init__(self, designSpace, previewCharacter="e"):
            from vanilla import Window
            from tnbits.toolparts.buildvariations.designspaceexplorer import DesignSpaceExplorer
            self.w = Window((1000, 500), "DesignSpace Explorer", minSize=(600, 300))
            self.w.designSpaceExplorer = DesignSpaceExplorer((0, 0, 0, 0), designSpace,
                previewCharacter=previewCharacter)
            self.w.open()

    from tnTestFonts import getFontPath
    p = getFontPath("Noordzij_e_varfont.ttf")
    ds = TTVarFontDesignSpace.fromVarFontPath(p)
    DesignSpaceExplorerTest(ds, "e")
