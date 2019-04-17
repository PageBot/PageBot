
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
#     filecontext.py

from pagebot.contexts.basecontext import BaseContext

class ZipContext(BaseContext):

    # Used by the generic BaseContext.newString( )
    #STRING_CLASS = ZipString
    EXPORT_TYPES = ('zip',)

    def __init__(self):
        """Constructor of InDesignContext.

        >>> context = IdmlContext()
        """
        super().__init__()
        self.b = ZipBuilder() # cls.b builder for this context.
        self.name = self.__class__.__name__

    def newDrawing(self, path=None):
        pass
