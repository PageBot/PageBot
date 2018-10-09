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


from pagebot.publications.publication import Publication

class BaseSite(Publication):
    u"""Build a basic website to show the core principles.

    >>> doc = BaseSite(name='Home', padding=30, viewId='Mamp')
    >>> view = doc.view
    >>> page = doc[1]
    >>> doc.export()
    """

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
