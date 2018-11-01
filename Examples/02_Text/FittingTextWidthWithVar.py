#!/usr/bin/evn python
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
#     FittingTextWidth.py
#
from pagebot.document import Document
from pagebot.elements import newText
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/UseFittingTextWidth.pdf'


def fit():
    varFont = findFont('RobotoDelta-VF')
    print(varFont.axes)
    wideFont = getVarFontInstance(varFont, dict(wdth=125, YTUC=528))
    boldFont = getVarFontInstance(varFont, dict(wght=900, GRAD=1))

    W, H = 500, 350
    PADDING = 20

    doc = Document(w=W, h=H, originTop=False)
    view = doc.view
    context = view.context

    page = doc[1] # Get page on pageNumber, first in row (this is only one now).
    page.padding = PADDING

    s = 'ABCDEF'

    labelStyle = dict(font=varFont.path, fontSize=8, textFill=(1, 0, 0))

    style = dict(font=varFont.path, fontSize=10)
    bs = context.newString(s, style=style, w=W-2*PADDING)
    newText(bs, x=20, y=180, w=W-2*PADDING, h=H, parent=page)
    labelS = context.newString('Original var-font %0.2fpt' % (bs.fontSize), style=labelStyle)
    newText(labelS, x=20, y=220, parent=page)

    style = dict(font=wideFont.path, fontSize=10)
    bs = context.newString(s, style=style, w=W-2*PADDING)
    newText(bs, x=20, y=100, w=W-2*PADDING, h=H, parent=page)
    labelS = context.newString('Wide %0.2fpt %s' % (bs.fontSize, wideFont.info.location), style=labelStyle)
    newText(labelS, x=20, y=130, parent=page)

    style = dict(font=boldFont.path, fontSize=10)
    bs = context.newString(s, style=style, w=W-2*PADDING)
    newText(bs, x=20, y=-30, w=W-2*PADDING, h=H, parent=page)
    labelS = context.newString('Bold %0.2fpt %s' % (bs.fontSize, boldFont.info.location), style=labelStyle)
    newText(labelS, x=20, y=10, parent=page)

    doc.export(EXPORT_PATH)

fit()
