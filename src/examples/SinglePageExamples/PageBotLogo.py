# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     PageBotLogo.py
#
#
import pagebot # Import to know the path of non-Python resources.
from pagebot.style import getRootStyle
from pagebot.document import Document
from pagebot.page import Page
from pagebot.elements import Rect

# Some flags to turn on/off extra debug information on the output pages.    
DEBUG = True

EXPORT_PATH = '_export/PageBotLogo.gif'

FRAMES = 30 # Number of frames for the logo gif.
  
LINE = 8
W = H = LINE*16

def makeLogo():
    rs = getRootStyle()
    rs['w'] = W
    rs['h'] = H
# Small scale class example model of how PageBot origanizes Document, Page and Element.
    doc = Document(rs) 
    for frame in range(FRAMES):
        page = doc.newPage()
        x = int(round(random()*(W-4*LINE)))
        y = int(round(random()*(H-4*LINE)))
        w = h = 4*LINE
        page.rect(x, y, w, h, style=dict(strokeWidth=LINE, stroke=0, fill=None))
    return doc
    
d = makeLogo()    
d.export(EXPORT_PATH) 

