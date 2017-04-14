# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# ---------------- -------------------------------------------------------------
#
#     ConditionalElements.py
#
#     This script generates a fake article on a single page, using Filibuster text,
#     automatic layout template, Galley, Typesetter and Composer classes.
#     Its purpose is to show the use of Validator
#
import pagebot # Import to know the path of non-Python resources.
from pagebot import getFormattedString, textBoxBaseLines
from pagebot.contributions.filibuster.blurb import blurb

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, LEFT_ALIGN, A4, A1, CENTER, RIGHT_ALIGN, BOTTOM_ALIGN, TOP_ALIGN
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.elements.document import Document
from pagebot.elements.galley import Galley
# The Typesetter instance takes content from a file (typically MarkDown text) and converts that 
# into Galley list of elements.
from pagebot.typesetter import Typesetter
# The Composer instance distributes the Galley content of the pages, according to the defined Templates.
from pagebot.composer import Composer 
from pagebot.conditions import *

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

# Make an instance of all conditions add as global in Variations.
ConditionsV = [
	Bottom2Bottom(),
	Bottom2BottomSide(),
	Bottom2VerticalCenter(),
	Bottom2VerticalCenterSides(),
	Center2Bottom(),
	Center2BottomSide(),
	Center2Top(),
	Center2TopSide(),
	Center2VerticalCenter(),
	Center2VerticalCenterSides(),
	FitBottom(),
	FitBottomSide(),
	FitTop(),
	FitTopSide(),
	Origin2Bottom(),
	Origin2BottomSide(),
	Origin2Top(),
	Origin2TopSide(),
	Origin2VerticalCenter(),
	Origin2VerticalCenterSides(),
	Top2Bottom(),
	Top2Top(),
	Top2TopSide(),
	Top2VerticalCenter(),
	Top2VerticalCenterSides(),
	FloatTop(),
	FloatBottom(),
	FloatTopLeft(),
	FloatTopRight(),
	FloatBottomLeft(),
	FloatBottomRight(),
	FloatLeftTop(),
	FloatRightTop(),
	FloatLeftBottom(),
	FloatRightBottom(),
	
]
ConditionsH = [
	Center2Center(),
	Center2CenterSides(),
	Center2Left(),
	Center2LeftSide(),
	Center2Right(),
	Center2RightSide(),
	Fit(),
	FitLeft(),
	FitLeftSide(),
	FitRight(),
	FitRightSide(),
	FitSides(),
	Left2Center(),
	Left2CenterSides(),
	Left2Left(),
	Left2LeftSide(),
	Left2Right(),
	Origin2Center(),
	Origin2CenterSides(),
	Origin2Left(),
	Origin2LeftSide(),
	Origin2Right(),
	Origin2RightSide(),
	Right2Center(),
	Right2CenterSides(),
	Right2Left(),
	Right2Right(),
	Right2RightSide(),
	FloatLeft(),
	FloatRight(),
	FloatTopLeft(),
	FloatTopRight(),
	FloatBottomLeft(),
	FloatBottomRight(),
	FloatLeftTop(),
	FloatRightTop(),
	FloatLeftBottom(),
	FloatRightBottom(),
]
ConditionsVDict = {}
for condition in ConditionsV:
    ConditionsVDict[condition.__class__.__name__] = condition
ConditionsHDict = {}
for condition in ConditionsH:
    ConditionsHDict[condition.__class__.__name__] = condition
ConditionH = 0
ConditionV = 0

Variable([
    dict(name='ConditionH', ui='PopUpButton', args=dict(items=sorted(ConditionsHDict.keys()))),
    dict(name='ConditionV', ui='PopUpButton', args=dict(items=sorted(ConditionsVDict.keys()))),
], globals())

       
# For clarity, most of the OneValidatingPage.py example documenet is setup as a sequential excecution of
# Python functions. For complex documents this is not the best method. More functions and classes
# will be used in the real templates, which are available from the OpenSource PageBotTemplates repository.
    
