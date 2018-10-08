
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
#     Supporting usage of InDesign API-scripting
# -----------------------------------------------------------------------------
#
#     idmlcontext.py

from pagebot.contexts.basecontext import BaseContext
from pagebot.contexts.builders.idmlbuilder import IDMLBuilder
from pagebot.contexts.strings.indesignstring import InDesignString

class IDMLContext(BaseContext):

    # In case of specific builder addressing, callers can check here.
    isInDesign = True

    # Used by the generic BaseContext.newString( )
    STRING_CLASS = InDesignString
    EXPORT_TYPES = ('idml',)

    def __init__(self):
        """Constructor of InDesignContext.

        >>> context = InDesignContext()
        >>> context.isInDesign
        True
        """
        self.b = IDMLBuilder() # cls.b builder for this canvas.
        self.name = self.__class__.__name__

    def newDrawing(self, path=None):
        pass
