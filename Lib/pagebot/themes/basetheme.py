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

import copy
from pagebot.style import getRootStyle

class Palette:

    def __init__(self, name, colors):
        self.name = name
        self._colors = colors # Store for length and optional reference.
        for attrName, value in colors.items():
            setattr(self, attrName, value)

    def __repr__(self):
        s = self.name
        for n in range(12):
            s += ' #%d=%s' % (n, self[n].spot)
        return '<%s>' % s

    def __getitem__(self, index):
        return getattr(self, 'c%d' % index)

    def __len__(self):
        return len(self._colors)
        
    def _get_colors(self):
        """Answer the colors a index list.
        """
        colors = []
        for cIndex in range(len(self._colors)):
            colors.append(self[cIndex])
        return colors
    colors = property(_get_colors)

class BaseTheme:
    u"""The Theme instances combines a number of style dictionaries (property
    values), in relation to a selector path for their usage. In Html/Css terms,
    a theme could describe the entire CSS file where the keys are used as CSS
    selector and the connected styles are used as property:value declaration.

    PageBot will support a growing number of predefined themes, that can be
    copied in a document and then modified. Thet CSS behavior of elements will
    comply to the selected theme of a document, unless they have their own
    style defined.



    >>> from pagebot.themes import BusinessAsUsual
    >>> theme = BusinessAsUsual()
    >>> theme.palette.c2
    Color(spot=877)
    >>> theme.palette[3]
    Color(spot=541)
    """
    # Predefined style names
    ROOT = 'root' # Rootstyle selector of a theme.
    H1, H2, H3, H4, H5, H6, H7, H8 = HEADS = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8')

    BASE_MOOD = {

    }
    COLORS = None # To redefined by inheriting Theme classes.

    def __init__(self, name=None, description=None, srcTheme=None, mood=None):
        self.name = name or self.NAME
        self.description = description
        self.styles = {} # Key is selector, value is a style.
        self.palette = Palette(self.name, self.COLORS)
        # Mood/function-names --> key to self.styles or self.palette
        # Make copy, so alterations don't reflect in original
        self.mood = mood or copy.deepcopy(self.BASE_MOOD) 

        self.initialize() # Call in inheriting Theme classes, to define their own valeus.

    def initialize(self):
    	pass

    def __repr__(self):
        return '<Theme %s styles:%d>' % (self.name, len(self.styles))

    def __getitem__(self, selector):
        return self.styles[selector]

    def __setitem__(self, selector, style):
        self.styles[selector] = style

    def cssPy2Css(self, cssPy):
        """Takes a cssPy source, inserts all theme parameters and hands it back.
        """
        return cssPy % self.mood # Instant translation from cssPy to css file output.

    def getStyles(self):
        """Answers the theme as a dictionary of styles."""
        self.applyPalette() # In case it was not executed before, substitute the palette values
        return self.styles

    def applyPalette(self, palette=None):
        """After setting style values, named typographic values and colors,
        apply them to the styles, overwriting values that start with "@"."""
        for style in self.styles.values():
            for name, value in style.items():
                if isinstance(value, str) and value and value[0] == '@':
                    # Replace this value if it exists by palette value.
                    orgValue = value[1:]
                    if orgValue in palette:
                        style[name] = palette[orgValue]

    def copyStyles(self):
        return copy.deepCopy(self.styles)



if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

