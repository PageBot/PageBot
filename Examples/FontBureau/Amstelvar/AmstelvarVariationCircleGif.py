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
#     AmstelvarVariableCircle.py
#
#     Example of the Variable axes is Amstelvar, as well as a demo of the workings
#     of the VariableCircle element.
#     Information is derived from the Variable Font and automatic converted into
#     an info-grapgic, showing a simplified model of the design space.
#     To show all possible interpoaltion, it would need to visualize an n-dimensional
#     space (where n is the amount of axes in the font). In the simplified model
#     all axes are represented as spikes/needles on a wheel, where the amount of
#     penetration in the neutral glyph defined the influence of that axis.
#     In that respect is it not much better than a list of sliders, but at least this
#     model allows to show interactions between axes, by putting them on another 
#     angle on the circle.
#
import math
import pagebot # Import to know the path of non-Python resources.

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, A4, CENTER, RIGHT, LEFT, NO_COLOR,TOP, BOTTOM, MM
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)

from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document
from pagebot.fonttoolbox.objects.font import Font
from pagebot.elements.variablefonts.variablecircle import VariableCircle
from pagebot.fonttoolbox.variablefontbuilder import getVariableFont

PagePadding = 24
PageSize = 500

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/AmstelvarVariableCircleGif.gif' 

FONT_PATH = pagebot.getFontPath()
fontPath = FONT_PATH + 'fontbureau/AmstelvarAlpha-VF.ttf'

FRAMES = 60
GLYPH_NAME = 'B'
CIRCLE_ELEMENT_FILL = 1

LOCATIONS = [
    ((0, 20), ['wght']),
    ((20, 40), ['wdth']),
    ((40, 60), ['wdth', 'wght']), 
    ]
def makeDocument(fontPath):
    u"""Make a new document."""

    f = Font(fontPath) # Get PageBot Font instance of Variable font.
    
    W = H = PageSize

    # Create a new document, default to the defined page size. 
    doc = Document(w=W, h=H, originTop=False, title='Text Flow', autoPages=FRAMES)
    
    view = doc.getView()
    view.padding = 0 # Aboid showing of crop marks, etc.
    view.showPageCropMarks = True
    view.showPageRegistrationMarks = True
    view.showPageFrame = False
    view.showPagePadding = False
    view.showElementOrigin = False
    view.showElementDimensions = False

    for frame in range(FRAMES):   
        # Get list of pages with equal y, then equal x.    
        #page = doc[0][0] # Get the single page from te document.
        page = doc.getPage(frame) # Get page on pageNumber, first in row (this is only one now).
        page.padding = PagePadding

        #wghtValue = 0.5*sin(math.radians(360.0*frame/FRAMES)) + 0.5
        #wdthValue = 0.5*cos(math.radians(360.0*frame/FRAMES)) + 0.5
        
        fs = doc.context.newString(f.info.familyName + ' ' + f.info.styleName, 
                                   style=dict(font=f.installedName,
                                              fontSize=18,
                                              textFill=0))
        _, th = textSize(fs)
        title = newTextBox(fs,
                           conditions=[Top2Top(), Fit2Width()],
                           parent=page, h=th*1.2)
    
        for (minF, maxF), axisNames in LOCATIONS:
            fIndex = frame - minF
            if fIndex >= 0 and fIndex < 20:
                # = axisNames
                break
        
        location = {}
        v = 0.5*cos(math.radians(360.0*fIndex/(FRAMES/len(LOCATIONS)))) + 0.5
        if 'wdth' in axisNames and 'wght' in axisNames:
            location['wdth'] = v
            location['wght'] = v
        elif 'wdth' in axisNames:
            location['wdth'] = v
            location['wght'] = 1
        elif 'wght' in axisNames:
            location['wdth'] = 1
            location['wght'] = v
        #print frame, axisNames, location
           
        circle = VariableCircle(f, s=GLYPH_NAME, name='VariableCircleSpeciment',
            parent=page, padding=4, #t=frame,
            maxW=W-2*PagePadding, minW=100, 
            # Location frame, float means 50% of defined axis range
            #location=dict(wght=v),
            #location=dict(wdth=wdthValue),
            location=location,
            # Fontsize of the neutral glyph. All measures in the info-graphic
            # are derived relative from this one.
            fontSize=64,
            # Show axis names with the axis max circle markers
            showAxisNames=True, 
            # Show 3D effect of needles enteting sphere, instead of circle.
            draw3D=True,    
            # Conditions make the element move to top-left of the page.
            # And the condition that there should be no overflow, otherwise the text box
            # will try to solve it.     
            conditions=[Float2Top(), Fit2Bottom(), Center2Center()],
            # Position of the origin of the element. Just to show where it is.
            # Has no effect on the position conditions. 
            yAlign=BOTTOM, xAlign=LEFT, fill=CIRCLE_ELEMENT_FILL, borders=0,
        )
    
        fs = doc.context.newString('Axiswheel created by PageBot',
                                   style=dict(font=f.installedName,
                                              fontSize=7,
                                              textFill=0))
        _, th = textSize(fs)
        created = newTextBox(fs,
                             conditions=[Top2Bottom(), Fit2Width()],
                             parent=page, h=th*1.2)
        
        score = doc.solve() # Try to solve all pages.
        if score.fails:
            print score.fails

        # To avoid circular dependent conditions, we correct the position of the title
        # on left to that the position of the circle has become. This is tricky, 
        # because as a result the title may go to 2 lines and then the size of the
        # circle should be adjusted again.
        title.pl = circle.x - page.pl
        created.pl = circle.x - page.pl
    
    return doc # Answer the doc for further doing.
 
       
d = makeDocument(fontPath)
d.export(EXPORT_PATH) 

