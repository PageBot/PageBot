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
from pagebot.publications.calendars.basecalendar import BaseCalendar
from pagebot.publications.calendars.photocalendar.coverpage import makeCoverPage
from pagebot.publications.calendars.photocalendar.monthpage import makeMonthPage
from pagebot.mining.filibuster.samplecontent import SampleContent
from pagebot.toolbox.units import mm
from pagebot.toolbox.color import Color, blackColor, whiteColor
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.toolbox.dating import now

class PhotoCalendar(BaseCalendar):
    """Create a photobook with a number of images in a layout and their 
    captions on each page.

    >>> from pagebot.contexts.drawbotcontext import DrawBotContext
    >>> context = DrawBotContext()
    >>> bk = PhotoCalendar()
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
        bookAuthor = context.newString(str(now().year), style=style)
        makeCoverPage(page, imagePath=imagePath0, title=bookTitle, author=bookAuthor, fill=blackColor)
        # Month page with photo and days table
        for month in range(1, 13):
            page = page.next
            makeMonthPage(page, month)
        doc.solve()

        view = doc.view

        return doc

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
