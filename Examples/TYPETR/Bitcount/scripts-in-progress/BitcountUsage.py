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
#     AutomaticPageComposition.py
#
#     This script generates an article (in Dutch) of 2009 about the approach to
#     generate automatic layouts, using Style, Galley, Typesetter and Composer classes.
#
from pagebot import newFS, textBoxBaseLines

import pagebot.style
reload(pagebot.style)
from pagebot.style import getRootStyle, LEFT

import pagebot.document 
reload(pagebot.document)
from pagebot.document import Document

import pagebot.page
reload(pagebot.page)
from pagebot.page import Page, Template

import pagebot.composer
reload(pagebot.composer)
from pagebot.composer import Composer

import pagebot.typesetter
reload(pagebot.typesetter)
from pagebot.typesetter import Typesetter

import pagebot.elements
reload(pagebot.elements)
from pagebot.elements import Galley, Rect

import pagebot.fonttoolbox.elements.variationcube
reload(pagebot.fonttoolbox.elements.variationcube)
from pagebot.fonttoolbox.elements.variationcube import VariationCube

import pagebot.fonttoolbox.variationbuilder
reload(pagebot.fonttoolbox.variationbuilder)
from pagebot.fonttoolbox.variationbuilder import getVariationFont
    
DEBUG = False

SHOW_GRID = DEBUG
SHOW_GRID_COLUMNS = DEBUG
SHOW_BASELINE_GRID = DEBUG
SHOW_FLOW_CONNECTIONS = DEBUG

EXPORT_PATH = 'export/variableFontDesign.pdf'
  
# Get the default root style and overwrite values for this document.
U = 7
baselineGrid = 2*U
listIndent = 1.5*U

RS = getRootStyle(
    u = U, # Page base unit
    # Basic layout measures altering the default rooT STYLE.
    w = 595, # Om root level the "w" is the page width 210mm, international generic fit.
    h = 11 * 72, # Page height 11", international generic fit.
    ml = 7*U, # Margin left rs.mt = 7*U # Margin top
    baselineGrid = baselineGrid,
    g = U, # Generic gutter.
    # Column width. Uneven means possible split in 5+1+5 or even 2+1+2 +1+ 2+1+2
    # 11 is a the best in that respect for column calculation.
    cw = 11*U, 
    ch = 6*baselineGrid - U, # Approx. square and fitting with baseline.
    listIndent = listIndent, # Indent for bullet lists
    listTabs = [(listIndent, LEFT)], # Match bullet+tab with left indent.
    # Display option during design and testing
    showGrid = SHOW_GRID,
    showGridColumns = SHOW_GRID_COLUMNS,
    showBaselineGrid = SHOW_BASELINE_GRID,
    showFlowConnections = SHOW_FLOW_CONNECTIONS,
    # Text measures
    leading = baselineGrid,
    rLeading = 0,
    fontSize = 9
)
# Tracking presets
H1_TRACK = H2_TRACK = 0.015 # 1/1000 of fontSize, multiplier factor.
H3_TRACK = 0.030 # Tracking as relative factor to font size.
P_TRACK = 0.030

FONT_DIR = '../../../fonts/'
FONT_NAME = 'BitcountGrid-GX.ttf'
FONT_PATH = FONT_DIR + FONT_NAME

# -----------------------------------------------------------------         
def makeSpecimen(rs):
        
    # Template 1
    template1 = Template(rs) # Create template of main size. Front page only.
    # Show grid columns and margins if rootStyle.showGrid or rootStyle.showGridColumns are True
    template1.grid(rs) 
    # Show baseline grid if rs.showBaselineGrid is True
    template1.baselineGrid(rs)
   
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template2
    doc = Document(rs, autoPages=2, template=template1) 

    page1 = doc[1]
    vCube = VariationCube(FONT_PATH, w=500, h=500, s='a', fontSize=86, dimensions=dict(wght=4,rnds=4))
    page1.place(vCube, 50, 160)

    font = getVariationFont(FONT_PATH, location=dict(wght=-0.5, rnds=2,diam=0.5))
    page2 = doc[2]
    for n in range(600):
        page2.text(FormattedString('@', font=font, fontSize=800, fill=(random(), random(), random(), 0.8)), 50+random()*100, 200+random()*100)
    return doc
        
d = makeSpecimen(RS)
d.export(EXPORT_PATH) 

