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
# ---------------- -------------------------------------------------------------
#
#     ConditionalElements.py
#
#     This script generates a fake article on a single page, using Filibuster text,
#     automatic layout template, Galley, Typesetter and Composer classes.
#     Its purpose is to show the use of Validator
#
import pagebot # Import to know the path of non-Python resources.
from pagebot import textBoxBaseLines
from pagebot.contributions.filibuster.blurb import blurb

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, LEFT, A4, A1, CENTER, RIGHT, BOTTOM, TOP, MIDDLE
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

class FontSizeWidthRatio(Condition):
    def evaluate(self, e):
        if abs(e.x) <= self.tolerance and e.css('fontSize') < 20:
            return self.value
        return self.value * self.errorFactor
		
    def solve(self, e):
        if self.evaluate(e) < 0:
            e.style['fontSize'] = 19
            return self.value
        return self.value * self.errorFactor
       
# For clarity, most of the OneValidatingPage.py example documenet is setup as a sequential excecution of
# Python functions. For complex documents this is not the best method. More functions and classes
# will be used in the real templates, which are available from the OpenSource PageBotTemplates repository.
    
W, H = A4 #or A1
H = W

Padding_Left = 50
Padding_Bottom = 100
Padding_Right = 50
Padding_Top = 100
Element1_W = 50
Element1_H = 50
Element2_W = 50
Element2_H = 50
Element3_W = 50
Element3_H = 50
Element4_W = 50
Element4_H = 50
Element5_W = 50
Element5_H = 50
Text_W = 200

# The standard PageBot function getRootStyle() answers a standard Python dictionary, 
# where all PageBot values are filled by their default values. The root style is kept in RS
# as reference to for all ininitialzaiton of elements. 
# Each element uses the root style as copy and then modifies the values it needs. 
# Note that the use of style dictionaries is fully recursive in PageBot, implementing a cascading structure
# that is very similar to what happens in CSS.

EXPORT_PATH = '_export/ConditionalElements.pdf' # Export in folder that does not commit un Git. Force to export PDF.

def makeDocument():
    u"""Demo page composer."""
    
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template
    doc = Document(w=W, h=H, autoPages=1) 

    # Get default view 
    view = doc.getView()
    view.padding = 0
    view.showElementOrigin = True
    view.showPageCropMarks = True
    view.showPageRegistrationMarks = True
    view.showPageFrame = True
    view.showPageNameInfo = True

    w = 300

    colorCondition1 = [ # Placement condition(s) for the color rectangle elements.
        Right2Right(),
        #Center2Right(),
        #Right2Right(),
        Top2Top(),
    ]
    colorCondition2 = [ # Placement condition(s) for the color rectangle elements.
        Right2Right(),
        #Top2Bottom(),
        Float2Left(),
        Float2Top(),
    ]
    colorCondition3 = [ # Placement condition(s) for the color rectangle elements.
        Right2Right(),
        #Top2Bottom(),
        Float2Left(),
        Float2Top(),
        Fit2Bottom(),
        #Bottom2Bottom(),
    ]
    textCondition = [ # Placement condition(s) for the text element..
        Float2Left(),
        Float2Top(),
    ]    
    page = doc.getPage(0) # Get the first/single page of the document.

    # Other z-layer, makes this element be ignored on floating checks.
    e0 = newRect(z=-10, name='Page area', parent=page, conditions=[Fit()], fill=0.9)
    
    # Add some color elements (same width, different height) at the “wrongOrigin” position.
    # They will be repositioned by solving the colorConditions.
    e1 = newRect(parent=page, name='Other element', 
        w=Element1_W, h=Element1_H, conditions=colorCondition1, 
        fill=(1, 0.5, 0.5), xAlign=RIGHT, yAlign=TOP)
    e2 = newRect(parent=page, w=Element2_W, h=Element2_H, name='Floating element 2', 
        conditions=colorCondition2, fill=(1, 1, 0), xAlign=LEFT, yAlign=TOP)
    e3 = newRect(parent=page, w=Element3_W, h=Element3_H, name='Floating element 3', 
        conditions=colorCondition2, fill=(1, 0, 1), xAlign=LEFT, yAlign=TOP)
    # Make text box at wrong origin. Apply same width a the color rect, which may
    # be too wide from typographic point ogf view. The MaxWidthByFontSize will set the 
    # self.w to the maximum width for this pointSize.
    if not hasattr(scriptGlobals, 'blurbText'):
        scriptGlobals.blurbText = doc.context.newString(blurb.getBlurb('article_summary', noTags=True),
                                                        page,
                                                        style=dict(font='Georgia',
                                                                   fontSize=12,
                                                                   leading=16,
                                                                   textColor=0))
    eTextBox = newTextBox(scriptGlobals.blurbText, parent=page, w=Text_W, 
        conditions=textCondition, xAlign=CENTER, yAlign=MIDDLE, stroke=None, fill=None)

    e4 = newRect(parent=page, w=Element4_W, h=Element4_H, name='Floating element 4', 
        conditions=colorCondition3, fill=(0, 1, 1), xAlign=RIGHT, yAlign=TOP, minH=50, maxH=150)
    e5 = newRect(parent=page, w=Element5_W, h=Element5_H, name='Floating element 5', 
        conditions=[Float2RightTopSides()], fill=(0, 1, 0), xAlign=LEFT, yAlign=TOP)

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
        dict(name='Element1_W', ui='Slider', args=dict(minValue=20, value=50, maxValue=W)),
        dict(name='Element1_H', ui='Slider', args=dict(minValue=20, value=50, maxValue=H)),
        dict(name='Element2_W', ui='Slider', args=dict(minValue=20, value=50, maxValue=W)),
        dict(name='Element2_H', ui='Slider', args=dict(minValue=20, value=50, maxValue=H)),
        dict(name='Element3_W', ui='Slider', args=dict(minValue=20, value=50, maxValue=W)),
        dict(name='Element3_H', ui='Slider', args=dict(minValue=20, value=50, maxValue=H)),
        dict(name='Element4_W', ui='Slider', args=dict(minValue=20, value=50, maxValue=W)),
        dict(name='Element4_H', ui='Slider', args=dict(minValue=20, value=50, maxValue=H)),
        dict(name='Element5_W', ui='Slider', args=dict(minValue=20, value=50, maxValue=W)),
        dict(name='Element5_H', ui='Slider', args=dict(minValue=20, value=50, maxValue=H)),
        dict(name='Text_W', ui='Slider', args=dict(minValue=100, value=200, maxValue=W)),
    ], globals())

    d = makeDocument()
    d.export(EXPORT_PATH) 

        
