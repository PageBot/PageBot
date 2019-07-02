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

    PAGE_CLASS = Page

    def __init__(self, autoPages=0, elements=None, name=None, compose=None,
            publication=None, useInToc=True, pn=None, **kwargs):
        """Abstract type of element that contain parts of the book and/or single pages.

        >>> elements = (
        ...     Cover(1, name='Cover'),
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
        ...     Ad(1, name='Backcover Ad'),
        ...     Back(1, name='Back'),
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
        24
        >>> spreads[12]
        [<Page #0 Article about something (100pt, 100pt)>, <Page #0 Article about something (100pt, 100pt)>]
        >>> spreads[12][0].pn
        (0, 0)
        """
        Element.__init__(self, name=name, **kwargs)

        # FIXME: causes pylint error:
        # E:164, 4: An attribute defined in pagebot.publications.magazines.glossy.parts line 70 hides this method (method-hidden)
        if compose is not None:
            self.compose = compose # Overwrite the standard composer method if defined.
        else:
            self.compose = self.composeFunction
        self.useInToc = useInToc # Flag indicates if this part should be added to the Table of Content.
        self.pages = []

        if pn is None:
            pn = 1
        self.pn = pn

        if elements is not None:
            self.elements = elements

        for n in range(autoPages):
            self.newPage(name, (pn, 0))
            pn += 1

    def newPage(self, name=None, pn=None):
        if self.thumbPath:
            thumbPath = self.thumbPath % (len(self.pages)+1)
        else:
            thumbPath = None
        page = self.PAGE_CLASS(name=name or self.__class__.__name__,
            pn=pn, w=self.w, h=self.h, thumbPath=thumbPath)
        self.pages.append(page)

    # Document[12] answers a list of pages where page.y == 12
    # This behaviour is different from regular elements, who want the page.eId as key.
    def __getitem__(self, index):
        """Answers the pages with pageNumber equal to page.y.
        """
        return self.pages[index]
    def __setitem__(self, index, page):
        self.pages[index] = page

    def __len__(self):
        return len(self.pages)

    def append(self, e):
        """If e is a PartOfBook, then add it to self.elements. If e is a page,
        then add it to self.pages. Otherwise it is supposed to be page element,
        append it to self.pages[-1]."""
        if isinstance(e, PartOfBook):
            print('Append part', self, e)
            self.appendElement(e)
        elif e.isPage:
            print('Append page', self, e)
            self.pages.append(e)
        else:
            if not self.pages:
                self.newPage()
            self.pages[-1].appendElement(e)
            print('Append element', self.pages[-1], e)
            print(self.pages[-1].elements)

    def getSpreads(self, spreads=None, pn=None):
        """Compose a list of spreads from self.pages. Nothing changes to the
        page.parent, pages remain unplaced. Recursively collect from all
        self.elements parts."""
        if spreads is None:
            spreads = [[]]

        for page in self.pages:
            if len(spreads[-1]) == 2:
                spreads.append([])
                spreads[-1].append(page)

        for part in self.elements:
            part.getSpreads(spreads)

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
        for part in self.elements:
            for tocPart in part.getToc(level+1, toc):
                toc.append(tocPart)
        return toc

    def _get_toc(self):
        """Recursively answer the content of the Table of Content, for those part-pages
        that indicate to be part of the TOC."""
        return self.getToc()
    toc = property(_get_toc)

    def getPageNumber(self, page):
        return (0, 0)

    def composeFunction(self, doc, publication):
        """Compose the part into doc. For every element in self.elements that is a page,
        add it to the document. Note that this will alter the e.parent to page.
        It practice it is safer to move the Page instance to become part of the document
        that to make a copy of it (with all dependencies. Also by making a copy, any
        high-level will loose control over the page instances.
        All element part that are not pages are call recusively to compose themselves
        into the document.
        """
        for page in self.pages:
            page.size = doc.size
            page.padding = doc.padding
            #print('3223233223', page.pn)
            doc.appendPage(page) # Add the page to the document. Note that this will alter the e.parent
        for e in self.elements:
            e.compose(doc, publication) # Recursively call composition for all other parts.

class CoverFront(PartOfBook):
    def __init__(self, elements=None, **kwargs):
        if elements is None:
            elements = [Cover(1, name='Cover')]
        PartOfBook.__init__(self, elements=elements, **kwargs)

    def _get_cover(self):
        """Answer the Cover instancec if it exists."""
        return self.find('Cover')
    cover = property(_get_cover)

class FrontOfTheBook(PartOfBook):
    pass

class Article(PartOfBook):
    pass

class BackOfTheBook(PartOfBook):
    pass

class CoverBack(PartOfBook):
    pass

class Cover(PartOfBook):
    pass

class Back(PartOfBook):
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