W, H = 400, 400#A4 # or A1
H = W

# The standard PageBot function getRootStyle() answers a standard Python dictionary, 
# where all PageBot values are filled by their default values. The root style is kept in RS
# as reference to for all ininitialzaiton of elements. 
# Each element uses the root style as copy and then modifies the values it needs. 
# Note that the use of style dictionaries is fully recursive in PageBot, implementing a cascading structure
# that is very similar to what happens in CSS.

RS = getRootStyle(
    w = W,
    h = H,
    ml = 100,
    mt = 50,
    mr = 50,
    mb = 100,
    conditions = [],
    fontSize = 10,
    rLeading = 0,
    showElementInfo = True,
    originTop = True
)

EXPORT_PATH = '_export/ConditionalElements.pdf' # Export in folder that does not commit un Git. Force to export PDF.

def makeDocument(rootStyle):
    u"""Demo page composer."""
    
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template
    doc = Document(rootStyle, pages=1) 
 
    w = 300

    colorCondition1 = [ # Placement condition(s) for the color rectangle elements.
        ConditionsHDict[sorted(ConditionsHDict.keys())[ConditionH]],
        ConditionsVDict[sorted(ConditionsVDict.keys())[ConditionV]],
    ]
    print colorCondition1
    colorCondition2 = [ # Placement condition(s) for the color rectangle elements.
        Right2Right(),
        Top2Top(),
        #FloatRightBottom(),
    ]
    print colorCondition2
    textCondition = [ # Placement condition(s) for the text element..
        Right2Right(),
        Top2Top(),
        #FloatRightBottom(),
    ]
    # Obvious wrong placement of all elements, to be corrected by solving conditions.
    # In this example the wrongOrigin still shows the elements in the bottom left corner,
    # so it is obvious where they are, of not corrected.
    wrongOrigin = (-300, -300)
    
    page = doc[1] # Get the first/single page of the document.
    if page.originTop:
        p = (page.css('ml'), page.css('mt'))
    else:
        p = (page.css('ml'), page.css('mb'))
    e0 = page.rect(point=p, style=rootStyle, name='Page area',
        w=page.w - page.css('ml') - page.css('mr'),
        h = page.h - page.css('mt') - page.css('mb'),
        fill=0.9)
    # Add some color elements (same width, different height) at the “wrongOrigin” position.
    # They will be repositioned by solving the colorConditions.
    #e1 = page.rect(point=wrongOrigin, style=rootStyle, name='Other element', w=100, h=150, conditions=colorCondition1, 
    #    fill=(1, 0.5, 0.5), align=RIGHT_ALIGN, vAlign=TOP_ALIGN)
    e2 = page.rect(point=wrongOrigin, style=rootStyle, w=50, h=50, name='Floating element', 
        conditions=colorCondition2, fill=(1, 1, 0), align=LEFT_ALIGN, vAlign=TOP_ALIGN)
    print e2.getFloatLeftSide()
    print e2.getFloatRightSide()
    # Make text box at wrong origin. Apply same width a the color rect, which may
    # be too wide from typographic point ogf view. The MaxWidthByFontSize will set the 
    # self.w to the maximum width for this pointSize.
    blurbText = getFormattedString(blurb.getBlurb('article', noTags=True), page,
        style=dict(font='Georgia', fontSize=9, rLeading=0.2, textColor=0))
    #eTextBox = page.textBox(blurbText, point=wrongOrigin, style=rootStyle, w=w, 
    #    vacuumH=True, conditions=textCondition, align=CENTER, vAlign=CENTER)

    score = page.evaluate()
    print 'Page value on evaluation:', score
    print score.fails
    # Try to solve the problems if evaluation < 0
    if score.result < 0:
        print 'Solving', score
        page.solve()
    print score.fails
    # Evaluate again, result should now be >= 0
    score = page.evaluate()
    print 'Page value after solving the problems:', score
    for fail in score.fails:
        print fail
    
    return doc
        
d = makeDocument(RS)
d.export(EXPORT_PATH) 

    
