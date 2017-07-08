# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     __init__.py
#
from pagebot.elements.element import Element
# Simple elements
from pagebot.elements.pbtext import Text
from pagebot.elements.pbtextbox import TextBox
from pagebot.elements.pbrect import Rect
from pagebot.elements.pbline import Line
from pagebot.elements.pbruler import Ruler
from pagebot.elements.pbpolygon import Polygon
from pagebot.elements.pboval import Oval
# Page elements
from pagebot.elements.pbimage import Image
from pagebot.elements.pbgalley import Galley
from pagebot.elements.pbpage import Page, Template
# Path and mask elements
from pagebot.elements.paths.pbpath import Path
from pagebot.elements.paths.glyphpath import GlyphPath
# Table elements
from pagebot.elements.pbtable import Table

#   S H O R T  C U T S  F O R  C H I L D  E L E M E N T S  G E N E R A T O R S

def newTextBox(fs, point=None, **kwargs):
    u"""Caller must supply formatted string. Note that w and h can also be defined in the style."""
    return TextBox(fs, point=point, **kwargs)

def newColTextBox(fs, cx=None, cy=None, cw=None, ch=None, **kwargs):
    u"""Caller must supply formatted string."""
    e = newTextBox(fs, **kwargs)
    e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch # Correct position from column index, based on style or parent.css
    return e

def newText(fs, point=None, **kwargs):
    u"""Draw formatted string. Normally we don't need w and h here, as it is made by the text and 
    style combinations. But in case the defined font is a Variable Font, then we can use the
    width and height to interpolate a font that fits the space for the given string and weight.
    Caller must supply formatted string. Support both (x, y) and x, y as position."""
    return Text(fs, point=point, **kwargs)

def newColText(fs, cx=None, cy=None, cw=None, ch=None, **kwargs):
    u"""Draw formatted string.
    We don't need w and h here, as it is made by the text and style combinations.
    Caller must supply formatted string."""
    e = newText(fs, **kwargs)
    e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
    return e
            
def newRect(point=None, **kwargs):
    u"""Draw the rectangle. Note that w and h can also be defined in the style. In case h is omitted,
    a square is drawn."""
    return Rect(point=point, **kwargs)
           
def newColRect(cx=None, cy=None, cw=None, ch=None, **kwargs):
    e = newRect(**kwargs)
    e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
    return e
            
def newOval(point=None, **kwargs):
    u"""Draw the oval. Note that w and h can also be defined in the style. In case h is omitted,
    a circle is drawn."""
    return Oval(point=point, **kwargs)

def newColOval(cx=None, cy=None, cw=None, ch=None, **kwargs):
    e = newOval(**kwargs)
    e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
    return e

def newLine(point=None, **kwargs):
    return Line(point=point, **kwargs)
            
def newColLine(cx=None, cy=None, cw=None, ch=None, **kwargs):
    e = newLine(**kwargs)
    e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
    return e

def newPolygon(point=None, **kwargs):
    return Polygon(point=point, **kwargs)

def newImage(path, point=None, **kwargs):
    u"""Create Image element as position (x, y) and optional width, height (w, h) of which
    at least one of them should be defined. The path can be None, to be filled later.
    If the image is drawn with an empty path, a missingImage cross-frame is shown.
    The optional imo attribute is an ImageObject() with filters in place. 
    The Image element is answered for convenience of the caller."""
    return Image(path, point=point, **kwargs)
      
def newColImage(path, cx=None, cy=None, cw=None, ch=None, parent=None, **kwargs):
    u"""Convert the column size into point size, depending on the column settings of the 
    current template, when drawing images "hard-coded" directly on a certain page.
    The optional imo attribute is an ImageObject() with filters in place. 
    The Image element is answered for convenience of the caller"""
    e = newImage(path, **kwargs)
    e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
    return e

def newTable(cols=1, rows=1, **kwargs):
    u"""Answer a new Table instanec."""
    return Table(rows=rows, cols=cols, **kwargs)

def newGalley(**kwargs):
    u"""Answer a new Galley instance."""
    return Galley(**kwargs)

