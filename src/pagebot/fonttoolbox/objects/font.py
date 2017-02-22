# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     font.py
#
#     Implements a PabeBot font style to get info from a TTFont.
#     The Style instance is a convenience caching storage, similar to RoboFont Font.
#     Using the Family/Font/Glyph classes, allows page layout in PageBot to access
#     all information in a font purpose of typography and layout.
#   
#     We'll call this class "Font" instead of "Style" (as in other TypeNetwerk tool code),
#     to avoid confusion with the PageBot style dictionary, which hold style parameters.
#
from AppKit import NSFont
from fontTools.ttLib import TTFont, TTLibError
from pagebot.fonttoolbox.objects.glyph import Glyph
from pagebot.fonttoolbox.objects.fontinfo import FontInfo
from pagebot.contributions.adobe.getKerningPairsFromOTF import OTFKernReader

def getFontPathOfFont(fontName):
    font = NSFont.fontWithName_size_(fontName, 25)
    if font is not None:
        fontRef = CTFontDescriptorCreateWithNameAndSize(font.fontName(), font.pointSize())
        url = CTFontDescriptorCopyAttribute(fontRef, kCTFontURLAttribute)
        return url.path()
    return None

class Font(object):
    # Storage of font information while composing the pages.
    GLYPH_CLASS = Glyph

    def __init__(self, path, name=None):
        self.path = path # File path of the font file.
        try: 
            self.ttFont = TTFont(path, lazy=True)
            self.info = FontInfo(self.ttFont) # TTFont is available as lazy style.info.font
            self.name = name # Keep original DrawBot name. Otherwise use from FontInfo
            self.path = path
            self._kerning = None # Lazy reading.
            self._groups = None # Lazy reading.
        except TTLibError:
            raise OSError('Cannot open font file "%s"' % path)

    def __repr__(self):
        return self.path or self.name

    def __getitem__(self, glyphName):
        return self.GLYPH_CLASS(self, glyphName)

    def _get_axes(self): # Answer dictionary of axes
        try:
            axes = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in self.ttFont['fvar'].axes}
        except KeyError:
            axes = {} # This is not a var font.
        return axes
    axes = property(_get_axes)

    def _get_kerning(self):
        if self._kerning is None: # Lazy read.
            self._kerning = OTFKernReader(self.path).kerningPairs
        return self._kerning
    kerning =  property(_get_kerning)

    def _get_groups(self):
        return self._groups
    groups = property(_get_groups)

    def save(self, path=None):
        u"""Save the font to optional path or to self.path."""
        self.ttFont.save(path or self.path)