#!/usr/bin/env python
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
#     basetheme.py
#
import copy
from scss import compiler
from pagebot.style import getRootStyle

class BaseTheme:
    u"""The Theme instances combines a number style dictionaries (property
    values), in relation to a selector path for their usage. In Html/Css terms,
    a theme could describe the entire CSS file where the keys are used as CSS
    selector and the connected styles are used as property:value declaration.

    PageBot will support a growing number of predefined themes, that can be
    copied in a document and then modified. Thet CSS behavior of elements will
    comply to the selected theme of a document, unless they have their own
    style defined."""
    SCSS_PATH = None # Needs to be redefined by inheriting theme classes.

    # Predefined style names
    ROOT = 'root' # Rootstyle selector of a theme.
    H1, H2, H3, H4, H5, H6, H7, H8 = HEADS = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8')

    def __init__(self, name=None, description=None, srcTheme=None):
        self.name = name
        self.description = description
        self.styles = {} # Key is selector, value is a style.
        self.palette = {} # Dicitionary of named generic style values

        if srcTheme is not None:
            self.styles = srcTheme.copyStyles()
        self.initialize() # Call in inheriting Theme classes, to define their own valeus.

    def initialize(self, srcTheme):
        u"""Theme styles are created here by inheriting them classes. If
        srcTheme is not None, start initialize with a copy of that one."""
        self[self.ROOT] = getRootStyle()
        for headName in self.HEADS:
            self[headName] = getRootStyle # Make sure there is something there.

    def __repr__(self):
        return '<Theme %s styles:%d>' % (self.name, len(self.styles))

    def __getitem__(self, selector):
        return self.styles[selector]

    def __setitem__(self, selector, style):
        self.styles[selector] = style

    def getStyles(self):
        u"""Answers the theme as a dictionary of styles."""
        self.applyPalette() # In case it was not executed before, substitute the palette values
        return self.styles

    def getCss(self):
        u"""Answers the theme as a CSS source, compiled from the available
        styles, the palette, and the optional file at self.SCSS_PATH.
        Construct the SCSS variable files, and compile the result into CSS."""
        if self.SCSS_PATH is not None:
            compiler(self.CSS_PATH)

    def applyPalette(self, palette=None):
        u"""After setting style values, named typographic values and colors,
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
