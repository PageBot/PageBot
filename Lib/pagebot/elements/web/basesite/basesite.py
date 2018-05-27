#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     basesite.py
#
from __future__ import division # Make integer division result in float.

from pagebot.publications.publication import Publication

class BaseSite(Publication):
    u"""Build a basic website to show the core principles.

    >>> baseSite = BaseSite(name='Home Site', pl=30, pr=30)
    >>> view = baseSite.newView('Mamp')
    >>> baseSite
    [Document-BaseSite "Home Site"]
    >>> len(baseSite.pages)
    1
    >>> baseSite.export('_export/BaseSite')
    """

    def initialize(self, **kwargs):
        u"""Initialize the generic website templates. """


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
