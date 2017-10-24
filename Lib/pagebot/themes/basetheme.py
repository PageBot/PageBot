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
#     basetheme.py
#
import copy
from pagebot.style import makeStyle, getRootStyle

ROOT = 'root' # Rootstyle selector of a theme.
H1, H2, H3, H4, H5, H6, H7, H8 = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8')

class BaseTheme(object):
    u"""The Theme instances combines a number style dictionaries (property values), 
    in relation to
    a selector path for their usage. In Html/Css terms, a theme could describe the entire
    CSS file where the keys are used as CSS selector and the connected styles are used
    as property:value declaration.

    PageBot will support a growing number of predefined themes, that can be copied in
    a document and then modified. Thet CSS behavior of elements will comply to the 
    selected theme of a document, unles they have their own style defined.
    """
    def __init__(self, srcTheme=None):
        self.styles = {} # Key is selector, value is a style.
        self.initialize(srcTheme) # Call of inheriting Theme classes, to define their own valeus.

    def initialize(self, srcTheme):
        u"""Theme styles are created here by inheriting them classes. If srcTheme is not None,
        start initialize with a copy of that one."""
        if srcTheme is not None:
            self.styles = srcTheme.copyStyles()
        self[ROOT] = getRootStyle()

    def __getitem__(self, selector):
        return self.styles[selector]

    def __setitem__(self, selector, style):
        self.styles[selector] = style

    def copyStyles(self):
        return copy.deepCopy(self.styles)