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
from pagebot.conditions import *
from pagebot.elements import *

class PartOfBook(Element):

    def __init__(self, length=None, elements=None, name=None, compose=None, useInToc=True, 
            pn=None, **kwargs):
        """Abstract type of element that contain parts of the book and/or single pages.

        >>> elements = (
        ...     Front(1, name='Front'),
        ...     Ad(2),
        ...     Ad(1),
        ... )
        >>> coverFront = CoverFront(elements=elements)
        >>> elements = (
        ...     TableOfContent(1, pn=1), # Right page, start of page count
        ...     MastHead(1),
        ...     Ad(1),
        ...     Dummy(12),
        ... )
        >>> frontOfTheBook = FrontOfTheBook(elements=elements)
        >>> elements = (
        ...     Article(2, name='Roger'),
        ...     Ad(1, name='Ad DDS?'),
        ...     Article(2, name='One More JB'),
        ... )
        >>> backOfTheBook = BackOfTheBook(elements=elements)
        >>> elements = (
        ...     Ad(1),
        ...     Ad(1, name='Backcover Ad')
        ... )
        >>> coverBack = CoverBack(elements=elements)
        >>> elements = (
        ...     coverFront,
        ...     frontOfTheBook,
        ...     Article(12, name='Article about something'),
        ...     Article(8, name='Article about something else'),
        ...     backOfTheBook,
        ...     coverBack,
        ... )
        >>> pob = PartOfBook(elements=elements)
        >>> spreads = pob.spreads # Identical to pob.getSpreads()
        >>> len(spreads)
        23
        >>> spreads[12]
        [<Page #0 Article about something (100pt, 100pt)>, <Page #0 Article about something (100pt, 100pt)>]
        >>> spreads[12][0].pn
        """
        Element.__init__(self, name=name, **kwargs)
        self.compose = compose
        self.useInToc = useInToc # Flag indicates if this part should be added to the Table of Content.

        if elements is not None:
            self.elements = elements
        elif length:
            for n in range(length):
                if self.thumbPath:
                    thumbPath = self.thumbPath % (n+1)
                else:
                    thumbPath = None
                self.appendElement(Page(name=name or self.__class__.__name__, 
                    pn=pn, w=self.w, h=self.h, thumbPath=thumbPath))
                if pn is not None:
                    pn += 1

    def __len__(self):
        if not self.elements:
            length = 1
        else:
            length = 0
            for e in self.elements:
                if e.isPage:
                    length += 1
                else:
                    length += len(e)
        return length

    def getSpreads(self, spreads=None, pn=None):
        if spreads is None:
            spreads = [[]]

        for e in self.elements:
            if e.isPage:
                if len(spreads[-1]) == 2:
                    spreads.append([])
                spreads[-1].append(e)
            else:
                e.getSpreads(spreads) 
        return spreads

    def _get_spreads(self):
        #for spread in self.getSpreads():
        #    print(spread)
        return self.getSpreads()
    spreads = property(_get_spreads)

    def getToc(self, level=0, toc=None):
        if toc is None:
            toc = []
        toc.append('%s %s' % ((level+1)*['#'], self.name))
        for e in self.elements:
            for tocPart in e.getToc(level+1, toc):
                toc.append(tocPart)
        return toc

    def _get_toc(self):
        """Recursively answer the content of the TOC."""
        return self.getToc()
    toc = property(_get_toc)

    def getPageNumber(self, page):
        return (0, 0)

class Cover(PartOfBook):
    pass

class FrontOfTheBook(PartOfBook):
    pass

class Article(PartOfBook):
    pass

class BackOfTheBook(PartOfBook):
    pass

class CoverBack(PartOfBook):
    pass

class Front(PartOfBook):
    pass
    
class TableOfContent(PartOfBook):
    pass

class MastHead(PartOfBook):
    pass
    
class Ad(PartOfBook):
    pass

class Dummy(PartOfBook):
    pass



if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
