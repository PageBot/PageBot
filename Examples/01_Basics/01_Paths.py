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
#     01_FilePaths.py
#
#     Shows how get pagebot file paths.
#     Not to be confused with BezierPaths and PageBotPath, which are a different things.
#
import glob
from pagebot import * # Import all top-level values, such as the getContext, function
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.toolbox.units import pt
# Import a standard page size tuple with format (w, h)
from pagebot.constants import A3 
from pagebot.conditions import * 
from pagebot.elements import *
from pagebot.document import Document
from pagebot.toolbox.units import pt

H, W = A3 # Unpack one of the standard page sizes 
GUTTER = pt(12)

def showFilePaths():
    # Get the context that this script runs in, e.g. DrawBotApp.
    context = getContext() 
    # Make a Document instance for this size and context, intializing one page.
    doc = Document(w=W, h=H, originTop=False, autoPages=1, context=context)
    # Get the page.
    page = doc[1]
    # Make a set of conditions for the element positions of this page.
    c = (Left2Left(), Fit2Right(), Float2Top())
    # Find the demo font, as supplied with the PageBot library installation.
    # This is a subset of TYPETR Upgrade Regular.
    f = findFont('PageBot-Regular') 
 
    rootPath = getRootPath() # Location of this PageBot library
    style = dict(fontSize=14, font=f)
    msg = 'Root path is %s' % rootPath
    bs = page.newString(msg, style=style)
    makeText(bs, page, f, c)
    
    resourcesPath = getResourcesPath()
    msg = 'Resources path is %s' % resourcesPath
    bs = page.newString(msg, style=style)
    makeText(bs, page, f, c)
    #print(glob.glob('%s/*' % resourcesPath))
    
    defaultFontPath = getDefaultFontPath()
    msg = 'Default font path is %s' % defaultFontPath
    msg = '\n\t'.join(msg.split('/'))
    bs = page.newString(msg, style=style)
    c = (Right2Right(), Float2Top())
    e = makeText(bs, page, f, c)
    e.w = page.pw/2 - 2*GUTTER
    e.mr = 0
    
    msg = 'PageBot font path is %s' % f.path
    msg = '\n\t'.join(msg.split('/'))
    bs = page.newString(msg, style=style)
    c = (Left2Left(), Float2Top())
    e = makeText(bs, page, f, c)
    e.w = page.pw/2 - 2*GUTTER
    # Let the page solve all of its child element layout conditions
    page.solve()
    doc.build()

def makeText(t, page, f, c):
    return newTextBox(t, font=f, parent=page, conditions=c, fill=0.8, 
        margin=GUTTER)

showFilePaths()
