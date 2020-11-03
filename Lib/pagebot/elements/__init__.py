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
#     __init__.py
#
#     New Elements to be added
#     Graphs, Maps, 3Dto2DContainers.
#

from pagebot.elements.element import Element
from pagebot.toolbox.transformer import path2Extension
from pagebot.constants import IMAGE_TYPES, TEXT_TYPES, FONT_TYPES, MOVIE_TYPES

# Simple elements.
from pagebot.elements.beziercurve import BezierCurve
from pagebot.elements.text import Text
from pagebot.elements.rect import Rect
from pagebot.elements.group import Group
from pagebot.elements.line import Line
from pagebot.elements.mask import  Mask
from pagebot.elements.oval import Oval
from pagebot.elements.circle import Circle
from pagebot.elements.polygon import Polygon
from pagebot.elements.ruler import Ruler
from pagebot.elements.docwrap import DocWrap
from pagebot.elements.bezierpaths import BezierPaths

# Page elements.
from pagebot.elements.image import Image
from pagebot.elements.galley import Galley, Column
from pagebot.elements.page import Page
from pagebot.elements.template import Template

# Placeholder element, typically for Templates. Shows name.
from pagebot.elements.placer import Placer

# Dating elements.
from pagebot.elements.dating.calendarmonth import CalendarMonth

# Artboard. SketchApp compatible, content element on pages.
from pagebot.elements.artboard import Artboard

from pagebot.elements.glyphpath import GlyphPath

# Table elements
from pagebot.elements.table import Table

# Views and code
from pagebot.elements.views import viewClasses
from pagebot.elements.quire import Quire
from pagebot.elements.codeblock import CodeBlock

# Vanilla based UI elements
#from pagebot.elements.ui.uiwindow import UIWindow
#from pagebot.elements.ui.uibutton import UIButton
#from pagebot.elements.ui.uigroup import UIGroup
#from pagebot.elements.ui.uicanvas import UICanvas

# Variable Font elements
from pagebot.elements.variablefonts.variablecircle import VariableCircle
from pagebot.elements.designspacegraph.designspacegraph import DesignSpace, DesignSpaceGraph
from pagebot.elements.variablefonts.specimen import TypeList, TypeFeatures, TypeGlyphSet, Waterfall

def elementFromPath(path, context=None, name=None, **kwargs):
    """Answer the element that is best suitable to hold the data in the path.
    """
    extension = path2Extension(path).lower()

    if extension in IMAGE_TYPES:
        e = newImage(path, context=context, name=name, **kwargs)
    elif extension in TEXT_TYPES:
        e = newText(path, context=context, name=name, **kwargs)
    elif extension in FONT_TYPES:
        # TODO: Answer a default specimen element to show the font.
        e = None
    elif extension in MOVIE_TYPES:
        # TODO: Answer a MovieElement instance (to be developed)
        e = None
    else:
        # If no extension-->element can be found.
        e = None

    return e

#   S H O R T C U T S   F O R   C H I L D   E L E M E N T    G E N E R A T O R S

def newView(viewId, **kwargs):
    """In most cases views are initialized as a dictionary by the Document
    class.  But since they inherit from Element, they also can be used as
    placable elements. Make sure to define the right parent (likely to be a
    Page or Template)."""
    return viewClasses[viewId](**kwargs)

def newPage(**kwargs):
    """In most cases views are initialized as a dictionary by the Document
    class.  But since they inherit from Element, they also can be used as
    placable elements. Make sure to define the right parent (likely to be a
    Page or Template). Embed the page in a View element, to control appearance,
    such as cropmarks."""
    return Page(**kwargs)

def newTemplate(**kwargs):
    """In most cases views are initialized as a dictionary by the Document
    class.  But since they inherit from Element, they also can be used as
    placable elements."""
    return Template(**kwargs)

def newPlacer(**kwargs):
    """Placer occupying a space on Page or Template. Is not visible exported
    documets."""
    return Placer(**kwargs)

def newColumn(**kwargs):
    """Answers a new Column instance, offering a squential paste-board for
    elements."""
    return Column(**kwargs)

def newText(bs='', **kwargs):
    """Creates a Text element. If w and h are not defined, then the Text is and
    elastic rectangle, base on the size of the content. If w is defined, then
    the Text element has regular “Text” behavior.
    """
    return Text(bs, **kwargs)

def newRect(**kwargs):
    """Creates a new Rect element. Note that points can also be defined in the
    style. When omitted, a square is drawn."""
    return Rect(**kwargs)

def newQuire(**kwargs):
    """Creates a new Quire element. When omitted, a square is drawn."""
    return Quire(**kwargs)

def newArtboard(**kwargs):
    """Create a new Artboard element."""
    return Artboard(**kwargs)

def newGroup(**kwargs):
    """Creates a new Group element. Note that points can also be defined in the
    style. When omitted, a square is drawn."""
    return Group(**kwargs)

def newOval(**kwargs):
    """Creates an Oval element. Note that points can also be defined in the
    style."""
    return Oval(**kwargs)

def newCircle(**kwargs):
    """Creates a Circle element. Note that points can also be defined in the
    style."""
    return Circle(**kwargs)

def newLine(**kwargs):
    """Creates a Line element."""
    return Line(**kwargs)

def newPolygon(points=None, **kwargs):
    """Creates a Polygon element."""
    return Polygon(points=points, **kwargs)

def newMask(points=None, **kwargs):
    """Creates a Mask element."""
    return Mask(points=points, **kwargs)

def newRuler(**kwargs):
    """Creates a Ruler element."""
    return Ruler(**kwargs)

def newBezierCurve(**kwargs):
    return BezierCurve(**kwargs)

def newBezierPaths(paths=None, **kwargs):
    """Creates a Paths element, containing BezierPath objects in an element
    frame. The paths can be a single BezierPath instance or a list / tuple of
    instances. Not be confused with the filePath "path" in Image."""
    return BezierPaths(paths, **kwargs)

def newGlyphPath(glyph, **kwargs):
    return GlyphPath(glyph, **kwargs)

def newImage(path=None, **kwargs):
    """Creates Image element as position (x, y) and optional width, height (w,
    h) of which at least one of them should be defined. The path can be None,
    to be filled later. If the image is drawn with an empty or non-existent
    file path, a missing Image cross-frame is shown. The optional imo attribute
    is an DrawBot-modelled ImageObject() with filters in place. The created
    Image element is answered."""
    return Image(path=path, **kwargs)

def newTable(cols=1, rows=1, **kwargs):
    """Answers a new Table instance."""
    return Table(rows=rows, cols=cols, **kwargs)

def newGalley(**kwargs):
    """Answers a new Galley instance."""
    return Galley(**kwargs)
