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
from pagebot.publications.books.photobook.coverpage import makeCoverPage
from pagebot.publications.books.photobook.titlepage import makeTitlePage
from pagebot.mining.filibuster.samplecontent import SampleContent
from pagebot.toolbox.units import mm
from pagebot.toolbox.color import Color, blackColor, whiteColor
from pagebot.fonttoolbox.objects.font import findFont

class PhotoBook(BaseBook):
    """Create a photobook with a number of images in a layout and their 
    captions on each page.

    >>> from pagebot.contexts.drawbotcontext import DrawBotContext
    >>> context = DrawBotContext()
    >>> bk = PhotoBook()
    >>> doc = bk.makeSample(context)
    >>> doc.export('_export/PhotoBookSample.pdf')

    """
    def makeSample(self, context, name=None):
        padding = mm(40) 
        w, h = A4Square
        styles = {}
        sampleContent = SampleContent()
        imagePath0 = sampleContent.imagePaths[0]
        imagePath1 = sampleContent.imagePaths[1]
        doc = self.newDocument(w=w, h=h, autoPages=1, padding=padding, originTop=False,
            context=context)
        # Book cover
        page = doc[1]
        fontLight = findFont('PageBot-Light')
        fontBook = findFont('PageBot-Book')
        fontSize = 80
        style = dict(font=fontLight, fontSize=fontSize, textFill=whiteColor)
        bookTitle = context.newString(name or self.__class__.__name__, style=style)
        style = dict(font=fontLight, fontSize=fontSize/2, textFill=whiteColor)
        bookAuthor = context.newString('Created by PageBot', style=style)
        makeCoverPage(page, imagePath=imagePath0, title=bookTitle, author=bookAuthor, fill=blackColor)
        # Page with title and 2 columns
        page = page.next
        makeTitlePage(page, bookTitle, bookAuthor)
        # Page with color square
        page = page.next
        newImage(imagePath0, w=page.pw, h=page.ph, parent=page, strokeWidth=6, stroke=Color(0x273818), 
            conditions=[Fit()])
        # Page with full untouched photo
        page = page.next
        newImage(imagePath0, x=padding, y=padding, 
            w=page.pw, h=page.ph, parent=page, conditions=[Fit()])
        # Page with filtered photos
        page = page.next
        for conditions in (
            (Left2Left(), Top2Top()),
            (Right2Right(), Top2Top()),
            (Left2Left(), Bottom2Bottom()),
            (Right2Right(), Bottom2Bottom())
        ):
            newImage(imagePath0, x=padding, y=padding, 
                w=page.pw/2, h=page.ph/2, parent=page, conditions=conditions)
        doc.solve()

        view = doc.view

        return doc

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
