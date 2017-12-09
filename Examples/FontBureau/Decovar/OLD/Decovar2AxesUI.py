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
#     DecovarAxes.py
#
#     Show a page with a single Decovar /A.
#     Open floating window with sliders for each axis. 
#     Glyph is updating for each move of a slider.
#
#     @@@ TODO: Speed could be optimized if we export a new font with just one glyph.
#     Now the whole font is interpreted if the variaion location changes.
#
from __future__ import division

import pagebot
from pagebot.elements.pbpage import Template
from pagebot.fonttoolbox.objects.font import Font

from pagebot.publications.typespecimen import TypeSpecimen
#from pagebot.elements.variablefonts.variationglyphs import VariationGlyphs

def ini():
    DEBUG = False # Make True to see grid and element frames.

    OUTPUT_FILE = 'DecovarAxes.pdf'

    FONT_PATH = pagebot.getFontPath()
    DecovarPath = FONT_PATH + 'fontbureau/Decovar-VF-chained3.ttf'
    #DecovarPath = u"/Users/petr/git/PageBotTYPETR/src/fonts/BitcountVar/BitcountGrid-GX.ttf"

    #decovarName = installFont(DecovarPath)

    #varFont = Font(DecovarPath)

    s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789'

    axes = varFont.axes
    print axes

    wght = axes['wght'][0]
    flow = axes['flow'][0]
    srif = axes['srif'][0]
    inli = axes['inli'][0]
    term = axes['term'][0]

    VARIABLES = []
    for axisName, (minValue, defaultValue, maxValue) in axes.items():
        VARIABLES.append(dict(name=axisName, ui='Slider', 
            args=dict(value=defaultValue, minValue=minValue, maxValue=maxValue)))
        globals()[axisName] = defaultValue        
    Variable(VARIABLES, globals())

class VariationTypeSpecimen(TypeSpecimen):

    def makeTemplate(self, rs):
        # Template for the main page.
        template = Template(rs) # Create second template. This is for the main pages.
        return template
         
    def buildPages(self, doc):
        # Build the pages, showing axes, samples, etc.
        # Using the first page as cover (to be filled...)
        page = doc[1] 
        location = dict(wght=wght, flow=flow, srif=srif, inli=inli, term=term)
        variationGlyphs = VariationGlyphs(varFont, s='A', style=page.style, fontSize=500, location=location) 
        page.place(variationGlyphs, (250, 100))

if 0:
    # Create a new specimen publications and add the list of system fonts.
    typeSpecimen = VariationTypeSpecimen([decovarName], showGrid=DEBUG) 
    # Build the pages of the publication, interpreting the font list.
    typeSpecimen.build()
    #typeSpecimen.draw()
    # Export the document of the publication to PDF.
    typeSpecimen.export(OUTPUT_FILE)

