# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     FontBureauSpecimen.py
#
from pagebot.contexts import defaultContext as context
from pagebot.contributions.filibuster.blurb import blurb
from pagebot.fonttoolbox.objects.family import guessFamiliesByPatterns

familyName = 'Roboto' # We know this exists in the PageBot repository
families = guessFamiliesByPatterns(familyName)
# We can be sure the family exists, as it comes from the embedded Roboto.
family = families[familyName]
# TODO: Finding font by name/weight/width association does not work properly yet.
font = family.findFont(name='Regular',width='Normal')
print font

fontPaths = []
# Make True to see the names of currently installed fonts, matching the pattern.
if 0: 
    for fontName in installedFonts():
        if 'Upgrade' in fontName:
            print fontName
        
from pagebot.style import getRootStyle, A2, A3, A4, CENTER, NO_COLOR, TOP, BOTTOM, MIDDLE, INLINE, ONLINE, OUTLINE, LEFT
# Document is the main instance holding all information about the document together (pages, views, etc.)
from pagebot.document import Document
# Import all element classes that can be placed on a page.
from pagebot.elements import *
# Import all layout condition classes
from pagebot.conditions import *

from pagebot.toolbox.transformer import path2ScriptId
from pagebot import getGlobals
# Get set of globals, unique for this script file name.
# This is used to store random information (such as blurb article text), to be consistent
# thought multiple runs of the script. Restart DrawBot to clean the cash and start fresh.
scriptGlobals = getGlobals(path2ScriptId(__file__))
# Allow some interactive size changed by sliders to show responsive behavior.
W, H = PAGE_SIZE = A4 # A3 A2
MinPageW = PAGE_SIZE[0]*0.9 # Minimum width of the page.
MaxPageW = PAGE_SIZE[0]*1.2 # Maximum siwidthze of the page.
MinPageH = PAGE_SIZE[1]*0.9 # Minimum height of the page.
MaxPageH = PAGE_SIZE[1]*1.2 # Maximum height of the page.

PageWidth, PageHeight = PAGE_SIZE # Small newspaper size
PADDING = PageWidth/18 # Padding based on size (= in book layout called margin) of the page.
pt = pl = pr = PADDING
pb = PADDING*1.2
pagePadding = (pt, pr, pb, pl)
G = 12 # Gutter
# Column widths
CW1 = (W - 2*PADDING - G)*3/5
CW2 = (W - 2*PADDING - G)*2/5
# Define grid measures for the pages. 
gridX = ((CW1, G), (CW2, None))

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/BookReview001.png' 

def makeDocument():
    u"""Create Document instance with a single page. Fill the page with elements
    and perform a conditional layout run, until all conditions are solved."""

    doc = Document(w=PageWidth, h=PageHeight, originTop=False, autoPages=1, gridX=gridX)
    # Get default view from the document and set the viewing parameters.
    view = doc.getView()
    view.style['fill'] = 1
    view.padding = 40 # To show cropmarks and such, make >40 or so.
    view.showPageCropMarks = True # Won't show if there is not padding in the view.
    view.showPageRegistrationMarks = True
    view.showPageFrame = True
    view.showPagePadding = True
    view.showPageNameInfo = True
    view.showElementOrigin = False
    view.showElementDimensions = False #ShowDimensions
    view.showElementInfo = False
    view.showGrid = True
    
    page = doc[0] # Get the single frint page from the document.
    page.padding = pagePadding 
     
    # Resources
    blockFill = None #(1, 1, 0) # Use color to debug page area
    
    # Styles
    titleStyle =dict(font='Georgia', fontSize=26, rLeading=1.4, xTextAlign=CENTER, textFill=1)
    authorStyle = dict(font='Georgia-Italic', textFill=1, fontSize=18, xTextAlign=CENTER)
    headStyle = dict(font='Verdana-Bold', textFill=0, fontSize=14, rLeading=1.4, 
        xTextAlign=LEFT, paragraphTopSpacing=30, paragraphBottomSpacing=0)
    bodyStyle = dict(font='Verdana', textFill=0, fontSize=12, rLeading=1.4, 
        xTextAlign=LEFT, paragraphTopSpacing=10, hyphenation=True)
   
     
    score = page.solve()
    if score.fails:
        print 'Condition fails', score.fails 
    
    return doc # Answer the doc for further doing.

  
context.Variable([
    dict(name='PageWidth', ui='Slider', args=dict(minValue=MinPageW, value=PAGE_SIZE[0], maxValue=MaxPageW)),
    dict(name='PageHeight', ui='Slider', args=dict(minValue=MinPageH, value=PAGE_SIZE[1], maxValue=MaxPageH)),
], globals())

        
d = makeDocument()
d.export(EXPORT_PATH) 

