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
# -----------------------------------------------------------------------------
#
#     magazine.py
#
from pagebot.publications.publication import Publication
from pagebot.document import Document
from pagebot.elements import newRect, Element
from pagebot.conditions import *
from pagebot.toolbox.units import p, pt

class PageSpread(Element):

    def __init__(self, spread, **kwargs):
        Element.__init__(self, **kwargs)
        self.spread = spread
        if spread[0] is not None:
            newRect(w=self.w/2, h=self.h, stroke=0, strokeWidth=0.5, padding=0, parent=self, 
                conditions=(Left2Left(), Top2Top()))
        if spread[1] is not None:
            newRect(w=self.w/2, h=self.h, stroke=0, strokeWidth=0.5, padding=0, parent=self, 
                conditions=(Right2Right(), Top2Top()))

class Magazine(Publication):
    """Create a default magazine, with cover, front-of-book, articles on different template
    layouts, table of content, layout and content options defined by external parameters.
    Subclassed from Element-->Publication-->Magazine.

    """
    def __len__(self):
        length = 0
        for e in self.elements:
            length += len(e)
        return length

    def _get_spreads(self):
        """Answer a flattened list of spread elements, containing all page elements.
        Note that the e.parent of all elements is untouched. If parts run over several
        pages, then the same part instance is there.
        """
        spreads = [[None]] # Keep left side of cover open.
        for e in self.elements:
            e.getSpreads(spreads)
        return spreads
    spreads = property(_get_spreads)

    def exportMap(self, cols=None, maxSpread=None, path=None):
        """Export the magazine map into a PDF document at path.
        """
        if cols is None:
            cols = 2 # Number of columns per spread  
        sw = self.cw*cols + self.gw*(cols-1)

        if maxSpread is None:
            maxSpread = 8

        if path is None:
            path = '_export/%s.pdf' % self.name.replace(' ', '_')
        doc = Document(w=self.w, h=self.h, originTop=False,  
            gw=self.gw, gh=self.gh, gridX=self.gridX, gridY=self.gridY,
            baseline=self.baselineGrid, baselineStart=self.baselineGridStart)
        view = doc.view
        view.showPadding = True
        view.showGrid = True

        page = None

        spreads = self.spreads
        for index in range(0, len(spreads), maxSpread):
            pageSpreads = spreads[index:index+maxSpread]
            if pageSpreads:
                if page is None:
                    page = doc[1]
                else:
                    page = page.next
                page.padding = self.padding
                for pageSpread in pageSpreads:
                    PageSpread(pageSpread, w=sw, h=self.h/self.w*sw/2, mr=self.gw, mb=self.gh, parent=page, 
                        conditions=(Right2RightSide(), Float2Top(), Float2Left()))

        doc.solve()
        doc.export(path)
