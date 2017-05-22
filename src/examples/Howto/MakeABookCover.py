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
from pagebot import newFS
from pagebot.contributions.filibuster.blurb import blurb # Create random title and names
from pagebot.toolbox.transformer import lighter, darker, moreBlue, lessRed

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, B4, CENTER, LEFT, TOP
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.document import Document
# Import element layout conditions.
from pagebot.conditions import *
from pagebot.elements import *
   
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
    showElementOrigin = True,
    originTop = True,
)

EXPORT_PATH = '_export/ABookCover.pdf' # Export in folder that does not commit un Git. Force to export PDF.

def makeDocument(rootStyle):
    u"""Demo random book cover generator."""
    
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template
    doc = Document(rootStyle, w=W, h=H, pages=1) # One page, just the cover.
 
    page = doc[0] # Get the first/single page of the document.

    C1 = (random()*0.2, random()*0.2, random()*0.9)
    C2 = lighter(C1, 0.9) # Almost white, tinted to the background color.
    C3 = darker(C1, 0.75) # Default parameter 50% between background color and white.
    C4 = darker(C1, 0.5) # Default parameter 50% between background color and white.
    
    # Make background element, filling the page color and bleed.
    colorRect1 = pageArea = newRect(z=-10, name='Page area', parent=page,
        conditions=[Top2TopSide(), Left2LeftSide(), Fit2RightSide(), Fit2BottomSide()], fill=C1)
    
    colorRect1.solve() # Solve element position, before we can make other elements depend on position and size.

    M = 64
    colorRect2 = newRect(z=-10, name='Frame 2', conditions=[Center2Center(), Middle2Middle()], 
        fill=C4, stroke=None, 
        w=colorRect1.w-M, h=colorRect1.h-M, xAlign=CENTER, yAlign=CENTER )

    # Add some title (same width, different height) at the “wrongOrigin” position.
    # They will be repositioned by solving the colorConditions.
    e1 = newText('Book Cover', style=rootStyle, parent=page, name='Other element', 
        font='Georgia', fontSize=40, fill=(0.3, 0.3, 0.5), textFill=(1, 0, 0),
        conditions=[Top2Middle(), Top2Top()], 
        xAlign=CENTER) #yAlign=TOP)
    """
    e2 = page.rect(point=wrongOrigin, style=rootStyle, w=W2, h=H2, name='Floating element 2', 
        conditions=colorCondition2, fill=(1, 1, 0), xAlign=LEFT, yAlign=TOP)
    e3 = page.rect(point=wrongOrigin, style=rootStyle, w=W3, h=H3, name='Floating element 3', 
        conditions=colorCondition2, fill=(1, 0, 1), xAlign=LEFT, yAlign=TOP)
    # Make text box at wrong origin. Apply same width a the color rect, which may
    # be too wide from typographic point ogf view. The MaxWidthByFontSize will set the 
    # self.w to the maximum width for this pointSize.
    if not hasattr(pbglobals, 'blurbText'):
        pbglobals.blurbText = newFS(blurb.getBlurb('article_summary', noTags=True), page,
        style=dict(font='Georgia', fontSize=12, rLeading=0.2, textColor=0))
    eTextBox = page.textBox(pbglobals.blurbText, point=wrongOrigin, style=rootStyle, w=WT, 
        conditions=textCondition, xAlign=CENTER, yAlign=CENTER)

    e4 = page.rect(point=wrongOrigin, style=rootStyle, w=W4, h=H4, name='Floating element 4', 
        conditions=colorCondition2, fill=(0, 1, 1), xAlign=LEFT, yAlign=TOP)
    e5 = page.rect(point=wrongOrigin, style=rootStyle, w=W5, h=H5, name='Floating element 5', 
        conditions=[FloatRightTopSides()], fill=(0, 1, 0), xAlign=LEFT, yAlign=TOP)
    """
    score = page.evaluate()
    #print 'Page value on evaluation:', score
    #print score.fails
    # Try to solve the problems if evaluation < 0
    if score.fails:
        print 'Solving', score.fails
        page.solve()
    #print score.fails
    # Evaluate again, result should now be >= 0
    score = page.evaluate()
    print 'Page value after solving the problems:', score
    for fail in score.fails:
        print fail
    
    return doc
  
if __name__ == '__main__':      
    d = makeDocument(RS)
    d.export(EXPORT_PATH) 

    
