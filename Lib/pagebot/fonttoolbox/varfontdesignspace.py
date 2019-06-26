# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#       from https://github.com/fonttools/fonttools/blob/master/Lib/fontTools/varLib/mutator.py
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     varfontdesignspace.py
#
#     D E P R E C A T E D
#

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph as TTGlyph, GlyphCoordinates
from fontTools.varLib.models import supportScalar, normalizeLocation # VariableModel
from fontTools.varLib import _GetCoordinates
from pagebot.fonttoolbox.dsmodel import DesignSpaceBase, Axis
from pagebot.fonttoolbox.ttftools import getBestCmap


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
    elif glyph.numberOfContours == 0:
        assert not coord
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


class TTVarFontGlyphSet:
    # TODO: Change to PageBot Font wrapper
    def __init__(self, ttFont):
        self._ttFont = ttFont
        self._axes = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in ttFont['fvar'].axes}
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


class TTVarGlyph:

    def __init__(self, ttFont, glyphName, location):
        self._ttFont = ttFont
        self._glyphName = glyphName
        self._location = location
        try:
            self.width, self.lsb = ttFont['hmtx'][glyphName]
        except KeyError:
            self.width = 1000
            self.lsb = 50

    @staticmethod
    def _copyGlyph(glyph, glyfTable):
        glyph = TTGlyph(glyph.compile(glyfTable))
        glyph.expand(glyfTable)
        return glyph

    def draw(self, pen):
        glyph = self._ttFont['glyf'][self._glyphName]
        glyph = self._copyGlyph(glyph, self._ttFont['glyf'])

        variables = self._ttFont['gvar'].variables[self._glyphName]
        coordinates, _ = _GetCoordinates(self._ttFont, self._glyphName)
        for var in variables:
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

    class DesignSpaceExplorerTest:

        def __init__(self, designSpace, previewCharacter="e"):
            from vanilla import Window
            from tnbits.toolparts.buildvariables.designspaceexplorer import DesignSpaceExplorer
            self.w = Window((1000, 500), "DesignSpace Explorer", minSize=(600, 300))
            self.w.designSpaceExplorer = DesignSpaceExplorer((0, 0, 0, 0), designSpace,
                previewCharacter=previewCharacter)
            self.w.open()

    #from tnTestFonts import getFontPath
    #p = getFontPath("Noordzij_e_varfont.ttf")
    #ds = TTVarFontDesignSpace.fromVarFontPath(p)
    #DesignSpaceExplorerTest(ds, "e")
