# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     glyph.py
#
#     Implements a PabeBot font classes to get info from a TTFont.
#   
import weakref
from AppKit import NSFont
from fontTools.ttLib import TTFont, TTLibError
from pagebot.fonttoolbox.objects.fontinfo import FontInfo

class Glyph(object):
    u"""This Glyph class is a wrapper around the glyph structure of a ttFont.
    It is supposed to copy the functions of the RoboFont raw glyph, for all needed functions
    in PageBot. It is not complete, will be added to when needed."""
    def __init__(self, font, name):
        self.name = name
        self.parent = font # Store as weakref

    def _get_ttGlyph(self):
        return self.parent.ttFont['glyf'][self.name]
    ttGlyph = property(_get_ttGlyph)

    def _set_parent(self, font):
        self._parent = weakref.ref(font)
    def _get_parent(self):
        if self._parent is not None:
            return self._parent()
        return None
    parent = property(_get_parent, _set_parent)

    def _get_width(self):
        return self.parent.ttFont['hmtx'][self.name][0]
    def _set_width(self, width):
        hmtx = list(self.parent.ttFont['hmtx'][self.name]) # Keep vertical value
        hmtx[0] = width
        self.parent.ttFont['hmtx'][self.name] = hmtx
    width = property(_get_width, _set_width)

    """
    TTGlyph Functions to implement

 |  Methods defined here:
 |  
 |  __eq__(self, other)
 |  
 |  __getitem__(self, componentIndex)
 |  
 |  __init__(self, data='')
 |  
 |  __ne__(self, other)
 |  
 |  compact(self, glyfTable, recalcBBoxes=True)
 |  
 |  compile(self, glyfTable, recalcBBoxes=True)
 |  
 |  compileComponents(self, glyfTable)
 |  
 |  compileCoordinates(self)
 |  
 |  compileDeltasGreedy(self, flags, deltas)
 |  
 |  compileDeltasOptimal(self, flags, deltas)
 |  
 |  decompileComponents(self, data, glyfTable)
 |  
 |  decompileCoordinates(self, data)
 |  
 |  decompileCoordinatesRaw(self, nCoordinates, data)
 |  
 |  draw(self, pen, glyfTable, offset=0)
 |  
 |  expand(self, glyfTable)
 |  
 |  fromXML(self, name, attrs, content, ttFont)
 |  
 |  getComponentNames(self, glyfTable)
 |  
 |  getCompositeMaxpValues(self, glyfTable, maxComponentDepth=1)
 |  
 |  getCoordinates(self, glyfTable)
 |  
 |  getMaxpValues(self)
 |  
 |  isComposite(self)
 |      Can be called on compact or expanded glyph.
 |  
 |  recalcBounds(self, glyfTable)
 |  
 |  removeHinting(self)
 |  
 |  toXML(self, writer, ttFont)
 |  
 |  trim(self, remove_hinting=False)
 |      Remove padding and, if requested, hinting, from a glyph.
 |      This works on both expanded and compacted glyphs, without
 |      expanding it.
    """
