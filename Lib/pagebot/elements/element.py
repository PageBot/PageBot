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
#     element.py
#

import weakref
import copy

from pagebot.conditions.score import Score
from pagebot.style import makeStyle, getRootStyle
from pagebot.constants import *
from pagebot.fonttoolbox.fontpaths import getDefaultFontPath
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.contexts.basecontext.bezierpath import BezierPath
from pagebot.contexts.basecontext.babelstring import BabelString
from pagebot.toolbox.units import (units, rv, pt, point2D, point3D,
        pointOffset, isUnit, degrees)
from pagebot.toolbox.color import noColor, color, Color, blackColor
from pagebot.toolbox.transformer import uniqueID, asNormalizedJSON
from pagebot.toolbox.timemark import TimeMark
from pagebot.toolbox.dating import now
from pagebot.gradient import Gradient, Shadow
from pagebot.elements.alignments import Alignments
from pagebot.elements.clippath import ClipPath
from pagebot.elements.conditions import Conditions
from pagebot.elements.flow import Flow
from pagebot.elements.imaging import Imaging
from pagebot.elements.shrinking import Shrinking
from pagebot.elements.showings import Showings

class Element(Alignments, ClipPath, Conditions, Flow, Imaging, Shrinking,
        Showings):
    """The base element object."""

    # Initializes the default Element behavior flags. These flags can be
    # overwritten by inheriting classes, or dynamically in instances, e.g.
    # where the settings of Text.nextBox and Text.nextPage define if a Text
    # instance can operate as a flow.
    isText = False

    #isFlow property answers if nextElement or prevElement is defined.
    # isFlow = False

    # Set to True by Page-like elements.
    isPage = False
    isView = False

    GRADIENT_CLASS = Gradient
    SHADOW_CLASS = Shadow
    PATH_CLASS = BezierPath
    STRING_CLASS = BabelString

    def __init__(self, context=None, x=0, y=0, z=0, xy=None, xyz=None,
            w=DEFAULT_WIDTH, h=DEFAULT_HEIGHT, d=DEFAULT_DEPTH, size=None,
            wh=None, whd=None, left=None, top=None, right=None, bottom=None,
            sId=None, lib=None, t=None, timeMarks=None, parent=None, name=None,
            cssClass=None, cssId=None, title=None, description=None,
            theme=None, keyWords=None, language=None, style=None,
            conditions=None, solve=False, framePath=None, elements=None,
            template=None, nextElement=None, prevElement=None, nextPage=None,
            clipPath=None, prevPage=None, thumbPath=None, bleed=None,
            padding=None, pt=0, pr=0, pb=0, pl=0, pzf=0, pzb=0, margin=None,
            mt=0, mr=0, mb=0, ml=0, mzf=0, mzb=0, scaleX=1, scaleY=1, scaleZ=1,
            scale=None, borders=None, borderTop=None, borderRight=None,
            borderBottom=None, borderLeft=None, shadow=None, gradient=None,
            radius=None, htmlCode=None,
            htmlPaths=None, xAlign=None, yAlign=None, zAlign=None,
            proportional=None,
            # Viewing parameters, local overwrite on self.doc.view parameters.
            showBaselineGrid=None, showCropMarks=None,
            showFlowConnections=None, showRegistrationMarks=None,
            showPadding=None, viewPaddingStroke=None,
            viewPaddingStrokeWidth=None, showMargin=None,viewMarginStroke=None,
            viewMarginStrokeWidth=None, showFrame=None, viewFrameStroke=None,
            viewFrameStrokeWidth=None, **kwargs):

        """Base initialize function for all Element constructors. Elements
        always have a location, even if not defined here. Values that are
        passed to the contructor (except for the keyword arguments), have
        default values if they aren't assigned by the parent class.

        >>> import sys
        >>> e = Element(name='TestElement', x=10, y=20, w=100, h=120, pl=11, pt=22, margin=(33,44,55,66))
        >>> e.name
        'TestElement'
        >>> e.description is None
        True
        >>> e.x, e.y, e.w, e.h, e.padding, e.margin
        (10pt, 20pt, 100pt, 120pt, (22pt, 0pt, 0pt, 11pt), (33pt, 44pt, 55pt, 66pt))
        >>> # Default element has default proportions
        >>> e = Element()
        >>> e.x, e.y, e.w, e.h, e.padding, e.margin
        (0pt, 0pt, 100pt, 100pt, (0pt, 0pt, 0pt, 0pt), (0pt, 0pt, 0pt, 0pt))
        >>> from pagebot.document import Document
        >>> from pagebot.contexts import getContext
        >>> # FIXME: don't call Flat explicitly?
        >>> context = getContext('Flat')
        >>> size = pt(300, 400)
        >>> doc = Document(size=size, autoPages=1, padding=30, context=context)
        >>> page = doc[1]
        >>> page.size
        (300pt, 400pt)
        >>> e = Element(parent=page, x=0, y=20, w=page.w, h=3)
        >>> e.context, e.context is doc.view.context
        (<FlatContext>, True)
        >>> doc.build()

        """
        self._parent = None

        # If not None, it overwrites property of searching up the parent tree.
        self._context = context

        # Set the local self._lib, validate it is a dictionary, otherwise
        # create new dictionary.
        self.lib = lib

        # Guaranteed to be unique. Cannot be set.
        self._eId = uniqueID(self)
        # Optional system / user / app ID, used by external application, such as
        # SketchContext. Can be None. If used self.findBysid(sId) works
        # recursively
        self.sId = sId

        # If undefined yAlign, then default yAlign to BOTTOM. Child value is
        # overwritten if a parent is defined. The origin is always at the
        # bottom (OS X style) for now.

        # Property seeks parent.
        if yAlign is None:
            yAlign = BOTTOM

        # Initialize self._elements and self._eIds.
        self.clearElements()
        self.checkStyleArgs(kwargs)

        # Make default style for t == 0 from remaining arguments such as fill,
        # stroke, strokeWidth, textFill, textStroke, textStrokewidth
        self.style = makeStyle(style, **kwargs)
        self.style['xAlign'] = xAlign
        self.style['yAlign'] = yAlign
        self.style['zAlign'] = zAlign

        # An element can have it's own theme (e.g. color palette). Set as property
        # If not defined, then use the parent theme
        self.theme = theme

        # Initialize style values that are not supposed to inherite from parent
        # styles. Always store point in style as separate (x, y, z) values.
        # Missing values are 0. Note that x, y, z, w, h, d, padding and margin
        # are not inherited by style.
        if xyz is not None:
            self.xyz = xyz
        elif xy is not None:
            # self.z is set to DEFAULT_DEPTH
            self.xy = xy
        else:
            self.xyz = x, y, z

        # Alternative attributes, to make it intuitive for the calling function.
        if whd is not None:
            size = whd
        elif wh is not None:
            size = wh

        # Convenience attribute, setting self.w, self.h, self.d
        if size is not None:
            # Works for (w, h) and (w, h, d)
            self.size = size
        else:
            # Otherwise it is assumed that the values are set separately, still
            # default if None.
            self.w = w
            self.h = h
            self.d = d

        # Convenience attribute, setting self.scaleX, self.scaleY, self.scaleZ
        if scale is not None:
            # Works for (scaleX, scaleY) and (scaleX, scaleY, scaleZ)
            self.scale = scale
        else:
            self.scaleX = scaleX
            self.scaleY = scaleY
            self.scaleZ = scaleZ

        # If defined, set after the sizes and scales are set.
        if proportional is not None:
            # Setting True keeps all size and scales proportional now.
            self.proportional = proportional

        self.padding = padding or (pt, pr, pb, pl, pzf, pzb)
        self.margin = margin or (mt, mr, mb, ml, mzf, mzb)

        if bleed is not None:
            # Property tuple (bt, br, bb, bl) ignores to expand into if None
            self.bleed = bleed

        # In case these specific position sides are defined, let them overwrite
        # any (x,y) Since top <--> bottom and left <--> right conflict, we only
        # need to test one of them.

        # to be defined.
        if top is not None:
            self.top = top
        elif bottom is not None:
            self.bottom = bottom
        if left is not None:
            self.left = left
        elif right is not None:
            self.right = right

        # Border info dict have format:
        # dict(line=ONLINE, dash=None, stroke=blackColor, strokeWidth=borderData)
        # If not borders defined, then drawing will use the stroke and
        # strokeWidth (if defined) for intuitive compatibility with DrawBot.
        self.borders = borders or (borderTop, borderRight, borderBottom, borderLeft)

        # Drawing hooks is same for 3 types of view/builders. Seperation must
        # be done by calling function.

        # Shadow and gradient, if defined
        self.shadow = shadow
        self.gradient = gradient
        # Optional frame path to draw instead of bounding box element rectangle.
        self.framePath = framePath

        # Set timer of this element.
        # Default TimeMarks from t == now() until arbitrary one day from now().

        #t0 = now()
        #if timeMarks is None:
        #    timeMarks = [TimeMark(t0, {}), TimeMark(t0 + days(1), {})]
        #self.timeMarks = timeMarks
        #if t is None: # Set the current time of this element.
        #    t = t0
        #self.t = t # Initialize self.style from t = 0
        # List of names of style entries that can interpolate in time.
        #self.timeKeys = INTERPOLATING_TIME_KEYS
        self.t = 0
        self.timeMarks = []
        self.timeKeys = []

        if padding is not None:
            self.padding = padding # Expand by property
        if margin is not None:
            self.margin = margin

        # Class and #Id attributes for HtmlContext usage. Optional CSS class
        # name. Ignored if None, not to overwrite cssClass of parents.
        self.cssClass = cssClass
        # Optional id name for use in CSS-output. Ignored if None.
        self.cssId = cssId

        # Optional resources that can be included for web output (HtmlContext).
        # Define string or file paths where to read content, instead of
        # constructing by the builder.
        # Set to string in case element has HTML as source.
        self.htmlCode = htmlCode
        # List or paths, in case full element HTML is defined in files.
        self.htmlPaths = htmlPaths

        # Generic naming and title.
        # Optional name of an element. Used as base for # id in case of
        # HTML/CSS export.
        self.name = name or 'Untitled'
        # Optional to make difference between title name, style property
        self.title = title or name

        # Element tree
        # Preset, so it exists for checking when appending parent.
        self._parent = None

        if parent is not None:
            # Add and set weakref to parent element or None, if it is the root.
            # Caller must add self to its elements separately. Set references
            # in both directions. Remove any previous parent links.
            self.parent = parent

        # Conditional placement stuff. Allow singles.
        if not conditions is None and not isinstance(conditions, (list, tuple)):
            conditions = [conditions]

        # Explicitedly stored local in element, not inheriting from ancesters.
        # Can be None.
        self.conditions = conditions

        # Optional storage of self.context.BezierPath() to clip the content of
        # self. Also note the possibility of the self.childClipPath property,
        # which returns a BezierPath instance, constructed from the position
        # and layout of self.elements.
        if clipPath is not None:
            # I case defined, make a copy, so translates won't affect the original
            clipPath = clipPath.copy()
        # Optional clip path property, stored as self._clipPath.
        # self.clipPath will first check for the self._clipPath to be set,
        # otherwis looks for a sibling element named "Mask" to render that
        # as clipPath (as generated by Sketch.) None otherwise.
        self.clipPath = clipPath

        # Area for conditions and drawing methods to report errors and
        # warnings.
        self.report = []
        # Optional description of this element or its content. Otherwise None.
        # Can be string or BabelString
        self.description = description
        # Optional used for web pages
        self.keyWords = keyWords
        # Optional language code from HTML standard. Otherwise
        # DEFAULT_LANGUAGE.
        self.language = language
        # Save flow reference names
        # Element itself or name of the prev flow element
        self.prevElement = prevElement
        # Element itself or name of the next flow element
        self.nextElement = nextElement
        # Page element itself or name, identifier or index of the next page
        # that nextElement refers to,
        self.nextPage = nextPage
        # if a flow must run over page boundaries.
        self.prevPage = prevPage
        # Optional storage for the a thumbnail image path visualizing this element.
        # Used by Magazine/PartOfBook and others, to show a predefined
        # thumbnail of a page.
        self.thumbPath = thumbPath

        # Copy relevant info from template: w, h, elements, style, conditions,
        # next, prev, nextPage Initialze self.elements, add template elements
        # and values, copy elements if defined. Note that this does not copy
        # the attributes from template to self. For that
        # self.applyAttributes(template, elements, <attributeName>) should be
        # called.
        self.applyTemplate(template, elements)

        # If flag is set, then solve the conditions upon creation of the
        # element (e.g. to define the height)
        if solve:
            self.solve()

        # View flags, set them as properties, so the right type is expanded
        # (e.g. from bool to list of sides). Initialize to default values by
        # property.
        self.showBaselineGrid = showBaselineGrid
        self.showCropMarks = showCropMarks
        self.showRegistrationMarks = showRegistrationMarks
        self.showPadding = showPadding
        self.showMargin = showMargin
        self.showFrame = showFrame
        self.showFlowConnections = showFlowConnections
        self.viewFrameStroke = viewFrameStroke
        self.viewFrameStrokeWidth = viewFrameStrokeWidth
        self.viewPaddingStroke = viewPaddingStroke
        self.viewPaddingStrokeWidth = viewPaddingStrokeWidth
        self.viewMarginStroke = viewMarginStroke
        self.viewMarginStrokeWidth = viewMarginStrokeWidth

    def __repr__(self):
        """Object as string.

        >>> from pagebot.toolbox.units import mm
        >>> e = Element(name='TestElement', x=10, y=20, w=100, h=120)
        >>> repr(e)
        '<Element "TestElement" x=10pt y=20pt w=100pt h=120pt>'
        >>> e.title = 'MyTitle'
        >>> e.x, e.y = 100, mm(200)
        >>> e
        <Element "MyTitle" x=100pt y=200mm w=100pt h=120pt>
        >>> e.title = None
        >>> e.x = e.y = e.h = 0
        >>> e
        <Element w=100pt>
        """
        s = '<%s' % self.__class__.__name__

        if self.title:
            s += ' "%s"' % self.title

        if self.elements:
            s += ' e=%d' % len(self.elements)
        if self.x:
            s += ' x=%s' % self.x
        if self.y:
            s += ' y=%s' % self.y
        if self.w:
            s += ' w=%s' % self.w
        if self.h:
            s += ' h=%s' % self.h
        return s+'>'

    def __len__(self):
        """Answers total amount of elements, placed or not. Note the various
        ways units, x, y, w and h can be defined.

        >>> # Set as separate units.
        >>> e = Element(name='TestElement', x=100, y=200, w=pt(100), h=pt(120))
        >>> childE1 = Element(name='E1', x=pt(0), y=pt(0), size=pt(21, 22))
        >>> # E.g. set as tuple of units.
        >>> childE2 = Element(name='E2', xy=pt(100, 0), size=pt(11, 12))
        >>> i1 = e.appendElement(childE1)
        >>> i2 = e.appendElement(childE2)
        >>> # Index of appended elements and length of parent.
        >>> i1, i2, len(e)
        (0, 1, 2)
        """
        return len(self.elements)

    def _get_context(self):
        """Answers the self._context if it is defined. Otherwise search
        for the doc.view.context if it exists.

        >>> from pagebot.document import Document
        >>> from pagebot.contexts import getContext
        >>> e = Element()
        >>> e.context is None
        True
        >>> context = getContext('Flat')
        >>> doc = Document(context=context) # Stored as doc.view.context
        >>> doc.view.context
        <FlatContext>
        >>> e = Element(parent=doc[1])
        >>> e.doc.view.context
        <FlatContext>
        >>> e.context
        <FlatContext>
        >>> e.context is doc.view.context is context
        True
        """
        if self._context is None:
            doc = self.doc
            if doc is not None and doc.view is not None:
                return doc.view.context

        for ancestor in self.ancestors:
            if ancestor.context:
                return ancestor.context

        return self._context

    def _set_context(self, context):
        self._context = context # Can be None to reset the search tree.

    context = property(_get_context)

    def _get_view(self):
        """Answers the doc.view if it exists.

        >>> from pagebot.document import Document
        >>> from pagebot.contexts import getContext
        >>> context = getContext('Flat')
        >>> # Stored as doc.view.context.
        >>> doc = Document(context=context)
        >>> e = Element(parent=doc[1])
        >>> e.view, doc.view, e.view is doc.view
        (<PageView>, <PageView>, True)
        """
        return self.doc.view
    view = property(_get_view)

    def _get_theme(self):
        """Answers the theme of this element. If undefined, answers the theme
        of self.parent. If no parent is defined, then answers None.

        >>> from pagebot.themes import BaseTheme, BackToTheCity
        >>> theme1 = BaseTheme()
        >>> theme2 = BackToTheCity()
        >>> e1 = Element(theme=theme1)
        >>> e1.theme
        <Theme BaseTheme mood=normal>
        >>> e2 = Element(parent=e1)
        >>> e2.theme # Inheriting theme from e1
        <Theme BaseTheme mood=normal>
        >>> e2.theme = theme2
        >>> e2.theme # Now e2 has it's own theme
        <Theme Back to the City mood=normal>
        """
        if self._theme is not None:
            return self._theme
        if self.parent is not None:
            return self.parent.theme

        # No theme of parent defined.
        return None

    def _set_theme(self, theme):
        self._theme = theme

    theme = property(_get_theme, _set_theme)

    def _get_isLocked(self):
        return self.css('isLocked', False)
    def _set_isLocked(self, isLocked):
        self.style['isLocked'] = isLocked
    isLocked = property(_get_isLocked, _set_isLocked)

    #   E L E M E N T S
    #
    #   Every element is potentially a container of other elements, in addition
    #   to its own behavior.

    def __getitem__(self, eIdOrName):
        """Answers the element with eIdOrName. Answers None if the element does
        not exist. Elements behave as a semi-dictionary for child elements.
        For retrieval by index, use e.elements[index]

        >>> e = Element(name='TestElement')
        >>> e1 = Element(name='E1', parent=e)
        >>> e['E1'] is e1
        True
        """
        return self.get(eIdOrName)

    def __setitem__(self, eId, e):
        if not e in self.elements:
            self.appendElement(e)
        self._eIds[eId] = e

    def _get_eId(self):
        """The eId guaranteed to be unique and cannot be set.

        >>> from pagebot.toolbox.transformer import hex2dec
        >>> e = Element(name='TestElement', xy=pt(100, 200), size=pt(100, 120))
        >>> # Answers unique hex string in self._eId, such as '234FDC09FC10A0FA790'
        >>> hex2dec(e.eId) > 1000
        True
        """
        return self._eId
    eId = property(_get_eId)

    def _get_elements(self):
        """Property to get / set elements to parent self. Answers a copy of the
        list, not self._elements itself, to avoid problems if iterations on the
        children is changing the parent. E.g. if elements of a Typesetter
        galley are composed on a page.

        >>> e = Element()
        >>> len(e), len(e.elements)
        (0, 0)
        >>> e.elements = (Element(), Element(), Element())
        >>> len(e), len(e.elements)
        (3, 3)
        """
        return list(self._elements)

    def _set_elements(self, elements):
        # Clear all existing child elements of self.
        self.clearElements()

        for e in elements:
            # Make sure to set all references.
            self.appendElement(e)

    elements = property(_get_elements, _set_elements)

    # Answers the x-ref dictionary with elements by their e.eIds
    def _get_elementIds(self):
        """Answers the list with child.eId

        >>> e = Element()
        >>> e.elements = (Element(), Element(), Element())
        >>> len(e.elementIds)
        3
        """
        return self._eIds
    elementIds = property(_get_elementIds)

    def _get_page(self):
        """Answers the page somewhere in the parent tree, if it exists.
        Answers None otherwise.

        >>> from pagebot.elements.page import Page
        >>> page = Page()
        >>> e1 = Element(parent=page)
        >>> e2 = Element(parent=e1)
        >>> e2.page.isPage
        True
        """
        return self.getElementPage()
    page = property(_get_page)

    def _get_root(self):
        """Answers the top of the parent tree.

        >>> e = Element(name='root')
        >>> e1 = Element(parent=e)
        >>> e2 = Element(parent=e1)
        >>> e3 = Element(parent=e2)
        >>> e3.root.name == 'root'
        True
        """
        if self.parent is None:
            return self
        return self.parent.root
    root = property(_get_root)

    def get(self, eIdOrName, default=None):
        """Answers the element by eId or name. Answers the same selection for
        default, if the element cannot be found. Answers None if it does not
        exist.

        >>> e = Element(name='Parent')
        >>> e1 = Element(name='Child')
        >>> i = e.appendElement(e1)
        >>> # Get child element by its name
        >>> child = e.get('Child')
        >>> child is e1
        True
        >>> # Get child elements by is eId
        >>> child = e.get(e1.eId)
        >>> child is e1
        True
        >>> # Child has e as parent
        >>> child.name, child.parent.name
        ('Child', 'Parent')
        >>> e.get('OtherName') is None
        True
        """
        if eIdOrName in self._eIds:
            return self._eIds[eIdOrName]
        e = self.getElementByName(eIdOrName)
        if e is not None:
            return e
        if default is not None:
            return self.get(default)
        return None

    def getElement(self, eId):
        """Answers the page element, if it has a unique element Id. Answers None
        if the eId does not exist as child.

        >>> e1 = Element(name='Child')
        >>> e = Element(name='Parent', elements=[e1])
        >>> child = e.getElement(e1.eId)
        >>> child is e1
        True
        >>> e.getElement('FalseId') is None
        True
        """
        return self._eIds.get(eId)

    def getElementPage(self):
        """Recursively answers the page of this element. This can be several
        layers above self. If there element has not a parent in the line of
        parents, then answers None.

        >>> from pagebot.elements.page import Page
        >>> eb = Element(name='Bottom')
        >>> e = Element(elements=[eb])
        >>> e = Element(elements=[e])
        >>> e = Element(elements=[e])
        >>> page = Page(elements=[e])
        >>> # Find page upwards of parent line, starting a lowest e.
        >>> parentPage = eb.getElementPage()
        >>> page is parentPage
        True
        >>> eb = Element(name='Bottom')
        >>> e = Element(elements=[eb])
        >>> # Element parent line does not contain a page.
        >>> eb.getElementPage() is None
        True
        """
        if self.isPage:
            # Answers if self is a page.
            return self
        if self.parent is not None:
            return self.parent.getElementPage()
        return None

    def getElementByName(self, name):
        """Answers the first element in the offspring list that fits the name.
        Answers None if it cannot be found.

        Note that the result of the search depends on where in the tree self is.
        If self.isPage there probably is a different set of elements found than
        searching witn self as arbitrary Element instance.

        >>> e1 = Element(name='Deeper')
        >>> e2 = Element(name='Deeper')
        >>> e3 = Element(name='Child', elements=[e1, e2])
        >>> e = Element(name='Parent', elements=[e3])
        >>> # Get child element by its name
        >>> child = e.get('Child')
        >>> child is e3
        True
        >>> # Find first down the list
        >>> e.get('Deeper') is e1, e.get('Deeper') is e2
        (True, False)
        """
        if self.name == name:
            return self
        for e in self.elements:
            # Don't search on next page yet.
            found = e.getElementByName(name)
            if found is not None:
                return found
        return None

    #   D R A W B O T / F L A T  S U P P O R T

    def prepare(self, view):
        """Responds to the top-down element broadcast to prepare for build. If
        the original image needs scaling, then prepare the build by letting the
        context make a new cache file with the scaled images. If the cache
        file already exists, then ignore, just continue the broadcast towards
        the child elements. Default behavior is to do nothing. Inheriting
        Element classes can redefine."""
        for e in self.elements:
            e.prepare(view)

    def prepare_flat(self, view):
        for e in self.elements:
            e.prepare_flat(view)

    def getPosition(self, view, origin):
        """Applies various offsets and transformations to determine final
        coordinates at which to place an element on a page."""
        p = pointOffset(self.origin, origin)
        self._applyScale(view, p)
        self._applyAlignment(p)
        self._applyRotation(view, p)
        return p

    def build(self, view, origin=ORIGIN, **kwargs):
        """Default drawing method just drawing the frame. Probably will be
        redefined by inheriting element classes."""
        p = self.getPosition(view, origin)
        self.buildFrame(view, p)
        view.drawPageMetaInfoBackground(self, p)
        view.drawElementFrame(self, p)
        self.buildElement(view, p, **kwargs)
        view.drawPageMetaInfo(self, p)
        self.restore(view, p)
        self.drawMeta(view, origin)

    def restore(self, view, p):
        self._restoreRotation(view, p)
        self._restoreScale(view)

    def drawMeta(self, view, origin):
        """Element draw function based on style settings."""
        # Depends on flag 'view.showElementInfo'.
        view.drawElementInfo(self, origin)
        view.drawElementOrigin(self, origin)
        view.drawFlowConnections(self, origin)

    def buildElement(self, view, p, **kwargs):
        """

        Draws the actual element content. Inheriting elements classes can
        redefine this method only to fill in drawing behaviour. @p is the
        transformed position to draw in the main canvas.

        Main drawing method for elements to draw their content and the
        content of their children if they exist. @p is the transformed position
        of the context canvas. To be redefined by inheriting element classes
        that need to draw more than just their child elements.

        """
        self.buildChildElements(view, p, **kwargs)

    def buildChildElements(self, view, origin=None, **kwargs):
        """Draws child elements, dispatching depends on the implementation of
        context specific build elements.

        If no specific builder_<view.context.b.PB_ID> is implemented, call
        default e.build(view, origin)."""
        hook = 'build_' + view.context.b.PB_ID

        for e in self.elements:
            if not e.show:
                continue
            if hasattr(e, hook):
                getattr(e, hook)(view, origin, **kwargs)
            else:
                # No implementation for this context, call default building
                # method for this element.
                e.build(view, origin, **kwargs)

    #   I N D E S I G N  S U P P O R T

    def prepare_inds(self, view):
        for e in self.elements:
            e.prepare_inds(view)

    def build_inds(self, view, origin, **kwargs):
        """It is better to have a separate InDesignContext build tree, since we
        need more information down there than just drawing instructions. This
        way the InDesignContext just gets the PageBot Element passed over,
        using it's own API."""
        p = pointOffset(self.origin, origin)
        p2D = point2D(self._applyAlignment(p)) # Ignore z-axis for now.
        # Inheriting Elements should add their context call here.
        for e in self.elements:
            e.build_inds(view, p2D, **kwargs)

    #   H T M L  /  S C S S / S A S S  S U P P O R T

    # Sass syntax is not supported yet. It does not appear to be standard and
    # cannot be easily converted from existing CSS. Meanwhile, many CSS
    # designers can extend easier to SCSS.

    def prepare_html(self, view):
        """Respond to the top-down view --> element broadcast in preparation for
        build_html. Default behavior is to do nothing other than recursively
        broadcast to all child element. Inheriting Element classes can
        redefine."""
        for e in self.elements:
            e.prepare_html(view)

    def prepare_zip(self, view):
        """Respond to the top-down view --> element broadcast in preparation
        for build_zip. Default behavior is to do nothing other than
        recursively broadcast to all child element. Inheriting Element classes
        can redefine."""
        for e in self.elements:
            e.prepare_zip(view)

    '''
    def build_scss(self, view):
        """Build the scss variables for this element."""
        b = self.context.b
        b.build_scss(self, view)
        for e in self.elements:
            if e.show:
                e.build_scss(view)
    '''

    def build_css(self, view, cssList=None):
        """Build the scss variables for this element and pass the request on
        to the child elements. This should harvest the CSS that is specific
        for a single page."""
        if cssList is None:
            cssList = []
        for e in self.elements:
            if e.show:
                e.build_css(view, cssList)
        return cssList

    def asNormalizedJSON(self):
        """Build self and all child elements as regular dict and add it to the
        list of siblings. Path points to the folder where elements can copy
        additional files, such as images, fonts, CSS, JS, etc.). This path will
        later be converted to zip file, as main storage of the current
        document.

        >>> import os
        >>> e = Element(x=50, y=60)
        >>> d = e.asNormalizedJSON()
        >>> d['style']['x']['v']
        50
        >>> d['style']['h']['v'], d['style']['h']['class_']
        (100, 'Pt')
        """
        elements = []
        d = dict(
            name=self.name,
            class_=self.__class__.__name__,
            elements=asNormalizedJSON(self.elements),
            style=asNormalizedJSON(self.style)
        )
        return d

    def build_html(self, view, path, **kwargs):
        """Build the HTML/CSS code through WebBuilder (or equivalent) that is
        the closest representation of self. If there are any child elements,
        then also included their code, using the level recursive indent. For
        HTML builder the origin is ignored, as all position is relative."""
        # Use the current context builder to write the HTML/CSS code.
        b = view.context.b

        if self.htmlCode is not None:
            # Add chunk of defined HTML to output.
            b.addHtml(self.htmlCode)
        elif self.htmlPaths is not None:
            for htmlPath in self.htmlPaths:
                # Add HTML content from file, if path is not None and the file
                # exists.
                b.importHtml(htmlPath)
        else:
            # No default class, ignore if not defined.
            b.div(cssClass=self.cssClass, cssId=self.cssId)
            # Build child elements, dispatch if they implemented generic or
            # context specific build method.
            self.buildChildElements(view, path, **kwargs)
            b._div()

    #   D R A W I N G  S U P P O R T

    def getMetricsString(self, view=None):
        """Answers a single string with metrics info about the element. Default
        is to show the posiiton and size (in points and columns). This method
        can be redefined by inheriting elements that want to show additional
        information."""
        s = '%s\nPosition: x=%s, y=%s, z=%s\nSize: w=%s, h=%s' % \
            (self.__class__.__name__ + ' ' + (self.name or ''), self.x, self.y,
                    self.z, self.w, self.h)
        if self.xAlign or self.yAlign:
            s += '\nAlign: %s, %s' % (self.xAlign, self.yAlign)
        if self.conditions:
            if view is None and self.doc is not None:
                view = self.doc.view
            if view is not None:
                score = self.evaluate(view)
                s += '\nConditions: %d | Evaluate %d' % (len(self.conditions), score.result)
                if score.fails:
                    s += ' Fails: %d' % len(score.fails)
                    for eFail in score.fails:
                        s += '\n%s %s' % eFail
        return s

    def buildFrame(self, view, p):
        """Draws optional frame or borders to display element space. self.fill
        defines the color of the element background. Instead of the DrawBot
        stroke and strokeWidth attributes, use borders or (borderTop,
        borderRight, borderBottom, borderLeft) attributes.

        TODO: move to view.
        """
        c = view.context
        eShadow = self.shadow

        if eShadow:
            c.save()
            c.setShadow(eShadow)
            c.rect(p[0], p[1], self.w, self.h)
            c.restore()

        eFill = self.fill # Default is noColor
        eStroke = self.stroke #self.css('stroke', default=noColor)
        eGradient = self.gradient

        #if eStroke is not noColor or eFill is not noColor or eGradient:
        c.save()

        # Drawing element fill and / or frame.
        if eGradient:
            # Gradient overwrites setting of fill.
            # TODO: Make bleed work here too.
            # Add self.w and self.h to define start/end from relative size.
            c.setGradient(eGradient, p, self.w, self.h)
        elif eFill is None or eFill is noColor:
            c.fill(None)
        else:
            c.fill(eFill)

        if eStroke in (None, noColor):
            c.stroke(None, 0)
        else: # Separate from border behavior if set.
            c.stroke(eStroke, self.strokeWidth)

        if self.framePath is not None: # In case defined, use instead of bounding box.
            c.drawPath(self.framePath)

        w = None
        h = None
        if len(p) == 4:
            x, y, w, h = p
        elif len(p) == 2:
            x, y = p
        else:
            x = y = 0
            #msg = 'Element.buildFrame(): Badly formatted position argument p'
            #print(msg)
            # TODO: raise error.

        w = w or self.w
        h = h or self.h

        # FIXME: gives an extra square in lower left corner.
        # Then draw the rectangle with the defined color/stroke/strokeWidth
        #c.rect(x, y, w, h) # Ignore bleed, should already have been applied on position and size.

        c.fill(None)
        c.stroke(None, 0)
        c.restore()

        # Instead of full frame drawing, check on separate border settings.
        borderTop = self.borderTop
        borderBottom = self.borderBottom
        borderRight = self.borderRight
        borderLeft = self.borderLeft

        if borderTop is not None:
            c.save()
            c.lineDash(borderTop.get('dash')) # None for no dash
            c.stroke(borderTop.get('stroke', noColor), borderTop.get('strokeWidth', 0))

            oLeft = 0 # Extra offset on left, if a left border exists.

            if borderLeft and (borderLeft.get('strokeWidth') or pt(0)) > 1:
                if borderLeft.get('line') == ONLINE:
                    oLeft = borderLeft.get('strokeWidth', 0)/2
                elif borderLeft.get('line') == OUTLINE:
                    oLeft = borderLeft.get('strokeWidth', 0)

            oRight = 0 # Extra offset on right, if a right border exists.

            if borderRight and (borderRight.get('strokeWidth') or pt(0)) > 1:
                if borderRight.get('line') == ONLINE:
                    oRight = borderRight.get('strokeWidth', 0)/2
                elif borderRight.get('line') == OUTLINE:
                    oRight = borderRight.get('strokeWidth', 0)

            if borderTop.get('line') == OUTLINE:
                oTop = borderTop.get('strokeWidth', 0)/2
            elif borderTop.get('line') == INLINE:
                oTop = -borderTop.get('strokeWidth', 0)/2
            else:
                oTop = 0

            c.line((x-oLeft, y+h+oTop), (x+w+oRight, y+h+oTop))
            c.restore()

        if borderBottom is not None:
            c.save()
            c.lineDash(borderBottom.get('dash')) # None for no dash
            c.stroke(borderBottom.get('stroke', noColor), borderBottom.get('strokeWidth', 0))

            oLeft = 0 # Extra offset on left, if a left border exists.
            if borderLeft and (borderLeft.get('strokeWidth') or pt(0)) > 1:
                if borderLeft.get('line') == ONLINE:
                    oLeft = borderLeft.get('strokeWidth', 0)/2
                elif borderLeft.get('line') == OUTLINE:
                    oLeft = borderLeft.get('strokeWidth', 0)

            oRight = 0 # Extra offset on right, if a right border exists.
            if borderRight and (borderRight.get('strokeWidth') or pt(0)) > 1:
                if borderRight.get('line') == ONLINE:
                    oRight = borderRight.get('strokeWidth', 0)/2
                elif borderRight.get('line') == OUTLINE:
                    oRight = borderRight.get('strokeWidth', 0)

            if borderBottom.get('line') == OUTLINE:
                oBottom = borderBottom.get('strokeWidth', 0)/2
            elif borderBottom.get('line') == INLINE:
                oBottom = -borderBottom.get('strokeWidth', 0)/2
            else:
                oBottom = 0

            c.line((x-oLeft, y-oBottom), (x+w+oRight, y-oBottom))
            c.restore()

        if borderRight is not None:
            c.save()
            c.lineDash(borderRight.get('dash')) # None for no dash
            c.stroke(borderRight.get('stroke', noColor), borderRight.get('strokeWidth', 0))

            oTop = 0 # Extra offset on top, if a top border exists.
            if borderTop and (borderTop.get('strokeWidth') or pt(0)) > 1:
                if borderTop.get('line') == ONLINE:
                    oTop = borderTop.get('strokeWidth', 0)/2
                elif borderLeft.get('line') == OUTLINE:
                    oTop = borderTop.get('strokeWidth', 0)

            oBottom = 0 # Extra offset on bottom, if a bottom border exists.
            if borderBottom and (borderBottom.get('strokeWidth') or pt(0)) > 1:
                if borderBottom.get('line') == ONLINE:
                    oBottom = borderBottom.get('strokeWidth', 0)/2
                elif borderBottom.get('line') == OUTLINE:
                    oBottom = borderBottom.get('strokeWidth', 0)

            if borderRight.get('line') == OUTLINE:
                oRight = borderRight.get('strokeWidth', 0)/2
            elif borderRight.get('line') == INLINE:
                oRight = -borderRight.get('strokeWidth', 0)/2
            else:
                oRight = 0

            c.line((x+w+oRight, y-oBottom), (x+w+oRight, y+h+oTop))
            c.restore()

        if borderLeft is not None:
            c.save()
            c.lineDash(borderLeft.get('dash')) # None for no dash
            c.stroke(borderLeft.get('stroke', noColor), borderLeft.get('strokeWidth', 0))

            oTop = 0 # Extra offset on top, if a top border exists.
            if borderTop and (borderTop.get('strokeWidth') or pt(0)) > 1:
                if borderTop.get('line') == ONLINE:
                    oTop = borderTop.get('strokeWidth', 0)/2
                elif borderLeft.get('line') == OUTLINE:
                    oTop = borderTop.get('strokeWidth', 0)

            oBottom = 0 # Extra offset on bottom, if a bottom border exists.
            if borderBottom and (borderBottom.get('strokeWidth') or pt(0)) > 1:
                if borderBottom.get('line') == ONLINE:
                    oBottom = borderBottom.get('strokeWidth', 0)/2
                elif borderBottom.get('line') == OUTLINE:
                    oBottom = borderBottom.get('strokeWidth', 0)

            if borderLeft.get('line') == OUTLINE:
                oLeft = borderLeft.get('strokeWidth', 0)/2
            elif borderLeft.get('line') == INLINE:
                oLeft = -borderLeft.get('strokeWidth', 0)/2
            else:
                oLeft = 0

            c.line((x-oLeft, y-oBottom), (x-oLeft, y+h+oTop))
            c.restore()

    #   V A L I D A T I O N


    # Find.

    def deepFindAll(self, name=None, pattern=None, result=None):
        """Perform a dynamic recursive deep find for all elements with the name.
        Don't include self. Either *name* or *pattern* should be defined,
        otherwise an error is raised. Return the collected list of matching child
        elements. Answers an empty list if no elements can be found.

        Note that the result of the search depends on where in the tree self is.
        If self.isPage there probably is a different set of elements found than
        searching witn self as arbitrary Element instance.

        >>> e1 = Element(name='DeeperChild')
        >>> e2 = Element(name='DeeperChild', elements=[e1])
        >>> e3 = Element(name='Child', elements=[e2])
        >>> e = Element(name='Parent', elements=[e3])
        >>> # Get all child elements matching name
        >>> elements = e.deepFindAll(name='DeeperChild')
        >>> len(elements)
        2
        >>> # Get all child elements matching pattern
        >>> elements = e.deepFindAll(pattern='Child')
        >>> len(elements)
        3
        >>> # Answers empty list if no element can be found
        >>> elements = e.deepFindAll(pattern='XYZ')
        >>> len(elements)
        0
        """
        assert name or pattern
        if result is None:
            result = []
        for e in self.elements:
            # Simple pattern match
            if pattern is not None and pattern in e.name:
                result.append(e)
            elif name is not None and name in (e.cssId, e.name):
                result.append(e)
            e.deepFindAll(name, pattern, result)
        return result

    def findAll(self, name=None, pattern=None, cls=None, result=None):
        """Perform a dynamic find for the named element(s) in self.elements.
        Don't include self. Either name or pattern should be defined, otherwise
        an error is raised. Return the collected list of matching child
        elements. Answers an empty list if no elements can be found.

        Note that the result of the search depends on where in the tree self is.
        If self.isPage there probably is a different set of elements found than
        searching witn self as arbitrary Element instance.

        >>> e1 = Element(name='OtherChild')
        >>> e2 = Element(name='OtherChild')
        >>> e3 = Element(name='Child')
        >>> e = Element(name='Parent', elements=[e1, e2, e3])
        >>> # Get all child element matching name
        >>> elements = e.findAll(name='OtherChild')
        >>> len(elements)
        2
        >>> # Get all child element matching name
        >>> elements = e.findAll(pattern='Child')
        >>> len(elements)
        3
        >>> # Answers empty list if no element can be found
        >>> elements = e.findAll(pattern='XYZ')
        >>> len(elements)
        0
        """
        assert name or pattern or cls
        result = []

        for e in self.elements:
            if cls is not None and (cls == e.__class__.__name__ or isinstance(e, cls)):
                 result.append(e)
                # Simple pattern match
            elif pattern is not None and pattern in e.name:
                result.append(e)
            elif name is not None and name in (e.cssId, e.name):
                result.append(e)

        return result

    def deepFind(self, name=None, pattern=None, cls=None):
        """Perform a dynamic recursive deep find for all elements with the
        name. Don't include self. Either *name* or *pattern* should be
        defined, otherwise an error is raised. Return the first matching child
        element. Answers None if no elements can be found.

        Note that the result of the search depends on where in the tree self is.
        If self.isPage there probably is a different set of elements found than
        searching witn self as arbitrary Element instance.

        The name, pattern and cls values are case-sensitive in the search.

        >>> e = Element(name='Parent')
        >>> e1 = Element(name='Child', parent=e)
        >>> e2 = Element(name='DeeperChild', parent=e1)
        >>> e3 = Element(name='DeeperChild', parent=e2)
        >>> e4 = Element(name='DeepestChild', parent=e3)
        >>> # Get all child elements matching name
        >>> element = e.deepFind(name='DeeperChild')
        >>> element is e2
        True
        >>> # Get first child elements matching pattern
        >>> element = e.deepFind(pattern='Child')
        >>> element is e1
        True
        >>> # Search is case-sensitive
        >>> e.select(name='child') is None
        True
        >>> # Get first child elements matching pattern
        >>> element = e.deepFind(pattern='Deepest')
        >>> element is e4
        True
        >>> # Answers None if element does not exist
        >>> element = e.deepFind(pattern='XYZ')
        >>> element is None
        True
        >>> # Get all child elements matching name
        >>> element = e.select(name='DeeperChild')
        >>> element is e2
        True
        """
        assert name or pattern or cls
        for e in self.elements:
            if cls is not None and (cls == e.__class__.__name__ or isinstance(e, cls)):
                 return e
            if pattern is not None and pattern in e.name: # Simple pattern match
                return e
            if name is not None and name in (e.__class__.__name__, e.cssId, e.name):
                return e
            found = e.deepFind(name, pattern)
            if found is not None:
                return found
        return None

    # Intuitive name with identical result. Can be used in MarkDown.
    select = deepFind

    def find(self, name=None, pattern=None, cls=None):
        """Perform a dynamic find for the named element(s) in self.elements.
        Don't include self. Either name or pattern should be defined, otherwise
        an error is raised. Return the first element that fist the criteria.
        Answers None if no element can be found.

        Note that the result of the search depends on where in the tree self is.
        If self.isPage there probably is a different set of elements found than
        searching witn self as arbitrary Element instance.

        >>> e = Element(name='Parent')
        >>> e1 = Element(name='OtherChild', parent=e)
        >>> e2 = Element(name='OtherChild', parent=e)
        >>> e3 = Element(name='LastChild', parent=e)
        >>> # Get first child element mathing class name
        >>> element = e.find(cls="Element")
        >>> element is e1
        True
        >>> # Get first child element mathing class
        >>> element = e.find(cls=Element)
        >>> element is e1
        True
        >>> # Get first child element matching name
        >>> element = e.find(name='OtherChild')
        >>> element is e1
        True
        >>> # Get first child element matching name
        >>> element = e.find(pattern='LastChild')
        >>> element is e3
        True
        >>> # Get first child element matching name
        >>> element = e.find(pattern='XYZ')
        >>> element is None
        True
        """
        assert name or pattern or cls

        for e in self.elements:
            if cls is not None:
                if e.__class__.__name__ == cls:
                    return e
                if e.__class__ == cls:
                    return e
            # Simple pattern match
            if pattern is not None and pattern in e.name:
                return e
            if name is not None and name in (e.cssId, e.name):
                return e

        return None

    def findBysId(self, sId):
        """If defined, the system self.sId can be used to recursively find self
        or a child. Answers None if nothing can be found that is exactly
        matching."""
        if sId is not None:
            if self.sId == sId:
                return self
            for e in self.elements:
                found = e.findBysId(sId)
                if found is not None:
                    return found
        return None

    def clearElements(self):
        """Properly initializes self._elements and self._eIds. Any existing
        element will get its parent weakrefs become None and will be garbage
        collected.

        >>> e1 = Element(name='Child')
        >>> e1 = Element(name='Child')
        >>> e = Element(name='Parent', elements=[e1])
        >>> len(e)
        1
        >>> e.clearElements()
        >>> len(e)
        0
        """
        self._elements = []
        self._eIds = {}

    def clear(self):
        """Make inheriting classes define a method to clear their content if
        appropriate. Default behavior of Element is to do nothing."""

    def copy(self, parent=None):
        """Answers a full copy of self, where the "unique" fields are set to
        default. Also perform a deep copy on all child elements.

        >>> e1 = Element(name='Child', w=100)
        >>> e = Element(name='Parent', elements=[e1], w=200)
        >>> copyE = e.copy()
        >>> copyE.name == e.name, copyE.eId == e.eId
        (True, False)
        >>> # Element tree is copied
        >>> copyE is e, copyE['Child'] is e['Child']
        (False, False)
        >>> # Values are copied
        >>> copyE.name == e.name, copyE.w == e.w == 200, copyE['Child'].w == e['Child'].w == 100
        (True, True, True)
        >>> e.copy().eId != e.eId
        True
        """
        # Deep-copies the element. Set the parent (if defined) and iterate
        # through the child tree to make a e.eId unique.

        savedElements = self._elements # Avoid deep copy on child elements
        self._elements = []
        copied = copy.deepcopy(self)
        self._elements = savedElements

        # Set some attributes on the copy
        copied._eId = uniqueID()

        if parent is not None:
            copied.parent = parent
        for e in self.elements:
            copied.appendElement(e.copy())
        return copied

    #   C H I L D  E L E M E N T  P O S I T I O N S

    def getElementsAtPoint(self, point):
        """Answers the list with elements that fit the point. Note None in the
        point will match any value in the element position. Where None in the
        element position with not fit any xyz of the point.

        >>> e1 = Element(name='Child1', x=20, y=30)
        >>> e2 = Element(name='Child2', x=20, y=40)
        >>> e = Element(name='Parent', elements=[e1, e2])
        >>> e.getElementsAtPoint((20, 30)) == [e1]
        True
        >>> # Search on wildcard x
        >>> e.getElementsAtPoint((None, 40)) == [e2]
        True
        >>> # Find both on wildcard y
        >>> e.getElementsAtPoint((20, None)) == [e1, e2]
        True
        """
        elements = []
        # Add z if tuple is only (x,y)
        px, py, pz = point3D(point)
        for e in self.elements:
            ex, ey, ez = e.xyz
            if (ex == px or px is None) and \
                    (ey == py or py is None) and \
                    (ez == pz or pz is None):
                elements.append(e)
        return elements

    def getElementsPosition(self):
        """Answers the dictionary of element Ids as key and their position as
        value.

        >>> e1 = Element(name='Child1', x=20, y=30)
        >>> e2 = Element(name='Child2', x=20, y=40)
        >>> e = Element(name='Parent', elements=[e1, e2])
        >>> d = e.getElementsPosition()
        >>> len(d)
        2
        >>> d[e1.eId], d[e2.eId]
        ((20pt, 30pt, 0pt), (20pt, 40pt, 0pt))
        """
        elements = {}
        for e in self.elements:
            if e.eId:
                elements[e.eId] = e.xyz
        return elements

    def getPositions(self):
        """"Answers the dictionary of positions of elements. Key is the local
        point of the child element. Value is list of elements.

        >>> e1 = Element(name='Child1', x=20, y=30)
        >>> e2 = Element(name='Child2', x=20, y=40, w=100)
        >>> # Same position, different size.
        >>> e3 = Element(name='Child3', x=20, y=40, w=200)
        >>> e = Element(name='Parent', elements=[e1, e2, e3])
        >>> e1.xyz, e2.xyz, e3.xyz
        ((20pt, 30pt, 0pt), (20pt, 40pt, 0pt), (20pt, 40pt, 0pt))
        >>> d = e.getPositions()
        >>> sorted(d.keys())
        [(20, 30, 0), (20, 40, 0)]
        >>> d[(20, 30, 0)] == [e1], d[(20, 40, 0)] == [e2, e3]
        (True, True)
        """
        positions = {}
        for e in self.elements:
            # Point needs to be tuple to be used a key.
            rxyz = rv(e.xyz)
            if rxyz not in positions:
                positions[rxyz] = []
            positions[rxyz].append(e)
        return positions


    # Text conditions, always True for non-text elements.

    def getDistance2Grid(self, y):
        """Answers the distance between y and y rounded to baseline grid.
        This can be a negative number showing the direction of rounding

        >>> e = Element(h=500, baselineGridStart=100, baselineGrid=10)
        >>> e.getDistance2Grid(pt(40))
        0pt
        >>> e.getDistance2Grid(45)
        -5pt
        >>> e.getDistance2Grid(38)
        2pt
        """
        # Calculate the position of top of the grid
        gridTopY = self.h - (self.baselineGridStart or self.pt)
        # Calculate distance of the line to top of the grid
        gy = gridTopY - y
        dy = gy - round(gy/self.baselineGrid) * self.baselineGrid

        # Now we can answers the difference of y to the nearest grid line
        return dy


    def isTopOnGrid(self, tolerance=0):
        """Answers True if self.top is on the parent grid.
        >>> e1 = Element(baselineGridStart=100, baselineGrid=10, h=1000)
        >>> e2 = Element(y=100, h=200, parent=e1)
        >>> e2.isTopOnGrid()
        True
        >>> e2.y = 102
        >>> e2.isTopOnGrid()
        False
        """
        return abs(self.getDistance2Grid(self.top)) <= tolerance

    def isBottomOnGrid(self, tolerance=0):
        """Answers True if self.bottom is on the parent grid.
        >>> e1 = Element(baselineGridStart=100, baselineGrid=10, h=1000)
        >>> e2 = Element(y=100, h=200, parent=e1)
        >>> e2.isBottomOnGrid()
        True
        >>> e2.y = 102
        >>> e2.isBottomOnGrid()
        False
        """
        return abs(self.getDistance2Grid(self.bottom)) <= tolerance

    def isMiddleOnGrid(self, tolerance=0):
        """Answers True if self.middle is on the parent grid.
        >>> e1 = Element(baselineGridStart=100, baselineGrid=10, h=1000)
        >>> e2 = Element(y=100, h=200, parent=e1)
        >>> e2.isMiddleOnGrid()
        True
        >>> e2.y = 102
        >>> e2.isMiddleOnGrid()
        False
        """
        return abs(self.getDistance2Grid(self.middle)) <= tolerance

    #   S T Y L E

    # Answers the cascaded style value, looking up the chain of ancestors,
    # until style value is defined.

    def css(self, name, default=None):
        """In case we are looking for a plain css value, cascading from the
        main ancestor styles of self, then follow the parent links until
        document or root, if self does not contain the requested value.

        >>> from pagebot.toolbox.units import em
        >>> from pagebot.document import Document
        >>> doc = Document()
        >>> page = doc[1]
        >>> e = Element(fontSize=pt(24), parent=page)
        >>> e.css('fontSize') # Find local style value
        24pt
        >>> e.css('leading') # Find value in root style. Default is absolute unit. Can be changed to em.
        1.4em
        >>> e = Element(fontSize=pt(24), leading=em(1.4))
        >>> e.css('leading'), round(e.css('leading').pt) # Show unit and rendered compared to
        (1.4em, 17)
        """
        if name in self.style and self.style[name] is not None:
            return self.style[name]
        if self.parent is not None:
            return self.parent.css(name, default)
        return default

    def checkStyleArgs(self, d):
        """Fix style values where necessary.
        TODO: make sure keys are correct.

        >>> e = Element()
        >>> style = dict(fill=(1, 0, 0), stroke=0.5)
        >>> e.checkStyleArgs(style)
        >>> style['fill']
        Color(r=1, g=0, b=0)
        >>> style['stroke']
        Color(r=0.5, g=0.5, b=0.5)
        """
        fill = d.get('fill')

        if fill is not None and not isinstance(fill, Color):
            d['fill'] = color(fill)

        stroke = d.get('stroke')

        if stroke is not None and not isinstance(stroke, Color):
            d['stroke'] = color(stroke)

    def getNamedStyle(self, styleName):
        """In case we are looking for a named style (e.g. used by the
        Typesetter to build a stack of cascading tag style, then query the
        ancestors for the named style. Default behavior of all elements is that
        they pass the request on to the root, which is normally the document.
        Use force attribute to overwrite an existing style with the same name.

        >>> from pagebot.document import Document
        >>> from pagebot.toolbox.color import color
        >>> doc = Document()
        >>> # Add named style to document.
        >>> doc.addStyle('body', force=True, style=dict(name='body', fill=color('red')))
        >>> page = doc[1]
        >>> e = Element(parent=page)
        >>>
        >>> e.getNamedStyle('body')['fill']
        Color(name="red")
        """
        if self.parent:
            return self.parent.getNamedStyle(styleName)
        return None

    def getFlattenedStyle(self):
        """Answers the flattened dictionary with all self.css(...) values, from
        the perspecive of self and upward on the parent tree. Evaluate for
        every value that is in the root style.

        >>> from pagebot.toolbox.color import color
        >>> from pagebot.document import Document
        >>> doc = Document()
        >>> page = doc[1]
        >>> e = Element(fill=color(0.1, 0.2, 0.3), parent=page)
        >>> style = e.getFlattenedStyle()
        >>> style['fill'], style['fontSize'], style['leading'], style['xAlign']
        (Color(r=0.1, g=0.2, b=0.3), 12pt, 1.4em, 'left')
        """
        flattenedStyle = {} # Create a dict with all keys from root style and values from self.css()
        for key in getRootStyle():
            flattenedStyle[key] = self.css(key)
        return flattenedStyle

    def getBlendedStyle(self, t=None):
        """Answers the blended style for self, blended between the current time
        marks on position t or self.t. If style values are not in the time
        marks, then their values.

        >>> e = Element(t=10)
        >>> e.getBlendedStyle()
        {}
        """
        blendedStyle = {}
        if t is None:
            t = self.t
        #for timeMark in self.timeMarks:
        #    print(timeMark.t, t)
        # TODO: write this method
        return blendedStyle

    def _get_em(self):
        """Answers the current em value (for use in relative units), as value of
        self.css('fontSize', DEFAULT_FONT_SIZE).

        >>> e = Element(style=dict(fontSize=pt(12)))
        >>> e.em
        12pt
        >>> e.em = pt(21)
        >>> e.em, e.style['fontSize']
        (21pt, 21pt)
        """
        return self.css('fontSize', DEFAULT_FONT_SIZE)
    def _set_em(self, em):
        """Store the em size (as fontSize) in the local style."""
        self.style['fontSize'] = em
    em = property(_get_em, _set_em)

    fontSize = em

    def _get_font(self):
        """Answers the current font instance as defined in style. Text based
        inheriting elements may want to implement as the font of the last added
        text.

        >>> e = Element(style=dict(font='Roboto-Bold'))
        >>> e.font
        <Font Roboto-Bold>
        >>> e.font.info.styleName
        'Bold'
        >>> print(type(e.font))
        <class 'pagebot.fonttoolbox.objects.font.Font'>
        >>> print(type(e.font.info))
        <class 'pagebot.fonttoolbox.objects.fontinfo.FontInfo'>
        """
        """
        >>> print(e.font.info.styleName)
        <BLANKLINE>
        # FIXME: yields 'Roboto-'
        >>> e.font.info.cssName
        'Roboto-Regular'
        """
        font = self.css('font', getDefaultFontPath())
        if isinstance(font, str):
            font = findFont(font)
        return font
    def _set_font(self, font):
        """Store the font in the local style. This can be a path, name or Font instance"""
        self.style['font'] = font
    font = property(_get_font, _set_font)

    def _get_leading(self):
        """Answers the current leading value as defined in style. Text based
        inheriting elements may want to implement leading as the value of the last
        added text.

        >>> from pagebot.toolbox.units import em
        >>> e = Element(style=dict(leading=em(1.4)))
        >>> e.leading
        1.4em
        """
        return self.css('leading', DEFAULT_LEADING)
    def _set_leading(self, leading):
        """Store the leading in the local style."""
        self.style['leading'] = units(leading)
    leading = property(_get_leading, _set_leading)

    def _get_tracking(self):
        """Answers the current tracking value as defined in style. Text based
        inheriting elements may want to implement tracking as the value of the last
        added text.

        >>> from pagebot.toolbox.units import em
        >>> e = Element(style=dict(tracking=em(0.05)))
        >>> e.tracking
        0.05em
        """
        return self.css('tracking', DEFAULT_TRACKING)
    def _set_tracking(self, tracking):
        """Store the tracking in the local style."""
        self.style['tracking'] = units(tracking)
    tracking = property(_get_tracking, _set_tracking)

    def _get_lib(self):
        """Answers the local element.lib dictionary by property, used for custom
        application value storage. Always make sure it is a dictionary.
        """
        return self._lib
    def _set_lib(self, lib):
        if lib  is None:
            lib = {}
        assert isinstance(lib, dict)
        self._lib = lib
    lib = property(_get_lib, _set_lib)

    def _get_docLib(self):
        """Answers the shared document.docLib dictionary by property, used for
        share global entry by elements.  Elements query their self.parent.docLib
        until the root document is reached.

        >>> from pagebot.document import Document
        >>> from pagebot.elements.page import Page
        >>> e = Element(name='Child')
        >>> page = Page(elements=[e])
        >>> doc = Document(pages=[page])
        >>> e.docLib.get('MyValue') == None # Get undefined value
        True
        >>> doc.docLib['MyValue'] = (1, 2, 3)
        >>> e.docLib.get('MyValue') # Get defined value, up parent tree.
        (1, 2, 3)
        """
        parent = self.parent
        if parent is not None:
            # Either parent element or document.docLib.
            return parent.docLib

        # Document cannot be found, or no parent is defined in the element.
        return None
    docLib = property(_get_docLib)

    def _get_doc(self):
        """Answers the root Document of this element by property, looking upward
        in the ancestor tree."""
        if self.parent is not None:
            return self.parent.doc
        return None
    doc = property(_get_doc)

    def _get_page(self):
        """Answers the Page that this element is part of, looking upward in the
        anscestor tree. Answers None, if no Page ascenstor can be found.

        >>> from pagebot.document import Document
        >>> from pagebot.elements import newRect
        >>> doc = Document()
        >>> page = doc[1]
        >>> e1 = newRect(parent=page)
        >>> e2 = newRect(parent=e1)
        >>> e3 = newRect(parent=e2)
        >>> e3.page is page
        True
        >>> newRect().page is None
        True
        """
        if self.isPage:
            return self
        if self.parent is not None:
            return self.parent.page
        return None

    def _get_builder(self):
        return self.view.context.b
    b = builder = property(_get_builder)

    # Most common properties

    def setParent(self, parent):
        """Set the parent of self as weakref if it is not None. Don't call
        self.appendElement(). Calling setParent is not the main way to add an
        element to a parent, because the original parent would not know that
        the element disappeared. Call self.appendElement(e), which will call
        this method. """
        if parent is not None:
            parent = weakref.ref(parent)

        # Can be None if self needs to be unlinked from a parent tree. E.g.
        # when it is moved.
        self._parent = parent

    def _get_parent(self):
        """Answers the parent of the element, if it exists, by weakref
        reference. Answers None if no parent is defined or if the parent
        not longer exists."""
        if self._parent is not None:
            return self._parent()
        return None

    def _set_parent(self, parent):
        # Note that the calling function must add self to its elements.
        if parent is not None:
            #assert not self in parent.ancestors, '[%s.%s] Cannot set one of the children "%s" as parent.' % (self.__class__.__name__, self.name, parent)
            parent.appendElement(self)
        else:
            self._parent = None
    parent = property(_get_parent, _set_parent)

    def _get_siblings(self):
        """Answers all elements that share self.parent, not including self in
        the list."""
        siblings = []
        for e in self.parent.elements:
            if not e is self:
                siblings.append(e)
        return siblings
    siblings = property(_get_siblings)

    def _get_ancestors(self):
        """Answers the list of anscestors of self, including the document root.
        Self is not included."""
        ancestors = []
        parent = self.parent
        while parent is not None:
            assert not parent in ancestors, '[%s.%s] Illegal loop in parent->ancestors reference.' % (self.__class__.__name__, self.name)
            ancestors.append(parent)
            parent = parent.parent
        return ancestors

    ancestors = property(_get_ancestors)

    # Orientation of elements (and pages)

    def _get_isLeft(self):
        """Normal elements don't know the left/right orientation of the page
        that they are on. Pass the request on to the parent, until a page is
        reached.

        >>> from pagebot.document import Document
        >>> doc = Document()
        """
        if self.parent is not None:
            return self.parent.isLeft
        return False
    isLeft = property(_get_isLeft)

    def _get_isRight(self):
        """Normal elements don't know the left / right orientation of the page
        that they are on. Pass the request on to the parent, until a page is
        reached."""
        if self.parent is not None:
            return self.parent.isRight
        return False
    isRight = property(_get_isRight)

    def _get_gridX(self):
        """Answers the grid, depending on the left / right orientation of self.

        >>> from pagebot.toolbox.units import mm
        >>> e = Element(w=mm(210), gridX=((mm(60), mm(5)), (mm(80), None)))
        >>> e.gridX # Two columns with gutter.
        ((60mm, 5mm), (80mm, None))
        >>> e.gridX = (mm(60), mm(5)), (mm(80), None)
        >>> e.gridX
        ((60mm, 5mm), (80mm, None))
        """
        return units(self.css('gridX'))

    def _set_gridX(self, gridX):
        self.style['gridX'] = gridX  # Save locally, blocking CSS parent scope for this param.
    gridX = property(_get_gridX, _set_gridX)

    def _get_gridY(self):
        """Answers the vertical grid, depending on the top/bottom orientation of
        self.

        >>> e = Element(gridY=(10,20,30))
        >>> e.gridY
        (10pt, 20pt, 30pt)
        >>> e.gridY = 40, 50, 60
        >>> e.gridY
        (40pt, 50pt, 60pt)
        """
        return units(self.css('gridY'))

    def _set_gridY(self, gridY):
        self.style['gridY'] = gridY  # Save locally, blocking CSS parent scope for this param.
    gridY = property(_get_gridY, _set_gridY)

    def _get_gridZ(self):
        """Answers the grid, depending on the left/right orientation of self.

        >>> e = Element(gridZ=(10,20,30))
        >>> e.gridZ
        (10pt, 20pt, 30pt)
        >>> e.gridZ = 40, 50, 60
        >>> e.gridZ
        (40pt, 50pt, 60pt)
        """
        return units(self.css('gridZ'))
    def _set_gridZ(self, gridZ):
        self.style['gridZ'] = gridZ  # Save locally, blocking CSS parent scope for this param.
    gridZ = property(_get_gridZ, _set_gridZ)

    def getGridColumns(self):
        """Answers the constructed sequence of [(columnX, columnW), ...] in the
        block of the element.  Note that this is different from the gridX
        definition [(wx, gutter), ...] If there are one or more instances of
        None in the grid definition, then try to fit equally on self.cw.  If
        gutter is left None, then the default style gutter is filled there.

        """
        """
        FIX Grids
        >>> column, gutter = 48, 8 # Preset padding
        >>> e = Element(w=300, h=100, cw=column, gw=gutter, isLeft=True)
        >>> e.getGridColumns() # Equal devided column widths
        [(0, 48), (56, 48), (112, 48), (168, 48), (224, 48)]
        >>> e.getGridColumns() # Changed equal deviced columns
        [(0, 64), (76, 64), (152, 64), (228, 64)]
        >>> e.gridX = (30, 40, 50, 60)
        >>> e.getGridColumns() # Columns from value list
        [(0, 30), (38, 40), (86, 50), (144, 60)]
        """
        gridColumns = []
        gridX = self.gridX
        pw = self.pw # Padded with, available space for columns.
        gw = self.gw or 0

        if gridX is not None: # If a non-linear grid sequence is defined, use that.
            undefined = 0
            usedWidth = 0
            # Make a first pass to see how many columns (None) need equal
            # division and what total width spare we have.
            for gridValue in gridX:
                if not isinstance(gridValue, (list, tuple)):
                    # Only single column width defined, force fill in with
                    # default gw gutter.
                    gridValue = (gridValue, None)
                cw, gutter = gridValue
                if cw is None:
                    undefined += 1
                else:
                    usedWidth += cw
                if gutter is None:
                    gutter = gw
                usedWidth += gutter
            equalWidth = (pw - usedWidth) / (undefined or 1)
            # Now we know the divide width, scan through the grid list again,
            # building x coordinates.
            x = 0
            for gridValue in gridX:
                if not isinstance(gridValue, (list, tuple)):
                    # Only single column width defined, force fill in with default gw gutter.
                    gridValue = (gridValue, None)
                cw, gutter = gridValue
                if cw is None:
                    cw = equalWidth
                if gutter is None:
                    gutter = gw
                gridColumns.append((x, cw))
                x += cw + gutter

        elif self.cw:
            # If no grid defined, and a general grid width is, then run the
            # squence for cw + gw gutter.
            cw = self.cw
            x = 0
            for index in range(int(pw/cw)): # Roughly the amount of columns to expect. Avoid while loop
                if x + cw > pw:
                    break
                gridColumns.append((x, cw))
                x += cw + gw # Next column start position.
        return gridColumns

    def _get_cw(self):
        """Property to access the column width self.css['cw'] style attribute."""
        return self.css('cw')
    def _set_cw(self, cw):
        self.style['cw'] = cw
    cw = property(_get_cw, _set_cw)

    def _get_ch(self):
        """Property to access the column height self.css['ch'] style attribute."""
        return self.css('ch')
    def _set_ch(self, ch):
        self.style['ch'] = ch
    ch = property(_get_ch, _set_ch)

    def getGridRows(self):
        """Answers the constructed sequence of [(columnX, columnW), ...] in the
        block of the element.  Note that this is different from the gridX
        definition [(wx, gutter), ...] If there are one or more instances of
        None in the grid definition, then try to fit equally on self.cw. If
        gutter is left
        None, then the default style gutter is filled there.

        """
        """
        FIXME: grid must not be derived from grid units.
        >>> column, gutter = 48, 8 # Preset padding
        >>> e = Element(w=100, h=300, ch=column, gh=gutter, isLeft=True)
        >>> e.getGridRows() # Equal devided row heights
        [(0, 48), (56, 48), (112, 48), (168, 48), (224, 48)]
        >>> e.ch = 64 # Change row height
        >>> e.gh = 12 # Change gutter
        >>> e.getGridRows() # Changed equal deviced row heights
        [(0, 64), (76, 64), (152, 64), (228, 64)]
        >>> e.gridY = (30, 40, 50, 60)
        >>> e.getGridRows() # Columns from value list
        [(0, 30), (42, 40), (94, 50), (156, 60)]
        """
        gridRows = []
        gridY = self.gridY
        ph = self.ph # Padded height, available space for vertical columns.
        gh = self.gh or 0

        if gridY is not None: # If a non-linear grid sequence is defined, use that.
            undefined = 0
            usedHeight = 0
            #usedWidth = 0
            # Make a first pass to see how many columns (None) need equal division.
            for gridValue in gridY:
                if not isinstance(gridValue, (list, tuple)):
                    # Only single column height defined, force fill in with
                    # default gh gutter.
                    gridValue = (gridValue, None)
                ch, gutter = gridValue
                if ch is None:
                    undefined += 1
                #else:
                #    usedWidth += ch
                if gutter is None:
                    gutter = gh
                usedHeight += gutter
            usedHeight = (ph - usedHeight) / (undefined or 1)
            # Now we know the divide width, scane through the grid list again,
            # building x coordinates.
            y = 0
            for gridValue in gridY:
                if not isinstance(gridValue, (list, tuple)):
                    # Only single column height defined, force fill in with
                    # default gutter.
                    gridValue = (gridValue, None)
                ch, gutter = gridValue
                if ch is None:
                    ch = usedHeight
                if gutter is None:
                    gutter = gh
                gridRows.append((y, ch))
                y += ch + gutter
        elif self.ch:
            # If no grid defined, and a general grid heighti is, then run
            # the squence for ch + gh gutter.
            ch = self.ch
            y = 0
            for index in range(int(ph/ch)):
                # Roughly the amount of columns to expect. Avoid while loop.
                if y + ch > ph:
                    break
                gridRows.append((y, ch))
                y += ch + gh # Next column start position.
        return gridRows

    # No getGrid in Z-direction for now.

    # Properties for unit access.

    def _get_parentW(self):
        """Answers the width if the parent element. If no parent exists,
        answers DEFAULT_WIDTH.

        >>> e0 = Element(w=500)
        >>> e1 = Element()
        >>> e1.parentW
        100pt
        >>> e1.parent = e0
        >>> e1.parentW
        500pt
        """
        if self.parent is None:
            return DEFAULT_WIDTH
        return self.parent.w # Answers total width as reference for relative units.
    parentW = property(_get_parentW)

    def _get_parentH(self):
        """Answers the height if the parent element. If no parent exists,
        answers DEFAULT_HEIGHT.

        >>> e0 = Element(h=500)
        >>> e1 = Element()
        >>> e1.parentH
        100pt
        >>> e1.parent = e0
        >>> e1.parentH
        500pt
        """
        if self.parent is None:
            return DEFAULT_HEIGHT
        return self.parent.h # Answers total height as reference for relative units.
    parentH = property(_get_parentH)

    def _get_parentD(self):
        """Answers the depth if the parent element. If no parent exists,
        answers DEFAULT_DEPTH.

        >>> e0 = Element(d=502)
        >>> e1 = Element()
        >>> e1.parentD # No parent, answers default value
        100pt
        >>> e1.parent = e0 # Set parent, now width of parent is answered.
        >>> e1.parentD
        502pt
        """
        if self.parent is None:
            return DEFAULT_DEPTH
        return self.parent.d # Answers total depth as reference for relative units.
    parentD = property(_get_parentD)

    # Plain coordinates

    def _get_x(self):
        """Answers the `x` position of self as Unit instance. In case it is a
        relative unit (such as Fr, Perc or Em), we just set the current parent
        total and em as reference. By not freezing or rendering the value yet,
        the calling function can decide to change parent value, and then render
        the value as with `u.get(optionalTotal)`. Some situations require the
        rendered value, but in case of CSS, the relative value should be
        maintained. Then the current parent total reference is not important.

        >>> from pagebot.toolbox.units import fr, isUnit
        >>> e = Element(x=100, w=400)
        >>> e.x, e.y, e.z
        (100pt, 0pt, 0pt)
        >>> e.x = 200
        >>> e.x, e.y, e.z
        (200pt, 0pt, 0pt)
        >>> isUnit(e.x) # These are Unit instances, not hard values.
        True
        >>> child = Element(x='40%', parent=e)
        >>> #child.x.pt # 40% of 400
        #160
        >>> e.w = 500 # Child percentage changes dynamically from parent
        >>> #child.x.pt # 40% of 500
        #200
        >>> child.x = fr(0.5)
        >>> child.x
        0.5fr
        """
        # Retrieve as Unit instance and adjust attributes to current settings.
        #base = dict(base=self.parentW, em=self.em) # In case relative units, use this as base.
        return units(self.style.get('x', 0))#, base=base)

    def _set_x(self, x):
        """Convert to units, if x is not already a Unit instance."""
        self.style['x'] = units(x)

    x = property(_get_x, _set_x)

    def _get_y(self):
        """Answers the y position of self.

        >>> e = Element(y=100, h=400)
        >>> e.x, e.y, e.z
        (0pt, 100pt, 0pt)
        >>> e.y = 200
        >>> e.x, e.y, e.z
        (0pt, 200pt, 0pt)
        >>> child = Element(y='40%', parent=e)
        >>> child.y#, child.y.pt # 40% of 400
        40%
        >>> e.h = 500
        >>> child.y#, child.y.pt # 40% of 500 dynamic calculation
        40%
        """
        # Retrieve as Unit instance and adjust attributes to current settings.
        #base = dict(base=self.parentH, em=self.em) # In case relative units, use this as base.
        return units(self.style.get('y', 0))#, base=base)
    def _set_y(self, y):
        """Convert to units, if y is not already a Unit instance."""
        self.style['y'] = units(y)
    y = property(_get_y, _set_y)

    def _get_z(self):
        """Answers the z position of self.

        >>> e = Element(z=100, d=400)
        >>> e.x, e.y, e.z
        (0pt, 0pt, 100pt)
        >>> e.size3D
        (100pt, 100pt, 400pt)
        >>> e.z = 200 # Auto conversion to point units.
        >>> e.x, e.y, e.z
        (0pt, 0pt, 200pt)
        >>> e.z = '20mm'
        >>> e.x, e.y, e.z
        (0pt, 0pt, 20mm)
        >>> e.size3D
        (100pt, 100pt, 400pt)
        >>> child = Element(z='40%', parent=e)
        >>> child.z#, child.z.base, child.z.rv, child.z.ru # 40% of 400
        40%
        >>> e.d = 500
        >>> child.z, child.z.pt # 40% of 500 dynamic calculation. Should have value or pt as result?
        (40%, 40)
        """
        # Retrieve as Unit instance and adjust attributes to current settings.
        #base = dict(base=self.parentD, em=self.em) # In case relative units, use this as base.
        return units(self.style.get('z', 0))#, base=base)
    def _set_z(self, z):
        """Convert to units, if z is not already a Unit instance."""
        self.style['z'] = units(z)
    z = property(_get_z, _set_z)

    def _get_xy(self):
        """Answers the Point2D tuple.

        >>> from pagebot.toolbox.units import perc, ru, rv
        >>> e = Element(x=10, y=20, w=400, h=400)
        >>> e.xy
        (10pt, 20pt)
        >>> e.xy = 11, 21
        >>> e.xy
        (11pt, 21pt)
        >>> e.xy = 12, 22, 32 # Ignore the z-value
        >>> e.xy
        (12pt, 22pt)
        >>> e.y += 100
        >>> e.xy
        (12pt, 122pt)
        >>> child = Element(xy=perc('50%', '50%'), parent=e)
        >>> #child.xy, ru(child.xy), rv(child.xy) # Position in middle of parent square
        #((50%, 50%), (200pt, 200pt), (200, 200))
        """
        return self.x, self.y
    def _set_xy(self, p):
        assert len(p) >= 2
        self.x = p[0] # Convert values to Unit instance if needed.
        self.y = p[1] # Ignore any z
        self.z = DEFAULT_DEPTH
    xy = property(_get_xy, _set_xy)

    def _get_xyz(self):
        """Answers the Point3D tuple.

        >>> from pagebot.toolbox.units import ru, rv
        >>> e = Element(x=10, y=20, z=30, w=400, h=400, d=400)
        >>> e.xyz
        (10pt, 20pt, 30pt)
        >>> e.xyz = 11, 21, 31
        >>> e.xyz
        (11pt, 21pt, 31pt)
        >>> e.xyz = 12, 22, 32
        >>> e.xyz
        (12pt, 22pt, 32pt)
        >>> child = Element(x='50%', y='50%', z='50%', parent=e)
        >>> child.xyz = units('12%'), 22, 32
        >>> child.xyz
        (12%, 22pt, 32pt)
        >>> child.x += 100
        >>> child.xyz
        (112%, 22pt, 32pt)
        >>> #child.xyz, ru(child.xyz), rv(child.xyz) # Position in middle of parent cube
        #((112%, 22pt, 32pt), (448pt, 22pt, 32pt), (448, 22, 32))
        """
        return self.x, self.y, self.z
    def _set_xyz(self, p):
        assert len(p) == 3
        self.x = p[0]
        self.y = p[1]
        self.z = p[2]
    xyz = property(_get_xyz, _set_xyz)

    def _get_origin(self):
        """Answers the self.xyz, where y can be flipped."""
        return self._applyOrigin(self.xyz)

    origin = property(_get_origin)

    def _applyOrigin(self, p):
        # Nothing for now, as origin-top function removed.
        return p

    def _get_angle(self):
        """Answers the rotation angle.

        >>> from pagebot.toolbox.units import degrees, radians
        >>> e = Element(angle=degrees(40))
        >>> e.angle
        40deg
        >>> e.angle = radians(0.4) + 0.25
        >>> e.angle
        0.65rad
        >>> e.angle = degrees(130) - radians(0.5)
        >>> e.angle
        40deg
        >>> e.angle = 30 # Degrees is default.
        """
        return self.style.get('angle', degrees(0))

    def _set_angle(self, angle):
        if isinstance(angle, (int, float)):
            angle = degrees(angle)
        self.style['angle'] = angle

    angle = property(_get_angle, _set_angle)

    def _get_rx(self):
        """Answers the relative rotation center for x.

        >>> from pagebot.toolbox.units import mm
        >>> e = Element(rx=120)
        >>> e.rx
        120pt
        >>> e.rx += 20
        >>> e.rx
        140pt
        >>> e.rx = mm(100)
        >>> e.rx
        100mm
        """
        # Retrieve as Unit instance and adjust attributes to current settings.
        #base = dict(base=self.parentW, em=self.em) # In case relative units, use this as base.
        return units(self.style.get('rx', 0))#, base=base)

    def _set_rx(self, rx):
        """Convert to units, if rx is not already a Unit instance."""
        self.style['rx'] = units(rx)

    rx = property(_get_rx, _set_rx)

    def _get_ry(self):
        """Answers the relative rotation center for y.

        >>> from pagebot.toolbox.units import mm
        >>> e = Element(ry=120)
        >>> e.ry
        120pt
        >>> e.ry += 20
        >>> e.ry
        140pt
        >>> e.ry = mm(100)
        >>> e.ry
        100mm
        """
        # Retrieve as Unit instance and adjust attributes to current settings.
        #base = dict(base=self.parentH, em=self.em) # In case relative units, use this as base.
        return units(self.style.get('ry', 0))#, base=base)

    def _set_ry(self, ry):
        """Convert to units, if rx is not already a Unit instance."""
        self.style['ry'] = units(ry)

    ry = property(_get_ry, _set_ry)

    def _get_rz(self):
        """Answers the relative rotation center for z.

        >>> from pagebot.toolbox.units import mm
        >>> e = Element(rz=120)
        >>> e.rz
        120pt
        >>> e.rz += 20
        >>> e.rz
        140pt
        >>> e.rz = mm(100)
        >>> e.rz
        100mm
        """
        # Retrieve as Unit instance and adjust attributes to current settings.
        #base = dict(base=self.parentD, em=self.em) # In case relative units, use this as base.
        return units(self.style.get('rz', 0))#, base=base)

    def _set_rz(self, rz):
        """Convert to units, if rx is not already a Unit instance."""
        self.style['rz'] = units(rz)

    rz = property(_get_rz, _set_rz)

    #   T I M E

    def _get_t(self):
        """The self._t status is the time status, interpolating between the
        values in self.tStyles[t1] and self.tStyles[t2] where t1 <= t <= t2 and
        these styles contain the requested parameters.

        >>> from pagebot.toolbox.dating import minutes
        >>> e = Element()
        >>> #now() - e.t < minutes(1)
        """
        return self._t

    def _set_t(self, t):
        if t is None:
            t = now()
        self._t = t
        # @@@ NOT YET
        #if self._tm0 is None or self._tm1 is None or t < self._tm0.t or self._tm1.t < t:
        #    # If not initialized or t outside cached time span, then create new expanded styles.
        #    self._tm0, self._tm1 = self.getExpandedTimeMarks(t)

    t = property(_get_t, _set_t)

    def appendTimeMark(self, tm):
        assert isinstance(tm, TimeMark)
        self.timeMarks.append(tm)
        self.timeMarks.sort() # Keep them in tm.t order.

    '''
    #FIXME: The 'timers' var below is undefined. Was it intended to be self.timeMarks perhaps?

    def NOTNOW_getExpandedTimeMarks(self, t):
        """Answers a new interpolated TimeState instance, from the enclosing time states for t."""
        timeValueNames = self.timeKeys
        rootStyleKeys = self.timeMarks[0].keys()
        for n in range(1, len(timers)):
            tm0 = self.timeMarks[timers[n-1]]
            if t < tm0.t:
                continue
            tm1 = self.timeMarks[timers[n]]
            futureTimers = timers[n:]
            pastTimers = timers[:n-1]
            for rootStyleKey in rootStyleKeys:
                if not rootStyleKey in tm1.style:
                    for futureTime in futureTimers:
                        futureTimeMark = self.timeMarks[futureTime]
                        if rootStyleKey in futureTimeMark.style:
                            tm1.style[rootStyleKey] = futureTimeMark.style[rootStyleKey]

            return tm0, tm1
        raise ValueError
    '''

    # Origin compensated by alignment. This is used for easy solving of
    # conditions, where the positioning can be compenssaring the element
    # alignment type.

    def _get_left(self):
        """Answers the position of the left side of the element, in relation to
        `self.x` and depending on horizontal alignment.

        >>> from pagebot.toolbox.units import mm
        >>> e = Element(x=100, w=248, xAlign=LEFT)
        >>> e.left
        100pt
        >>> e.left = mm(100)
        >>> e.left
        100mm
        >>> e.w = mm(120)
        >>> e.xAlign = CENTER
        >>> e.left
        40mm
        >>> e.x = mm(0)
        >>> e.left
        -60mm
        >>> e.xAlign = RIGHT
        >>> e.left
        -120mm
        >>> e.left = mm(0)
        >>> e.x
        120mm
        """
        xAlign = self.xAlign
        if xAlign == CENTER:
            return self.x - self.w/2
        if xAlign == RIGHT:
            return self.x - self.w
        return self.x
    def _set_left(self, x):
        xAlign = self.xAlign
        if xAlign == CENTER:
            self.x = x + self.w/2
        elif xAlign == RIGHT:
            self.x = x + self.w
        else:
            self.x = x
    left = property(_get_left, _set_left)

    def _get_mLeft(self):
        """Answers left position, including left margin of self

        >>> from pagebot.toolbox.units import mm
        >>> e = Element(x=mm(100), w=248, xAlign=LEFT, margin=mm(15))
        >>> e.mLeft
        85mm
        >>> e.mLeft = mm(50)
        >>> e.x, e.mLeft
        (65mm, 50mm)
        >>> e.ml = mm(25) # x does not change,
        >>> e.x, e.mLeft # but margin increases, so e.mLeft decreases.
        (65mm, 40mm)
        """
        return self.left - self.ml
    def _set_mLeft(self, x):
        self.left = x + self.ml
    mLeft = property(_get_mLeft, _set_mLeft)

    def _get_center(self):
        """Answers the position of the horizontal center of the element, in
        relation to `self.x` and depending on horizontal alignment.

        >>> e = Element(x=100, w=248, xAlign=LEFT)
        >>> e.center
        224pt
        >>> e.center = 224
        >>> e.center
        224pt
        >>> e.xAlign = CENTER
        >>> e.center
        100pt
        >>> e.xAlign = RIGHT
        >>> e.center
        -24pt
        """
        xAlign = self.xAlign
        if xAlign == LEFT:
            return self.x + self.w/2
        if xAlign == RIGHT:
            return self.x - self.w/2
        return self.x
    def _set_center(self, x):
        xAlign = self.xAlign
        if xAlign == LEFT:
            self.x = units(x) - self.w/2
        elif xAlign == RIGHT:
            self.x = units(x) + self.w/2
        else:
            self.x = x
    center = property(_get_center, _set_center)

    def _get_right(self):
        """Answers the position of the right side of the element, in relation to
        self.x and depending on horiontal alignment.

        >>> e = Element(x=50, w=240, xAlign=LEFT)
        >>> e.right
        290pt
        >>> e.x += 50 # Move x by 50, e.right moves by 50 too
        >>> e.right
        340pt
        >>> e.xAlign = CENTER
        >>> e.right
        220pt
        >>> e.xAlign = RIGHT
        >>> e.right
        100pt
        >>> # Move by right side, setting the value.
        >>> e.xAlign = LEFT
        >>> e.right = 500 # Numbers get converted to default pt units
        >>> e.x, e.left, e.center, e.right, e.w # Right align, so e.x is on 500pt too.
        (260pt, 260pt, 380pt, 500pt, 240pt)
        >>> e.xAlign = CENTER
        >>> e.right = 500 # Run again after alignment changed, it's not a status, it calculates e.x
        >>> e.x, e.left, e.center, e.right # Centered, so e.x is now on 500pt - 240pt/2 = 380pt
        (380pt, 260pt, 380pt, 500pt)
        >>> e.xAlign = RIGHT
        >>> e.right = 500 # Run again after alignment changed, it's not a status, it calculates e.x
        >>> e.x, e.left, e.center, e.right # Left align, so e.x is now on 500pt - 240pt = 260pt
        (500pt, 260pt, 380pt, 500pt)
        """
        xAlign = self.xAlign
        if xAlign == LEFT:
            return self.x + self.w
        if xAlign == CENTER:
            return self.x + self.w/2
        return self.x
    def _set_right(self, x):
        xAlign = self.xAlign
        if xAlign == LEFT:
            self.x = x - self.w # Creates a unit, even when x is a number.
        elif xAlign == CENTER:
            self.x = x - self.w/2 # Creates a unit, even when x is a number.
        else:
            self.x = x # Automatic conversion to pt-units, in case x is a number.
    right = property(_get_right, _set_right)

    def _get_mRight(self):
        """Right position, including right margin.

        >>> e = Element(x=100, w=248, mr=44, xAlign=LEFT)
        >>> e.mRight
        392pt
        >>> e.xAlign = RIGHT
        >>> e.mRight
        144pt
        >>> e.xAlign = CENTER
        >>> e.mRight
        268pt
        """
        return self.right + self.mr
    def _set_mRight(self, x):
        self.right = x - self.mr
    mRight = property(_get_mRight, _set_mRight)

    # Vertical

    def _get_top(self):
        """Answers the top position (relative to self.parent) of self.

        >>> e = Element(y=100, h=248, yAlign=TOP)
        >>> e.top
        100pt
        >>> e.yAlign = BOTTOM
        >>> e.top
        348pt
        >>> e.yAlign = MIDDLE
        >>> e.top
        224pt
        """
        yAlign = self.yAlign

        if yAlign == MIDDLE:
            return self.y + self.h/2
        if yAlign == BOTTOM:
            return self.y + self.h
        # yAlign must be TOP or None
        return self.y

    def _set_top(self, y):
        """Shift the element so `self.top == y`. Where the "top" is, depends on
        the setting of `self.yAlign`. If `self.isText`, then vertical position
        can also be defined by the top or bottom position of the baseline."""
        yAlign = self.yAlign

        if yAlign == MIDDLE:
            self.y = units(y) - self.h/2
        elif yAlign == BOTTOM:
            self.y = units(y) - self.h
        else: # yAlign must be TOP or None
            self.y = y

    top = property(_get_top, _set_top)

    def _get_mTop(self):
        """Answers the top position, including top margin.

        >>> e = Element(y=100, h=248, yAlign=TOP, mt=20)
        >>> e.mTop
        120pt
        >>> e.yAlign = BOTTOM
        >>> e.top
        348pt
        >>> e.yAlign = MIDDLE
        >>> e.top
        224pt
        """
        return self.top + self.mt

    def _set_mTop(self, y):
        self.top = units(y) - self.mt

    mTop = property(_get_mTop, _set_mTop)

    def _get_middle(self):
        """On bounding box, not including margins.

        >>> e = Element(y=100, h=248, yAlign=TOP)
        >>> e.yAlign = TOP
        >>> e.middle
        -24pt
        >>> e.yAlign = BOTTOM
        >>> e.middle
        224pt
        >>> e.yAlign = MIDDLE
        >>> e.middle
        100pt
        """
        yAlign = self.yAlign
        if yAlign == TOP:
            return self.y - self.h/2
        if yAlign == BOTTOM:
            return self.y + self.h/2
        return self.y
    def _set_middle(self, y):
        yAlign = self.yAlign
        if yAlign == TOP:
            self.y = y + self.h/2
        elif yAlign == BOTTOM:
            self.y = y - self.h/2
        else:
            self.y = y
    middle = property(_get_middle, _set_middle)

    def _get_bottom(self):
        """On bounding box, not including margins.

        >>> e = Element(h=500, yAlign=TOP)
        >>> e.bottom
        -500pt
        >>> e.yAlign = MIDDLE
        >>> e.bottom
        -250pt
        >>> e.yAlign = BOTTOM
        >>> e.bottom
        0pt
        >>> e.bottom = 300
        >>> e.bottom
        300pt
        """
        yAlign = self.yAlign
        if yAlign == TOP:
            return self.y - self.h
        if yAlign == MIDDLE:
            return self.y - self.h/2
        return self.y
    def _set_bottom(self, y):
        yAlign = self.yAlign
        if yAlign == TOP:
            self.y = units(y) + self.h
        elif yAlign == MIDDLE:
            self.y = units(y) + self.h/2
        else:
            self.y = y
    bottom = property(_get_bottom, _set_bottom)

    def _get_mBottom(self):
        # Bottom, including bottom margin.
        return self.bottom - self.mb

    def _set_mBottom(self, y):
        b = units(y) + self.mb
        self.bottom = units(y) + self.mb

    mBottom = property(_get_mBottom, _set_mBottom)

    # Depth, running  in vertical z-axis dirction. Viewer is origin, positive
    # value is perpendicular into the screen. Besides future usage in real 3D
    # rendering, the z-axis is used to compare conditional status in element
    # layers.

    def _get_front(self):
        zAlign = self.css('zAlign')
        if zAlign == MIDDLE:
            return self.z - self.d/2
        if zAlign == BACK:
            return self.z - self.d
        return self.z
    def _set_front(self, z):
        zAlign = self.css('zAlign')
        if zAlign == MIDDLE:
            self.z = units(z) + self.d/2
        elif zAlign == BACK:
            self.z = units(z) + self.d
        else:
            self.z = z
    front = property(_get_front, _set_front)

    def _get_mFront(self): # Front, including front margin
        return self.front + self.css('mzf')
    def _set_mFront(self, z):
        self.front = units(z) + self.css('mzf')
    mFront = property(_get_mFront, _set_mFront)

    def _get_back(self):
        zAlign = self.css('zAlign')
        if zAlign == MIDDLE:
            return self.z + self.d/2
        if zAlign == FRONT:
            return self.z + self.d
        return self.z
    def _set_back(self, z):
        zAlign = self.css('zAlign')
        if zAlign == MIDDLE:
            self.z = units(z) - self.d/2
        elif zAlign == FRONT:
            self.z = units(z) - self.d
        else:
            self.z = z
    back = property(_get_back, _set_back)

    def _get_mBack(self):
        # Front, including front margin.
        return self.back - self.css('mzb')
    def _set_mBack(self, z):
        self.back = units(z) - self.css('mzb')
    mBack = property(_get_mBack, _set_mBack)

    # Colors for fill and stroke

    def _get_fill(self):
        """Fill color property in style, using self.css to query cascading
        values. Setting the color will overwrite the cascade, by storing as
        local value.

        >>> e = Element(fill=color('red'))
        >>> e.fill
        Color(name="red")
        >>> # Construct color from tuple.
        >>> e.fill = 1, 0, 0
        >>> e.fill
        Color(r=1, g=0, b=0)
        >>> e.fill = 0.5
        >>> e.fill
        Color(r=0.5, g=0.5, b=0.5)
        """
        return self.css('fill', noColor)
    def _set_fill(self, c):
        self.style['fill'] = color(c)
    fill = property(_get_fill, _set_fill)

    def _get_stroke(self):
        """Stroke color property in style, using self.css to query cascading
        values. Setting the color will overwrite the cascade, by storing as
        local value.

        >>> e = Element(stroke=color('red'))
        >>> e.stroke
        Color(name="red")
        >>> e.stroke = 1, 0, 0 # Construct color from tuple
        >>> e.stroke
        Color(r=1, g=0, b=0)
        >>> e.stroke = 0.5
        >>> e.stroke
        Color(r=0.5, g=0.5, b=0.5)
        """
        return self.css('stroke', noColor)
    def _set_stroke(self, c):
        self.style['stroke'] = color(c)
    stroke = property(_get_stroke, _set_stroke)

    def _get_strokeWidth(self):
        """Stroke width property in style, using self.css to query cascading
        values. Setting the color will overwrite the cascade, by storing as
        local value.

        >>> from pagebot.toolbox.units import mm, p
        >>> e = Element(strokeWidth=p(6))
        >>> e.strokeWidth
        6p
        >>> e.strokeWidth = mm(2)
        >>> e.strokeWidth
        2mm
        """
        return self.css('strokeWidth', pt(1))
    def _set_strokeWidth(self, u):
        self.style['strokeWidth'] = units(u)
    strokeWidth = property(_get_strokeWidth, _set_strokeWidth)

    def _get_textFill(self):
        """Fill color property in style for text, using self.css to query
        cascading values. Setting the color will overwrite the cascade, by
        storing as local value.

        >>> e = Element(textFill=color('red'))
        >>> e.textFill
        Color(name="red")
        >>> # Construct color from tuple.
        >>> e.textFill = 1, 0, 0
        >>> e.textFill
        Color(r=1, g=0, b=0)
        >>> e.textFill = 0.5
        >>> e.textFill
        Color(r=0.5, g=0.5, b=0.5)
        """
        return self.css('textFill', noColor)
    def _set_textFill(self, c):
        self.style['textFill'] = color(c)
    textFill = property(_get_textFill, _set_textFill)

    def _get_textStroke(self):
        """Stroke color property in style, using self.css to query cascading
        values. Setting the color will overwrite the cascade, by storing as
        local value.

        >>> e = Element(textStroke=color('red'))
        >>> e.textStroke
        Color(name="red")
        >>> # Construct color from tuple.
        >>> e.textStroke = 1, 0, 0
        >>> e.textStroke
        Color(r=1, g=0, b=0)
        >>> e.textStroke = 0.5
        >>> e.textStroke
        Color(r=0.5, g=0.5, b=0.5)
        """
        return self.css('textStroke', noColor)
    def _set_textStroke(self, c):
        self.style['textStroke'] = color(c)
    textStroke = property(_get_textStroke, _set_textStroke)

    def _get_textStrokeWidth(self):
        """Stroke width property in style for text, using self.css to query
        cascading values. Setting the color will overwrite the cascade, by
        storing as local value.

        >>> from pagebot.toolbox.units import mm, p
        >>> e = Element(textStrokeWidth=p(6))
        >>> e.textStrokeWidth
        6p
        >>> e.textStrokeWidth = mm(2)
        >>> e.textStrokeWidth
        2mm
        """
        return self.css('textStrokeWidth', pt(1))
    def _set_textStrokeWidth(self, u):
        self.style['textStrokeWidth'] = units(u)
    textStrokeWidth = property(_get_textStrokeWidth, _set_textStrokeWidth)

    # Borders (equivalent for element stroke and strokWidth)

    def getBorderDict(self, stroke=None, strokeWidth=None, line=None,
            dash=None, border=None):
        """Internal method to create a dictionary with border info. If no valid
        border dictionary is defined, then use optional stroke and strokeWidth
        to create one. Otherwise answers *None*."""
        if border is False:
            return {}

        if isinstance(border, dict):
            return border

        # If number, assume it is strokeWidth
        if isinstance(border, (int, float)):
            strokeWidth = units(border)

        if stroke is None:
            stroke = self.css('stroke', blackColor)

        # Take current stroke width setting in css
        #if strokeWidth is None:
        #    strokeWidth = self.strokeWidth

        if line is None:
            line = ONLINE

        # Dash can be None
        # If 0, then answers an empty dict.
        if not strokeWidth:
            return {}
        return dict(stroke=stroke, strokeWidth=units(strokeWidth), line=line, dash=dash)

    def _get_borders(self):
        """Set all borders of the element.

        >>> from pagebot.toolbox.units import p
        >>> e = Element(stroke=(1, 0, 0))
        >>> e.borders = 2 # Value converts to units
        >>> e.borders[0].get('strokeWidth')
        2pt
        >>> e.borders = p(5) # Set a unit
        >>> e.borders[0].get('strokeWidth')
        5p
        >>> e.borders[0]['stroke']
        Color(r=1, g=0, b=0)
        """
        return self.borderTop, self.borderRight, self.borderBottom, self.borderLeft
    def _set_borders(self, borders):
        if isUnit(borders) or isinstance(borders, (int, float)):
            borders = self.getBorderDict(strokeWidth=borders)
        if not isinstance(borders, (list, tuple)):
            # Make copy, in case it is a dict, otherwise changes will be made in all.
            borders = copy.copy(borders), copy.copy(borders), copy.copy(borders), copy.copy(borders)
        elif len(borders) == 2:
            borders = [borders[0], borders[0], borders[1], borders[1]]
        elif len(borders) == 1:
            borders = [borders[0],borders[0],borders[0],borders[0]]
        self.borderTop, self.borderRight, self.borderBottom, self.borderLeft = borders
    # Seems to be confusing having only one of the two. So allow both property
    # names for the same property.
    border = borders = property(_get_borders, _set_borders)

    def _get_borderTop(self):
        """Set the border data on top of the element.

        >>> from pagebot.toolbox.color import color, blackColor
        >>> e = Element()
        >>> e.borderTop = e.getBorderDict(strokeWidth=pt(5), stroke=blackColor)
        >>> sorted(e.borderTop.items())
        [('dash', None), ('line', 'online'), ('stroke', Color(r=0, g=0, b=0)), ('strokeWidth', 5pt)]
        >>> e.borderTop = 2

        """
        return self.css('borderTop')
    def _set_borderTop(self, border):
        self.style['borderTop'] = self.getBorderDict(border=border)
    borderTop = property(_get_borderTop, _set_borderTop)

    def _get_borderRight(self):
        return self.css('borderRight')
    def _set_borderRight(self, border):
        self.style['borderRight'] = self.getBorderDict(border=border)
    borderRight = property(_get_borderRight, _set_borderRight)

    def _get_borderBottom(self):
        return self.css('borderBottom')
    def _set_borderBottom(self, border):
        self.style['borderBottom'] = self.getBorderDict(border=border)
    borderBottom = property(_get_borderBottom, _set_borderBottom)

    def _get_borderLeft(self):
        return self.css('borderLeft')
    def _set_borderLeft(self, border):
        self.style['borderLeft'] = self.getBorderDict(border=border)
    borderLeft = property(_get_borderLeft, _set_borderLeft)

    # Alignment types, defines where the origin of the element is located.

    def _validateXAlign(self, xAlign): # Check and answers value
        assert xAlign in XALIGNS, '[%s.xAlign] Alignment "%s" not valid in %s' % (self.__class__.__name__, xAlign, XALIGNS)
        return xAlign
    def _validateYAlign(self, yAlign): # Check and answers value
        assert yAlign in YALIGNS, '[%s.yAlign] Alignment "%s" not valid in %s' % (self.__class__.__name__, yAlign, YALIGNS)
        return yAlign
    def _validateZAlign(self, zAlign): # Check and answers value
        assert zAlign in ZALIGNS, '[%s.zAlign] Alignment "%s" not valid in %s' % (self.__class__.__name__, zAlign, ZALIGNS)
        return zAlign

    def _get_xAlign(self): # Answers the type of x-alignment. For compatibility allow align and xAlign as equivalents.
        return self._validateXAlign(self.css('xAlign'))
    def _set_xAlign(self, xAlign):
        self.style['xAlign'] = self._validateXAlign(xAlign) # Save locally, blocking CSS parent scope for this param.
    xAlign = property(_get_xAlign, _set_xAlign)

    def _get_yAlign(self): # Answers the type of y-alignment.
        return self._validateYAlign(self.css('yAlign'))
    def _set_yAlign(self, yAlign):
        self.style['yAlign'] = self._validateYAlign(yAlign) # Save locally, blocking CSS parent scope for this param.
    yAlign = property(_get_yAlign, _set_yAlign)

    def _get_zAlign(self): # Answers the type of z-alignment.
        return self._validateZAlign(self.css('zAlign'))
    def _set_zAlign(self, zAlign):
        self.style['zAlign'] = self._validateZAlign(zAlign) # Save locally, blocking CSS parent scope for this param.
    zAlign = property(_get_zAlign, _set_zAlign)


    # Validation to be used by text supporting subclasses
    def _validateXTextAlign(self, xAlign): # Check and answers value
        assert xAlign in XTEXTALIGNS, '[%s.xAlign] Alignment "%s" not valid in %s' % (self.__class__.__name__, xAlign, XALIGNS)
        return xAlign
    def _validateYTextAlign(self, yAlign): # Check and answers value
        assert yAlign in YTEXTALIGNS, '[%s.yAlign] Alignment "%s" not valid in %s' % (self.__class__.__name__, yAlign, YALIGNS)
        return yAlign

    def _get_xTextAlign(self):
        """Answers the type of x-alignment for text strings. Mostly used for elements that support text.

        >>> e = Element()
        >>> e.xTextAlign is None
        True
        """
        return self._validateXTextAlign(self.css('xTextAlign'))
    def _set_xTextAlign(self, xTextAlign):
        self.style['xTextAlign'] = self._validateXTextAlign(xTextAlign) # Save locally, blocking CSS parent scope for this param.
    xTextAlign = property(_get_xTextAlign, _set_xTextAlign)


    def _get_gw(self): # Gutter width
        return self.css('gw', 0)
    def _set_gw(self, gw):
        self.style['gw'] = gw # Set local.
    gw = property(_get_gw, _set_gw)

    def _get_gh(self): # Gutter height
        return self.css('gh', 0)
    def _set_gh(self, gh):
        self.style['gh'] = gh # Set local
    gh = property(_get_gh, _set_gh)

    def _get_gd(self): # Gutter depth
        return self.css('gd', 0)
    def _set_gd(self, gd):
        self.style['gd'] = gd
    gd = property(_get_gd, _set_gd)

    def _get_gutter(self): # Tuple of (w, h) gutters
        """Gutter property for (e.gw, e.gh)

        >>> e = Element()
        >>> e.gutter
        (0, 0)
        >>> e.gutter = 10, 8
        >>> e.gutter, e.gw, e.gh
        ((10, 8), 10, 8)
        >>> e.gutter = 12 # Set both values
        >>> e.gutter
        (12, 12)
        >>> e = Element(style=dict(gw=13, gh=9))
        >>> e.gutter
        (13, 9)
        >>> e.gutter[0] == e.gw, e.gutter[1] == e.gh
        (True, True)
        """
        return self.gw, self.gh
    def _set_gutter(self, gutter):
        if not isinstance(gutter, (list, tuple)):
            gutter = [gutter]
        if len(gutter) == 1:
            gutter = (gutter[0], gutter[0])
        elif len(gutter) == 2:
            pass
        else:
            raise ValueError
        self.gw, self.gh = gutter
    gutter = property(_get_gutter, _set_gutter)

    def _get_gutter3D(self): # Tuple of (gw, gh, gd) gutters
        """Gutter 3D property for (e.gw, e.gh, e.gd)

        >>> e = Element()
        >>> e.gutter3D
        (0, 0, 0)
        >>> e.gutter3D = 10, 8, 6
        >>> e.gutter3D, e.gw, e.gh, e.gd
        ((10, 8, 6), 10, 8, 6)
        >>> e.gutter3D = 12 # Set all 3 values values
        >>> e.gutter3D
        (12, 12, 12)
        >>> e = Element(style=dict(gw=13, gh=9, gd=7))
        >>> e.gutter3D
        (13, 9, 7)
        >>> e.gutter3D[0] == e.gw, e.gutter3D[1] == e.gh, e.gutter3D[2] == e.gd
        (True, True, True)
        """
        return self.gw, self.gh, self.gd
    def _set_gutter3D(self, gutter3D):
        if not isinstance(gutter3D, (list, tuple)):
            gutter3D = [gutter3D]
        if len(gutter3D) == 1:
            gutter3D = (gutter3D[0], gutter3D[0], gutter3D[0])
        elif len(gutter3D) == 3:
            pass
        else:
            raise ValueError
        self.gw, self.gh, self.gd = gutter3D
    gutter3D = property(_get_gutter3D, _set_gutter3D)

    def _get_bleed(self):
        """Answers the value for bleed over the sides of parent or page objects.
        Elements will take care of reposition / scaling themselves

        >>> from pagebot.toolbox.units import mm
        >>> e = Element(bleed=21)
        >>> e.bleed
        (21pt, 21pt, 21pt, 21pt)
        >>> e.bleed = 22 # Auto-convert to pt-units
        >>> e.bleed
        (22pt, 22pt, 22pt, 22pt)
        >>> e.bleed = mm(3)
        >>> e.style['bleedTop'] = pt(8.5) # Overwrite the top bleed from generic set.
        >>> e.bleed
        (8.5pt, 3mm, 3mm, 3mm)
        """
        return self.bleedTop, self.bleedRight, self.bleedBottom, self.bleedLeft
    def _set_bleed(self, bleed):
        if isinstance(bleed, (list, tuple)):
            if len(bleed) == 4:
                self.bleedTop, self.bleedRight, self.bleedBottom, self.bleedLeft = bleed
            elif len(bleed) == 2:
                self.bleedTop, self.bleedRight = self.bleedBottom, self.bleedLeft = bleed
            else: # Any other length, we just take the first one and copy
                self.bleedTop = self.bleedRight = self.bleedBottom = self.bleedLeft = bleed[0]
        else: # If there's only one value, copy onto all sides.
            self.bleedTop = self.bleedRight = self.bleedBottom = self.bleedLeft = bleed
    bleed = property(_get_bleed, _set_bleed)

    def _get_bleedTop(self):
        """Answers the value for bleed over the sides of parent or page objects.
        Elements will take care of reposition / scaling themselves.

        >>> from pagebot.toolbox.units import mm
        >>> e = Element(bleedTop=20)
        >>> e.bleedTop
        20pt
        >>> e.bleed = 6
        >>> e.bleedTop = mm(5)
        >>> e.bleed
        (5mm, 6pt, 6pt, 6pt)
        """
        #base = dict(base=self.h, em=self.em) # In case relative units, use this as base.
        return units(self.css('bleedTop', 0))#, base=base)
    def _set_bleedTop(self, bleed):
        self.style['bleedTop'] = units(bleed, default=0)
    bleedTop = property(_get_bleedTop, _set_bleedTop)

    def _get_bleedBottom(self):
        """Answers the value for bleed over the sides of parent or page objects.
        Elements will take care of reposition / scaling themselves.

        >>> from pagebot.toolbox.units import mm
        >>> e = Element(bleedBottom=20)
        >>> e.bleedBottom
        20pt
        >>> e.bleed = 6
        >>> e.bleedBottom = mm(5)
        >>> e.bleedBottom
        5mm
        >>> e.bleed
        (6pt, 6pt, 5mm, 6pt)
        """
        base = dict(base=self.h, em=self.em) # In case relative units, use this as base.
        return units(self.css('bleedBottom', 0), base=base)
    def _set_bleedBottom(self, bleed):
        self.style['bleedBottom'] = units(bleed, default=0)
    bleedBottom = property(_get_bleedBottom, _set_bleedBottom)

    def _get_bleedLeft(self):
        """Answers the value for bleed over the sides of parent or page
        objects. Elements will take care of reposition / scaling themselves.

        >>> from pagebot.toolbox.units import mm
        >>> e = Element(bleedLeft=20)
        >>> e.bleedLeft
        20pt
        >>> e.bleed = 6
        >>> e.bleedLeft = mm(5)
        >>> e.bleed
        (6pt, 6pt, 6pt, 5mm)
        """
        #base = dict(base=self.w, em=self.em) # In case relative units, use this as base.
        return units(self.css('bleedLeft', 0))#, base=base)
    def _set_bleedLeft(self, bleed):
        self.style['bleedLeft'] = units(bleed, default=0)
    bleedLeft = property(_get_bleedLeft, _set_bleedLeft)

    def _get_bleedRight(self):
        """Answers the value for bleed over the sides of parent or page
        objects. Elements will take care of reposition / scaling themselves.

        >>> from pagebot.toolbox.units import mm
        >>> e = Element(bleedRight=20)
        >>> e.bleedRight
        20pt
        >>> e.bleed = 21
        >>> e.bleedRight = mm(5)
        >>> e.bleed
        (21pt, 5mm, 21pt, 21pt)
        """
        #base = dict(base=self.w, em=self.em) # In case relative units, use this as base.
        return units(self.css('bleedRight', 0))#, base=base)
    def _set_bleedRight(self, bleed):
        self.style['bleedRight'] = units(bleed, default=0)
    bleedRight = property(_get_bleedRight, _set_bleedRight)

    def _get_bleedW(self):
        """Answers the width of the element, including the bleed left and right,
        if defined.

        >>> from pagebot.toolbox.units import p
        >>> e = Element(w=p(100), bleed=p(1))
        >>> e.bleedW
        102p
        >>> e.w, e.bleedLeft, e.bleedRight
        (100p, 1p, 1p)
        """
        return self.w + self.bleedLeft + self.bleedRight
    bleedW = property(_get_bleedW)

    def _get_bleedH(self):
        """Answers the height of the element, including the bleed top and
        bottom, if defined.

        >>> from pagebot.toolbox.units import p
        >>> e = Element(h=p(100), bleed=p(1.5))
        >>> e.bleedH
        103p
        >>> e.h, e.bleedTop, e.bleedBottom
        (100p, 1p6, 1p6)
        """
        return self.h + self.bleedTop + self.bleedBottom
    bleedH = property(_get_bleedH)

    # Absolute positions

    def _get_bleedOrigin(self):
        """Answers the origin of the element, shifted by the defined bleed and
        and depending the side of alignment.
        """

        """
        >>> from pagebot.toolbox.units import p
        >>> e = Element(bleed=p(1), xAlign=LEFT, yAlign=TOP)
        >>> e.bleed
        (1p, 1p, 1p, 1p)
        >>> e.bleedOrigin
        (-12pt, -12pt)
        >>> e.xAlign=RIGHT
        >>> e.yAlign=BOTTOM
        >>> e.bleedOrigin
        (12pt, 12pt)
        """
        ox, oy = self.xy
        if self.xAlign == LEFT:
            ox -= self.bleedLeft
        elif self.xAlign == RIGHT:
            ox += self.bleedRight
        if self.yAlign == TOP:
            oy += self.bleedTop
        elif self.yAlign == BOTTOM:
            oy -= self.bleedBottom
        return ox, oy
    bleedOrigin = property(_get_bleedOrigin)

    def _get_viewCropMarkDistance(self):
        return self.css('viewCropMarkDistance', 0)
    def _set_viewCropMarkDistance(self, d):
        self.style['viewCropMarkDistance'] = units(d)
    viewCropMarkDistance = property(_get_viewCropMarkDistance, _set_viewCropMarkDistance)

    def _get_viewCropMarkSize(self):
        return self.css('viewCropMarkSize', pt(40))
    def _set_viewCropMarkSize(self, d):
        self.style['viewCropMarkSize'] = units(d)
    viewCropMarkSize = property(_get_viewCropMarkSize, _set_viewCropMarkSize)

    def _get_viewCropMarkStrokeWidth(self):
        return self.css('viewCropMarkStrokeWidth', pt(0.25))
    def _set_viewCropMarkStrokeWidth(self, d):
        self.style['viewCropMarkStrokeWidth'] = units(d)
    viewCropMarkStrokeWidth = property(_get_viewCropMarkStrokeWidth, _set_viewCropMarkStrokeWidth)


    def _get_viewRegistrationMarkDistance(self):
        return self.css('viewRegistrationMarkDistance', 0)
    def _set_viewRegistrationMarkDistance(self, d):
        self.style['viewRegistrationMarkDistance'] = units(d)
    viewRegistrationMarkDistance = property(_get_viewRegistrationMarkDistance, _set_viewRegistrationMarkDistance)

    def _get_viewRegistrationMarkSize(self):
        return self.css('viewRegistrationMarkSize', pt(40))
    def _set_viewRegistrationMarkSize(self, d):
        self.style['viewRegistrationMarkSize'] = units(d)
    viewRegistrationMarkSize = property(_get_viewRegistrationMarkSize, _set_viewRegistrationMarkSize)

    def _get_viewRegistrationMarkStrokeWidth(self):
        return self.css('viewRegistrationMarkStrokeWidth', pt(0.25))
    def _set_viewRegistrationMarkStrokeWidth(self, d):
        self.style['viewRegistrationMarkStrokeWidth'] = units(d)
    viewRegistrationMarkStrokeWidth = property(_get_viewRegistrationMarkStrokeWidth, _set_viewRegistrationMarkStrokeWidth)

    def _get_rootX(self):
        """Answers the read-only property root value of local self.x,
        from the whole tree of ancestors.

        >>> e1 = Element(x=10)
        >>> e2 = Element(x=20, elements=[e1])
        >>> e3 = Element(x=44, elements=[e2])
        >>> e1.x, e1.rootX, e2.x, e2.rootX, e3.x, e3.rootX
        (10pt, 74pt, 20pt, 64pt, 44pt, 44pt)
        """
        parent = self.parent
        if parent is not None:
            return self.x + parent.rootX # Add relative self to parents position.
        return self.x
    rootX = property(_get_rootX)

    def _get_rootY(self):
        """Answers the read-only property root value of local self.y,
        from the whole tree of ancestors.

        >>> e1 = Element(y=10)
        >>> e2 = Element(y=20, elements=[e1])
        >>> e3 = Element(y=44, elements=[e2])
        >>> e1.y, e1.rootY, e2.y, e2.rootY, e3.y, e3.rootY
        (10pt, 74pt, 20pt, 64pt, 44pt, 44pt)
        """
        parent = self.parent
        if parent is not None:
            return self.y + parent.rootY # Add relative self to parents position.
        return self.y
    rootY = property(_get_rootY)

    def _get_rootZ(self):
        """Answers the read-only property root value of local self.z,
        from the whole tree of ancestors.

        >>> e1 = Element(z=10)
        >>> e2 = Element(z=20, elements=[e1])
        >>> e3 = Element(z=44, elements=[e2])
        >>> e1.z, e1.rootZ, e2.z, e2.rootZ, e3.z, e3.rootZ
        (10pt, 74pt, 20pt, 64pt, 44pt, 44pt)
        """
        parent = self.parent
        if parent is not None:
            # Add relative self to parents position.
            return self.z + parent.rootZ
        return self.z
    rootZ = property(_get_rootZ)

    # (w, h, d) size of the element.

    def _get_proportional(self):
        """Get/set the proportional style flag as property. If True, setting
        self.w or self.h will keep the original proportions, but setting the
        other side as well. By default the self.proportional flag is False for
        most types of elements.

        >>> e = Element(w=100, h=200, proportional=True)
        >>> e.w = 200
        >>> e.h # Keeps proportions
        400pt
        >>> e.w = 10
        >>> e.h # Keeps proportions
        20pt
        >>> e.proportional = False
        >>> e.w = 100
        >>> e.h # Does not change
        20pt
        >>> e.proportional = True
        >>> e.h = 1000
        >>> e.w # Keeps proportions again
        5000pt
        """
        return self.css('proportional')
    def _set_proportional(self, proportional):
        self.style['proportional'] = proportional
    proportional = property(_get_proportional, _set_proportional)

    def _get_w(self):
        """Answers the width of the element.

        >>> e = Element(w=100)
        >>> e.w
        100pt
        >>> e.w = 101
        >>> e.w
        101pt
        >>> e.w = 0 # Zero width expands to DEFAULT_WIDTH (100)
        >>> e.w, e.w == DEFAULT_WIDTH
        (100pt, True)
        >>> child = Element(w='20%', parent=e)
        >>> child.w, child.w.pt
        (20%, 20)
        >>> child.w = '2fr' # Set as string get interpreted.
        >>> #FIX child.w, child.w.pt
        (2fr, 50)
        >>> e.style['fontSize'] = 10
        >>> child.w = '4.5em' # Multiplication factor with current e.style['fontSize'] (e.fontSize)
        >>> #child.w, child.w.pt
        #(4.5em, 45)
        """
        #base = dict(base=self.parentW, em=self.em) # In case relative units, use this as base.
        return units(self.css('w'))#, base=base)

    def _set_w(self, w):
        w = units(w or DEFAULT_WIDTH)

        if self.proportional and self.w:
            self.style['h'] = w * self.h.pt / self.w.pt
            self.style['d'] = w * self.d.pt / self.w.pt

        # Overwrites element local style from here, parent css becomes inaccessable.
        self.style['w'] = w

    w = property(_get_w, _set_w)

    def _get_mw(self): # Width, including margins
        """Width property for self.mw style. Answers the width of the elements
        with added left/right margins.
        Note that since the margins are not considered by the self.proportional flag,
        changed in self.mw, self.mh and self.md may not stay proportional.

        >>> e = Element(w=10, ml=22, mr=33)
        >>> e.mw
        65pt
        >>> e = Element()
        >>> e.w = 100 # Numbers convert to points by default
        >>> e.ml = 44
        >>> e.mr = 55
        >>> e.mw # e.ml + e.w + e.mr
        199pt
        """
        return self.w + self.ml + self.mr # Add margins to width

    def _set_mw(self, w):
        self.w = max(0, w - self.ml - self.mr) # Should not become < 0

    mw = property(_get_mw, _set_mw)

    def _get_h(self):
        """Answers the height of the element.

        >>> e = Element(h=222)
        >>> e.h
        222pt
        >>> e.h = 440
        >>> e.h
        440pt
        >>> child = Element(h='20%', parent=e)
        >>> #child.h.base
        #440pt
        >>> #FIX child.h, child.h.ru, child.h.rv
        (20%, 88pt, 88)
        >>> e.style['fontSize'] = 12
        >>> child.h = '4.5em' # Multiplication with current e.style['fontSize']
        >>> #child.h, child.h.pt
        #(4.5em, 54)
        """
        # In case relative units, use this as base.
        #base = dict(base=self.parentH, em=self.em)
        return units(self.css('h', 0))#, base=base)

    def _set_h(self, h):
        h = units(h)
        if self.proportional and self.h:
            self.style['w'] = h * self.w.pt/self.h.pt
            self.style['d'] = h * self.d.pt/self.h.pt

        # Overwrite element local style from here, parent css becomes
        # inaccessable.
        self.style['h'] = h
    h = property(_get_h, _set_h)

        # Height, including margins
    def _get_mh(self):
        """Height property for self.mh style.  Note that since the margins are
        not considered by the self.proportional flag, changed in self.mw,
        self.mh and self.md may not stay proportional.

        >>> e = Element(h=10, mt=22, mb=33)
        >>> e.mh
        65pt
        >>> e = Element()
        >>> e.h = 100
        >>> e.mt = 44
        >>> e.mb = 55
        >>> e.mh # e.mt + e.h + e.mb
        199pt
        """
        return self.h + self.mt + self.mb # Add margins to height
    def _set_mh(self, h):
        self.h = max(0, h - self.mt - self.mb) # Should not become < 0
    mh = property(_get_mh, _set_mh)

    def _get_d(self):
        """Answers and set the depth of the element.

        >>> e = Element()
        >>> # Default value
        >>> e.d
        100pt
        >>> # Set min/max of element with constructor
        >>> e = Element(d=100)
        >>> # Set depth value
        >>> e.d = 101
        >>> e.d
        101pt
        """
        # In case relative units, use this as base.
        base = dict(base=self.parentD, em=self.em)
        return units(self.css('d', 0), base=base)

    def _set_d(self, d):
        d = units(d)
        if self.proportional and self.d:
            self.style['w'] = d * self.w.pt/self.d.pt
            self.style['h'] = d * self.h/self.d
        # Overwrite element local style from here, parent css becomes inaccessable.
        self.style['d'] = d
    d = property(_get_d, _set_d)

    def _get_md(self): # Depth, including margin front and margin back in z-axis.
        """Width property for self.md style. Note that since the margins are
        not considered by the self.proportional flag, changed in self.mw,
        self.mh and self.md may not stay proportional.

        >>> e = Element(d=10, mzb=22, mzf=33)
        >>> e.md
        65pt
        >>> e = Element()
        >>> e.d = 10
        >>> e.mzb = 22
        >>> e.mzf = 33
        >>> e.md
        65pt
        """
        return self.d + self.mzb + self.mzf # Add front and back margins to depth
    def _set_md(self, d):
        self.d = max(0, d - self.mzf - self.mzb) # Should not become < 0, behind viewer?
    md = property(_get_md, _set_md)

    def _get_folds(self):
        """List if [(x, y), ...] (one of them can be None) that indicate the
        position of folding lines on a page. In general this is a view
        parameter (applying to all pages), but it can be overwritten by
        individual pages or other elements, if their folding pattern is
        different. The position of folds is ignored by self.w and self.h. It
        is mostly to show folding markers by PageView. The fold property is
        stored in style and not inherited."""
        return self.style.get('folds', []) # Not inherited
    def _set_folds(self, folds):
        self.style['folds'] = folds
    folds = property(_get_folds, _set_folds)

    # Margin properties

    # TODO: Add support of "auto" values, doing live centering.

    def _get_margin(self):
        """Tuple of paddings in CSS order, direction of clock
        Can be 123, [123], [123, 234], [123, 234, 345], [123, 234, 345, 456]
        or [123, 234, 345, 456, 567, 678]

        >>> from pagebot.toolbox.units import mm, perc, ru, rv
        >>> e = Element(margin=(10, 20, 30, 40))
        >>> e.mt, e.mr, e.mb, e.ml
        (10pt, 20pt, 30pt, 40pt)
        >>> e.ml = 123
        >>> e.margin
        (10pt, 20pt, 30pt, 123pt)
        >>> e.margin = mm(20) # Works in other types of units too.
        >>> e.margin
        (20mm, 20mm, 20mm, 20mm)
        >>> e.margin = (11, 22)
        >>> e.margin
        (11pt, 22pt, 11pt, 22pt)
        >>> e.margin = (11, 22, 33)
        >>> e.margin
        (11pt, 22pt, 33pt, 11pt)
        >>> e.margin = (11, 22, 33, 44)
        >>> e.margin
        (11pt, 22pt, 33pt, 44pt)
        >>> e.mt, e.mr, e.mb, e.ml
        (11pt, 22pt, 33pt, 44pt)
        >>> e.margin = (11, 22, 33, 44, 55, 66)
        >>> e.margin, ru(e.margin), rv(e.margin)
        ((11pt, 22pt, 33pt, 44pt), (11pt, 22pt, 33pt, 44pt), (11, 22, 33, 44))
        >>> e.w = e.h = e.d = 500
        >>> e.margin = '10%'
        >>> e.margin
        (10%, 10%, 10%, 10%)
        >>> e.margin = perc(15)
        >>> e.margin
        (15%, 15%, 15%, 15%)
        """
        return self.mt, self.mr, self.mb, self.ml

    def _set_margin(self, margin):
        # Can be 123, [123], [123, 234] or [123, 234, 345, 4565, ]
        if not isinstance(margin, (list, tuple)):
            margin = [margin]
        if len(margin) == 1: # All same value
            margin = (margin[0], margin[0], margin[0], margin[0], margin[0], margin[0])
        elif len(margin) == 2: # mt == mb, ml == mr, mzf == mzb
            margin = (margin[0], margin[1], margin[0], margin[1], margin[0], margin[1])
        elif len(margin) == 3: # mt == ml == mzf, mb == mr == mzb
            margin = (margin[0], margin[1], margin[2], margin[0], margin[1], margin[2])
        elif len(margin) == 4: # mt, mr, mb, ml, pt(0), pt(0)
            margin = (margin[0], margin[1], margin[2], margin[3], pt(0), pt(0))
        elif len(margin) == 6:
            pass
        else:
            raise ValueError
        # Conversion to units is done by the properties
        self.mt, self.mr, self.mb, self.ml, self.mzf, self.mzb = margin
    margin = property(_get_margin, _set_margin)

    def _get_margin3D(self):
        """Tuple of margin in CSS order + (front, back), direction of clock

        >>> from pagebot.toolbox.units import perc, ru, rv
        >>> e = Element(margin=(10, 20, 30, 40))
        >>> e.mt, e.mr, e.mb, e.ml
        (10pt, 20pt, 30pt, 40pt)
        >>> e.ml = 123
        >>> e.margin3D
        (10pt, 20pt, 30pt, 123pt, 0pt, 0pt)
        >>> e.margin3D = 11
        >>> e.margin3D
        (11pt, 11pt, 11pt, 11pt, 11pt, 11pt)
        >>> e.margin3D = (11, 22)
        >>> e.margin3D
        (11pt, 22pt, 11pt, 22pt, 11pt, 22pt)
        >>> e.margin3D = (11, 22, 33)
        >>> e.margin3D
        (11pt, 22pt, 33pt, 11pt, 22pt, 33pt)
        >>> e.margin3D = (11, 22, 33, 44)
        >>> e.margin3D
        (11pt, 22pt, 33pt, 44pt, 0pt, 0pt)
        >>> e.margin3D = (11, 22, 33, 44, 55, 66)
        >>> e.margin3D
        (11pt, 22pt, 33pt, 44pt, 55pt, 66pt)
        >>> e.w = e.h = e.d = 500
        >>> e.margin3D = '10%'
        >>> e.margin3D, ru(e.margin3D), rv(e.margin3D)
        ((10%, 10%, 10%, 10%, 10%, 10%), (50pt, 50pt, 50pt, 50pt, 50pt, 50pt), (50, 50, 50, 50, 50, 50))
        >>> e.margin3D = perc(15)
        >>> e.margin3D, ru(e.margin3D), rv(e.margin3D)
        ((15%, 15%, 15%, 15%, 15%, 15%), (75pt, 75pt, 75pt, 75pt, 75pt, 75pt), (75, 75, 75, 75, 75, 75))
        """
        return self.mt, self.mr, self.mb, self.ml, self.mzf, self.mzb
    margin3D = property(_get_margin3D, _set_margin)

    def _get_mt(self):
        """Margin top property. Relative unit values refer to self.h.

        >>> e = Element(mt=12)
        >>> e.mt
        12pt
        >>> e.mt = 13
        >>> e.mt
        13pt
        >>> e.style = dict(mt=14, h=500)
        >>> e.mt
        14pt
        >>> e.mt = '10%'
        >>> e.mt
        10%
        >>> e.mt.pt
        50
        """
        # In case relative units, use this as base.
        base = dict(base=self.h, em=self.em)
        return units(self.css('mt', 0), base=base)

    def _set_mt(self, mt):
        # Overwrite element local style from here, parent css becomes
        # inaccessable.
        self.style['mt'] = units(mt or 0)
    mt = property(_get_mt, _set_mt)

    # Margin bottom
    def _get_mb(self):
        """Margin bottom property. Relative unit values refer to the current
        self.h or self.em.

        >>> e = Element(mb=12)
        >>> e.mb
        12pt
        >>> e.mb.pt
        12
        >>> e.mb = 13
        >>> e.mb
        13pt
        >>> e.style = dict(mb=14, h=500)
        >>> e.mb
        14pt
        >>> e.mb = '10%'
        >>> e.mb
        10%
        >>> e.mb.pt
        50
        """
        base = dict(base=self.h, em=self.em) # In case relative units, use this as base.
        return units(self.css('mb', 0), base=base)
    def _set_mb(self, mb):
        """Precompile as Unit instance from whatever format mb has."""
        self.style['mb'] = units(mb) # Overwrite element local style from here, parent css becomes inaccessable.
    mb = property(_get_mb, _set_mb)

    def _get_ml(self): # Margin left
        """Margin left property. Relative unit values refer to self.w.

        >>> e = Element(ml=12)
        >>> e.ml
        12pt
        >>> e.ml = 13
        >>> e.ml
        13pt
        >>> e.style = dict(ml=14, w=500)
        >>> e.ml
        14pt
        >>> e.ml = '10%'
        >>> e.ml
        10%
        >>> e.ml.pt
        50
        """
        base = dict(base=self.w, em=self.em) # In case relative units, use this as base.
        return units(self.css('ml', 0), base=base)
    def _set_ml(self, ml):
        # Overwrite element local style from here, parent css becomes inaccessable.
        self.style['ml'] = units(ml)
    ml = property(_get_ml, _set_ml)

    def _get_mr(self): # Margin right
        """Margin right property. Relative unit values refer to self.w.

        >>> e = Element(mr=12)
        >>> e.mr
        12pt
        >>> e.mr = 13
        >>> e.mr
        13pt
        >>> e.style = dict(mr=14, w=500)
        >>> e.mr
        14pt
        >>> e.mr = '10%'
        >>> e.mr
        10%
        >>> e.mr.pt
        50
        """
        # In case relative units, use this as base.
        base = dict(base=self.w, em=self.em)
        return units(self.css('mr', 0), base=base)

    def _set_mr(self, mr):
        # Overwrite element local style from here, parent css becomes
        # inaccessable.
        self.style['mr'] = units(mr)
    mr = property(_get_mr, _set_mr)

    def _get_mzf(self): # Margin z-axis front
        """Margin z-axis front property (closest to view point). Relative unit
        values refer to self.d.

        >>> e = Element(mzf=12)
        >>> e.mzf
        12pt
        >>> e.mzf = 13
        >>> e.mzf
        13pt
        >>> e.style = dict(mzf=14, d=500)
        >>> e.mzf
        14pt
        >>> e.mzf = '10%'
        >>> e.mzf
        10%
        >>> e.mzf.pt
        50
        """
        base = dict(base=self.d, em=self.em) # In case relative units, use this as base.
        return units(self.css('mzf', 0), base=base)
    def _set_mzf(self, mzf):
        self.style['mzf'] = units(mzf or 0) # Overwrite element local style from here, parent css becomes inaccessable.
    mzf = property(_get_mzf, _set_mzf)

    def _get_mzb(self): # Margin z-axis back
        """Margin z-axis back property (most distant to view point). Relative
        unit values refer to self.d.

        >>> e = Element(mzb=12)
        >>> e.mzb
        12pt
        >>> e.mzb = 13
        >>> e.mzb
        13pt
        >>> e.style = dict(mzb=14, d=500)
        >>> e.mzb
        14pt
        >>> e.mzb = '10%'
        >>> e.mzb
        10%
        >>> e.mzb.pt
        50
        """
        # In case relative units, use this as base.
        base = dict(base=self.d, em=self.em)
        return units(self.css('mzb', 0), base=base)
    def _set_mzb(self, mzb):
        # Overwrite element local style from here, parent css becomes
        # inaccessable.
        self.style['mzb'] = units(mzb)
    mzb = property(_get_mzb, _set_mzb)

    # Padding properties

    # TODO: Add support of "auto" values, doing live centering.

    def _get_padding(self):
        """Tuple of paddings in CSS order, direction of clock starting on top
        Can be 123, [123], [123, 234], [123, 234, 345], [123, 234, 345, 456]
        or [123, 234, 345, 456, 567, 678]

        >>> from pagebot.toolbox.units import perc, ru, rv
        >>> e = Element(padding=(10, 20, 30, 40))
        >>> e.pt, e.pr, e.pb, e.pl
        (10pt, 20pt, 30pt, 40pt)
        >>> e.pl = 123
        >>> e.padding
        (10pt, 20pt, 30pt, 123pt)
        >>> e.padding = 11
        >>> e.padding
        (11pt, 11pt, 11pt, 11pt)
        >>> e.padding = (11, 22)
        >>> e.padding
        (11pt, 22pt, 11pt, 22pt)
        >>> e.padding = (11, 22, 33)
        >>> e.padding
        (11pt, 22pt, 33pt, 11pt)
        >>> e.padding = (11, 22, 33, 44)
        >>> e.padding
        (11pt, 22pt, 33pt, 44pt)
        >>> e.pt, e.pr, e.pb, e.pl
        (11pt, 22pt, 33pt, 44pt)
        >>> e.padding = (11, 22, 33, 44, 55, 66)
        >>> e.padding
        (11pt, 22pt, 33pt, 44pt)
        >>> e.padding3D
        (11pt, 22pt, 33pt, 44pt, 55pt, 66pt)
        >>> e.w = e.h = e.d = 500
        >>> e.padding = '10%'
        >>> #e.padding, ru(e.padding), rv(e.padding)
        #((10%, 10%, 10%, 10%), (50pt, 50pt, 50pt, 50pt), (50, 50, 50, 50))
        >>> e.padding = perc(15)
        >>> #e.padding, ru(e.padding), rv(e.padding)
        #((15%, 15%, 15%, 15%), (75pt, 75pt, 75pt, 75pt), (75, 75, 75, 75))
        """
        return self.pt, self.pr, self.pb, self.pl

    def _set_padding(self, padding):
        # Can be 123, [123], [123, 234] or [123, 234, 345, 4565]
        assert padding is not None
        if not isinstance(padding, (list, tuple)):
            padding = [padding]
        if len(padding) == 1: # All same value
            padding = (padding[0], padding[0], padding[0], padding[0], padding[0], padding[0])
        elif len(padding) == 2: # pt == pb, pl == pr, pzf == pzb
            padding = (padding[0], padding[1], padding[0], padding[1], padding[0], padding[1])
        elif len(padding) == 3: # pt == pl == pzf, pb == pr == pzb
            padding = (padding[0], padding[1], padding[2], padding[0], padding[1], padding[2])
        elif len(padding) == 4: # pt, pr, pb, pl, pt(0), pt(0)
            padding = (padding[0], padding[1], padding[2], padding[3], pt(0), pt(0))
        elif len(padding) == 6:
            pass
        else:
            raise ValueError
        # Conversion to units is done in the properties.
        self.pt, self.pr, self.pb, self.pl, self.pzf, self.pzb = padding

    padding = property(_get_padding, _set_padding)

    def _get_padding3D(self):
        """Tuple of padding in CSS order + (front, back), direction of clock

        >>> from pagebot.toolbox.units import perc, ru, rv
        >>> e = Element(padding=(10, 20, 30, 40))
        >>> e.pt, e.pr, e.pb, e.pl
        (10pt, 20pt, 30pt, 40pt)
        >>> e.pl = 123
        >>> e.padding3D
        (10pt, 20pt, 30pt, 123pt, 0pt, 0pt)
        >>> e.padding3D = 11
        >>> e.padding3D
        (11pt, 11pt, 11pt, 11pt, 11pt, 11pt)
        >>> e.padding3D = (11, 22)
        >>> e.padding3D
        (11pt, 22pt, 11pt, 22pt, 11pt, 22pt)
        >>> e.padding3D = (11, 22, 33)
        >>> e.padding3D
        (11pt, 22pt, 33pt, 11pt, 22pt, 33pt)
        >>> e.padding3D = (11, 22, 33, 44)
        >>> e.padding3D
        (11pt, 22pt, 33pt, 44pt, 0pt, 0pt)
        >>> e.padding3D = (11, 22, 33, 44, 55, 66)
        >>> e.padding3D
        (11pt, 22pt, 33pt, 44pt, 55pt, 66pt)
        >>> e.w = e.h = e.d = 500
        >>> e.padding3D = '10%'
        >>> #e.padding3D, ru(e.padding3D), rv(e.padding3D)
        #((10%, 10%, 10%, 10%, 10%, 10%), (50pt, 50pt, 50pt, 50pt, 50pt, 50pt), (50, 50, 50, 50, 50, 50))
        >>> e.padding3D = perc(15)
        >>> #e.padding3D, ru(e.padding3D), rv(e.padding3D)
        #((15%, 15%, 15%, 15%, 15%, 15%), (75pt, 75pt, 75pt, 75pt, 75pt, 75pt), (75, 75, 75, 75, 75, 75))
        """
        return self.pt, self.pr, self.pb, self.pl, self.pzf, self.pzb
    padding3D = property(_get_padding3D, _set_padding)

    def _get_pt(self):
        """Padding top property. Relative unit values refer to self.h.

        NOTE that in usage, the "pt" is abbreviation for padding-top, not
        point units.

        >>> e = Element(pt=12, h=500)
        >>> e.pt
        12pt
        >>> # Default conversion from numberts to points
        >>> e.pt = 13
        >>> e.pt
        13pt
        >>> e.pt = pt(14)
        >>> e.pt
        14pt
        >>> # Verify that other padding did not change.
        >>> e.padding
        (14pt, 0pt, 0pt, 0pt)
        >>> e.pt = '10%'
        >>> # e.pt is abbreviation for padding-top. .pt is the property that converts to points.
        >>> #e.pt, e.pt.pt
        #(10%, 50)
        """
        # Copy from self.h --> self._get_h to avoid circular reference to self.h
        # in case _get_h is redefined by inheriting classes (such as Text)
        #base = dict(base=self.parentH, em=self.em)
        h = units(self.css('h', 0))#, base=base)
        #base = dict(base=h, em=self.em) # In case relative units, use this as base.
        return units(self.css('pt', 0))#, base=base)
    def _set_pt(self, pt):
        self.style['pt'] = units(pt or 0)  # Overwrite element local style from here, parent css becomes inaccessable.
    pt = property(_get_pt, _set_pt)

    def _get_pb(self): # Padding bottom
        """Padding bottom property. Relative unit values refer to self.h.

        >>> e = Element(padding=(10, 20, 30, 40))
        >>> e.pb
        30pt
        >>> e = Element(pb=12, h=500)
        >>> e.pb
        12pt
        >>> e.pb = 13
        >>> e.pb
        13pt
        >>> e.pb = pt(14)
        >>> e.pb
        14pt
        >>> e.pt, e.pr, e.pb, e.pl # Make sure other did not change.
        (0pt, 0pt, 14pt, 0pt)
        >>> e.padding
        (0pt, 0pt, 14pt, 0pt)
        >>> e.pb = '10%'
        >>> e.pb
        10%
        >>> #e.pb.pt # 10% of base 500pt
        #50
        """
        # Copy from self.h --> self._get_h to avoid circular reference to self.h
        # in case _get_h is redefined by inheriting classes (such as Text)
        #base = dict(base=self.parentH, em=self.em)
        h = units(self.css('h', 0))#, base=base)
        #base = dict(base=h, em=self.em) # In case relative units, use this as base.
        return units(self.css('pb', 0))#, base=base)
    def _set_pb(self, pb):
        self.style['pb'] = units(pb or 0) # Overwrite element local style from here, parent css becomes inaccessable.
    pb = property(_get_pb, _set_pb)

    def _get_pl(self):
        """Padding left property. Relative unit values refer to self.w.

        >>> e1 = Element(w=660)
        >>> e2 = Element(padding=(10, 20, 30, 40), parent=e1)
        >>> e2.pl
        40pt
        >>> e2 = Element(pl=12, parent=e1)
        >>> e2.pl
        12pt
        >>> e2.pl = 13
        >>> e2.pl
        13pt
        >>> e2.padding # Make sure other did not change.
        (0pt, 0pt, 0pt, 13pt)
        >>> e2.pl = '10%' # Relating Unit instance
        >>> e2.pl, e2.pl.pt
        (10%, 10)
        """
        #base = dict(base=self.w, em=self.em) # In case relative units, use this as base.
        return units(self.css('pl', 0))#, base=base)
    def _set_pl(self, pl):
        self.style['pl'] = units(pl or 0) # Overwrite element local style from here, parent css becomes inaccessable.
    pl = property(_get_pl, _set_pl)

    def _get_pr(self): # Margin right
        """Padding right property. Relative unit values refer to self.w.

        >>> e = Element(padding=(10, 20, 30, 40))
        >>> e.pr
        20pt
        >>> e = Element(pr=12)
        >>> e.pr
        12pt
        >>> e.pr = 13
        >>> e.pr
        13pt
        >>> e.style = dict(pr=14, w=500)
        >>> e.pr
        14pt
        >>> e.pt, e.pr, e.pb, e.pl # Make sure others did not change.
        (0pt, 14pt, 0pt, 0pt)
        >>> e.padding # Make sure other did not change.
        (0pt, 14pt, 0pt, 0pt)
        >>> e.pr = '10%'
        >>> e.pr # Padding right as Unit instance
        10%
        >>> #e.pr.pt # Get padding-right, cast to points
        #50
        """
        #base = dict(base=self.w, em=self.em) # In case relative units, use this as base.
        return units(self.css('pr', 0))#, base=base)
    def _set_pr(self, pr):
        self.style['pr'] = units(pr or 0)
    pr = property(_get_pr, _set_pr)

    def _get_pzf(self):
        """Padding z-axis front property. Relative unit values refer to self.d.

        >>> e1 = Element(d=300)
        >>> e2 = Element(pzf=12, parent=e1)
        >>> e2.pzf
        12pt
        >>> e2.pzf = 13
        >>> e2.pzf
        13pt
        >>> e2.pzf = 14
        >>> e2.d = 500
        >>> e2.pzf
        14pt
        >>> e2.padding3D # Make sure other did not change.
        (0pt, 0pt, 0pt, 0pt, 14pt, 0pt)
        >>> e2.pzf = '10%'
        >>> e2.pzf
        10%
        >>> #e2.pzf.pt # Padding-front, cast to point
        #50
        """
        #base = dict(base=self.d, em=self.em) # In case relative units, use this as base.
        return units(self.css('pzf', 0))#, base=base)
    def _set_pzf(self, pzf): # padding z-axis front
        self.style['pzf'] = units(pzf or 0) # Overwrite element local style from here, parent css becomes inaccessable.
    pzf = property(_get_pzf, _set_pzf)

    def _get_pzb(self):
        """Padding z-axis back property. Relative unit values refer to self.d.

        >>> e1 = Element(d=300)
        >>> e2 = Element(pzb=12, parent=e1)
        >>> e2.pzb
        12pt
        >>> e2.pzb = 13
        >>> e2.pzb
        13pt
        >>> e2.pzb, e2.d
        (13pt, 100pt)
        >>> e2.pzb=14
        >>> e2.d = 500
        >>> e2.pzb, e2.d
        (14pt, 500pt)
        >>> e2.padding3D # Make sure other did not change.
        (0pt, 0pt, 0pt, 0pt, 0pt, 14pt)
        >>> e2.pzb = '10%'
        >>> e2.pzb #, e2.pzb.base
        10%
        >>> #e2.pzb.pt
        #50
        """
        #base = dict(base=self.d, em=self.em) # In case relative units, use this as base.
        return units(self.css('pzb', 0))#, base=base)
    def _set_pzb(self, pzb):
        self.style['pzb'] = units(pzb or 0) # Overwrite element local style from here, parent css becomes inaccessable.
    pzb = property(_get_pzb, _set_pzb)

    def _get_pw(self):
        """Padded width (space between the horizontal paddings) read-only
        property of the element block.

        >>> e = Element(w=400, pl=22, pr=33)
        >>> e.pw
        345pt
        >>> e.pl = e.pr = '10%'
        >>> #e.pl, e.pl.pt, e.pr, e.pr.pt
        #(10%, 40, 10%, 40)
        >>> #e.pw
        #320pt
        """
        return self.w - self.pl - self.pr

    pw = property(_get_pw)

    def _get_ph(self):
        """Padded height (space between the vertical paddings) read-only
        property of the element block.

        >>> e = Element(h=400, pb=22, pt=33)
        >>> e.ph
        345pt
        >>> e.pb = e.pt = '10%'
        >>> #e.pb, e.pb.pt, e.pt, e.pt.pt # e.pt is Abbreviation of padding-top, .pt is points
        #(10%, 40, 10%, 40)
        >>> #e.ph
        #320pt
        """
        return self.h - self.pb - self.pt
    ph = property(_get_ph)

    def _get_pd(self):
        """Padded depth read-only property of the element block. Answers the
        distance between depth padding.

        >>> e = Element(d=400, pzf=22, pzb=33)
        >>> e.pd
        345pt
        >>> e.pzf = e.pzb = '10%'
        >>> #e.pzf, e.pzf.pt, e.pzb, e.pzb.pt
        #(10%, 40, 10%, 40)
        >>> #e.pd
        #320pt
        """
        return self.d - self.pzf - self.pzb
    pd = property(_get_pd)

    def _get_radius(self):
        """Property answers the element generic radius value. It is up to specific
        types of elements to decide that “radius” is used for. It can be the rounding
        of corners or the radius of a circle node in a network drawing."""
        return self.css('radius')
    def _set_radius(self, radius):
        self.style['radius'] = radius # Overwrite as local value.
    radius = property(_get_radius, _set_radius)

    def _get_frameDuration(self):
        """Property answers the element frameDuration parameters, used for speed
        when exporting animated gifs. Normally only set in page or document."""
        return self.css('frameDuration')
    def _set_frameDuration(self, frameDuration):
        self.style['frameDuration'] = frameDuration # Overwrite as local value.
    frameDuration = property(_get_frameDuration, _set_frameDuration)

    def _get_size(self):
        """Set the size of the element by calling by properties self.w and self.h.
        If set, then overwrite access from style width and height. self.d is optional attribute.
        Setting size this way, temporarily disables the self.proportional flag.

        >>> e = Element()
        >>> e.size = 101, 202, 303
        >>> e.w, e.h, e.d
        (101pt, 202pt, 303pt)
        >>> e.size
        (101pt, 202pt)
        >>> e.size3D
        (101pt, 202pt, 303pt)
        >>> e.size = 101 # Set all w, h, d to the same value.
        >>> e.size3D
        (101pt, 101pt, 101pt)
        >>> e.size = 660, 201 # e.d is untouched.
        >>> e.size3D
        (660pt, 201pt, 101pt)
        >>> child = Element(parent=e)
        >>> child.size = '20%', '75%'
        >>> child.w, child.h, child.d
        (20%, 75%, 100pt)
        >>> child.size3D
        (20%, 75%, 100pt)
        >>> child.size
        (20%, 75%)
        >>> #child.w.pt, child.size[0].pt # Render to pt by 20% of parent.w --> 0.2 * 660 = 132
        #(132, 132)
        """
        return self.w, self.h

    def _set_size(self, size):
        # Disable the flag, we want to set the values independently
        saveFlag = self.proportional
        self.proportional = False
        if isinstance(size, (tuple, list)):
            assert len(size) in (2,3)
            if len(size) == 2:
                self.w, self.h = size # Don't touch self.d
            else:
                self.w, self.h, self.d = size
        else:
            self.w = self.h = self.d = size
        self.proportional = saveFlag

    size = property(_get_size, _set_size)

    def _get_size3D(self):
        return self.w, self.h, self.d

    # Setting is idential for self.size3D and self.size
    size3D = property(_get_size3D, _set_size)

    #   S H A D O W   &  G R A D I E N T

    def _get_shadow(self):
        """Answers the Shadow instance of self.

        >>> from pagebot.gradient import Shadow
        >>> e = Element()
        >>> e.shadow = Shadow(offset=pt(6, -6), blur=pt(6), color=0)
        >>> e.shadow
        <Shadow offset=(6pt, -6pt) blur=6pt Color(r=0, g=0, b=0)>
        """
        return self.css('shadow')
    def _set_shadow(self, shadow):
        assert shadow is None or isinstance(shadow, self.SHADOW_CLASS)
        self.style['shadow'] = shadow
    shadow = property(_get_shadow, _set_shadow)

    def _get_textShadow(self):
        return self.css('textShadow')
    def _set_textShadow(self, textShadow):
        assert textShadow is None or isinstance(textShadow, self.SHADOW_CLASS)
        self.style['textShadow'] = textShadow
    textShadow = property(_get_textShadow, _set_textShadow)

    def _get_gradient(self):
        return self.css('gradient')
    def _set_gradient(self, gradient):
        assert gradient is None or isinstance(gradient, self.GRADIENT_CLASS)
        self.style['gradient'] = gradient
    gradient = property(_get_gradient, _set_gradient)

    def _get_textGradient(self):
        return self.css('textGradient')
    def _set_textGradient(self, textGradient):
        assert textGradient is None or isinstance(textGradient, self.GRADIENT_CLASS)
        self.style['textGradient'] = textGradient
    textGradient = property(_get_textGradient, _set_textGradient)

    def _get_box3D(self):
        """Answers the 3D bounding box of self from (self.x, self.y, self.w,
        self.h) properties."""
        return self.x, self.y, self.z, self.w, self.h, self.d
    box3D = property(_get_box3D)

    def _get_box(self):
        """Construct the bounding box from (self.x, self.y, self.w, self.h)
        properties.

        >>> e = Element(x=150, y=150, w=300, h=400)
        >>> e.box
        (150pt, 150pt, 300pt, 400pt)
        >>> e.box = 50, 50, 200, 300
        >>> e.box
        (50pt, 50pt, 200pt, 300pt)
        >>> child = Element(x='10%', y='20%', w='50%', h='40%', parent=e)
        >>> child.box
        (10%, 20%, 50%, 40%)
        """
        return self.x, self.y, self.w, self.h
    def _set_box(self, box):
        self.x, self.y, self.w, self.h = box
    box = property(_get_box, _set_box)

    def _get_marginBox(self):
        """Calculate the margin position and margin resized box of the element,
        after applying the option style margin.

        >>> from pagebot.toolbox.units import ru
        >>> e = Element(w=500, h=500)
        >>> e.margin = 10
        >>> e.marginBox
        (-10pt, -10pt, 520pt, 520pt)
        >>> ru(e.marginBox)
        (-10pt, -10pt, 520pt, 520pt)
        >>> rv(e.marginBox)
        (-10, -10, 520, 520)
        >>> e.margin = '10%'
        >>> e.marginBox
        (-50pt, -50pt, 600pt, 600pt)
        >>> ru(e.marginBox)
        (-50pt, -50pt, 600pt, 600pt)
        >>> rv(e.marginBox)
        (-50, -50, 600, 600)
        """
        mt = self.mt
        mb = self.mb
        ml = self.ml
        y = self.y - mb
        return (self.x - ml, y, self.w + ml + self.mr, self.h + mt + mb)
    marginBox = property(_get_marginBox)

    def _get_paddedBox(self):
        """Calculate the padded position and padded resized box of the element,
        after applying the style padding. Answered format (x, y, w, h).

        >>> from pagebot.toolbox.units import ru
        >>> e = Element(w=500, h=500)
        >>> e.padding = 10
        >>> e.paddedBox
        ((10pt, 10pt), (480pt, 480pt))
        >>> e.padding = '10%'
        >>> e.padding
        (10%, 10%, 10%, 10%)
        >>> #e.paddedBox
        #((50pt, 50pt), (400pt, 400pt))
        >>> #ru(e.paddedBox)
        #((50pt, 50pt), (400pt, 400pt))
        >>> #rv(e.paddedBox)
        #((50, 50), (400, 400))
        """
        pl = self.pl
        pt = self.pt # pt is abbreviation from padding-top here, not points.
        pb = self.pb
        y = self.y + pb
        return (self.x + pl, y), (self.w - pl - self.pr, self.h - pt - pb)
    paddedBox = property(_get_paddedBox)

    def _get_paddedBox3D(self):
        """Calculate the padded position and padded resized box in 3D of the
        lement, after applying the style padding. Answered format (x, y, z, w,
        h, d).

        >>> from pagebot.toolbox.units import ru
        >>> e = Element(w=500, h=500, d=500)
        >>> e.padding3D = 10
        >>> e.paddedBox3D
        ((10pt, 10pt, 10pt), (480pt, 480pt, 480pt))
        >>> ru(e.paddedBox3D)
        ((10pt, 10pt, 10pt), (480pt, 480pt, 480pt))
        >>> rv(e.paddedBox3D)
        ((10, 10, 10), (480, 480, 480))
        >>> e.padding3D = '10%'
        >>> e.padding3D
        (10%, 10%, 10%, 10%, 10%, 10%)
        >>> #e.paddedBox3D
        #((50pt, 50pt, 50pt), (400pt, 400pt, 400pt))
        >>> #ru(e.paddedBox3D)
        #((50pt, 50pt, 50pt), (400pt, 400pt, 400pt))
        >>> #rv(e.paddedBox3D)
        #((50, 50, 50), (400, 400, 400))
        """
        (x, y), (w, h) = self.paddedBox
        pzf = self.pzf
        return (x, y, self.z + pzf), (w, h, self.d - pzf - self.pzb)
    paddedBox3D = property(_get_paddedBox3D)

    # PDF naming: MediaBox is highlighted with a magenta rectangle, the BleedBox with a cyan
    # one while dark blue is used for the TrimBox.
    # https://www.prepressure.com/pdf/basics/page-boxes

    # "Box" is bounding box on a single element.
    # "Block" is here used as bounding box of a group of elements
    # or otherwise the wrapped bounding box on self.

    def _get_block3D(self):
        """Answers the vacuum 3D bounding box around all child elements,
        including margin, relative to (self.x, self.y)

        >>> e1 = Element(x=10, y=52, z=14, w=100, h=110, d=801)
        >>> e2 = Element(x=50, y=12, z=54, w=200, h=210, d=401)
        >>> e3 = Element(x=70, y=72, z=74, w=300, h=310, d=101)
        >>> e1.w, e1.h
        (100pt, 110pt)
        >>> e = Element(elements=[e1, e2, e3])
        >>> #FIX e1.left, e1.right
        (10pt, 110pt)
        >>> #FIX e.block3D
        (10pt, 12pt, 14pt, 0, 0, 0)
        """
        x1 = y1 = z1 = XXXL
        x2 = y2 = z2 = -XXXL
        if not self.elements:
            # No element, answers vacuum block (x, y, z), (w, h, d)
            return pt(0, 0, 0), pt(0, 0, 0)
        for e in self.elements:
            x1 = min(x1, e.left)
            x2 = max(x2, e.right)
            y1 = min(y1, e.mBottom)
            y2 = max(y2, e.mTop)
            z1 = min(z1, e.front)
            z2 = max(z2, e.back)

        return (x1, y1, z1), (x2 - x1, y2 - y1, z2 - z1)
    block3D = property(_get_block3D)

    def _get_block(self):
        """Answers the vacuum bounding box around all child elements in 2D,
        including margin.

        >>> e1 = Element(x=10, y=10, w=100, h=100)
        >>> e2 = Element(x=50, y=50, w=200, h=100)
        >>> e3 = Element(x=70, y=30, w=801, h=10)
        >>> e = Element(elements=[e1, e2, e3])
        >>> #e.block
        (10, 10, 871, 150)
        """
        x, y, _, w, h, _ = self._get_block3D()
        return x, y, w, h
    block = property(_get_block)

    def _get_paddedBlock3D(self):
        """Answers the vacuum 3D bounding box around all child elements,
        subtracting their paddings. Sizes cannot become nextive."""
        x1 = y1 = z1 = XXXL
        x2 = y2 = z2 = -XXXL
        if not self.elements:
            # No element, answers vacuum block (x, y, z), (w, h, d)
            return pt(0, 0, 0), pt(0, 0, 0)
        for e in self.elements:
            x1 = max(x1, e.left + e.pl)
            x2 = min(x2, e.right - e.pl)
            y1 = max(y1, e.bottom + e.pb)
            y2 = min(y2, e.top - e.pt)
            z1 = max(z1, e.front + e.zpf)
            z2 = min(z2, e.back - e.zpb)

        # Make sure that the values cannot overlap.
        if x2 < x1: # If overlap
            x1 = x2 = (x1 + x2)/2 # Middle the x position
        if y2 < y1: # If overlap
            y1 = y2 = (y1 + y2)/2 # Middle the y position
        if z2 < z1: # If overlap
            z1 = z2 = (z1 + z2)/2 # Middle the z position
        return (x1, y1, z1), (x2 - x1, y2 - y1, z2 - z1)
    paddedBlock3D = property(_get_paddedBlock3D)

    def _get_paddedBlock(self):
        """Answers the vacuum bounding box around all child elements in 2D"""
        (x, y, _), (w, h, _) = self._get_paddedBlock3D()
        return (x, y), (w, h)
    paddedBlock = property(_get_paddedBlock)

    def _get_originsBlock3D(self):
        """Answers (minX, minY, maxX, maxY, minZ, maxZ) for all element origins."""
        minX = minY = minZ = XXXL
        maxX = maxY = maxZ = -XXXL
        for e in self.elements:
            minX = min(minX, e.x)
            maxX = max(maxX, e.x)
            minY = min(minY, e.y)
            maxY = max(maxY, e.y)
            minZ = min(minZ, e.z)
            maxZ = max(maxZ, e.z)
        return (minX, minY, minZ), (maxX, maxY, maxZ)
    originsBlock3D = property(_get_originsBlock3D)

    def _get_originsBlock(self):
        minX, minY, _, maxX, maxY, _ = self._get_originsBlock3D()
        return (minX, minY), (maxX, maxY)
    originsBlock = property(_get_originsBlock)

    # Scale

    def _get_scaleX(self):
        """Get/set the scale from the style. If the self.proportional flag is set,
        then also alter the other scales propotionally.

        >>> e = Element(scaleX=0.5, proportional=True)
        >>> e.scaleY, e.scaleZ
        (1, 1)
        >>> e.scaleX = 3
        >>> e.scaleY, e.scaleZ # Keeps proportion
        (6.0, 6.0)
        """
        return self.css('scaleX', 1)
    def _set_scaleX(self, scaleX):
        assert scaleX != 0
        if self.proportional:
            if self.scaleX:
                self.style['scaleY'] = scaleX * self.scaleY/self.scaleX
                self.style['scaleZ'] = scaleX * self.scaleZ/self.scaleX
        self.style['scaleX'] = scaleX # Set on local style, shielding parent self.css value.
    scaleX = property(_get_scaleX, _set_scaleX)

    def _get_scaleY(self):
        """Get/set the scale from the style. If the self.proportional flag is set,
        then also alter the other scales propotionally.

        >>> e = Element(scaleY=0.5, proportional=True)
        >>> e.scaleX, e.scaleZ
        (1, 1)
        >>> e.scaleY = 3
        >>> e.scaleX, e.scaleZ # Keeps proportion
        (6.0, 6.0)
        """
        return self.css('scaleY', 1)
    def _set_scaleY(self, scaleY):
        assert scaleY != 0
        if self.proportional:
            if self.scaleY:
                self.style['scaleX'] = scaleY * self.scaleX/self.scaleY
                self.style['scaleZ'] = scaleY * self.scaleZ/self.scaleY
        self.style['scaleY'] = scaleY # Set on local style, shielding parent self.css value.
    scaleY = property(_get_scaleY, _set_scaleY)

    def _get_scaleZ(self):
        """Get/set the scale from the style. If the self.proportional flag is set,
        then also alter the other scales propotionally.

        >>> e = Element(scaleY=0.5, proportional=True)
        >>> e.scaleX, e.scaleZ
        (1, 1)
        >>> e.scaleY = 3
        >>> e.scaleX, e.scaleZ # Keeps proportion
        (6.0, 6.0)
        """
        return self.css('scaleZ', 1)
    def _set_scaleZ(self, scaleZ):
        assert scaleZ != 0
        if self.proportional:
            if self.scaleZ:
                self.style['scaleX'] = scaleZ * self.scaleX/self.scaleZ
                self.style['scaleY'] = scaleZ * self.scaleY/self.scaleZ
        self.style['scaleZ'] = scaleZ # Set on local style, shielding parent self.css value.
    scaleZ = property(_get_scaleZ, _set_scaleZ)

    def _get_scale(self):
        """Answers the 2-tuple of (self.scaleX, self.scaleY)
        If scale it set this way, self.proportional will reset to False.

        >>> e = Element(scale=2)
        >>> e.scaleX, e.scaleY
        (2, 2)
        >>> e.scale
        (2, 2)
        >>> e.scale = (2, 3, 4)
        >>> e.scale
        (2, 3)
        >>> e.scale3D
        (2, 3, 4)
        >>> e.scaleZ = 5
        >>> e.scale3D
        (2, 3, 5)
        >>> e.scale = 1.5
        >>> e.scale
        (1.5, 1.5)
        >>> e.scale = None
        >>> e.scale
        (1, 1)
        """
        return self.scaleX, self.scaleY
    def _set_scale(self, scale):
        savedFlag = self.proportional # If probably setting to disproportional, save flag
        self.proportional = False # Allow setting of all scales, without changing the others.
        if not scale: # Reset to 1. Scale cannot be 0
            scale = 1
        if not isinstance(scale, (list, tuple)):
            scale = [scale]
        if len(scale) == 1:
            self.scaleX = self.scaleY = self.scaleZ = scale[0]
        elif len(scale) == 2:
            self.scaleX, self.scaleY = scale
            self.scaleZ = 1
        else:
            self.scaleZ, self.scaleY, self.scaleZ = scale[:3]
        self.proportiona = savedFlag # Restore the proportional flag.
    scale = property(_get_scale, _set_scale)

    def _get_scale3D(self):
        return self.scaleX, self.scaleY, self.scaleZ
    scale3D = property(_get_scale3D, _set_scale)

    # Element positions

    def getFloatSideTop(self, previousOnly=True, tolerance=0):
        """Answers the max y that can float to top, without overlapping previous
        sibling elements. This means we are just looking at the vertical
        projection between (self.mLeft, self.mRight). Note that the y may be
        outside the parent box. Only elements with identical z-value are
        compared. Comparison of available space, includes the margins of the
        elements."""
        y = self.parent.h
        for e in self.parent.elements:
            if previousOnly and e is self: # Only look at siblings that are previous in the list.
                break
            if abs(e.z - self.z) > tolerance or e.mRight < self.mLeft or self.mRight < e.mLeft:
                continue # Not equal z-layer or not in window of vertical projection.
            y = min(y, e.mBottom)
        return y

    def getFloatSideBottom(self, previousOnly=True, tolerance=0):
        """Answers the max y that can float to bottom, without overlapping
        previous sibling elements. This means we are just looking at the
        vertical projection of (self.mLeft, self.mRight). Note that the y may
        be outside the parent box. Only elements with identical z-value are
        compared. Comparison of available space, includes the margins of the
        elements."""
        y = 0
        for e in self.parent.elements: # All elements that share self.parent, except self.
            if previousOnly and e is self: # Only look at siblings that are previous in the list.
                break
            if abs(e.z - self.z) > tolerance or e.mRight < self.mLeft or self.mRight < e.mLeft:
                continue # Not equal z-layer or not in window of vertical projection.
            y = max(y, e.mTop)
        return y

    def getFloatSideLeft(self, previousOnly=True, tolerance=0):
        """Answers the max `x` that can float to the left, without overlapping
        previous sibling elements. This means we are just looking at the
        horizontal projection of `(self.mTop, self.mBottom)`. Note that the `x`
        may be outside the parent box. Only elements with identical z-value are
        compared. Comparison of available space, includes the margins of the
        elements."""
        x = 0

        # All elements that share self.parent, except self.
        for e in self.parent.elements:
            # Only look at siblings that are previous in the list.
            if previousOnly and e is self:
                break
            if abs(e.z - self.z) > tolerance:
                continue # Not equal z-layer

            if e.mBottom >= self.mTop or self.mBottom >= e.mTop:
                continue
            x = max(e.mRight, x)
        return x

    def getFloatSideRight(self, previousOnly=True, tolerance=0):
        """Answers the max Y that can float to the right, without overlapping
        previous sibling elements. This means we are just looking at the
        vertical projection of (self.mLeft, self.mRight). Note that the y may
        be outside the parent box. Only elements with identical z-value are
        compared. Comparison of available space, includes the margins of the
        elements."""
        x = self.parent.w
        for e in self.parent.elements: # All elements that share self.parent, except self.
            if previousOnly and e is self: # Only look at siblings that are previous in the list.
                break
            if abs(e.z - self.z) > tolerance:
                continue # Not equal z-layer
            if e.mBottom >= self.mTop or self.mBottom >= e.mTop:
                continue
            x = min(e.mLeft, x)
        return x

    # Private alignment, scale and rotation functions.

    def _applyAlignment(self, p):
        """Answers point `p` according to the alignment status in the css.

        TODO: handle other text alignments.
        """
        px, py, pz = point3D(p)

        # Horizontal.
        xAlign = self.xAlign

        if xAlign == CENTER:
            px -= self.w / 2 / self.scaleX
        elif xAlign == RIGHT:
            px -= self.w / self.scaleX

        # Vertical.
        yAlign = self.yAlign

        if yAlign == MIDDLE:
            py -= self.h / 2 / self.scaleY
        elif yAlign == TOP:
            py -= self.h / self.scaleY

        # Currently no alignment in z-axis implemented
        return px, py, pz

    def _applyRotation(self, view, p):
        """Apply the rotation for angle, where (mx, my) is the rotation center."""
        if self.angle:
            px, py, _ = point3D(p)
            self.view.context.rotate(self.angle, center=(px+self.rx, py+self.ry))

    def _restoreRotation(self, view, p):
        """Reset graphics state from rotation mode."""
        if self.angle:
            px, py, _ = point3D(p)
            self.view.context.rotate(-self.angle, center=(px+self.rx, py+self.ry))

    def _applyScale(self, view, p):
        """Internal method to apply the scale, if both *self.scaleX* and
        *self.scaleY* are set. Use this method paired with
        self._restoreScale(). The (x, y) answered as reversed scaled tuple, so
        drawing elements can still draw on "real size", while the other element
        is in scaled mode."""
        sx = self.scaleX
        sy = self.scaleY
        sz = self.scaleZ
        p = point3D(p)

        # Make sure these are value scale values.
        if sx and sy and sz and (sx != 1 or sy != 1 or sz != 1):
            self.view.context.save()
            view.scale = sx, sy
            # Scale point in 3 dimensions.
            p = (p[0] / sx, p[1] / sy, p[2] / sz)
        return p

    def _restoreScale(self, view):
        """Reset graphics state from svaed scale mode. Make sure to match the
        call of self._applyScale. If one of (self.scaleX, self.scaleY,
        self.scaleZ) is not 0 or 1, then do the restore."""
        sx = self.scaleX
        sy = self.scaleY
        sz = self.scaleZ
        # Make sure these are value scale values.
        if sx and sy and sz and (sx != 1 or sy != 1 or sz != 1):
            self.view.context.restore()

    #   S P E L L  C H E C K

    def _spellCheckWords(self, languages, unknown, minLength):
        """Spellcheck the words of self. Default behavior is to do nothing.
        Inheriting classes can redefined this method.
        """

    def spellCheck(self, languages=None, unknown=None, minLength=3):
        """Recursively spellchecks all child elements for the given languages.
        Answers a list with unknown words. Default is to do nothing and just
        pass the call on to child elements. Inheriting classes can redefine
        _spellCheckWords to check on their on text content. Words with a
        length smaller than minLength are skipped."""
        if unknown is None:
            unknown = []
        if isinstance(languages, str):
            languages = [languages]
        elif languages is None:
            languages = [self.language or DEFAULT_LANGUAGE]
        self._spellCheckWords(languages, unknown, minLength)
        for e in self.elements:
            e.spellCheck(languages, unknown, minLength)
        return unknown

    #   C O M P O S I T I O N  S U P P O R T

    def compose(self, doc, publication):
        """Recursively composes Publication, Pages and Elements to build the
        document of a publication. Default behavior is to just pass it on to
        the chidren."""
        for e in self.elements:
            e.compose(doc, publication)

    def evaluate(self, score=None):
        """Evaluates the content of element `e` with all the conditions."""
        if score is None:
            score = Score()

        # Can be None or empty.
        if self.conditions:
            # Skip in case there are no conditions in the style.
            for condition in self.conditions:
             condition.evaluate(self, score)

        # Also works if showing element is not a container.
        for e in self.elements:
            if e.show:
                e.evaluate(score)

        return score

    def solve(self, score=None):
        """Evaluates the content of element e with the all the conditions. The
        view is passed as an argument because it (or its builder) may be needed
        to solve specific text conditions, such as the run length of text and
        overflow of text boxes."""
        if score is None:
            score = Score()

        # Can be None or empty list. Skip in case there are no conditions in
        # the style.
        if self.conditions:
            for condition in self.conditions:
                condition.solve(self, score)

        else:
            # Also works if showing element is not a container.
            for e in self.elements:
                if e.show:
                    e.solve(score)

        return score

    def _get_viewFrameStrokeWidth(self):
        """Answers local setting of frame stroke width, used if self.showFrame
        is True. Note that this is independent from the element border
        showing."""
        return self.style.get('viewFrameStrokeWidth') # Not inherited
    def _set_viewFrameStrokeWidth(self, strokeWidth):
        self.style['viewFrameStrokeWidth'] = strokeWidth
    viewFrameStrokeWidth = property(_get_viewFrameStrokeWidth, _set_viewFrameStrokeWidth)

    def _get_viewPaddingStroke(self):
        """Answers local setting of padding stroke color, used if
        self.showPadding is True."""
        return self.style.get('viewPaddingStroke') # Not inherited

    def _set_viewPaddingStroke(self, stroke):
        self.style['viewPaddingStroke'] = stroke

    viewPaddingStroke = property(_get_viewPaddingStroke, _set_viewPaddingStroke)

    def _get_viewPaddingStrokeWidth(self):
        """Answers local setting of padding stroke width, used if
        self.showFrame is True."""
        return self.style.get('viewPaddingStrokeWidth') # Not inherited

    def _set_viewPaddingStrokeWidth(self, strokeWidth):
        self.style['viewPaddingStrokeWidth'] = strokeWidth
    viewPaddingStrokeWidth = property(_get_viewPaddingStrokeWidth, _set_viewPaddingStrokeWidth)

    def _get_viewMarginStroke(self):
        """Answers local setting of margin stroke color, used if
        self.showMargin is True."""
        return self.style.get('viewMarginStroke') # Not inherited

    def _set_viewMarginStroke(self, stroke):
        self.style['viewMarginStroke'] = stroke

    viewMarginStroke = property(_get_viewMarginStroke, _set_viewMarginStroke)

    def _get_viewMarginStrokeWidth(self):
        """Answers local setting of margin stroke width, used if
        self.showMargin is True."""
        return self.style.get('viewMarginStrokeWidth') # Not inherited

    def _set_viewMarginStrokeWidth(self, strokeWidth):
        self.style['viewMarginStrokeWidth'] = strokeWidth
    viewMarginStrokeWidth = property(_get_viewMarginStrokeWidth, _set_viewMarginStrokeWidth)

    #   CSS flags

    def _get_cssVerbose(self):
        """Boolean value. If True, adds information comments with original
        values to CSS export."""
        return self.css('cssVerbose', False) # Inherited

    def _set_cssVerbosee(self, cssVerbose):
        self.style['cssVerbose'] = bool(cssVerbose)

    cssVerbose = property(_get_cssVerbose, _set_cssVerbosee)

    #   Exporting

    def _get_saveUrlAsDirectory(self):
        """Boolean value. Flag to turn off saving self.url pages as directory.
        Instead, all "/" is replaced by "-". This choice is made for exprot
        .html paths, where a flat directory is less of a problem than adjusting
        all relative urls for images/CSS/JS"""
        return self.css('saveUrlAsDirectory', False) # Inherited

    def _set_saveUrlAsDirectory(self, saveUrlAsDirectory):
        self.style['saveUrlAsDirectory'] = saveUrlAsDirectory

    saveUrlAsDirectory = property(_get_saveUrlAsDirectory, _set_saveUrlAsDirectory)

    def _get_doExport(self):
        """Boolean value. Flag to turn off any export, for view, e.g. in case
        of testing with docTest."""
        return self.css('doExport', False)

    def _set_doExport(self, doExport):
        self.style['doExport'] = bool(doExport)
    doExport = property(_get_doExport, _set_doExport)

    # Apply template.

    def applyTemplate(self, template, elements=None):
        """Copy relevant info from template: w, h, elements, style, conditions
        when element is created. Don't call later.

        >>> from pagebot.toolbox.units import mm, pt
        >>> from pagebot.elements.template import Template
        >>> e = Element(name='TestElement')
        >>> t = Template(xy=pt(11, 12), size=(100, mm(200)))
        >>> e.applyTemplate(t)
        >>> e.x, e.y, e.w, e.h
        (11pt, 12pt, 100pt, 200mm)
        """
        # Set template value by property call, copying all template elements
        # and attributes.
        self.template = template

        if elements is not None:
            # Add optional list of additional elements.
            for e in elements or []:
                # Add cross reference searching for eId of elements.
                self.appendElement(e)

    def _get_template(self):
        """Property get/set for e.template.

        >>> from pagebot.elements.template import Template
        >>> e = Element(name='TestElement')
        >>> t = Template(name='MyTemplate', x=11, y=12, w=100, h=200)
        >>> e.applyTemplate(t)
        >>> e.template
        <Template>
        """
        return self._template

    def _set_template(self, template):
        # Clear all existing child elements in self.
        self.clearElements()
        # Keep template reference to clone pages or if additional template info
        # is needed later.
        self._template = template

        # Copy optional template stuff
        if template is not None:
            # Copy elements from the template and put them in the designated
            # positions.
            self.w = template.w
            self.h = template.h
            self.padding = template.padding
            self.margin = template.margin
            self.prevElement = template.prevElement
            self.nextElement = template.nextElement
            self.nextPage = template.nextPage

            # Copy style items.
            for  name, value in template.style.items():
                self.style[name] = value

            # Copy condition list. Does not have to be deepCopy, condition
            # instances are multi-purpose.
            self.conditions = copy.copy(template.conditions)

            for e in template.elements:
                self.appendElement(e.copy(parent=self))

    template = property(_get_template, _set_template)
if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
