#    Take text of 3-4 paragraphs (headline, body text, caption)
#    Make 2 rect elements, with a color
#    Organize those 3-4 elements on a responsive page.
     
from pagebot.document import Document
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.style import A5, TOP
from pagebot.contributions.filibuster.blurb import Blurb

blurb = Blurb()
#print blurb.getBlurb('design_headline')
#print blurb.getBlurb('news_headline')
#print blurb.getBlurb('article')

W, H = int(A5[0]), int(A5[1])
print W, H

doc = Document(w=W, h=H, originTop=False, autoPages=1)

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
