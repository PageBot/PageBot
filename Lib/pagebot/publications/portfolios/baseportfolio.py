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

from pagebot.publications.publication import Publication
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.toolbox.units import pt
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.constants import *

class BasePortfolio(Publication):
    """Create a default portfolio, with cover, front-of-book and automatic composed
    pages from a recursive search in child folders. By defaul the name of the folders
    is used as chapter headers.
    Subclassed from Element-->Publication-->Magazine.
    """

    # Default paper sizes that are likely to be used for 
    # portfolios in portrait ratio.
    PAGE_SIZES = {
        'A2': A2,
        'A3': A3,
        'A4': A4,
        'A5': A5,
        'B4': B4,
        'B5': B5,
        'HalfLetter': HalfLetter,
        'Letter': Letter,
        'Legal': Legal,
        'JuniorLegal': JuniorLegal,
        'Tabloid': Tabloid,
        'Ledger': Ledger,
        'Statement': Statement,
        'Executive': Executive,
        'Folio': Folio,
        'Quarto': Quarto,
        'Size10x14': Size10x14,
        'A4Letter': A4Letter,
        'A4Oversized': A4Oversized,
        'A3Oversized': A3Oversized,
    }
    DEFAULT_PAGE_SIZE_NAME = 'A3'
    DEFAULT_PAGE_SIZE = PAGE_SIZES[DEFAULT_PAGE_SIZE_NAME]

    def __init__(self, path=None, cols=None, rows=None, imageTypes=None, styles=None, 
            resolution=1, **kwargs):
        Publication.__init__(self, **kwargs)
        self.path = path
        self.imageTypes = imageTypes # If None, select all standard image types.
        if styles is None:
            styles = self.getDefaultStyles()
        self.styles = styles
        self.cols = cols or DEFAULT_COLS
        self.rows = rows or DEFAULT_ROWS
        self.imagePaths = self.findImagePaths(path)
        self.resolution = resolution # Factor that scaled images should be larger than usage.

    def getDefaultStyles(self):
        styles = dict(
            title=dict(font=findFont('Upgrade-Regular'), fontSize=pt(32))
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
            if fileName.startswith('.') or fileName == '_scaled':
                continue
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
        page.padding = doc.padding
        prevTitle = None
        gutter = pt(8)

        index = 0 #
        for title, imagePaths in sorted(self.imagePaths.items()):
            if page is None:
                page = doc[1]
            elif index == 7:
                page = page.next
                page.padding = doc.padding
                index = 0

            h = (page.ph - (self.rows - 1) * gutter) / self.rows
            if title != prevTitle:
                bs = doc.context.newString(title, style=self.styles['title'])
                tw, th = bs.size
                newTextBox(bs, conditions=[Left2Left(), Fit2Width(), Float2Top()], h=1.5*th, parent=page)
                prevTitle = title
            
            for imagePath in sorted(imagePaths):
                newImage(path=imagePath, h=h, mr=gutter, mb=gutter, resolution=self.resolution,
                    conditions=[Right2Right(), Float2Top(), Float2Left()], parent=page)
                index += 1
                if index == 8:
                    newRect(parent=page, h=2, w=page.pw, conditions=[Left2Left(), Float2Top()])
                    page = page.next
                    page.padding = doc.padding
                    index = 0
        return doc

    def export(self, name, start=0, end=None, path=None, showGrid=False, showPadding=False):
        if path is None:
            path = '_export/%s-%s.pdf' % (self.name, name)

        doc = self.compose()

        view = doc.view
        view.showGrid = showGrid
        view.showPadding = showPadding

        doc.solve()
        doc.export(path)


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
