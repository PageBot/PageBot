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
#     AmsterlvarDesignSpace.py
#
from __future__ import division

import pagebot
from pagebot.contexts.platform import getRootFontPath
from pagebot.elements import *
# For Variable Fonts we can use the plain Font-->TTFont wrapper for all styles. No need to use Family.
from pagebot.fonttoolbox.objects.font import Font
from pagebot.conditions import *
from pagebot.publications.typespecimen import TypeSpecimen
from pagebot.elements.variablefonts.variablecircle import VariableCircle

OUTPUT_FILE = '_export/AmstelvarVariableCircle.pdf'

CONDITIONS = [Fit2Width(), Float2Top()] # Stacking conditions for all elements in this page.

fontPath = getRootFontPath() + 'fontbureau/AmstelvarAlpha-VF.ttf'
varFont = Font(fontPath)
varFontName = varFont.install() # Do DrawBot font install.

s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789'

TERMINALS = ('trmA', 'trmB', 'trmC', 'trmD', 'trmE', 'trmF', 'trmG', 'trmH', 'trmF', 'trmG', 'trmK', 'trmL',)
SKL = ('sklA', 'sklB', 'sklD')
BLD = ('bldA', 'bldB')
WMX = ('wmx2',)

class VariableCircleSpecimen(TypeSpecimen):
    u"""Inherit from generic publication class the implements default specimen behavior."""
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

    def makeTemplate(self, rootStyle):
        # Template for the main page.
        template = Template(style=rootStyle) # Create second template. This is for the main pages.
        # Add named text box to template for main specimen text.
        newLine(parent=template, conditions=CONDITIONS, stroke=0, strokeWidth=0.25)       
        newTextBox('', parent=template, conditions=CONDITIONS, eId=self.titleBoxId)       
        newTextBox('', parent=template, conditions=CONDITIONS, eId=self.specimenBoxId)       
        newLine(parent=template, conditions=CONDITIONS, stroke=0, strokeWidth=0.25)       
        newRect(fill=(1,0,0), w=300,h=400,parent=template)
        return template
         
    def buildPages(self, doc, varFont):
        # Build the pages, showing axes, samples, etc.
        # Using the first page as cover (to be filled...)
        page = doc[0]
        page.applyTemplate(self.makeTemplate(doc.getRootStyle()))
        glyphName = 'A'

        newLine(parent=page, conditions=CONDITIONS, stroke=0, strokeWidth=0.25)       
        newTextBox('', parent=page, conditions=CONDITIONS, eId=self.titleBoxId)       
        newTextBox('', parent=page, conditions=CONDITIONS, eId=self.specimenBoxId)       
        newLine(parent=page, conditions=CONDITIONS, stroke=0, strokeWidth=0.25)       
        newRect(fill=(1,0,0), w=300,h=400,conditions=CONDITIONS, parent=page)
        
        view = doc.getView()
        view.showElementOrigin = True
        view.showElementDimensions = False
        vce = VariableCircle(varFont, conditions=CONDITIONS, parent=page, s=glyphName)
        newLine(parent=page, conditions=CONDITIONS, stroke=0, strokeWidth=0.25)       
        
        score = page.solve()
        if score.fails:
            print score.fails
        print vce.x, vce.y, vce.w, vce.h 
                   
if __name__ == '__main__':
    # Create a new specimen publications and add the list of system fonts.
    typeSpecimen = VariableCircleSpecimen([varFontName]) 
    # Build the pages of the publication, interpreting the font list.
    typeSpecimen.build(varFont)
    # Export the document of the publication to PDF.
    typeSpecimen.export(OUTPUT_FILE)

