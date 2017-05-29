# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# ---------------- -------------------------------------------------------------
#
#     ResponsiveTextBox.py
#
#     This script generates a fake article on a single page, using Filibuster text,
#     automatic layout template, Galley, Typesetter and Composer classes.
#     Its purpose is to show the use of Validator
#
import pagebot # Import to know the path of non-Python resources.
from pagebot import newFS, textBoxBaseLines
from pagebot.contributions.filibuster.blurb import blurb

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, LEFT, A4, A1, CENTER, RIGHT, BOTTOM, TOP
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import *
# The Typesetter instance takes content from a file (typically MarkDown text) and converts that 
# into Galley list of elements.
from pagebot.typesetter import Typesetter
# The Composer instance distributes the Galley content of the pages, according to the defined Templates.
from pagebot.composer import Composer 
from pagebot.conditions import *

from pagebot.toolbox.transformer import path2ScriptId
scriptGlobals = pagebot.getGlobals(path2ScriptId(__file__))

    
W, H = A4 #or A1
H = W

Padding_Left = 50
Padding_Bottom = 100
Padding_Right = 50
Padding_Top = 100

Text_Font_Size = 12
Text_Leading = 14
Small_Font_Size = 12
Small_Leading = 14
Small_Top_Spacing = 10

# The standard PageBot function getRootStyle() answers a standard Python dictionary, 
# where all PageBot values are filled by their default values. The root style is kept in RS
# as reference to for all ininitialzaiton of elements. 
# Each element uses the root style as copy and then modifies the values it needs. 
# Note that the use of style dictionaries is fully recursive in PageBot, implementing a cascading structure
# that is very similar to what happens in CSS.

RS = getRootStyle(
    w = W,
    h = H,
    pl = Padding_Left, # Page padding
    pt = Padding_Top,
    pr = Padding_Right,
    pb = Padding_Bottom,
    conditions = [],
    fontSize = 10,
    rLeading = 0,
    originTop = False
)

EXPORT_PATH = '_export/ConditionalElements.pdf' # Export in folder that does not commit un Git. Force to export PDF.

def makeDocument(rootStyle):
    u"""Demo page composer."""
    
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template
    doc = Document(rootStyle, pages=1) 

    # Get default view 
    view = doc.getView()
    view.padding = 40 # Padding space for registration marks and crop marks
    view.showElementOrigin = True
    view.showPageCropMarks = True
    view.showPageRegistrationMarks = True
    view.showPageFrame = True
    view.showPageNameInfo = True

    w = 300

    # Obvious wrong placement of all elements, to be corrected by solving conditions.
    # In this example the wrongOrigin still shows the elements in the bottom left corner,
    # so it is obvious where they are, of not corrected.
    outsideOrigin = (-300, -300)
    
    page = doc.getPage(0) # Get the first/single page of the document.

    e0 = newRect(point=outsideOrigin, name='Page area', parent=page, conditions=[Fit()], fill=0.9)
    e0.z = -10 # Other z-layer, makes this element be ignored on floating checks.

    if not hasattr(scriptGlobals, 'blurbText'):
        scriptGlobals.blurbText = blurb.getBlurb('article_summary', noTags=True)+'\n'
            
    # Construct the text
    headLineFS = newFS(u'Headline\n', style=dict(font='Verdana', fontSize=24, leading=26, textFill=0))

    blurbTextFS = newFS(scriptGlobals.blurbText, page,
        style=dict(font='Georgia', fontSize=Text_Font_Size, leading=Text_Leading, textFill=0))

    smallTextFS = newFS('Closing with a smaller text line.\n', page,
    style=dict(font='Verdana', fontSize=Small_Font_Size, leading=Small_Leading, textFill=0, paragraphTopSpacing=Small_Top_Spacing))
    textFS = headLineFS + blurbTextFS + smallTextFS

    tb = newTextBox(textFS, point=(page.pl, page.pb), parent=page, 
         yAlign=TOP, conditions=[Top2Top(), FitWidth()], stroke=None, fill=None)

    bl = tb.getBaseLines()
    if bl:
        print bl
        print tb.top, bl[0]
        yy = tb.top - bl[0]
        for y in bl:
            stroke(1, 0, 0)
            strokeWidth(0.5)
            fill(None)
            newLine((tb.left, yy - y), parent=page, w=tb.w, h=0, stroke=(1, 0, 0))

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
        
if __name__ == '__main__':

    Variable([
        dict(name='Padding_Left', ui='Slider', args=dict(minValue=0, value=100, maxValue=W)),
        dict(name='Padding_Right', ui='Slider', args=dict(minValue=0, value=50, maxValue=W)),
        dict(name='Padding_Top', ui='Slider', args=dict(minValue=0, value=50, maxValue=W)),
        dict(name='Padding_Bottom', ui='Slider', args=dict(minValue=0, value=100, maxValue=W)),
        dict(name='Text_Font_Size', ui='Slider', args=dict(minValue=9, value=10, maxValue=24)),
        dict(name='Text_Leading', ui='Slider', args=dict(minValue=0, value=10, maxValue=24)),
        dict(name='Small_Font_Size', ui='Slider', args=dict(minValue=9, value=10, maxValue=24)),
        dict(name='Small_Leading', ui='Slider', args=dict(minValue=0, value=10, maxValue=24)),
        dict(name='Small_Top_Spacing', ui='Slider', args=dict(minValue=0, value=10, maxValue=24)),
    ], globals())

    d = makeDocument(RS)
    d.export(EXPORT_PATH) 

        
