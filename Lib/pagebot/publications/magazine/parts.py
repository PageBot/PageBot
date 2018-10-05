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

    def __init__(self, length=None, elements=None, name=None, **kwargs):
        Element.__init__(self, name=name, **kwargs)
        if elements is not None:
            self.elements = elements
        elif length:
            for n in range(length):
                if self.thumbPath:
                    thumbPath = self.thumbPath % (n+1)
                else:
                    thumbPath = None
                self.appendElement(Page(name=name or self.__class__.__name__, thumbPath=thumbPath))

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

    def getSpreads(self, spreads):
        for e in self.elements:
            if e.isPage:
                if len(spreads[-1]) == 2:
                    spreads.append([])
                spreads[-1].append(e)
            else:
                e.getSpreads(spreads) 
        return spreads

    def getPageNumber(self, page):
        return (0, 0)

class CoverFront(PartOfBook):
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
