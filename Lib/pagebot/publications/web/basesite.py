#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     basesite.py
#
#     Implements the basic behavior of website publications classes.
#
from pagebot.publications.publication import Publication

class BaseSite(Publication):

    def __repr__(self):
        """Site as string.

        >>> site = BaseSite(name='Test Site')
        >>> str(site)
        '<BaseSite:Test Site>'
        """
        if self.title:
            name = ':'+self.title
        elif self.name:
            name = ':'+self.name
        else: # No naming, show unique self.eId:
            name = ':'+self.eId
        return '<%s%s>' % (self.__class__.__name__, name)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

