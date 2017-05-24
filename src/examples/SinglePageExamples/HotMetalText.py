# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     BookReview.py
#
import copy
import pagebot # Import to know the path of non-Python resources.
from pagebot.contributions.filibuster.blurb import blurb
from pagebot import Gradient, Shadow

# Make True to see the names of currently installed fonts, matching the pattern.
if 0: 
    for fontName in installedFonts():
        if 'Bodoni' in fontName:
            print fontName
        
from pagebot.style import getRootStyle, A4, A3, A2, CENTER, NO_COLOR, TOP, BOTTOM, MIDDLE, INLINE, ONLINE, OUTLINE, LEFT
# Document is the main instance holding all information about the document together (pages, views, etc.)
from pagebot.document import Document
# Import all element classes that can be placed on a page.
from pagebot.elements import *
# Import all layout condition classes
from pagebot.conditions import *

from pagebot.toolbox.transformer import path2ScriptId
from pagebot import newFS, getGlobals
# Get set of globals, unique for this script file name.
# This is used to store random information (such as blurb article text), to be consistent
# thought multiple runs of the script. Restart DrawBot to clean the cash and start fresh.
scriptGlobals = getGlobals(path2ScriptId(__file__))

# Some fixed content, as the filling in this example is not robust,
# as there is no overfill function yet.
t = u"""Different from the traditional method (our current system of typesetting is still based on the restriction of type cast in hot metal), Variable Fonts can adapt to any circumstances where text is used. Size, width, weight, typographic details and ornaments, all can be adjusted if needed. E.g. to make a headline fit the width of given column, such as the width of your window or screen."""

topT = u"""Variable Fonts offer great opportunity for publishers, typographers amd graphic designer. And especially for all users of text."""


# Allow some interactive size changed by sliders to show responsive behavior.
MinPageW = A3[0]*0.9 # Minimum width of the page.
MaxPageW = A3[0]*1.2 # Maximum siwidthze of the page.
MinPageH = A3[1]*0.9 # Minimum height of the page.
MaxPageH = A3[1]*1.2 # Maximum height of the page.

PageWidth, PageHeight = A3 # Small newspaper size
PADDING = PageWidth/18 # Padding based on size (= in book layout called margin) of the page.
pt = pl = pr = PADDING
pb = PADDING*1.2
pagePadding = (pt, pr, pb, pl)
G = 12 # Gutter

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/BookReview001.png' 

def drawAfter(e, origin, view):
    # Now the text box must have done the type setting. We can query
    # the position of lines and glyphs.
    for textLine in e.textLines:
        run = textLine.runs[0]
        print run.nsFont
        y = textLine.y
        for index, (x, ry) in enumerate(run.positions):
            if index < len(run.positions)-1:
                nextX, _ = run.positions[index+1]
                fill(None)
                stroke(1)
                rect(origin[0]+x, origin[1]+y+ry-20, nextX-x, 80) 
    

def makeDocument():
    u"""Create Document instance with a single page. Fill the page with elements
    and perform a conditional layout run, until all conditions are solved."""

    doc = Document(w=PageWidth, h=PageHeight, originTop=False, pages=1)
    # Get default view from the document and set the viewing parameters.
    view = doc.getView()
    view.style['fill'] = 1
    view.padding = 0 # To show cropmarks and such, make >40 or so.
    view.showPageCropMarks = True # Won't show if there is not padding in the view.
    view.showPageRegistrationMarks = True
    view.showPageFrame = True
    view.showPageNameInfo = True
    view.showElementOrigin = False
    view.showElementDimensions = False #ShowDimensions
    view.showElementInfo = False
       
    page = doc[0] # Get the single frint page from the document.
    
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding
    
    pageAreaW = PageWidth-pl-pr
    pageAreaH = PageHeight-pt-pb
    
    # Resources
    blockFill = None #(1, 1, 0) # Use color to debug page area
    gradient = Gradient(locations=[1,0], colors=((0.6, 0.6, 0.6), (0.8, 0.8, 0.8)))
    shadow = Shadow(offset=(6, -6), blur=10, color=(0.2, 0.2, 0.2, 0.5))
    bookBorders = dict(stroke=(1, 1, 1, 0.5),strokeWidth=0.1,line=OUTLINE)
    bookPadding = (25, 30, 40, 30)
    
    # Styles
    titleStyle =dict(font='Georgia', fontSize=26, rLeading=1.4, xAlign=CENTER, textFill=1)
    authorStyle = dict(font='Georgia-Italic', textFill=1, fontSize=18, xAlign=CENTER)
    headStyle = dict(font='Proforma-Bold', textFill=0, fontSize=64, rLeading=1.4, 
        xAlign=LEFT, paragraphTopSpacing=30,
    paragraphBottomSpacing=0)
    bodyStyle = dict(font='Verdana', textFill=0, fontSize=12, rLeading=1.4, 
        xAlign=LEFT, paragraphTopSpacing=10, hyphenation=True)
    italicBodyStyle = copy.copy(bodyStyle)
    italicBodyStyle['font'] = 'Verdana-Italic'
    italicBodyStyle['paragraphTopSpacing'] = 0
    
    # Make new container for adding elements inside with alignment.
    newRect(z=10, w=pageAreaW, h=pageAreaH, fill=blockFill, 
        parent=page, margin=0, padding=0, yAlign=MIDDLE, maxW=pageAreaW, 
        maxH=pageAreaH, xAlign=CENTER,  
        conditions=(Center2Center(), Middle2Middle()))
    
    t1 = newTextBox('PageBot Educational Series', z=0, font='Proforma-Book', 
        fontSize=42, w=pageAreaW*0.75,  
        parent=page, conditions=(Left2Left(), Top2Top()))
        
    w = pageAreaW*0.75 # Used as element width and relative font size. 
    padding = 24
    
    t2 = newTextBox('Variable Fonts', z=0, font='Productus-Medium', 
        fontSize=w/7, w=pageAreaW*0.75, parent=page, mt=14,
        conditions=(Left2Left(), Float2Top()))

    i1 = newRect(z=0, h=PageHeight/2, pl=padding, pr=padding,
        gradient=gradient, borders=None, parent=page, 
        conditions=(Fit2Width(), Float2Top(), Fit2Bottom()))
    i1.solve()

    fs = newFS(topT, style=bodyStyle)
    fs += newFS('\nBetter prepare for what comes next.', style=italicBodyStyle)
    topText = newTextBox(fs, w=w/3-16, parent=page, 
        conditions=(Top2Top(), Right2Right()))
    
    # Review content
    fs = newFS('This is an example of hot metal type setting, where every letter has a fixed shape and a fixed width.\nVariable Fonts can adjust, fit and decorate letters where it is most needed in a column of text. ', style=headStyle)
    t4 = newTextBox(fs, w=w/2-G, mt=10, parent=i1, gradient=None, 
        drawAfter=drawAfter, conditions=(Fit2Width(), Float2Top()))
        
    score = page.solve()
    if score.fails:
        print 'Condition fails', score.fails 
    return doc # Answer the doc for further doing.

if __name__ == '__main__':
    
    Variable([
        dict(name='PageWidth', ui='Slider', args=dict(minValue=MinPageW, value=A3[0], maxValue=MaxPageW)),
        dict(name='PageHeight', ui='Slider', args=dict(minValue=MinPageH, value=A3[1], maxValue=MaxPageH)),
    ], globals())

            
    d = makeDocument()
    d.export(EXPORT_PATH) 

