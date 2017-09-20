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
#     HotMetalText.py
#
#     This scripts generates a look-alike revival type specimen for
#     a selection of system fonts.
#
import copy
import pagebot # Import to know the path of non-Python resources.
from pagebot.contributions.filibuster.blurb import blurb
from pagebot import Gradient, Shadow
from pagebot.fonttoolbox.objects.font import findInstalledFonts
      
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

forceTN = False # Look into system fonts, instead of TypeNetwork TYPETR fonts.

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
EXPORT_PATH = '_export/HotMetalText.png' 

def findFont(styleNames, italic=False):
    u"""Find available fonts and closest styles."""
    # Any TypeNetwork TYPETR Productus or Proforma installed in the system?
    fontNames = findInstalledFonts(('Proforma', 'Productus'))
    if not forceTN or not fontNames: # Not installed, find something else that is expected to exist in OSX:
        for pattern in ('Bodoni', 'AmericanTypewriter', 'Avenir', 'Georgia'):
            fontNames = findInstalledFonts(pattern)
            if fontNames:
                break
    for styleName in styleNames:
        for fontName in fontNames:
            if styleName in fontName:
                return fontName
    return None # Nothing found.
    
def drawBefore(e, origin, view):
    # Now the text box must have done the type setting. We can query
    # the position of lines and glyphs.
    for textLine in e.textLines:
        if not textLine.runs:
            continue
        run = textLine.runs[0]
        y = textLine.y
        for index, (x, ry) in enumerate(run.positions):
            if index < len(run.positions)-1:
                nextX, _ = run.positions[index+1]
                fill(0.7)
                stroke(0.8)
                rect(origin[0]+x, origin[1]+y+ry-20, nextX-x, 72) 
                stroke(1)
                line((origin[0]+x, origin[1]+y+ry-20), 
                     (origin[0]+x, origin[1]+y+ry-20+72))
                line((origin[0]+x, origin[1]+y+ry-20+72), 
                     (origin[0]+nextX, origin[1]+y+ry-20+72))
    
def makeDocument():
    u"""Create Document instance with a single page. Fill the page with elements
    and perform a conditional layout run, until all conditions are solved."""
    
    bookName = findFont(('Book', 'Regular')) # Find these styles in order.
    mediumName = findFont(('Medium', 'Book', 'Regular'))
    boldName = findFont(('Bold', 'Medium'))
    
    doc = Document(w=PageWidth, h=PageHeight, originTop=False, autoPages=1)
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
    gradient = Gradient(locations=[1,0], colors=((0.3, 0.3, 0.3), (0.6, 0.6, 0.6)))
    shadow = Shadow(offset=(6, -6), blur=10, color=(0.2, 0.2, 0.2, 0.5))
    bookBorders = dict(stroke=(1, 1, 1, 0.5),strokeWidth=0.1,line=OUTLINE)
    bookPadding = (25, 30, 40, 30)
    
    # Styles
    titleStyle = dict(font=bookName, fontSize=26, rLeading=1.4, xTextAlign=CENTER, textFill=1)
    authorStyle = dict(font=bookName, textFill=1, fontSize=18, xTextAlign=CENTER)
    headStyle = dict(font=boldName, textFill=0, fontSize=62, rLeading=1.4, 
        xTextAlign=LEFT, paragraphTopSpacing=30, openTypeFeatures=dict(liga=True),
        paragraphBottomSpacing=0)
    bodyStyle = dict(font=bookName, textFill=0, fontSize=12, rLeading=1.4, 
        xTextAlign=LEFT, paragraphTopSpacing=10, hyphenation=True)
    
    # Make new container for adding elements inside with alignment.
    newRect(z=10, w=pageAreaW, h=pageAreaH, fill=blockFill, 
        parent=page, margin=0, padding=0, yAlign=MIDDLE, maxW=pageAreaW, 
        maxH=pageAreaH, xAlign=CENTER,  
        conditions=(Center2Center(), Middle2Middle()))
    
    t1 = newTextBox('PageBot Educational Series', z=0, font=bookName, 
        fontSize=42, w=pageAreaW*0.75,  
        parent=page, conditions=(Left2Left(), Top2Top()))
        
    w = pageAreaW*0.75 # Used as element width and relative font size. 
    padding = 24
    
    t2 = newTextBox('Hot metal typesetting', z=0, font=mediumName, 
        fontSize=w/8, w=pageAreaW, parent=page, mt=14,
        conditions=(Left2Left(), Float2Top()))

    i1 = newRect(z=0, h=PageHeight/2, pl=padding, pr=padding,
        gradient=gradient, borders=None, parent=page, 
        conditions=(Fit2Width(), Float2Top(), Fit2Bottom()))
    i1.solve()

    fs = newFS(topT, style=bodyStyle)
    fs += newFS('\nPrepare for what comes next.', style=bookName)
    topText = newTextBox(fs, w=w/3-16, parent=page, 
        conditions=(Top2Top(), Right2Right()))
    
    # Review content. Hard coded ligatures.
    t = u'This is an example of hot metal typesetting, where every letter had a ﬁxed shape and its own width as rectangular box.\nVariable Fonts could adjust, ﬁt and decorate letters where it is most needed in a column of text. Not in this example.'
    fs = newFS(t, style=headStyle)
    t4 = newTextBox(fs, w=w/2-G, mt=10, parent=i1, gradient=None, 
        drawBefore=drawBefore, 
        conditions=(Fit2Width(), Float2Top()))
        
    # Font names
    if 'Proforma' in bookName or 'Productus' in bookName:
        fontNamesFeatures = 'Example featuring typefaces TypeNetwork TYPETR Productus and Proforma'
    else:
        fontNamesFeatures = 'Example featuring OSX system fonts %s' % ', '.join(sorted(set((bookName, mediumName, boldName))))
    fs = newFS(fontNamesFeatures, style=dict(font=bookName, fontSize=14, textFill=0))
    t5 = newTextBox(fs, w=w/2-G, mt=10, parent=page, gradient=None, 
        conditions=(Fit2Width(), Float2Top()))
        
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

