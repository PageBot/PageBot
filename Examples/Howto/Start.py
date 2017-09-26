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
#     HowTo/Start.py
#
#     Shows the most simple step how to start a document and export it to ,png and ,pdl
#
from __future__ import division # Make integer division result in float.
from random import random

USE_DRAWBOT = False
USE_FLAT = not USE_DRAWBOT

import pagebot # Import to know the path of non-Python resources.
from pagebot.contexts import defaultContext, FlatContext
if USE_FLAT:
    EXPORT_PATH = '_export/FlatStart' 
    defaultContext = FlatContext()
else:
    EXPORT_PATH = '_export/Start' 
# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH_PDF = EXPORT_PATH + '.pdf'
EXPORT_PATH_PNG = EXPORT_PATH + '.png'

# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.document import Document
    
W, H = 500, 400

# Create the publication/document that holds the pages.
doc = Document(w=W, h=H, originTop=False, autoPages=1, context=defaultContext)
doc.view.padding = 0 # Don't show cropmarks in this example.
doc.view.showPagePadding = True

# Get page by pageNumber, first in row (there is only one now in this row).
page = doc[0] 
page.padding = 30

conditions = [Right2Right(), Float2Top(), Float2Left()]
# TODO: Solve this bug, does not mirror.
#conditions = [Left2Left(), Float2Top(), Float2Right()]

for n in range(62):
    mm = newRect(w=40, h=42, mr=4, mt=4, parent=page, 
        fill=(random()*0.5+0.5, 0, 0.5),
        conditions=conditions)  
    
# Recursively solve the conditions in all pages.
# If there are failing conditions, then the status is returned in the Score instance.
score = doc.solve()
if score.fails:
    print score.fails
    
doc.export(EXPORT_PATH_PNG) 
doc.export(EXPORT_PATH_PDF) 

