# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     portfolio.py
#
import os
from copy import copy

from pagebot.publications.publication import Publication
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.toolbox.units import pt
from pagebot.toolbox.color import noColor
from pagebot.toolbox.dating import now
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.constants import LEFT, RIGHT, IMAGE_TYPES

class PortFolio(Publication):
    """Create a default portfolio, with cover, front-of-book and automatic composed
    pages from a recursive search in child folders. By defaul the name of the folders
    is used as chapter headers.
    Subclassed from Element-->Publication-->Magazine.

    >>> path = '/Volumes/Flatter/2018-10 tekeningen clau bijeenkomst nina'
    >>> from pagebot.constants import A4
    >>> name = 'Portfolio Claudia Mens'
    >>> pf = PortFolio(path=path, cols=2, rows=3, size=A4, name=name)
    >>> doc = pf.compose()
    >>> doc.export()

    """
    def __init__(self, path=None, cols=None, rows=None, imageTypes=None, styles=None, **kwargs):
        Publication.__init__(self, **kwargs)
        self.path = path
        self.imageTypes = imageTypes # If None, select all standard image types.
        if styles is None:
            styles = self.getDefaultStyles()
        self.styles = styles
        self.cols = cols or DEFAULT_COLS
        self.rows = rows or DEFAULT_ROWS
        self.imagePaths = self.findImagePaths(path)
        
    def getDefaultStyles(self):
        styles = dict(
            title=dict(font=findFont('Roboto-Regular'), fontSize=pt(32))
        )
        return styles

    def findImagePaths(self, path, imagePaths=None):
        """Answer the dictionary with images, Key is chapter name, derived from the enclosing 
        folder. Value is list of image paths.
        """
        if imagePaths is None:
            imagePaths = {}
        title = path.split('/')[-1]
        for fileName in os.listdir(path):
            filePath = path + '/' + fileName
            if os.path.isdir(filePath):
                self.findImagePaths(filePath, imagePaths)
            elif filePath.split('.')[-1].lower() in IMAGE_TYPES:
                if not title in imagePaths:
                    imagePaths[title] = []
                imagePaths[title].append(filePath)
        return imagePaths

    def compose(self):
        doc = self.newDocument()
        page = doc[1]
        prevTitle = None
        for title, imagePaths in sorted(self.imagePaths.items()):
            if title != prevTitle:
                bs = doc.context.newString(title, style=self.styles['title'])
                newTextBox(bs, conditions=[Left2Left(), Top2Top(),Fit2Width()], parent=page)
                prevTitle = title
            for imagePath in sorted(imagePaths):
                newImage(path=imagePath, conditions=[Left2Left(), Fit2Width(), Float2Top()], parent=page)
        return doc

    def export(self, name, start=0, end=None, path=None, showGrid=False, showPadding=False):
        if path is None:
            path = '_export/%s-%s.pdf' % (self.name, name)

        doc = self.compose(name)

        view = doc.view
        view.showGrid = showGrid
        view.showPadding = showPadding

        doc.export(path)


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
