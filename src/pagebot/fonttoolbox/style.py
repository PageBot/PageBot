# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     style.py
#
#     Implements a PabeBot font style to get info from a TTFont.
#     The Style instance is a convenience caching storage, similar to RoboFont Font.
#
from pagebot.fonttoolbox.fontinfo import FontInfo
from fontTools.ttLib import TTLibError

class Style(object):
    # Storage of style information while composing the pages.
    def __init__(self, path, name=None):
        self.path = path # File path of the font file.
        try: 
            self.info = FontInfo(path) # TTFont is available as lazy style.info.font
            self.name = name # Keep original DrawBot name. Otherwise use from FontInfo
        except TTLibError:
            raise OSError('Cannot open font file "%s"' % path)
 
    def _get_styleName(self):
        return self.name or self.info.styleName
    styleName = property(_get_styleName)