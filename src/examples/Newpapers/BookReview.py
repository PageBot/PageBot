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
import pagebot # Import to know the path of non-Python resources.
from pagebot.contributions.filibuster.blurb import blurb
from pagebot import Gradient, Shadow

if 0:
    for fontName in installedFonts():
        if 'Bodoni' in fontName:
            print fontName
        
from pagebot import getFormattedString
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, A4, A3, A2, CENTER, NO_COLOR, TOP, BOTTOM, MIDDLE, INLINE, ONLINE, OUTLINE
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
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
 
MinPage = A4[0] # Minimum size of the page.
MaxPage = A2[1] # Maximum size of the page.

PageWidth, PageHeight = A3 # Small newspaper size
PADDING = PageWidth/18 # Padding (= in book layout called margin) of the page.

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/FrontPage001.pdf' 

def makeDocument():
    u"""Create Document instance with a single page. Fill the page with elements
    and perform a conditional layout run, until all conditions are solved."""

    doc = Document(w=PageWidth, h=PageHeight, originTop=False, pages=1)
    # Get default view from the document and set the viewing parameters.
    view = doc.getView()
    view.padding = 0 # To show cropmarks and such, make >40 or so.
    view.showPageCropMarks = False # Won't show if there is not padding in the view.
    view.showElementOrigin = False
    view.showElementDimensions = False #ShowDimensions
    view.showElementInfo = False
       
    page = doc[0] # Get the single frint page from the document.
    
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = PADDING
    
    pageAreaW = PageWidth-2*PADDING
    pageAreaH = PageHeight-2*PADDING
    
    blockFill = None
    gradient = Gradient(locations=[1,0], colors=((0, 0, 0), (0.8, 0.8, 0.8)))
    shadow = Shadow(offset=(6, -6), blur=10, color=(0.2, 0.2, 0.2, 0.5))
    
    # Make new container for adding elements inside with alignment.
    newRect(z=10, w=pageAreaW, h=pageAreaH, fill=blockFill, 
        parent=page, margin=0, padding=0, yAlign=MIDDLE, maxW=pageAreaW, 
        maxH=pageAreaH, xAlign=CENTER,  
        conditions=(Center2Center(), Middle2Middle()))
    
    t1 = newTextBox('The PageBot Times', z=0, font='BlackmoorLetPlain', 
        fontSize=40, w=pageAreaW/2, 
        parent=page, conditions=(Left2Left(), Top2Top()), mb=30)
        
    w = pageAreaW*0.75 # Used as element width and relative font size. 
    t2 = newTextBox('Book Review', z=0, font='NewOdanaLarge-Black', 
        fontSize=w/7, w=PageWidth*0.75, parent=page, 
        conditions=(Left2Left(), Float2Top()))

    i1 = newRect(z=0, h=PageHeight/2, padding=PageHeight/20,
        gradient=gradient, borders=None, parent=page, 
        conditions=(Fit2Width(), Float2Top()))
    i1.solve()
    m = i1.h/10    
    titleStyle = style=dict(font='Georgia', fontSize=26, rLeading=1.4,
        xAlign=CENTER, textFill=1)
        
    book1 = newRect(z=0, margin=m, w=(i1.w-3*m)/2, 
        fill=(0.05, 0.05, 0.25), 
        gradient=None, parent=i1, shadow=shadow, padding=30,
        conditions=(Fit2Height(), Top2Top(), Left2Left()),
        borders=dict(stroke=(1, 1, 1, 0.5),strokeWidth=0.1,line=OUTLINE))
    
    fs = getFormattedString('\n\nThrilling title\nfor my first book\nabout Design', style=titleStyle)
    
    frame = newRect(margin=10, conditions=(Fit(),), 
    title1 = newTextBox(fs, parent=book1, marginTop=120,
        conditions=(Fit2Width(), Center2Center(), Top2Top())))
    # Book 1 cover
    
    book2 = newRect(z=0, margin=m, w=(i1.w-3*m)/2, 
        fill=(0.1, 0.2, 0.45), 
        gradient=None, parent=i1, shadow=shadow, padding=20,
        conditions=(Fit2Height(), Top2Top(), Right2Right()),
        borders=dict(stroke=(1, 1, 1, 0.5),strokeWidth=0.1,line=OUTLINE))
    # Book 2 cover
    fs = getFormattedString('\n\nPredictable title of my second book about Typography',
        style=titleStyle)
    title2 = newTextBox(fs, parent=book2, marginTop=120,
        conditions=(Fit2Width(), Center2Center(), Top2Top()))
   
    t3 = newTextBox('Reviewing 2017 score', z=0, 
        font='BodoniSvtyTwoOSITCTT-Book', 
        fontSize=w/8.5, w=w, stroke=NO_COLOR, 
        paddingBottom=20,
        borderBottom=dict(strokeWidth=2), parent=page, 
        conditions=(Left2Left(), Float2Top()), mt=24)
                   
    score = page.solve()
    if score.fails:
        print 'Condition fails', score.fails 
    
    return doc # Answer the doc for further doing.

if __name__ == '__main__':
    
    Variable([
        dict(name='ShowOrigin', ui='CheckBox', args=dict(value=True)),
        #dict(name='ShowDimensions', ui='CheckBox', args=dict(value=True)),
        dict(name='ShowElementInfo', ui='CheckBox', args=dict(value=False)),
        dict(name='PageWidth', ui='Slider', args=dict(minValue=MinPage, value=A3[0], maxValue=MaxPage)),
        dict(name='PageHeight', ui='Slider', args=dict(minValue=MinPage, value=A3[1], maxValue=MaxPage)),
    ], globals())

            
    d = makeDocument()
    d.export(EXPORT_PATH) 

