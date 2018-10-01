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
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.toolbox.units import p, pt
from pagebot.toolbox.color import noColor
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.constants import LEFT, RIGHT

class ThumbPage(Element):
    """Contains a single page thumbnail. Either as page object or a path to a thumbnail file."""
    def __init__(self, spread, pageNumber, path=None, page=None, w=None, h=None, **kwargs):
        Element.__init__(self, w=w, h=h, **kwargs)
        context = self.context
        self.spread = spread
        self.pageNumber = pageNumber
        bookFont = findFont('Upgrade-Book')

        # Name of the page or spread
        bs = self.context.newString(spread.name, style=dict(font=bookFont, fontSize=pt(7)))
        tb1 = newTextBox(bs, w=w, y=h-self.gh/2, h=self.gh/2, parent=self, stroke=noColor)
        # Thumbnail of the page
        if page is not None:
            # Show scaled page here.
            pass
        elif path is not None:
            im = newImage(path=path, y=self.h-self.gh/2, w=w, parent=self, borders=pt(0.5))
        else: # Page has no instance or path
            im = newImage(w=w, y=self.gh/2, h=h-self.gh, parent=self, borders=pt(0.5))
        # Pagenumber of the page, alignment left or right
        if pageNumber % 2:
            xAlign = RIGHT
        else:
            xAlign = LEFT
        bs = context.newString(pageNumber, style=dict(font=bookFont, fontSize=pt(7), xTextAlign=xAlign))
        tb2 = newTextBox(bs, w=w, h=self.gh/2, parent=self, stroke=noColor)
                

class PageSpread(Element):

    def __init__(self, spread, pageNumber=0, **kwargs):
        Element.__init__(self, **kwargs)
        self.spread = spread
        if len(spread) and spread[0] is not None:
            ThumbPage(spread[0], pageNumber, w=self.w/2, h=self.h, padding=0, parent=self)
        if len(spread) > 1 and spread[1] is not None:
            ThumbPage(spread[1], pageNumber+1, x=self.w/2, w=self.w/2, h=self.h, padding=0, parent=self)

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
        """Answers a flattened list of spread elements, containing all page elements.
        Note that the e.parent of all elements is untouched. If parts run over several
        pages, then the same part instance is there.
        """
        spreads = [[None]] # Skip first to keep left side of cover open.
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
        pn = 0

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
                    PageSpread(pageSpread, pn, w=sw, h=self.h/self.w*sw/2+self.gh, mr=self.gw, mb=self.gh, parent=page, 
                        conditions=(Right2RightSide(), Float2Top(), Float2Left()))
                    pn += 2

        doc.solve()
        doc.export(path)
