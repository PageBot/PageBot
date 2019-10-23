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
from pagebot.elements.pbtext import Text
from pagebot.elements.pbtextbox import TextBox
from pagebot.elements.pbrect import Rect
from pagebot.elements.pbgroup import Group
from pagebot.elements.pbline import Line
from pagebot.elements.pbruler import Ruler
from pagebot.elements.pbpolygon import Polygon
from pagebot.elements.pboval import Oval
from pagebot.elements.pboval import Circle
from pagebot.elements.pbdocwrap import DocWrap

# Page elements.
from pagebot.elements.pbimage import Image
from pagebot.elements.pbgalley import Galley, Column
from pagebot.elements.pbpage import Page, Template

# Placeholder element, typically for Templates. Shows name.
from pagebot.elements.pbplacer import Placer

# Dating elements.
from pagebot.elements.dating.calendarmonth import CalendarMonth

# Artboard. SketchApp compatible, content element on pages.
from pagebot.elements.pbartboard import Artboard

# Path and mask elements. Generic PageBot equivalent of DrawBot.BezierPath.
from pagebot.elements.paths.pagebotpath import PageBotPath, newRectPath

# Element that holds a number of styled PageBotPath instances to draw.
from pagebot.elements.paths.pbpaths import Paths, Mask

# Table elements
from pagebot.elements.pbtable import Table

# Views and code
from pagebot.elements.views import viewClasses
from pagebot.elements.pbquire import Quire
from pagebot.elements.pbcodeblock import CodeBlock

# Vanilla based UI elements
#from pagebot.elements.ui.uiwindow import UIWindow
#from pagebot.elements.ui.uibutton import UIButton
#from pagebot.elements.ui.uigroup import UIGroup
#from pagebot.elements.ui.uicanvas import UICanvas

# Variable Font elements
# NOTE: `variablefonts` is deprecated.
# Elements should be tested and moved to elements.vf.
from pagebot.elements.variablefonts.variablecircle import VariableCircle
from pagebot.elements.vf.designspacegraph import DesignSpace, DesignSpaceGraph
from pagebot.elements.vf.specimen import TypeList, Waterfall

def elementFromPath(path, name=None, **kwargs):
    """Answer the element that is best suitable to hold the data in the path.
    """
    extension = path2Extension(path).lower()
    if extension in IMAGE_TYPES:
        e = newImage(path, name=name, **kwargs)
    elif extension in FONT_TYPES:
        # TODO: Answer a default specimen element to show the font.
        e = None
    elif extension in MOVIE_TYPES:
        # TODO: Answer a MovieElement instance (to be developed)
        e = None
    elif extension in TEXT_TYPES:
        # TODO: Answer TextBox on the parsed content of the file, instead of
        # the path.
        e = newTextBox(path, name=name, **kwargs)
    else:
        # If no extension-->element can be found.
        e = None

    return e


#   S H O R T C U T S   F O R   C H I L D   E L E M E N T    G E N E R A T O R S

def newView(viewId, **kwargs):
    """In most cases views are initialized as dictionary by the Document class.
    But since they inherit from Element, they also can be used as placable
    elements. Make sure to define the right parent (likely to be a Page or
    Template)."""
    return viewClasses[viewId](**kwargs)

def newPage(**kwargs):
    """In most cases views are initialized as dictionary by the Document class.
    But since they inherit from Element, they also can be used as placable
    elements. Make sure to define the right parent (likely to be a Page or
    Template). Embed the page in a View element, to control appearance, such as
    cropmarks."""
    return Page(**kwargs)

def newTemplate(**kwargs):
    """In most cases views are initialized as dictionary by the Document class.
    But since they inherit from Element, they also can be used as placable
    elements."""
    return Template(**kwargs)

def newPlacer(**kwargs):
    """Placer occupying a space on Page or Template. Is not visible exported
    documets."""
    return Placer(**kwargs)

def newColumn(**kwargs):
    """Answer a new Column instance, offering a squential paste-board for
    elements."""
    return Column(**kwargs)

def newTextBox(bs='', **kwargs):
    """Caller must supply a formatted string. Note that w and h can also be
    defined in the style."""
    return TextBox(bs, **kwargs)

def newText(bs='', **kwargs):
    """Create a Text element. Normally we don't need w and h here, as it is
    made by the text and style combinations. But in case the defined font is a
    Variable Font, then we can use the width and height to interpolate a font
    that fits the space for the given string and weight. Caller must supply
    formatted string. Support both (x, y) and x, y as position."""
    return Text(bs, **kwargs)

def newRect(**kwargs):
    """Create a new Rect element. Note that points can also be defined in the
    style. When omitted, a square is drawn."""
    return Rect(**kwargs)

def newQuire(**kwargs):
    """Create a new Quire element. When omitted, a square is drawn."""
    return Quire(**kwargs)

def newArtboard(**kwargs):
    """Create a new Artboard element."""
    return Artboard(**kwargs)

def newGroup(**kwargs):
    """Create a new Group element. Note that points can also be defined in the
    style. When omitted, a square is drawn."""
    return Group(**kwargs)

def newOval(**kwargs):
    """Create an Oval element. Note that points can also be defined in the
    style."""
    return Oval(**kwargs)

def newCircle(**kwargs):
    """Create a Circle element. Note that points can also be defined in the
    style."""
    return Circle(**kwargs)

def newLine(**kwargs):
    """Create a Line element."""
    return Line(**kwargs)

def newPolygon(points=None, **kwargs):
    """Create a Polygon element."""
    return Polygon(points=points, **kwargs)

def newRuler(**kwargs):
    """Create a Ruler element."""
    return Ruler(**kwargs)

def newPageBotPath(**kwargs):
    return PageBotPath(**kwargs)

def newPaths(paths=None, **kwargs):
    """Creates a Paths element, holding PageBotPath object(s) in the element
    frame. The paths can be a single PageBotPath instance or a list / tuple of
    instances. Not be confused with the filePath "path" in Image."""
    return Paths(paths, **kwargs)

def newImage(path=None, **kwargs):
    """Create Image element as position (x, y) and optional width, height (w,
    h) of which at least one of them should be defined. The path can be None,
    to be filled later. If the image is drawn with an empty or non-existent
    file path, a missingImage cross-frame is shown. The optional imo attribute
    is an DrawBot-modelled ImageObject() with filters in place. The created
    Image element is answered as convenience to the caller."""
    return Image(path=path, **kwargs)

def newTable(cols=1, rows=1, **kwargs):
    """Answers a new Table instanec."""
    return Table(rows=rows, cols=cols, **kwargs)

def newGalley(**kwargs):
    """Answers a new Galley instance."""
    return Galley(**kwargs)
