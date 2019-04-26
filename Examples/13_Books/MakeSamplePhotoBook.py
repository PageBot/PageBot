#!/usr/bin/env python3
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
#     MakeSamplePhotoBook.py
#
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.publications.books import PhotoBook

context = DrawBotContext()
bk = PhotoBook()
doc = bk.makeSample(context)
doc.export('_export/PhotoBookSample.pdf')

