# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     MakeABookCover.py
#
import pagebot # Import to know the path of non-Python resources.
from pagebot import getFormattedString
from pagebot.contributions.filibuster.blurb import blurb # Create random title and names
from pagebot.toolbox.transformer import lighter, darker, moreBlue, lessRed

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, B4, CENTER, LEFT_ALIGN, TOP_ALIGN
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.elements.document import Document
# Import element layout conditions.
from pagebot.conditions import *
   
# For clarity, most of the OneValidatingPage.py example documenet is setup as a sequential excecution of
# Python functions. For complex documents this is not the best method. More functions and classes
# will be used in the real templates, which are available from the OpenSource PageBotTemplates repository.
    
W, H = B4 
W -= 48 # Make a bit more narrow format.

if 0: # If showing registration/cutting marks, increase side of the document.
    docW = W+200
    docH = H+200
else:
    docW = W
    docH = H
# The standard PageBot function getRootStyle() answers a standard Python dictionary, 
# where all PageBot values are filled by their default values. The root style is kept in RS
# as reference to for all ininitialzaiton of elements. 
# Each element uses the root style as copy and then modifies the values it needs. 
# Note that the use of style dictionaries is fully recursive in PageBot, implementing a cascading structure
# that is very similar to what happens in CSS.

RS = getRootStyle(
    w = W,
    h = H,
    pl = 64,
    pt = 64,
    pr = 64,
    pb = 80,
    docW = docW,
    docH = docH,
    showElementInfo = False,
    originTop = True,
)

EXPORT_PATH = '_export/ABookCover.pdf' # Export in folder that does not commit un Git. Force to export PDF.

def makeDocument(rootStyle):
    u"""Demo random book cover generator."""
    
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template
    doc = Document(rootStyle, pages=1) # One page, just the cover.
 
    page = doc[1] # Get the first/single page of the document.

    C1 = (random()*0.2, random()*0.2, random()*0.9)
    C2 = lighter(C1, 0.9) # Almost white, tinted to the background color.
    C3 = darker(C1, 0.75) # Default parameter 50% between background color and white.
    C4 = darker(C1, 0.5) # Default parameter 50% between background color and white.
    
    # Make background element, filling the page color and bleed.
    background = page.rect(name='Page area', conditions=[Top2TopSide(), Left2LeftSide(), FitRightSide(), FitBottomSide()], fill=C1)
    background.z = -10 # Other z-layer, makes this element be ignored on floating checks.
    
    frame1 = page.rect(name='Frame', conditions=[Top2Top(), Left2Left(), FitRight(), FitBottom()], fill=C3, stroke=None)
    frame1.z = -10 # Other z-layer, makes this element be ignored on floating checks.
    frame1.solve() # Solve element position, before we can make other elements depend on position and size.

    M = 64
    frame2 = page.rect(name='Frame', conditions=[Center2Center(), Center2VerticalCenter()], fill=C4, stroke=None, 
        w=frame1.w-M, h=frame1.h-M, align=CENTER, vAlign=CENTER )
    frame2.z = -10 # Other z-layer, makes this element be ignored on floating checks.

    # Add some title (same width, different height) at the “wrongOrigin” position.
    # They will be repositioned by solving the colorConditions.
    e1 = page.text('Book Cover', style=rootStyle, name='Other element', font='Georgia', fontSize=40,
        fill=(0.3, 0.3, 0.5), textFill=(1, 0, 0),
        conditions=[Top2VerticalCenter(), Top2Top()], 
        align=CENTER) #vAlign=TOP_ALIGN)
    e1.y = e1.css('pt')
    e1.center = page.w/2
    print '@#@#@#', e1.h, e1.getTextSize()
    """
    e2 = page.rect(point=wrongOrigin, style=rootStyle, w=W2, h=H2, name='Floating element 2', 
        conditions=colorCondition2, fill=(1, 1, 0), align=LEFT_ALIGN, vAlign=TOP_ALIGN)
    e3 = page.rect(point=wrongOrigin, style=rootStyle, w=W3, h=H3, name='Floating element 3', 
        conditions=colorCondition2, fill=(1, 0, 1), align=LEFT_ALIGN, vAlign=TOP_ALIGN)
    # Make text box at wrong origin. Apply same width a the color rect, which may
    # be too wide from typographic point ogf view. The MaxWidthByFontSize will set the 
    # self.w to the maximum width for this pointSize.
    if not hasattr(pbglobals, 'blurbText'):
        pbglobals.blurbText = getFormattedString(blurb.getBlurb('article_summary', noTags=True), page,
        style=dict(font='Georgia', fontSize=12, rLeading=0.2, textColor=0))
    eTextBox = page.textBox(pbglobals.blurbText, point=wrongOrigin, style=rootStyle, w=WT, 
        vacuumH=True, conditions=textCondition, align=CENTER, vAlign=CENTER)

    e4 = page.rect(point=wrongOrigin, style=rootStyle, w=W4, h=H4, name='Floating element 4', 
        conditions=colorCondition2, fill=(0, 1, 1), align=LEFT_ALIGN, vAlign=TOP_ALIGN)
    e5 = page.rect(point=wrongOrigin, style=rootStyle, w=W5, h=H5, name='Floating element 5', 
        conditions=[FloatRightTopSides()], fill=(0, 1, 0), align=LEFT_ALIGN, vAlign=TOP_ALIGN)
    """
    score = page.evaluate()
    #print 'Page value on evaluation:', score
    #print score.fails
    # Try to solve the problems if evaluation < 0
    if score.result < 0:
        print 'Solving', score
        page.solve()
    #print score.fails
    # Evaluate again, result should now be >= 0
    score = page.evaluate()
    print 'Page value after solving the problems:', score
    for fail in score.fails:
        print fail
    
    return doc
        
d = makeDocument(RS)
d.export(EXPORT_PATH) 

    
