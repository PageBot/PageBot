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
#     numpytransform.py
#

from math import cos, sin, radians
import numpy as np

def trig(angle):
    """
    >>> trig(0)
    (1.0, 0.0)
    """
    r = radians(angle)
    return cos(r), sin(r)

def transform(point, TransformArray):
    """
    >>> TransformArray = np.array([1, 0, 0, 1])
    """
    p = np.array([0,0,0,1])

    for i in range (0,len(point)-1):
        p[i] = point[i]

    p = np.dot(TransformArray, np.transpose(p))

    for i in range (0, len(point) - 1):
        point[i] = p[i]

    return point

def matrix(rotation, translation):
    xC, xS = trig(rotation[0])
    yC, yS = trig(rotation[1])
    zC, zS = trig(rotation[2])
    dX = translation[0]
    dY = translation[1]
    dZ = translation[2]

    Translate_matrix = np.array([[1, 0, 0, dX],
                                 [0, 1, 0, dY],
                                 [0, 0, 1, dZ],
                                 [0, 0, 0, 1]])

    Rotate_X_matrix = np.array([[1, 0, 0, 0],
                                [0, xC, -xS, 0],
                                [0, xS, xC, 0],
                                [0, 0, 0, 1]])

    Rotate_Y_matrix = np.array([[yC, 0, yS, 0],
                                [0, 1, 0, 0],
                                [-yS, 0, yC, 0],
                                [0, 0, 0, 1]])

    Rotate_Z_matrix = np.array([[zC, -zS, 0, 0],
                                [zS, zC, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])

    return np.dot(Rotate_Z_matrix, np.dot(Rotate_Y_matrix, np.dot(Rotate_X_matrix, Translate_matrix)))

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
