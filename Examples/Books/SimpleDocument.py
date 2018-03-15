
#import drawBot
#drawBot.fill(1, 0, 0)
#drawBot.rect(10,40, 200, 400)

#fill(1, 0, 0)
#rect(10,40, 200, 400)

from pagebot.style import A4
from pagebot.document import Document
from pagebot.elements import newRect
from pagebot.conditions import *

W, H = A4
PAD = 40
doc = Document(w=W, h=H, title="Demo pages", originTop=False, autoPages=1)

print(page)

view = doc.view
view.padding = 50
view.showPageCropMarks = True
view.showPageRegistrationMarks = True
view.showPagePadding = True
view.showPageFrame = True
view.showPageNameInfo = True

page = doc[1]
page.padding = PAD, PAD, 2*PAD, PAD

newRect(fill=(1, 0, 0), parent=page, h=50, conditions=(Left2Left(), Float2Top(),Fit2Right()))
newRect(fill=(1, 0, 1), parent=page, conditions=(Left2LeftSide(), Float2Top()))
#newRect(fill=(0, 1, 1), parent=page, conditions=(Left2Left(), Float2Top(), Fit2Right()))
newRect(fill=(0, 1, 1), parent=page, conditions=(Right2Right(), Float2Top(), Float2Left(), Fit2Right()))

doc.solve()
doc.export('_export/SimpleDocument.pdf')
