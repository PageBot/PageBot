#    Take text of 3-4 paragraphs (headline, body text, caption)
#    Make 1-2 formatted strings from that (with newFS)
#    Make 2 rect elements, with a color
#    Organize those 3-4 elements on a responsive page.
     
from pagebot.document import Document
from pagebot.elements import *
from pagebot.style import A5

W, H = A5

doc = Document(w=W, h=H, originTop=False, autoPages=1)

page = doc[0]
newRect(parent=page, fill=(1, 0, 0))
newRect(parent=page, x=10, y=10, fill=(1, 0, 1))
newTextBox('This is dummy text', parent=page, x=20, y=20, fill=0, fontSize=20)

doc.export('_export/TextAssignment.pdf')