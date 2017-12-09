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
#     PageBotLogo.py
#
#     TODO: Get this to work.
#
import pagebot # Import to know the path of non-Python resources.
from pagebot.style import getRootStyle
from pagebot.document import Document
from pagebot.elements import * # Page and Rect

# Some flags to turn on/off extra debug information on the output pages.    
DEBUG = True

EXPORT_PATH = '_export/PageBotLogo.gif'

FRAMES = 30 # Number of frames for the logo gif.
  
LINE = 8
W = H = LINE*16

def makeLogo():
    doc = Document(w=W, h=W, autoPages=1) 
    for frame in range(FRAMES):
        page = doc.newPage()
        x = int(round(random()*(W-4*LINE)))
        y = int(round(random()*(H-4*LINE)))
        w = h = 4*LINE
        newRect(x=x, y=y, w=w, h=h, parent=page, style=dict(strokeWidth=LINE, stroke=0, fill=None))
    return doc
 
if __name__ == '__main__':   
    d = makeLogo()    
    d.export(EXPORT_PATH) 

