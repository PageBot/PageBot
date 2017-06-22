#    Take text of 3-4 paragraphs (headline, body text, caption)
#    Make 1-2 formatted strings from that (with newFS)
#    Make 2 rect elements, with a color
#    Organize those 3-4 elements on a responsive page.
     
from pagebot import newFS
from pagebot.document import Document
#from pagebot.elements import *
from pagebot.conditions import *
from pagebot.style import A5, TOP
from pagebot.contributions.filibuster.blurb import Blurb

W, H = int(A5[0]), int(A5[1])
print W, H

doc = Document(w=W, h=H, originTop=False, autoPages=1)
doc.newStyle(name='h1', fontSize=30, font='Verdana', textFill=(1, 0, 0), 
        leading=36)
doc.newStyle(name='h2', fontSize=22, font='Verdana', textFill=0, 
        leading=24)
doc.newStyle(name='h3', fontSize=16, font='Verdana', textFill=0, 
        leading=14)
doc.newStyle(name='p', fontSize=10, font='Verdana', textFill=0, 
        leading=12)
        
def getExtendedBlurb(doc):
    blurb = Blurb()
    fs = newFS(blurb.getBlurb('news_headline')+'\n', style=doc.styles['h1'])
    for n in range(50):
        fs += newFS(blurb.getBlurb('design_headline')+'\n', style=doc.styles['h2'])
        fs += newFS(blurb.getBlurb('design_headline')+'\n', style=doc.styles['h3'])
        fs += newFS(blurb.getBlurb('article')+'\n', style=doc.styles['p'])
        fs += newFS(blurb.getBlurb('design_headline')+'\n', style=doc.styles['h3'])
        fs += newFS(blurb.getBlurb('article')+'\n', style=doc.styles['p'])
    return fs
    
extendedBlurb = getExtendedBlurb(doc)
print textSize(extendedBlurb)
fill(0)
textBox(extendedBlurb, (20, 20, 500, 1000))
"""
view = doc.getView()
view.showPagePadding = True
view.showElementOrigin = True
view.showFlowConnections = True

page = doc[0]
page.padding = int(page.h/12), int(page.w/12)


newRect(parent=page, z=10, fill=(1, 0, 0), conditions=[Left2LeftSide(), Bottom2Top(), Fit2TopSide(), Fit2WidthSides()])
newRect(parent=page, z=10, x=10, y=10, fill=(1, 0, 1, 0.5), conditions=[Left2LeftSide(), 
    Top2Bottom(), Fit2BottomSide(), Fit2WidthSides()])

cId2 = 'colum2'
fontSize = 10

he = newTextBox(blurb.getBlurb('news_headline'), parent=page, x=20, y=220, w=page.pw, fill=0, fontSize=18,
    conditions=[Left2Left(), Top2Top()], mb=20)
ce1 = newTextBox(blurb.getBlurb('article', noTags=True), parent=page, x=20, y=20, w=page.pw/2-page.gw, mr=page.gw,
    fill=0, fontSize=fontSize,
    conditions=[Left2Left(), Float2Top(), Fit2Bottom(), Overflow2Next()], nextElement=cId2)
#print ce1.isOverflow()

newTextBox('', name=cId2, parent=page, ml=page.gw, x=20, y=20, fill=0, fontSize=fontSize,
    w=page.pw/2-page.gw,
    conditions=[Float2Right(), Float2Top(),Float2Left(), Fit2Bottom()]
)
#print he.x, he.y 
print page.solve()
#print he.x, he.y 

doc.export('_export/TextAssignment.pdf')

"""