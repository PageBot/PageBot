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
from pagebot.elements.textbox import TextBox
from pagebot.elements.text import Text
from pagebot.elements.rect import Rect
from pagebot.elements.line import Line
from pagebot.elements.ruler import Ruler
from pagebot.elements.polygon import Polygon
from pagebot.elements.oval import Oval
from pagebot.elements.image import Image
from pagebot.elements.galley import Galley
from pagebot.elements.grid import Grid, BaselineGrid
from pagebot.elements.page import Page

#   S H O R T  C U T S  F O R  C H I L D  E L E M E N T S  G E N E R A T O R S

def newTextBox(fs, point=None, parent=None, style=None, eId=None, **kwargs):
    u"""Caller must supply formatted string. Note that w and h can also be defined in the style."""
    e = TextBox(fs, point=point, parent=parent, style=style, eId=eId, **kwargs)
    if parent is None: # Make style tree availabe.
    	parent.appendElement(e)  # Append to element list of parent container.
    return e

def newColTextBox(fs, cx=None, cy=None, cw=None, ch=None, parent=None, style=None, eId=None, **kwargs):
    u"""Caller must supply formatted string."""
    e = newTextBox(fs, point=None, parent=parent, style=style, eId=eId, **kwargs)
    e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch # Correct position from column index, based on style or parent.css
    return e

def newText(fs, point=None, parent=None, style=None, eId=None, **kwargs):
    u"""Draw formatted string. Normally we don't need w and h here, as it is made by the text and 
    style combinations. But in case the defined font is a Variable Font, then we can use the
    width and height to interpolate a font that fits the space for the given string and weight.
    Caller must supply formatted string. Support both (x, y) and x, y as position."""
    e = Text(fs, point=point, parent=parent, style=style, eId=eId, **kwargs)
    if parent is None: # Make style tree availabe.
    	parent.appendElement(e)  # Append to element list of parent container.
    return e
            
def newColText(fs, cx=None, cy=None, cw=None, ch=None, parent=None, style=None, eId=None, **kwargs):
    u"""Draw formatted string.
    We don't need w and h here, as it is made by the text and style combinations.
    Caller must supply formatted string."""
    e = newText(fs, point=None, parent=parent, style=style, w=1, eId=eId, **kwargs)
    e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
    return e
            
def newRect(point=None, parent=None, style=None, eId=None, **kwargs):
    u"""Draw the rectangle. Note that w and h can also be defined in the style. In case h is omitted,
    a square is drawn."""
    if parent is None: parent = self # Make style tree availabe.
    e = Rect(point=point, parent=parent, style=style, eId=eId, **kwargs)
    if parent is None: # Make style tree availabe.
    	parent.appendElement(e)  # Append to element list of parent container.
    return e
            
def newColRect(cx=None, cy=None, cw=None, ch=None, parent=None, style=None, eId=None, **kwargs):
    e = newRect(point=None, parent=parent, eId=eId, style=style, **kwargs)
    e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
    return e
            
def newOval(point=None, parent=None, eId=None, style=None, **kwargs):
    u"""Draw the oval. Note that w and h can also be defined in the style. In case h is omitted,
    a circle is drawn."""
    e = Oval(point=point, parent=parent, eId=eId, style=style, **kwargs)
    if parent is None: # Make style tree availabe.
    	parent.appendElement(e)  # Append to element list of parent container.
    return e

def newColOval(cx=None, cy=None, cw=None, ch=None, parent=None, style=None, eId=None, **kwargs):
    e = newOval(point=None, parent=parent, style=style, eId=eId, **kwargs)
    e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
    return e

def newLine(point=None, parent=None, style=None, eId=None, **kwargs):
    e = Line(point=point, parent=parent, style=style, eId=eId, **kwargs)
    if parent is None: # Make style tree availabe.
    	parent.appendElement(e)  # Append to element list of parent container.
    return e
            
def newColLine(cx=None, cy=None, cw=None, ch=None, parent=None, style=None, eId=None, **kwargs):
    e = newLine(point=None, parent=parent, style=style, eId=eId, **kwargs)
    e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
    return e

def polygon(point=None, parent=None, style=None, eId=None, points=[], **kwargs):
    e = Polygon(point=point, parent=parent, style=style, eId=eId, points=points, **kwargs)
    if parent is None: # Make style tree availabe.
    	parent.appendElement(e)  # Append to element list of parent container.
    return e

def image(path, point=None, parent=None, eId=None, style=None, mask=None, imo=None, pageNumber=0, clipRect=None, **kwargs):
    u"""Create Image element as position (x, y) and optional width, height (w, h) of which
    at least one of them should be defined. The path can be None, to be filled later.
    If the image is drawn with an empty path, a missingImage cross-frame is shown.
    The optional imo attribute is an ImageObject() with filters in place. 
    The Image element is answered for convenience of the caller."""
    if parent is None: parent = self # Make style tree availabe.
    e = Image(path, point=point, parent=parent, eId=eId, style=style, mask=None, imo=imo, pageNumber=pageNumber, clipRect=clipRect, **kwargs)
    if parent is None: # Make style tree availabe.
    	parent.appendElement(e)  # Append to element list of parent container.
    return e
        
def newColImage(path, cx=None, cy=None, cw=None, ch=None, parent=None, style=None, eId=None, mask=None, imo=None, pageNumber=0, cClipRect=None, **kwargs):
    """Convert the column size into point size, depending on the column settings of the 
    current template, when drawing images "hard-coded" directly on a certain page.
    The optional imo attribute is an ImageObject() with filters in place. 
    The Image element is answered for convenience of the caller"""
    e = newImage(path, point=None, parent=parent, eId=eId, style=style, mask=None, imo=imo, pageNumber=pageNumber, w=1, **kwargs)
    e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
    if cClipRect is not None:
        e.cClipRect = cClipRect
    return e

def grid(point=None, parent=None, style=None, eId=None, **kwargs):
    u"""Direct way to add a grid element to a single page, if not done through its template."""
    e = Grid(point=point, parent=None, style=style, eId=eId, **kwargs)
    if parent is None: # Make style tree availabe.
    	parent.appendElement(e)  # Append to element list of parent container.
    return e
    
def baselineGrid(point=None, parent=None, style=None, eId=None, **kwargs):
    u"""Direct way to add a baseline grid element to a single page, if not done through its template."""
    e = BaselineGrid(point=point, parent=parent, style=style, eId=eId, **kwargs)
    if parent is None: # Make style tree availabe.
    	parent.appendElement(e)  # Append to element list of parent container.
    return e
