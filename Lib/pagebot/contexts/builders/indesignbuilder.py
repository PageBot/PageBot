#!/usr/bin/env python
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
#     indesignbuilder.py
#
#     Version 0.1
#
import os
import codecs
from pagebot.contexts.builders.basebuilder import BaseBuilder
from pagebot.toolbox.transformer import value2Bool
from pagebot.toolbox.dating import now
from pagebot.toolbox.color import Color
from pagebot.toolbox.transformer import object2SpacedString

class BezierPath(object):
    u"""Make BezierPath with the same API for DrawBotBuilder drawing.

    >>> from pagebot.contexts.builders.indesignbuilder import IndesignBuilder
    >>> indesignBuilder = IndesignBuilder()
    >>> path = BezierPath(indesignBuilder)
    >>> path.moveTo((0, 0))
    >>> path.lineTo((0, 100))
    >>> path.lineTo((100, 100))
    >>> path.lineTo((100, 0))
    >>> path.lineTo((0, 0))
    >>> path.closePath()

    """
    def __init__(self, b):
        self.b = b
        self.commands = []

    def append(self, command):
        self.commands.append(command)

    def moveTo(self, p):
        pass

    def lineTo(self, p):
        pass

    def quadTo(self, bcp, p):
        pass

    def curveTo(self, bcp1, bcp2, p):
        pass
        
    def closePath(self):
        pass
        # TODO Seems to be a problem in direct closing, not storing as command?
        #self.commands.append(self.b.closepath

    def appendPath(self, path):
        self.commands += path.commands

        
class IndesignBuilder(BaseBuilder):
    """
    The IndesignBuilder class implements the all necessary API-Javascript to communicate with Indesign. 

    >>> b = IndesignBuilder()
    >>> b.compact = True
    >>> b.newDocument()
    >>> b.getJs(newLine=False)
    '/* Created by PageBot */ var myDocument = app.documents.add(false);'
    """
    PB_ID = 'indesign' # Id to make build_indesign hook name. Views will be calling e.build_html()
    
    def __init__(self):
        self._jsOut = []
        self._initialize()

    def _initialize(self):
        self.comment('Created by PageBot')

    #   Chunks of Indesign functions

    def newDocument(self):
        # Creates a new document without showing the document window.
        # The first parameter (showingWindow) controls the visibility of the document.
        # Hidden documents are not minimized, and will not appear until you add a new window to the document.
        self.addJs('var myDocument = app.documents.add(false);')
        # To show the window:
        # var myWindow = myDocument.windows.add();

    def save(self, path):
        self.writeJs(path)
   
    #   J S

    def addJs(self, js):
        self._jsOut.append(js)

    def hasJs(self):
        return len(self._jsOut)

    def importJs(self, path):
        u"""Import a chunk of UTF-8 CSS code from the path."""
        if os.path.exists(path):
            f = codecs.open(path, 'r', 'utf-8')
            self.addJs(f.read())
            f.close()
        else:
            self.comment('Cannot find JS file "%s"' % path)

    def copyPath(self, path):
        u"""Collect path of files to copy to the output website."""
        self._copyPaths.append(path)

    def getJs(self, newLine=True):
        u"""Answer the flat string of JS."""
        if newLine:
            newLine = '\n'
        else:
            newLine = ' '
        return newLine.join(self._jsOut)
    
    def writeJs(self, path):
        u"""Write the collected set of css JS to path."""
        try:
            f = codecs.open(path, 'w', 'utf-8')
            f.write(self.getJs())
            f.close()
        except IOError:
            print('[%s.writeCss] Cannot write JS file "%s"' % (self.__class__.__name__, path))

    # N O N - J S

    def comment(self, s):
        if s:
            self.addJs('/* %s */' % object2SpacedString(s))


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
