# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# ---------------------------------------------------------
#
#     testPreVarFamily.py
#
#     Test script to show working and position of child elements in a layout.
#
from pagebot.elements import Element, newRect
from pagebot.conditions import *
from pagebot.style import HalfLetter
from pagebot.toolbox.color import blackColor, color

W, H = HalfLetter

class VariableFontPlay(Element):
    """This element will show a summery of VF functions. 
    Including but not limited to showing file size as an 
    animation in relation to several axes, such as width 
    and weight."""

from pagebot.document import Document 
document = Document(w=W, h=H, originTop=False)
view = document.view 
view.padding = 30
view.showCropMarks = True
view.showRegistrationMarks = True
view.showPadding = True
view.showFrame = True
view.showNameInfo = True
view.showPageMetaInfo = True
page = document[1]
page.padding = 30
vfp = VariableFontPlay(fill=blackColor, parent=page, padding=20, conditions=[Top2Top(), Left2Left(), Fit()])
for n in range(4):
    newRect(parent=vfp, w=30, h=40, margin=10, fill=color(1,0,0), stroke=0,  conditions=[Right2Right(), Bottom2Bottom(), Float2Left(), Float2Top()])
document.solve()


document.export("_export/VariableFontPlay.png")
