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
#     flatconversion.py

def iround(value):
    return min(255, max(0, int(round(value*255.0))))

def to255(values):
    return [round(val * 255) for val in values]

def getFlatRGB(c):
    """Answer the color tuple that is valid for self.fileType, otherwise
    Flat gives an error.

    TODO: Make better match for all file types, transparency and spot
    color."""
    from flat import rgb
    return rgb(*to255(c.rgb))
