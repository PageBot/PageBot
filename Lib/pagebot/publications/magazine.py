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
from copy import copy

from pagebot.publications.publication import Publication
from pagebot.document import Document
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.toolbox.units import pt
from pagebot.toolbox.color import noColor
from pagebot.toolbox.dating import now
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.constants import LEFT, RIGHT

class ThumbPage(Element):
    """Contains a single page thumbnail. Either as page object or a path to a thumbnail file."""
    def __init__(self, page, pageNumber, style=None, **kwargs):
        Element.__init__(self, **kwargs)
        context = self.context
        self.thumbPage = page
        self.pageNumber = pageNumber

        if style is None:
            style = dict(font='Verdana', fontSize=pt(7))
        # Name of the page or spread
        bs = context.newString(page.name, style=style)
        tb1 = newTextBox(bs, w=self.w, y=self.h-self.gh/2, h=self.gh/2, parent=self, stroke=noColor)
        # Thumbnail of the page
        if page.thumbPath is not None:
            im = newImage(path=page.thumbPath, y=self.gh/2, w=self.w, parent=self, borders=pt(0.5))
        else: # Page has no thumbnail
            im = newImage(w=self.w, y=self.gh/2, h=self.h-self.gh, parent=self, borders=pt(0.5))
        # Pagenumber of the page, alignment left or right
        style = copy(style)
        if pageNumber % 2:
            style['xTextAlign'] = RIGHT
        else:
            style['xTextAlign'] = LEFT

        bs = context.newString(pageNumber, style=style)
        tb2 = newTextBox(bs, w=self.w, h=self.gh/2, parent=self, stroke=noColor)


class PageSpread(Element):

    def __init__(self, spread, pageNumber=0, **kwargs):
        Element.__init__(self, **kwargs)
        self.spread = spread
        if spread and spread[0] is not None:
            ThumbPage(spread[0], pageNumber, w=self.w/2, h=self.h, padding=0, parent=self, style=self.style)
        if len(spread) > 1 and spread[1] is not None:
            ThumbPage(spread[1], pageNumber+1, x=self.w/2, w=self.w/2, h=self.h, padding=0, parent=self, style=self.style)

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

    def newDocument(self):

        doc = Document(w=self.w, h=self.h, originTop=False,
            gw=self.gw, gh=self.gh, gridX=self.gridX, gridY=self.gridY,
            baseline=self.baselineGrid, baselineStart=self.baselineGridStart)

    def exportMap(self, cols=None, maxSpread=None, path=None, showGrid=False, showPadding=False):
        """Export the magazine map into a PDF document at path.
        """
        if cols is None:
            cols = 2 # Number of columns per spread
        sw = self.cw*cols + self.gw*(cols-1)
        sh = self.h/self.w*sw/2+self.gh

        if maxSpread is None:
            maxSpread = 8

        date = now()
        if path is None:
            path = '_export/%d-%02d-%02d-%02d %s.pdf' % (date.year, date.month, date.day, date.hour, 
                self.name.replace(' ', '_'))

        doc = self.newDocument()

        font = self.style['font']
        headStyle = dict(font=font, fontSize=pt(24))
        labelStyle = dict(font=font, fontSize=pt(7))

        # Set to True if padding and grid to be shown. The magazine map has the same layout
        # as the main magazine pages, which allows the map export to be used as full page
        # illustration in the magazine. :)
        view = doc.view
        view.showPadding = showPadding 
        view.showGrid = showGrid

        page = None # Force first page to initialize.
        pn = 0 # Pagenumber: TODO--> Translate to real pagenumber, this is only page index.
        headerH = pt(80) # Height of the header box.

        spreads = self.spreads # Run property that accumulates all spreads width Page instances.
        for index in range(0, len(spreads), maxSpread): # Take chunks of spreads for each page.
            pageSpreads = spreads[index:index+maxSpread]
            if pageSpreads: # If there still are spreads in the chunk, process them on a new page.
                if page is None:
                    page = doc[1] # Start at first (autoPage) of the document.
                else:
                    page = page.next # Otherwise automatic create a new page in the document.
                page.padding = self.padding # Set the padding of this page from self.
                # Create a new header text box for each page.
                # TODO: This could contain more info from self, number of pager, etc.
                bs = self.context.newString('Map %s' % self.name, style=headStyle)
                newTextBox(bs, x=page.pl, y=page.pb + page.ph - headerH, w=page.pw, h=headerH, parent=page)

                # Set coordinate of the first spread thumbnail to be positioned.
                x = page.pl
                y = page.pb + page.ph - sh - headerH

                for pageSpread in pageSpreads: # Process all spreads in the chunk of this page.
                    ps = PageSpread(pageSpread, pn, x=x, y=y, w=sw, h=sh, parent=page, style=labelStyle)
                    pn += 2
                    x += sw + page.gw # Position of next spread thumbnail
                    if x >= page.pw: # If all columns used, then continue on the next row.
                        x = page.pl
                        y -= ps.h

        # TODO: Why is export so slow?
        doc.export(path)

    def composePartOfBook(self, name):
        part = self.select(name) # Find the selected part of self (e.g. a chapter in the magazine)
        doc = self.newDocument()
        #for page in part.elements:
        #    doc.

        return doc

    def exportPart(self, name, start=0, end=None, path=None, showGrid=False, showPadding=False):
        if path is None:
            path = '_export/%s-%s.pdf' % (self.name, name)

        doc = self.composePartOfBook(showGrid)
        doc.export(path)


