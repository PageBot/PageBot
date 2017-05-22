# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     FrontPage1.py
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
t = u"""Amy's Sun paper hit by hackers. Ignoring the fact that the problem, “was resolved through troubleshooting procedures and restored at midnight,” wrote KLM spokesman Liz Ali III in an e-mail to BSN. Ignoring the fact that the computer malfunction brought Sky Team’s system of scheduling departures, reservations and processing passengers to a halt at airports across Norfolk Island. The problem left passengers stranded for hours in grounded planes, airport lobbies and security lines.
"""
topT = u"""Amy's Sun paper hit by hackers. Ignoring the fact that the problem, was resolved through general procedures."""

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

def makeDocument():
    u"""Create Document instance with a single page. Fill the page with elements
    and perform a conditional layout run, until all conditions are solved."""

    doc = Document(w=PageWidth, h=PageHeight, originTop=False, pages=1)
    # Get default view from the document and set the viewing parameters.
    view = doc.getView()
    view.style['fill'] = 1
    view.padding = 40 # To show cropmarks and such, make >40 or so.
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
    gradient = Gradient(locations=[1,0], colors=((0, 0, 0), (0.8, 0.8, 0.8)))
    shadow = Shadow(offset=(6, -6), blur=10, color=(0.2, 0.2, 0.2, 0.5))
    bookBorders = dict(stroke=(1, 1, 1, 0.5),strokeWidth=0.1,line=OUTLINE)
    bookPadding = (25, 30, 40, 30)
    
    # Styles
    titleStyle =dict(font='Georgia', fontSize=26, rLeading=1.4, xAlign=CENTER, textFill=1)
    authorStyle = dict(font='Georgia-Italic', textFill=1, fontSize=18, xAlign=CENTER)
    headStyle = dict(font='Verdana-Bold', textFill=0, fontSize=14, rLeading=1.4, 
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
    
    t1 = newTextBox('The PageBot Times', z=0, font='BlackmoorLetPlain', 
        fontSize=40, w=pageAreaW/2, 
        parent=page, conditions=(Left2Left(), Top2Top()))
        
    w = pageAreaW*0.75 # Used as element width and relative font size. 
    padding = PageHeight/24
    
    t2 = newTextBox('Book Review', z=0, font='NewOdanaLarge-Black', 
        fontSize=w/7, w=PageWidth*0.75, parent=page, 
        conditions=(Left2Left(), Float2Top()))

    i1 = newRect(z=0, h=PageHeight/2, padding=padding,
        gradient=gradient, borders=None, parent=page, 
        conditions=(Fit2Width(), Float2Top()))
    i1.solve()
    m = i1.h/10    
 
    # Book 1 cover          
    book1 = newRect(z=0, margin=m, w=(i1.w-3*m)/2, 
        fill=(0.05, 0.05, 0.25), 
        gradient=None, parent=i1, shadow=shadow, padding=bookPadding,
        conditions=(Fit2Height(), Top2Top(), Left2Left()),
        borders=bookBorders)
    
    fs = newFS('Educational series', style=authorStyle)
    fs += newFS('\n\nThrilling title\nfor my first book\nabout Design', style=titleStyle)
    fs += newFS('\n'*3 + 'John Smith', style=authorStyle)
    
    frame = newRect(margin=6, conditions=(Fit(),), 
    title1 = newTextBox(fs, parent=book1, shadow=None,
        conditions=(Fit2Width(), Center2Center(), Top2Top())))

    fs = newFS(u'¶', style=authorStyle)
    publisher1 = newTextBox(fs, parent=book1, shadow=None, 
        conditions=(Fit2Width(), Bottom2Bottom()))
    
    # Book 2 cover
    book2 = newRect(z=0, margin=m, w=(i1.w-3*m)/2, 
        fill=(0.1, 0.2, 0.45), 
        gradient=None, parent=i1, shadow=shadow, padding=bookPadding,
        conditions=(Fit2Height(), Top2Top(), Right2Right()),
        borders=bookBorders)

    fs = newFS('Educational series', style=authorStyle)
    fs += newFS('\n\nPredictable title of my second book about Typography', 
        style=titleStyle)
    fs += newFS('\n'*3 + 'John Smith', style=authorStyle)

    title2 = newTextBox(fs, parent=book2, marginTop=120, shadow=None,
        conditions=(Fit2Width(), Center2Center(), Top2Top()))
    
    fs = newFS(u'¶', style=authorStyle)
    publisher2 = newTextBox(fs, parent=book2, shadow=None, 
        conditions=(Fit2Width(), Bottom2Bottom()))
    
    bottomContainer = newRect(parent=page, w=w, 
        borderBottom=dict(strokeWidth=1), padding=0,
        conditions=(Left2Left(), Float2Top(), Fit2Bottom()))
        
    t3 = newTextBox('Reviewing 2017 score', z=0, 
        font='BodoniSvtyTwoOSITCTT-Book', 
        fontSize=w/8.5+3, w=w, stroke=NO_COLOR, pb=16,
        borderBottom=dict(strokeWidth=1), parent=bottomContainer, 
        conditions=(Fit2Width(), Float2Top()), mt=20)
    
    # Review content
    fs = newFS('About the thrilling title\n', style=headStyle)
    fs += newFS(t, style=bodyStyle)    
    t4 = newTextBox(fs, w=w/2-G, mt=10, parent=bottomContainer, 
        conditions=(Left2Left(), Float2Top()))

    fs = newFS('Second column\n', style=headStyle)
    fs += newFS(t, style=bodyStyle)
    t5 = newTextBox(fs, w=w/2-G, mt=10, parent=bottomContainer, 
        conditions=(Float2Right(), Float2Top()))
        
    # Text box on bottom right
    fs = newFS('This is a funny head.\n', style=headStyle)
    fs += newFS(t, style=bodyStyle)
    t6 = newTextBox(fs, w=w/3-16, pt=34, parent=page, 
        conditions=(Float2Right(), Float2Top(), ))

    fs = newFS(topT, style=bodyStyle)
    fs += newFS('\nAn addition italic line', style=italicBodyStyle)
    topText = newTextBox(fs, w=w/3-16, parent=page, 
        conditions=(Top2Top(), Right2Right()))
                      
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

