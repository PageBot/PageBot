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
#     01_Paths.py
#
#     Shows how get pagebot file paths.
#     Not to be confused with BezierPaths, which is a different thing.
#
from pagebot import *
import glob
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.toolbox.units import pt
from pagebot.constants import A3
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document

H, W = A3

def showPaths():
    context = getContext()
    doc = Document(w=W, h=H, originTop=False, autoPages=1, context=context)
    page = doc[1]

    c = (Fit2Right(), Left2Left(), Float2Top())
    f = findFont('PageBot-Regular')

    # FIXME: text disappears with padding.
    #t = newText('bla', font='Helvetica', parent=page, conditions=c, fontSize=200, padding=1)

    # FIXME: causes scaling unit error.
    #path = newPageBotPath(context=context)
    #path.text('ABCD', style=dict(font=f, fontSize=30, fill=(0, 1, 0)))
    #newPaths(path, parent=page, fill=(0, 1, 1), conditions=c, stroke=None)

    rootPath = getRootPath()
    s = dict(fontSize=24, font=f)
    msg = 'Root path is %s' % rootPath
    bs = page.newString(msg, style=s)
    makeText(bs, page, c)
    resourcesPath = getResourcesPath()
    msg = 'Resources path is %s' % resourcesPath
    bs = page.newString(msg, style=s)
    makeText(bs, page, c)
    print(glob.glob('%s/*' % resourcesPath))
    defaultFontPath = getDefaultFontPath()
    msg = 'Default font path is %s' % defaultFontPath
    bs = page.newString(msg, style=s)
    makeText(bs, page, c)
    page.solve()
    doc.build()

def makeText(t, page, c):
    newText(t, font='Helvetica', parent=page, conditions=c, fontSize=32)

showPaths()
