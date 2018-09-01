from pagebot.document import Document
from pagebot.conditions import *
from pagebot.elements import newTextBox
from pagebot.toolbox.units import pt
from pagebot.contexts.platform import getContext

context = getContext()

def gridFit(e, index):
    line = tb.textLines[index]
    #print(line.y)
    
def drawGrid(e):   
    for textLine in tb.textLines:
        x, y, w = tb.x, textLine.y, tb.w
        context.stroke((1, 0, 0), 0.5)
        context.fill(None)
        yy = page.h.v - tb.top.v - y.v
        context.line((x.v, yy),((x+w).v, yy))
 
BASELINE = pt(14)

doc = Document(w=500, h=500, baselineGrid=BASELINE, originTop=True)

view = doc.view
view.showBaselineGrid = True
view.showTextBoxBaselines = False

page = doc[1]
page.padding = pt(40)
style = dict(font='Verdana', fontSize=pt(12), leading=BASELINE+2)
conditions = [Fit(), Baseline2Grid()]

#tb = newTextBox('Test '*100, parent=page, style=style, conditions=conditions)
doc.solve()

   
doc.export('_export/Baselines.pdf')

#drawGrid(tb)
#gridFit(tb, 4)
