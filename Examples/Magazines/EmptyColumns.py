# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     UpgradePaper.py
#
import copy
import pagebot # Import to know the path of non-Python resources.
from pagebot.contributions.filibuster.blurb import blurb
from pagebot import Gradient, Shadow

# Make True to see the names of currently installed fonts, matching the pattern.
if 0: 
    for fontName in installedFonts():
        if 'Upgrade' in fontName:
            print fontName
        
from pagebot.style import getRootStyle, A4, FIT, CENTER, NO_COLOR, TOP, BOTTOM, MIDDLE, INLINE, ONLINE, OUTLINE, LEFT
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

PageWidth, PageHeight = A4 # Small magazine size
PADDING = PageWidth/22 # Padding based on size (= in book layout called margin) of the page.
pt = pl = pr = PADDING
pb = PADDING*1.2
pagePadding = (pt, pr, pb, pl)
G = 12 # Gutter

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/BookReview001.png' 

def makeDocument():
    u"""Create Document instance with a single page. Fill the page with elements
    and perform a conditional layout run, until all conditions are solved."""

    doc = Document(w=PageWidth, h=PageHeight, originTop=False, autoPages=1)
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
    view.showGridColumns = True
    view.showGrid = True
    #view.style['showGridCo
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
    
    # Styles
    coverTitleStyle = dict(font='Georgia', fontSize=80, rLeading=1.4, xTextAlign=CENTER, textFill=(1,0,0))
    titleStyle = dict(font='Georgia', fontSize=26, rLeading=1.4, xTextAlign=CENTER, textFill=1)
    authorStyle = dict(font='Georgia-Italic', textFill=1, fontSize=18, xTextAlign=CENTER)
    headStyle = dict(font='Verdana-Bold', textFill=0, fontSize=14, rLeading=1.4, 
        xTextAlign=LEFT, paragraphTopSpacing=30,
    paragraphBottomSpacing=0)
    bodyStyle = dict(font='Verdana', textFill=0, fontSize=12, rLeading=1.4, 
        xTextAlign=LEFT, paragraphTopSpacing=10, hyphenation=True)
    italicBodyStyle = copy.copy(bodyStyle)
    italicBodyStyle['font'] = 'Verdana-Italic'
    italicBodyStyle['paragraphTopSpacing'] = 0
 
    # Adding width to formatted string request will scale fontSize of 
    # style to force fit width.
    fs = newFS('Magazine', w=page.pw, style=coverTitleStyle)
    # Keep h=None, to make vertical elastic box, depending on content.
    tb = newTextBox(fs, parent=page,  
        showBaselines=True,
        conditions=[Fit2Width(), Top2TopSide()] 
    )
        
    score = page.solve()
    if score.fails:
        print 'Condition fails', score.fails 
    
    return doc # Answer the doc for further doing.

            
d = makeDocument()
d.export(EXPORT_PATH) 

