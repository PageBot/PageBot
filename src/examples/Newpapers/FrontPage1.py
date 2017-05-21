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

if 0:
    for fontName in installedFonts():
        if 'Bodoni' in fontName:
            print fontName
        
from pagebot import getFormattedString
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, A4, A3, A2, CENTER, NO_COLOR, TOP, BOTTOM, MIDDLE
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
PADDING = PageWidth/15 # Padding (= normally called margin) of the page.


ShowOrigin = False
#ShowDimensions = False
ShowElementInfo = False

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/FrontPage001.pdf' 

def makeDocument():
    u"""Create Document instance with a single page. Fill the page with elements
    and perform a conditional layout run, until all conditions are solved."""

    doc = Document(w=PageWidth, h=PageHeight, originTop=False, pages=1)
    # Get default view from the document and set the viewing parameters.
    view = doc.getView()
    view.padding = 0 # To show cropmarks and such, make >40 or so.
    view.showPageCropMarks = True # Won't show if there is not padding in the view.
    view.showElementOrigin = ShowOrigin
    view.showElementDimensions = False #ShowDimensions
    view.showElementInfo = ShowElementInfo
       
    page = doc[0] # Get the single frint page from the document.
    
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = PADDING
    
    pageAreaW = PageWidth-2*PADDING
    pageAreaH = PageHeight-2*PADDING
    
    # Make new container for adding elements inside with alignment.
    newRect(z=10, w=pageAreaW, h=pageAreaH, fill=(0.8, 0.8, 0.8, 0.4), 
        parent=page, margin=0, padding=0, yAlign=MIDDLE, maxW=pageAreaW, 
        maxH=pageAreaH, xAlign=CENTER, stroke=None, 
        conditions=(Center2Center(), Middle2Middle()))
    
    t1 = newTextBox('The PageBot Times', z=0, font='BlackmoorLetPlain', 
        fontSize=40, w=pageAreaW/2,
        parent=page, conditions=(Left2Left(), Top2Top()), mb=30)
        
    w = pageAreaW*0.75 # Used as element width and relative font size. 
    t2 = newTextBox('Book Review', z=0, font='NewOdanaLarge-Black', 
        fontSize=w/8, w=PageWidth*0.75,
        parent=page, conditions=(Left2Left(), Float2Top()))
            
    i1 = newRect(z=0, fill=(0.7, 0, 0), h=PageHeight/2, borderLeft=40, 
        parent=page, conditions=(Fit2Width(), Float2Top()))
    print i1.borders
    i2 = newRect(z=0, fill=(0.7, 0.7, 0), h=48,
        parent=page, conditions=(Fit2Width(), Float2Top()))

    t3 = newTextBox('Reviewing 2017 score', z=0, font='BodoniSvtyTwoOSITCTT-Book', 
        fontSize=w/10, w=w, borders=3,
        parent=page, conditions=(Left2Left(), Float2Top()), mt=24)
                   
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

