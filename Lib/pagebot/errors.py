#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
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
#     errors.py
#
#

class PageBotError(TypeError):
    pass

class PageBotFileFormatError(Exception):
    """

    >>> e = PageBotFileFormatError('This format is currently not available.')
    >>> print(e)
    ! PageBot file format error: This format is currently not available.
    """

    def __init__(self, msg):
        super().__init__()
        self.msg = msg

    def __str__(self):
        return '! PageBot file format error: %s' % self.msg

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
