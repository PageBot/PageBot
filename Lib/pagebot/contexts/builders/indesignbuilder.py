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
#     indesignbuilder.py
#
#     InDesign scripting docs:
#
#     - https://www.adobe.com/devnet/indesign/documentation.html
#     - https://wwwimages2.adobe.com/content/dam/acom/en/devnet/indesign/sdk/cs6/scripting/InDesign_ScriptingGuide_JS.pdf
#

import os
import codecs
from pagebot.contexts.builders.basebuilder import BaseBuilder
from pagebot.toolbox.transformer import object2SpacedString
from pagebot.toolbox.units import asFormatted, pt
from pagebot.constants import A4Rounded
from pagebot.contexts.bezierpaths.commandbezierpath import CommandBezierPath as BezierPath

class InDesignBuilder(BaseBuilder):
    """The InDesignBuilder class uses the InDesign Javascript API to
    generate output.

    >>> import os
    >>> W, H = A4Rounded
    >>> b = InDesignBuilder()
    >>> b.compact = True
    >>> b.newDocument(W, H)
    >>> b.getJs(newLine=False).startswith('/* Created by PageBot */')
    True
    >>> b.newPage()
    >>> # FIXME: should be points (pt())
    >>> b.oval(100, 100, 200, 200) # x, y, w, h
    >>> b.rect(300, 100, 100, 200)
    >>> b.rect(100, 300, 200, 100)
    >>> b.oval(300, 300, 100, 100)
    >>> scriptPath = '_export/InDesign.jsx'
    >>> #b.writeJs(scriptPath)
    >>> scriptPath = b.getInDesignScriptPath()
    >>> if not os.path.exists(scriptPath):
    ...     os.makedirs(scriptPath)
    >>> scriptPath += 'InDesignExample2.jsx'
    >>> b.writeJs(scriptPath)
    """
    PB_ID = 'indesign' # Id to make build_indesign hook name. Views will be calling e.build_html()
    INDESIGN_SCRIPT_PATH = '~/Library/Preferences/Adobe InDesign/Version 13.0/en_US/Scripts/Scripts Panel/PageBot/'

    def __init__(self):
        self.openDocument = True # Set to False if document creation should run in background.
        self.font = None
        self.fontSize = None
        self.title = None
        self._jsOut = []
        self._initialize()
        self.w, self.h = A4Rounded
        self.mr = self.mt = self.mb = self.mr = pt(24)
        self._path = None
        self._hyphenation = False
        self.numberOfPages = 0
        self.margin = pt(36)

    def __repr__(self):
        return '\n'.join(self._jsOut)

    def _initialize(self):
        self.comment('Created by PageBot')

    #   Chunks of InDesign functions

    def newDocument(self, w, h, units='pt'):
        """Create a new document. Store the (w, h) for the moment that pages
        are created."""
        self.w = w
        self.h = h
        self.units = units

        # Creates a new document without showing the document window.  The
        # first parameter (showingWindow) controls the visibility of the
        # document. Hidden documents are not minimized and will not appear
        # until you add a new window to the document.
        if self.title:
            self.comment('--- %s ---' % (self.title or 'Untitled'))

        self.addJs('var currentDocument = app.documents.add(%s);' % str(self.openDocument).lower()) # Make document in background

        self.addJs('var currentElement;') # Storage of current parent element
        #self.comment('-'*60)
        self.addJs('with(currentDocument.documentPreferences){')
        self.addJs('    pageWidth = "%s%s";' % (asFormatted(h), self.units))
        self.addJs('    pageHeight = "%s%s";' % (asFormatted(w), self.units))
        self.addJs('    pageOrientation = PageOrientation.%s;' % {False:'landscape', True:'portrait'}[w > h])
        #self.addJs('    pagesPerDocument = %d;' % pageCount)
        self.addJs('}')
        self.addJs('var currentPage = currentDocument.pages.item(0);')
        self.addJs('var currentTextFrames = currentPage.textFrames;')
        # To show the window
        # var myWindow = currentDocument.windows.add();

    def newPage(self, w=None, h=None):
        # NOTE: first page is added by default.
        self.addJs('currentPage = currentDocument.pages.add();')

    def newDrawing(self):
        pass

    def BezierPath(self):
        if self._path is None:
            self._path = BezierPath(self)
        return self._path

    # Basic shapes.

    def line(self, p1, p2):
        pass
        #self.addJs('currentElement = currentPage.paths.add();')
        #self.addJs('currentElement.geometricBounds = ["%s", "%s", "%s", "%s"];' % (p1[0].v, p1[1].v, p2[0].v, p2[1].v))

    def oval(self, x, y, w, h):
        """Export the InDesign bounding box for the Oval."""
        self.addJs('currentElement = currentPage.ovals.add({geometricBounds: ["%s", "%s", "%s", "%s"]});' % (y, x+w, y+h, x))
        self.addJs('currentElement.fillColor = fill')
        self.addJs('currentElement.strokeColor = stroke')

    def rect(self, x, y, w, h):
        self.addJs('currentElement = currentPage.rectangles.add({geometricBounds: ["%s", "%s", "%s", "%s"]});' % (y, x+w, y+h, x))
        self.addJs('currentElement.fillColor = fill')
        self.addJs('currentElement.strokeColor = stroke')

    # Colors.

    def fill(self, r, g=None, b=None, alpha=None):
        print('!!! InDesign RGB fill to be implemented')
        return
        '''
        js = 'var fill = '
        value = '{name:"%s", model:ColorModel.process, colorValue:[%d, %d, %d, %d]}' % ('fill', r, g, b, alpha)
        js += 'currentDocument.colors.add(%s);' % value
        self.addJs(js)
        '''

    def stroke(self, r, g, b, alpha=None):
        print('!!! InDesign RGB stroke to be implemented')
        return
        '''
        js = 'var stroke = '
        value = '{name:"%s", model:ColorModel.process, colorValue:[%d, %d, %d, %d]}' % ('stroke', r, g, b, alpha)
        js += 'currentDocument.colors.add(%s);' % value
        self.addJs(js)
        '''

    def cmykFill(self, c, m, y, k, alpha=None):
        # TODO: alpha.
        js = 'var fill = '
        value = '{name:"%s", model:ColorModel.process, colorValue:[%d, %d, %d, %d]}' % ('fill', c, m, y, k)
        js += 'currentDocument.colors.add(%s);' % value
        self.addJs(js)

    def cmykStroke(self, c, m, y, k, alpha=None):
        # TODO: alpha.
        js = 'var stroke = '
        value = '{name:"%s", model:ColorModel.process, colorValue:[%d, %d, %d, %d]}' % ('stroke', c, m, y, k)
        js += 'currentDocument.colors.add(%s);' % value
        self.addJs(js)

    # Paths.

    # Text.

    def text(self, bs, p):
        """Place the babelstring instance at position p. The position can be
        any 2D or 3D points tuple. Currently the z-axis is ignored
        """
        #msg = 'InDesignString.text: bs not of type %s' % InDesignString.__name__
        #assert isinstance(bs, InDesignString), msg
        # TODO: get text dimensions or element dimensions.
        self.addJs('var currentTextFrame = currentTextFrames.add();')
        p3 = self.w - self.margin
        p4 = self.h - self.margin
        self.addJs('currentTextFrame.geometricBounds = ["%s", "%s", "%s", "%s"];' % (p[0], p[1], pt(p3), pt(p4)))
        self.addJs('currentTextFrame.contents = "%s";' % bs)

        #assert self.page is not None, 'FlatString.text: self.page is not set.'
        #placedText = self.page.place(bs.s)
        #xpt, ypt = point2D(upt(p))
        #placedText.position(xpt, ypt) # Render unit tuple to value tuple

    #   J S

    def addJs(self, js):
        self._jsOut.append(js)

    def hasJs(self):
        return len(self._jsOut)

    def importJs(self, path):
        """Import a chunk of UTF-8 CSS code from the path."""
        if os.path.exists(path):
            f = codecs.open(path, 'r', 'utf-8')
            self.addJs(f.read())
            f.close()
        else:
            self.comment('Cannot find JS file "%s"' % path)

    def copyPath(self, path):
        """Collect path of files to copy to the output website."""
        self._copyPaths.append(path)

    def getJs(self, newLine=True):
        """Answers the flat string of JS."""
        if newLine:
            newLine = '\n'
        else:
            newLine = ' '
        return newLine.join(self._jsOut)

    def writeJs(self, path):
        """Write the collected set of css JS to path."""
        try:
            f = codecs.open(path, 'w', 'utf-8')
            f.write(self.getJs())
            f.close()
        except IOError:
            print('[%s.writeCss] Cannot write JS file "%s"' % (self.__class__.__name__, path))

    def getInDesignScriptPath(self):
        """Answers the user local script path. For now this assumes one version
        of InDesign.

        TODO: Should be made more generic.

        >>> b = InDesignBuilder()
        >>> b.getInDesignScriptPath().endswith('/PageBot/')
        True
        """
        return os.path.expanduser(self.INDESIGN_SCRIPT_PATH)

    # N O N - J S

    def comment(self, s):
        if s:
            self.addJs('/* %s */' % object2SpacedString(s))

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
