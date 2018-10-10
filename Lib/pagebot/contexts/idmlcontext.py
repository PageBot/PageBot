
#!/usr/bin/env python3
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
#     Supporting usage of InDesign API-scripting
# -----------------------------------------------------------------------------
#
#     idmlcontext.py

from pagebot.contexts.basecontext import BaseContext
from pagebot.contexts.builders.idmlbuilder import IdmlBuilder
from pagebot.contexts.strings.idmlstring import IdmlString

class IdmlContext(BaseContext):

    # Used by the generic BaseContext.newString( )
    STRING_CLASS = IdmlString
    EXPORT_TYPES = ('idml',)

    def __init__(self):
        """Constructor of InDesignContext.

        >>> context = InDesignContext()
        >>> context.isInDesign
        True
        """
        self.b = IdmlBuilder() # cls.b builder for this canvas.
        self.name = self.__class__.__name__

    def newDrawing(self, path=None):
        pass
