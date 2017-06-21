
# Demo Spreadsheet Element

from pagebot import newFS     
from pagebot.document import Document
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.style import A5, TOP
from pagebot.contributions.filibuster.blurb import Blurb
from pagebot.toolbox.transformer import pointOffset, lighter

class DemoSpreadSheet(Element):
    
    CW = 64
    
    def _drawSpreadSheet(self, p, view):
        px, py, _ = p
        leading = self.css('fontSize') * self.css('rLeading')
        c = self.css('fill')
        colRowFill = c+(1-c)/2
        fill(colRowFill)
        stroke(None)
        rect(px, py, self.CW, self.h)
        
        fill(None)
        stroke(c/2)
        strokeWidth(0.5)
        # Draw horizontal lines
        for iy in range(int(self.h/leading)+1):
            y = py + iy*leading
            line((px,y), (px+self.w, y)) 
            fs = newFS(str(iy), style=dict(font='Verdana', fontSize=6, textFill=(1, 0, 0)))
            tw, th = textSize(fs)
            #print y, leading, leading/2, th, th/2
            text(fs, (px+self.CW-4-tw, y+th/2))
            
        # Draw vertical lines
        for ix in range(int(self.w/self.CW)+1):
            x = px + ix*self.CW
            line((x,py), (x, py+self.h)) 
        
    def draw(self, origin, view, drawElements=True):
        u"""Default drawing method just drawing the frame. 
        Probably will be redefined by inheriting element classes."""

        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        self.drawFrame(p, view) # Draw optional frame or borders.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, p, view)

        self._drawSpreadSheet(p, view)
        
        if drawElements:
            # If there are child elements, draw them over the pixel image.
            self._drawElements(p, view)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, p, view)

        self._restoreScale()
        view.drawElementMetaInfo(self, origin) # Depends on flag 'view.showElementInfo'

    
W, H = A5

doc = Document(w=W, h=H, originTop=False, autoPages=1)

view = doc.getView()
view.showPagePadding = True
view.showElementOrigin = True
view.showFlowConnections = True

page = doc[0]
page.padding = int(page.h/12), int(page.w/12)

DemoSpreadSheet(parent=page, w=200, h=200, fill=0.8, fontSize=10, rLeading=1.2,
    conditions=[Left2Left(), Fit2Width(), Top2Top()]
)
#print he.x, he.y 
print page.solve()
#print he.x, he.y 

doc.export('_export/DemoSpreadSheetElement.pdf')