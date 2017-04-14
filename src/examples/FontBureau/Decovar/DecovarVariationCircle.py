# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     DecovarVariationCircle.py
#
from __future__ import division

import pagebot
from pagebot.page import Template
# For Variation Fonts we can use the plain Font-->TTFont wrapper for all styles. No need to use Family.
from pagebot.fonttoolbox.objects.font import Font

from pagebot.publications.typespecimen import TypeSpecimen
from pagebot.fonttoolbox.elements.variationcircle import VariationCircle

DEBUG = False # Make True to see grid and element frames.

OUTPUT_FILE = 'DecovarVariationCircle.pdf'

FONT_PATH = pagebot.getFontPath()
fontPath = FONT_PATH + 'fontbureau/Decovar-VF_2017-02-06.ttf'
decovar = Font(fontPath)
decovarName = decovar.install() # Do DrawBot font install.

s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789'

TERMINALS = ('trmA', 'trmB', 'trmC', 'trmD', 'trmE', 'trmF', 'trmG', 'trmH', 'trmF', 'trmG', 'trmK', 'trmL',)
SKL = ('sklA', 'sklB', 'sklD')
BLD = ('bldA', 'bldB')
WMX = ('wmx2',)

class VariationCircleSpecimen(TypeSpecimen):

    def getAxisCombinations(self):
        # Answer specific interesting combinations for axes in Decovar.
        combinations = []
        for skl in SKL:
            for bld in BLD:
                combinations.append((skl, bld))
            for terminal in TERMINALS:
                combinations.append((skl, terminal))
        return combinations
    
    def getLocations(self, font):
        u"""Answer all possible locations."""
        print font.axes
        locations = []
        # A+B
        for terminal in TERMINALS:
            for t in (500, 1000):
                for skeleton in SKL:
                    for s in (250, 500, 750, 1000):
                        locations.append({terminal:t, skeleton:s})
        # A+C
        for terminal in TERMINALS:
            for t in (500, 1000):
                for parametric in WMX:
                    for p in range(125, 1001, int((1000-125)/8)):
                        locations.append({terminal:t, parametric:p})
        # B+C
        for skeleton in SKL:
            for s in (250, 500, 750, 1000):
                for parametric in WMX:
                    for p in range(125, 1001, int((1000-125)/8)):
                        locations.append({skeleton:s, parametric:p})
        # A+B+C
        for terminal in TERMINALS:
            for t in (500, 1000):
                for skeleton in SKL:
                    for s in (250, 500, 750, 1000):
                        for parametric in WMX:
                            for p in range(125, 1001, int((1000-125)/8)):
                                locations.append({skeleton:s, parametric:p, terminal:t})
        # C+D
        for blending in BLD:
            for b in range(125, 1001, int((1000-125)/8)):
                for parametric in WMX:
                    for p in range(125, 1001, int((1000-125)/8)):
                        locations.append({blending:b, parametric:p})
        
        return locations

    def makeTemplate(self, rs):
        hyphenation(False)
        # Template for the main page.
        template = Template(rs) # Create second template. This is for the main pages.
        # Show grid columns and paddings if rootStyle.showGrid or 
        # rootStyle.showGridColumns are True.
        # The grid is just a regular element, like all others on the page. Same parameters apply.
        template.grid(rs)  
        # Add named text box to template for main specimen text.
        template.cTextBox('', 0, 0, 6, 1, eId=self.titleBoxId, style=rs)       
        template.cTextBox('', 1, 1, 5, 6, eId=self.specimenBoxId, style=rs)       
        #template.cTextBox('', 0, 1, 2, 6, eId=self.infoBoxId, style=rs)
        # Some lines, positioned by vertical and horizontal column index.
        template.cLine(0, 0, 6, 0, style=rs, stroke=0, strokeWidth=0.25)       
        template.cLine(0, 1, 6, 0, style=rs, stroke=0, strokeWidth=0.25)       
        template.cLine(0, 7, 6, 0, style=rs, stroke=0, strokeWidth=0.25)       
        return template
         
    def buildPages(self, doc):
        # Build the pages, showing axes, samples, etc.
        # Using the first page as cover (to be filled...)
        page = doc[1]
        glyphName = 'A'        
        scatter = VariationCircle(decovar, w=500, h=500, s=glyphName)
        page.place(scatter, 50, 100)
                    
# Create a new specimen publications and add the list of system fonts.
typeSpecimen = VariationCircleSpecimen([decovarName], showGrid=DEBUG) 
# Build the pages of the publication, interpreting the font list.
typeSpecimen.build()
# Export the document of the publication to PDF.
typeSpecimen.export(OUTPUT_FILE)

