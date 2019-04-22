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
#     books/photobook/__init__.py
#
from pagebot import getResourcesPath
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.constants import *
from pagebot.publications.books.basebook import BaseBook
from pagebot.publications.books.photobook.cover import Cover
from pagebot.mining.samplecontent import SampleContent
from pagebot.toolbox.units import inch

class PhotoBook(BaseBook):
    """Create a photobook with a number of images in a layout and their 
    captions on each page.

    >>> bk = PhotoBook()
    >>> doc = bk.makeSample()
    >>> doc.export('_export/PhotoBookSample.pdf')

    """
    def makeSample(self):
        padding = inch(1.5) 
        w, h = A4Square
        sampleContent = SampleContent()
        imagePath = sampleContent.imagePaths[0]
        doc = self.newDocument(w=w, h=h, autoPages=3, padding=padding)
        # Book cover
        page = doc[1]
        newRect(fill=(1, 0,0), parent=page, conditions=[Fit()])
        # Page with full untouched photo
        page = page.next
        newImage(imagePath, x=padding, y=padding, 
            w=page.pw, h=page.ph, parent=page, conditions=[Fit()])
        page = page.next
        for conditions in (
            (Left2Left(), Top2Top()),
            (Right2Right(), Top2Top()),
            (Left2Left(), Bottom2Bottom()),
            (Right2Right(), Bottom2Bottom())
        ):
            newImage(imagePath, x=padding, y=padding, 
                w=page.pw/2, h=page.ph/2, parent=page, conditions=conditions)

        doc.solve()
        return doc

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
