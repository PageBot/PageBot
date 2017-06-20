
from pagebot.document import Document
from pagebot.style import A4Letter, INCH, CENTER, MIDDLE
from pagebot.elements import *
from pagebot.conditions import *

W, H = A4Letter
print W, H

def makeDocument():
    
    doc = Document(w=W, h=H, originTop=False)
    view = doc.getView()
    view.padding = INCH/2
    view.showPageNameInfo = True
    view.showPageCropMarks = True
    view.showPagePadding = True
    view.showPageFrame = True
    view.showPageRegistrationMarks = True
    view.showGrid = False
    view.showGridColumns = True
    view.showElementOrigin = True
    view.showElementInfo = False

    page = doc[0]
    page.padding = INCH
    
    #rr = newRect(parent=page, x=100, y=200, w=50, h=50, fill=(1, 0, 0))
    cc = [Left2Left(), Float2Top()]
    rr = newRect(parent=page, h=300, conditions=cc, fill=(1, 0, 0))

    print page.elements

    conditions = [Left2LeftSide(), Top2TopSide(), Fit2Width()]
    conditions = [Left2Left(), Float2Top()]
    
    pr = newRect(parent=page, conditions=conditions, w=page.pw*2/3, fill=(1, 0, 1))
    doc.solve()
    
    #rr.left = pr.right
    #rr.top = pr.bottom
    
    return doc




d = makeDocument()
d.export('_export/DemoDocument.pdf')