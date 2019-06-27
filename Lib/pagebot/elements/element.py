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
from pagebot.constants import (MIDDLE, CENTER, RIGHT, TOP, BOTTOM, LEFT, FRONT,
        BACK, XALIGNS, YALIGNS, ZALIGNS, DEFAULT_FONT_SIZE, DEFAULT_WIDTH,
        DEFAULT_HEIGHT, DEFAULT_DEPTH, XXXL, DEFAULT_LANGUAGE, ONLINE, INLINE,
        DEFAULT_RESOLUTION_FACTORS, OUTLINE, GRID_OPTIONS, BASE_OPTIONS,
        DEFAULT_GRID, DEFAULT_BASELINE, DEFAULT_COLOR_BARS,
        DEFAULT_REGISTRATIONMARKS, DEFAULT_CROPMARKS,
        DEFAULT_BASELINE_COLOR, DEFAULT_BASELINE_WIDTH,
        DEFAULT_MININFOPADDING, VIEW_PRINT, VIEW_PRINT2, VIEW_DEBUG,
        VIEW_DEBUG2, VIEW_FLOW)
from pagebot import DEFAULT_FONT_PATH
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.elements.paths.pagebotpath import PageBotPath # PageBot generic equivalent of DrawBot.BezierPath
from pagebot.toolbox.units import (units, rv, pt, point3D, pointOffset,
        asFormatted, isUnit, degrees)
from pagebot.toolbox.color import noColor, color, Color, blackColor
from pagebot.toolbox.transformer import uniqueID, asNormalizedJSON
from pagebot.toolbox.timemark import TimeMark
from pagebot.toolbox.dating import now
from pagebot.gradient import Gradient, Shadow

class Element:
    """The base element object."""

    # Initializes the default Element behavior flags. These flags can be
    # overwritten by inheriting classes, or dynamically in instances, e.g.
    # where the settings of TextBox.nextBox and TextBox.nextPage define if a
    # TextBox instance can operate as a flow.
    isText = False
    isTextBox = False
    #isFlow property answers if nextElement or prevElement is defined.
    isPage = False # Set to True by Page-like elements.
    isView = False
    isImage = False

    GRADIENT_CLASS = Gradient
    SHADOW_CLASS = Shadow
    PATH_CLASS = PageBotPath

    def __init__(self, x=0, y=0, z=0, xy=None, xyz=None, w=DEFAULT_WIDTH,
            h=DEFAULT_HEIGHT, d=DEFAULT_DEPTH, size=None, wh=None, whd=None,
            originTop=False,
            left=None, top=None, right=None, bottom=None, sId=None, lib=None,
            t=None, timeMarks=None, parent=None, context=None, name=None,
            cssClass=None, cssId=None, title=None, description=None, theme=None,
            keyWords=None, language=None, style=None, conditions=None,
            solve=False, framePath=None, elements=None, template=None,
            nextElement=None, prevElement=None, nextPage=None, clipPath=None,
            prevPage=None, thumbPath=None, bleed=None, padding=None, pt=0,
            pr=0, pb=0, pl=0, pzf=0, pzb=0, margin=None, mt=0, mr=0, mb=0,
            ml=0, mzf=0, mzb=0, scaleX=1, scaleY=1, scaleZ=1, scale=None,
            borders=None, borderTop=None, borderRight=None, borderBottom=None,
            borderLeft=None, shadow=None, gradient=None, drawBefore=None,
            radius=None, drawAfter=None, htmlCode=None, htmlPaths=None,
            xAlign=None, yAlign=None, zAlign=None, proportional=None,
            showBaselineGrid=None,
            **kwargs):
        """Base initialize function for all Element constructors. Element
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
        >>> e = Element() # Default element has default proportions
        >>> e.x, e.y, e.w, e.h, e.padding, e.margin
        (0pt, 0pt, 100pt, 100pt, (0pt, 0pt, 0pt, 0pt), (0pt, 0pt, 0pt, 0pt))

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.document import Document
        >>> c = DrawBotContext()
        >>> size = pt(300, 400)
        >>> doc = Document(size=size, autoPages=1, padding=30, originTop=False, context=c)
        >>> page = doc[1]
        >>> e = Element(parent=page, x=0, y=20, w=page.w, h=3)
        >>> e.build(doc.getView(), pt(0, 0))
        >>> e.xy
        (0pt, 20pt)
        >>> e.size
        (300pt, 3pt)
        >>> view = doc.getView()
        >>> e.build(view, pt(0, 0))
        """
        """
        >>> from pagebot.contexts.flatcontext import FlatContext
        >>> from pagebot.document import Document
        >>> c = FlatContext()
        >>> size = pt(320, 420)
        >>> doc = Document(size=size, autoPages=1, padding=30, originTop=False, context=c)
        >>> page = doc[1] # First page is left 1
        >>> page.size
        (320pt, 420pt)
        >>> pt(12, 20)
        (12pt, 20pt)
        >>> e = Element(parent=page, xy=pt(12, 20), w=page.w, h=pt(3))
        >>> e.x, e.y, e.xy
        (12pt, 20pt, (12pt, 20pt))
        >>> e.build(doc.getView(), pt(0, 0))

        >>> e.x, e.y, e.xy
        (12pt, 20pt, (12pt, 20pt))
        >>> e.size
        (320pt, 3pt)
        >>> e.size3D
        (320pt, 3pt, 100pt)
        """
        # Optionally set the property for elements that need their own context.
        # Mostly these are only set for views (which are also Elements) If None
        # the property will query parent --> root document --> view.
        self.context = context
        self._parent = None

        # Set the local self._lib, validate it is a dictionary, otherwise create new dict.
        self.lib = lib

        # Guaranteed to be unique. Cannot be set.
        self._eId = uniqueID(self)
        # Optional systen/user/app id, used by external application, such as SketchContext
        self.sId = sId # Can be None. If used self.findBysid(sId) works recursively

        # Initialize self._elements and self._eIds.
        self.clearElements()
        self.checkStyleArgs(kwargs)
        self.style = makeStyle(style, **kwargs) # Make default style for t == 0 from args

        # If undefined yAlign and parent has origin on top, then default yAlign to TOP
        self._originTop = originTop # Local value is overwritten if there is a parent defined.
        if yAlign is None and self.originTop: # Property seeks parent-->page.originTop value.
            yAlign = TOP
        self.xAlign = xAlign
        self.yAlign = yAlign
        self.zAlign = zAlign

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
            self.xy = xy # self.z is set to DEFAULT_DEPTH
        else:
            self.xyz = x, y, z

        if whd is not None: # Alternative attributes, to make it intuitive for the caller.
            size = whd
        elif wh is not None:
            size = wh
        if size is not None: # Convenience attribute, setting self.w, self.h, self.d
            self.size = size # Works for (w, h) and (w, h, d)
        else: # Otherwise it is assumed that the values are set separately, still default if None.
            self.w = w
            self.h = h
            self.d = d

        if scale is not None: # Convenience attribute, setting self.scaleX, self.scaleY, self.scaleZ
            self.scale = scale # Works for (scaleX, scaleY) and (scaleX, scaleY, scaleZ)
        else:
            self.scaleX = scaleX
            self.scaleY = scaleY
            self.scaleZ = scaleZ

        if proportional is not None: # If defined, set after the sizes and scales are set.
            self.proportional = proportional # Setting True keeps all size and scales proportional now.

        self.padding = padding or (pt, pr, pb, pl, pzf, pzb)
        self.margin = margin or (mt, mr, mb, ml, mzf, mzb)

        if bleed is not None:
            self.bleed = bleed # Property tuple (bt, br, bb, bl) ignores to expand into if None

        # In case these specific position sides are defined, let them overwrite any (x,y)
        # Since top <--> bottom and left <--> right conflict, we only need to test one of them.
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
        # be done by caller.
        # Optional method to draw before child elements are drawn.
        self.drawBefore = drawBefore # Call as: self.drawBefore(e, view)
        # Optional method to draw right after child elements are drawn.
        self.drawAfter = drawAfter # Call as: self.drawAfter(e, view)

        # Shadow and gradient, if defined
        self.shadow = shadow
        self.gradient = gradient
        self.framePath = framePath # Optiona frame path to draw instead of bounding box element rectangle.

        # Set timer of this element.
        # Default TimeMarks from t == now() until arbitrary one day from now().
        """
        t0 = now()
        if timeMarks is None:
            timeMarks = [TimeMark(t0, {}), TimeMark(t0 + days(1), {})]
        self.timeMarks = timeMarks
        if t is None: # Set the current time of this element.
            t = t0
        self.t = t # Initialize self.style from t = 0
        self.timeKeys = INTERPOLATING_TIME_KEYS # List of names of style entries that can interpolate in time.
        """
        self.t = 0
        self.timeMarks = []
        self.timeKeys = []

        if padding is not None:
            self.padding = padding # Expand by property
        if margin is not None:
            self.margin = margin

        # Class and #Id attributes for HtmlContext usage.
        self.cssClass = cssClass # Optional CSS class name. Ignored if None, not to overwrite cssClass of parents.
        self.cssId = cssId # Optional id name for use in CSS-output. Ignored if None.

        # Optional resources that can be included for web output (HtmlContext).
        # Define string or file paths where to read content, instead of
        # constructing by the builder.
        self.htmlCode = htmlCode # Set to string in case element has HTML as source.
        self.htmlPaths = htmlPaths # List or paths, in case full element HTML is defined in files.

        # Generic naming and title.
        self.name = name # Optional name of an element. Used as base for # id in case of HTML/CSS export.
        self.title = title or name # Optional to make difference between title name, style property

        # Element tree
        self._parent = None # Preset, so it exists for checking when appending parent.
        if parent is not None:
            # Add and set weakref to parent element or None, if it is the root. Caller must add self
            # to its elements separately.
            self.parent = parent # Set references in both directions. Remove any previous parent links

        # Conditional placement stuff
        if not conditions is None and not isinstance(conditions, (list, tuple)): # Allow singles
            conditions = [conditions]
        # Explicitedly stored local in element, not inheriting from ancesters. Can be None.
        self.conditions = conditions

        # Optional storage of self.context.BezierPath() to clip the content of
        # self.  Also note the possibility of the self.childClipPath property,
        # which returns a PageBotPath instance, constructed from the position
        # and layout of self.elements
        if clipPath is not None:
            clipPath = clipPath.copy() # Make a copy, so translates won't affect the original
        self.clipPath = clipPath # Optional clip path to show the content. None otherwise.

        self.report = [] # Area for conditions and drawing methods to report errors and warnings.
        # Optional description of this element or its content. Otherwise None. Can be string or BabelString
        self.description = description
        self.keyWords = keyWords # Optional used for web pages
        self.language = language # Optional language code from HTML standard. Otherwise DEFAULT_LANGUAGE.
        # Save flow reference names
        self.prevElement = prevElement # Element itself or name of the prev flow element
        self.nextElement = nextElement # Element itself or name of the next flow element
        self.nextPage = nextPage # Page element itself or name, identifier or index of the next page that nextElement refers to,
        self.prevPage = prevPage # if a flow must run over page boundaries.
        # Optional storage for the a thumbnail image path visualizing this element.
        self.thumbPath = thumbPath # Used by Magazine/PartOfBook and others, to show a predefined thumbnail of a page.
        # Copy relevant info from template: w, h, elements, style, conditions, next, prev, nextPage
        # Initialze self.elements, add template elements and values, copy elements if defined.
        # Note that this does not copy the attributes from template to self.
        # For that self.applyAttributes(template, elements, <attributeName>) should be called.
        self.applyTemplate(template, elements)
        # If flag is set, then solve the conditions upon creation of the element (e.g. to define the height)
        if solve:
            self.solve()

        # View flags
        self.showBaselineGrid = showBaselineGrid # Initialize to default values by property.

    def __repr__(self):
        """Object as string.

        >>> from pagebot.toolbox.units import mm
        >>> e = Element(name='TestElement', x=10, y=20, w=100, h=120)
        >>> repr(e)
        '<Element:TestElement (10pt, 20pt, 100pt, 120pt)>'
        >>> e.title = 'MyTitle'
        >>> e.x, e.y = 100, mm(200)
        >>> repr(e)
        '<Element:MyTitle (100pt, 200mm, 100pt, 120pt)>'
        """
        if self.title:
            name = ':'+self.title
        elif self.name:
            name = ':'+self.name
        else: # No naming, show unique self.eId:
            name = ':'+self.eId

        if self.elements:
            elements = ' E(%d)' % len(self.elements)
        else:
            elements = ''
        return '<%s%s (%s, %s, %s, %s)%s>' % (self.__class__.__name__, name, self.x, self.y, self.w, self.h, elements)

    def __len__(self):
        """Answers total amount of elements, placed or not. Note the various
        ways units, x, y, w and h can be defined.

        >>> e = Element(name='TestElement', x=100, y=200, w=pt(100), h=pt(120)) # Set as separate units
        >>> childE1 = Element(name='E1', x=pt(0), y=pt(0), size=pt(21, 22))
        >>> childE2 = Element(name='E2', xy=pt(100, 0), size=pt(11, 12)) # E.g. set as tuple of units
        >>> i1 = e.appendElement(childE1)
        >>> i2 = e.appendElement(childE2)
        >>> i1, i2, len(e) # Index of appended elements and length of parent
        (0, 1, 2)
        """
        return len(self.elements)

    def _get_theme(self):
        """Answer the theme of this element. If undefined, answer the theme of self.parent.
        If no parent is defined, then answer None.

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
        return None # No theme of parent defined.
    def _set_theme(self, theme):
        self._theme = theme
    theme = property(_get_theme, _set_theme)

    def checkStyleArgs(self, d):
        """Fix style values where necessary.

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

    def _get_isLocked(self):
        return self.css('isLocked', False)
    def _set_isLocked(self, isLocked):
        self.style['isLocked'] = isLocked
    isLocked = property(_get_isLocked, _set_isLocked)

    #   I M A G I N G

    def _get_resolution(self):
        """Answer the style value self.css('resolution') for the amount of
        DPI."""
        return self.css('resolution')
    def _set_resolution(self, resolution):
        self.style['resolution'] = resolution
    resolution = property(_get_resolution, _set_resolution)

    def _get_resolutionFactors(self):
        """Answer the style value self.css('resolutionFactors') for image
        cacheing size factors.  If set to None, the resolutionFactor defaults
        to DEFAULT_RESOLUTION_FACTORS. This will indicate, e.g. value 2, to
        write a thumbnail png twice the size it will be used in.
        """
        return self.css('resolutionFactors', default=DEFAULT_RESOLUTION_FACTORS)
    def _set_resolutionFactors(self, resolutionFactors):
        if resolutionFactors is None:
            resolutionFactors = DEFAULT_RESOLUTION_FACTORS
        assert isinstance(resolutionFactors, dict)
        self.style['resolutionFactors'] = resolutionFactors
    resolutionFactors = property(_get_resolutionFactors, _set_resolutionFactors)

    #   T E M P L A T E

    def applyTemplate(self, template, elements=None):
        """Copy relevant info from template: w, h, elements, style, conditions
        when element is created. Don't call later.

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot.elements import Template
        >>> e = Element(name='TestElement')
        >>> t = Template(xy=pt(11, 12), size=(100, mm(200)))
        >>> e.applyTemplate(t)
        >>> e.x, e.y, e.w, e.h
        (11pt, 12pt, 100pt, 200mm)
        """
        self.template = template # Set template value by property call, copying all template elements and attributes.
        if elements is not None:
            # Add optional list of additional elements.
            for e in elements or []:
                self.appendElement(e) # Add cross reference searching for eId of elements.

    def _get_template(self):
        """Property get/set for e.template.

        >>> from pagebot.elements import Template
        >>> e = Element(name='TestElement')
        >>> t = Template(name='MyTemplate', x=11, y=12, w=100, h=200)
        >>> e.applyTemplate(t)
        >>> e.template
        <Template>
        """
        return self._template
    def _set_template(self, template):
        self.clearElements() # Clear all existing child elements in self.
        self._template = template # Keep template reference to clone pages or if additional template info is needed later.
        # Copy optional template stuff
        if template is not None:
            # Copy elements from the template and put them in the designated positions.
            self.w = template.w
            self.h = template.h
            self.padding = template.padding
            self.margin = template.margin
            self.prevElement = template.prevElement
            self.nextElement = template.nextElement
            self.nextPage = template.nextPage
            # Copy style items
            for  name, value in template.style.items():
                self.style[name] = value
            # Copy condition list. Does not have to be deepCopy, condition instances are multi-purpose.
            self.conditions = copy.copy(template.conditions)
            for e in template.elements:
                self.appendElement(e.copy(parent=self))
    template = property(_get_template, _set_template)

    #   E L E M E N T S
    #   Every element is potentially a container of other elements, beside its own specific behavi.

    def __getitem__(self, eIdOrName):
        """Answers the element with eIdOrName. Answer None if the element does not exist.
        Elements behave as a semi-dictionary for child elements.
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
        >>> hex2dec(e.eId) > 1000 # Answers unique hex string in self._eId, such as '234FDC09FC10A0FA790'
        True
        """
        return self._eId
    eId = property(_get_eId)

    def _get_elements(self):
        """Property to get/set elements to parent self. Answer a copy of the list,
        not self._elements itself, to avoid problems if iterations on the children
        is changing the parent. E.g. if elements of a Typesetter galley are composed
        on a page.

        >>> e = Element()
        >>> len(e), len(e.elements)
        (0, 0)
        >>> e.elements = (Element(), Element(), Element())
        >>> len(e), len(e.elements)
        (3, 3)
        """
        return list(self._elements)
    def _set_elements(self, elements):
        self.clearElements() # Clear all existing child elements of self.
        for e in elements:
            self.appendElement(e) # Make sure to set all references.
    elements = property(_get_elements, _set_elements)

    def _get_elementIds(self): # Answer the x-ref dictionary with elements by their e.eIds
        """Answers the list with child.eId

        >>> e = Element()
        >>> e.elements = (Element(), Element(), Element())
        >>> len(e.elementIds)
        3
        """
        return self._eIds
    elementIds = property(_get_elementIds)

    def get(self, eIdOrName, default=None):
        """Answers the element by eId or name. Answer the same selection for
        default, if the element cannot be found. Answer None if it does not
        exist.

        >>> e = Element(name='Parent')
        >>> e1 = Element(name='Child')
        >>> i = e.appendElement(e1)
        >>> child = e.get('Child') # Get child element by its name
        >>> child is e1
        True
        >>> child = e.get(e1.eId) # Get child elements by is eId
        >>> child is e1
        True
        >>> child.name, child.parent.name # Child has e as parent
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
        """Answers the page element, if it has a unique element Id. Answer None
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
        """Recursively answer the page of this element. This can be several
        layers above self. If there element has not a parent in the line of
        parents, then answer None.

        >>> from pagebot.elements.pbpage import Page
        >>> eb = Element(name='Bottom')
        >>> e = Element(elements=[eb])
        >>> e = Element(elements=[e])
        >>> e = Element(elements=[e])
        >>> page = Page(elements=[e])
        >>> parentPage = eb.getElementPage() # Find page upwards of parent line, starting a lowest e.
        >>> page is parentPage
        True
        >>> eb = Element(name='Bottom')
        >>> e = Element(elements=[eb])
        >>> eb.getElementPage() is None # Element parent line does not contain a page.
        True
        """
        if self.isPage:
            return self # Answer if self is a page.
        if self.parent is not None:
            return self.parent.getElementPage()
        return None

    def _get_page(self):
        """Answers the page somewhere in the parent tree, if it exists.
        Answer None otherwise.

        >>> from pagebot.elements.pbpage import Page
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

    def getElementByName(self, name):
        """Answers the first element in the offspring list that fits the name.
        Answer None if it cannot be found.
        Note that the result of the search depends on where in the tree self is.
        If self.isPage there probably is a different set of elements found than
        searching witn self as arbitrary Element instance.

        >>> e1 = Element(name='Deeper')
        >>> e2 = Element(name='Deeper')
        >>> e3 = Element(name='Child', elements=[e1, e2])
        >>> e = Element(name='Parent', elements=[e3])
        >>> child = e.get('Child') # Get child element by its name
        >>> child is e3
        True
        >>> e.get('Deeper') is e1, e.get('Deeper') is e2 # Find first down the list
        (True, False)
        """
        if self.name == name:
            return self
        for e in self.elements:
            found = e.getElementByName(name) # Don't search on next page yet.
            if found is not None:
                return found
        return None

    def deepFindAll(self, name=None, pattern=None, result=None):
        """Perform a dynamic recursive deep find for all elements with the name.
        Don't include self. Either *name* or *pattern* should be defined,
        otherwise an error is raised. Return the collected list of matching child
        elements. Answer an empty list if no elements can be found.

        Note that the result of the search depends on where in the tree self is.
        If self.isPage there probably is a different set of elements found than
        searching witn self as arbitrary Element instance.

        >>> e1 = Element(name='DeeperChild')
        >>> e2 = Element(name='DeeperChild', elements=[e1])
        >>> e3 = Element(name='Child', elements=[e2])
        >>> e = Element(name='Parent', elements=[e3])
        >>> elements = e.deepFindAll(name='DeeperChild') # Get all child elements matching name
        >>> len(elements)
        2
        >>> elements = e.deepFindAll(pattern='Child') # Get all child elements matching pattern
        >>> len(elements)
        3
        >>> elements = e.deepFindAll(pattern='XYZ') # Answer empty list if no element can be found
        >>> len(elements)
        0
        """
        assert name or pattern
        if result is None:
            result = []
        for e in self.elements:
            if pattern is not None and pattern in e.name: # Simple pattern match
                result.append(e)
            elif name is not None and name in (e.cssId, e.name):
                result.append(e)
            e.deepFindAll(name, pattern, result)
        return result

    def findAll(self, name=None, pattern=None, cls=None, result=None):
        """Perform a dynamic find for the named element(s) in self.elements.
        Don't include self. Either name or pattern should be defined, otherwise
        an error is raised. Return the collected list of matching child
        elements. Answer an empty list if no elements can be found.

        Note that the result of the search depends on where in the tree self is.
        If self.isPage there probably is a different set of elements found than
        searching witn self as arbitrary Element instance.

        >>> e1 = Element(name='OtherChild')
        >>> e2 = Element(name='OtherChild')
        >>> e3 = Element(name='Child')
        >>> e = Element(name='Parent', elements=[e1, e2, e3])
        >>> elements = e.findAll(name='OtherChild') # Get all child element matching name
        >>> len(elements)
        2
        >>> elements = e.findAll(pattern='Child') # Get all child element matching name
        >>> len(elements)
        3
        >>> elements = e.findAll(pattern='XYZ') # Answer empty list if no element can be found
        >>> len(elements)
        0
        """
        assert name or pattern or cls
        result = []
        for e in self.elements:
            if cls is not None and (cls == e.__class__.__name__ or isinstance(e, cls)):
                 result.append(e)
            elif pattern is not None and pattern in e.name: # Simple pattern match
                result.append(e)
            elif name is not None and name in (e.cssId, e.name):
                result.append(e)
        return result

    def deepFind(self, name=None, pattern=None, cls=None):
        """Perform a dynamic recursive deep find for all elements with the name.
        Don't include self. Either *name* or *pattern* should be defined,
        otherwise an error is raised. Return the first matching child
        element. Answer None if no elements can be found.

        Note that the result of the search depends on where in the tree self is.
        If self.isPage there probably is a different set of elements found than
        searching witn self as arbitrary Element instance.

        The name, pattern and cls values are case-sensitive in the search.

        >>> e = Element(name='Parent')
        >>> e1 = Element(name='Child', parent=e)
        >>> e2 = Element(name='DeeperChild', parent=e1)
        >>> e3 = Element(name='DeeperChild', parent=e2)
        >>> e4 = Element(name='DeepestChild', parent=e3)
        >>> element = e.deepFind(name='DeeperChild') # Get all child elements matching name
        >>> element is e2
        True
        >>> element = e.deepFind(pattern='Child') # Get first child elements matching pattern
        >>> element is e1
        True
        >>> e.select(name='child') is None # Search is case-sensitive
        True
        >>> element = e.deepFind(pattern='Deepest') # Get first child elements matching pattern
        >>> element is e4
        True
        >>> element = e.deepFind(pattern='XYZ') # Answer None if element does not exist
        >>> element is None
        True
        >>> element = e.select(name='DeeperChild') # Get all child elements matching name
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

    select = deepFind # Intuitive name with identical result. Can be used in MarkDown.

    def find(self, name=None, pattern=None, cls=None):
        """Perform a dynamic find for the named element(s) in self.elements.
        Don't include self. Either name or pattern should be defined, otherwise
        an error is raised. Return the first element that fist the criteria.
        Answer None if no element can be found.

        Note that the result of the search depends on where in the tree self is.
        If self.isPage there probably is a different set of elements found than
        searching witn self as arbitrary Element instance.

        >>> e = Element(name='Parent')
        >>> e1 = Element(name='OtherChild', parent=e)
        >>> e2 = Element(name='OtherChild', parent=e)
        >>> e3 = Element(name='LastChild', parent=e)
        >>> element = e.find(name='OtherChild') # Get first child element matching name
        >>> element is e1
        True
        >>> element = e.find(pattern='LastChild') # Get first child element matching name
        >>> element is e3
        True
        >>> element = e.find(pattern='XYZ') # Get first child element matching name
        >>> element is None
        True
        """
        assert name or pattern or cls
        for e in self.elements:
            if cls is not None and (cls == e.__class__.__name__ or isinstance(e, cls)):
                return e
            if pattern is not None and pattern in e.name: # Simple pattern match
                return e
            if name is not None and name in (e.cssId, e.name):
                return e
        return None

    def findBysId(self, sId):
        """If defined, the system self.sId can be used to recursively find self or a child.
        Answer None if nothing can be found that is exactly matching.
        """
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
        """Make inheriting classes define a method to clear their content if appropriate.
        Default behavior of Element is to do nothing."""
        pass

    def copy(self, parent=None):
        """Answers a full copy of self, where the "unique" fields are set to
        default. Also perform a deep copy on all child elements.

        >>> e1 = Element(name='Child', w=100)
        >>> e = Element(name='Parent', elements=[e1], w=200)
        >>> copyE = e.copy()
        >>> copyE.name == e.name, copyE.eId == e.eId
        (True, False)
        >>> copyE is e, copyE['Child'] is e['Child'] # Element tree is copied
        (False, False)
        >>> copyE.name == e.name, copyE.w == e.w == 200, copyE['Child'].w == e['Child'].w == 100 # Values are copied
        (True, True, True)
        >>> e.copy().eId != e.eId
        True
        """
        # Deep-copies the element. Set the parent (if defined) and iterate through
        # the child tree to make a e.eId unique.

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

        """" REMOVE THIS
        self.__class__(
            x=self.x,
            y=self.y,
            z=self.z,
            w=self.w,
            h=self.h,
            d=self.d,
            t=self.t, # Copy type frame.
            parent=parent, # Allow to keep reference to current parent context and style.
            context=self._context, # Copy local context, None most cases, where reference to parent->doc context is required.
            name=self.name,
            #cssId is copied conditionally by copyCssId flag. E.g. applying template to web page.
            cssClass=self.cssClass,
            title=self.title,
            description=self.description,
            language=self.language,
            lib=copy.deepcopy(self.lib),
            style=copy.deepcopy(self.style), # Style is supposed to be a deep-copyable dictionary.
            conditions=copy.deepcopy(self.conditions), # Conditions may be modified by the element of ascestors.
            framePath=self.framePath,
            elements=None, # Will be copied separately, if there are child elements
            template=self.template,
            nextElement=self.nextElement,
            prevElement=self.prevElement,
            nextPage=self.nextPage,
            prevPage=self.prevPage,
            padding=self.padding, # Copies all padding values at once
            margin=self.margin, # Copies all margin values at once,
            borders=self.borders, # Copies all borders at once.
            gridX=copy.deepcopy(self.gridX),
            gridY=copy.deepcopy(self.gridY),
            shadow=self.shadow, # Needs to be copied?
            gradient=self.gradient, # Needs to be copied?
            drawBefore=self.drawBefore,
            drawAfter=self.drawAfter)

        # If any additional attribute names defined, then deepcopy these as well.
        for attrName in (attrNames or []): # Any additional attributes to copy? :
            setattr(e, attrName, copy.deepcopy(getattr(self, attrName)))

        # Now do the same for each child element and append it to self.
        for child in self.elements:
            # Add the element to child list and update self._eId dictionary
            # Keep the copyCssIf flag downwards, in case we are applying a template on
            # a web page.
            e.appendElement(child.copy(attrNames=attrNames))
        return e
        """

    def _get_childClipPath(self):
        """Answer the clipping context.BezierPath, derived from the layout of child elements.

        >>> from pagebot.conditions import *
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> e = Element(w=500, h=500, context=context)
        >>> e1 = Element(parent=e, x=0, y=0, w=50, h=80)
        >>> e.childClipPath.points
        [(50.0, 0.0), (500.0, 0.0), (500.0, 500.0), (0.0, 500.0), (0.0, 80.0), (50.0, 80.0), (50.0, 0.0)]
        >>> e = Element(w=500, h=500, context=context)
        >>> e1 = Element(parent=e, w=100, h=100, conditions=[Left2Left(), Top2Top()])
        >>> e2 = Element(parent=e, w=100, h=100, conditions=(Left2Left(), Bottom2Bottom()))
        >>> score = e.solve()
        >>> e.childClipPath.points
        [(100.0, 0.0), (500.0, 0.0), (500.0, 500.0), (0.0, 500.0), (0.0, 100.0), (100.0, 100.0), (100.0, 0.0)]
        >>> e.childClipPath.__class__.__name__
        'PageBotPath'
        """
        path = self.PATH_CLASS(self.context)
        path.rect(-self.ml, -self.mb, self.ml + self.w + self.mr, self.mb + self.h + self.mt)
        for e in self.elements:
            path = path.difference(e.childClipPath)
        path.translate(self.xy)
        return path
    childClipPath = property(_get_childClipPath)

    def setElementByIndex(self, e, index):
        """Replace the element, if there is already one at index. Otherwise
        append it to self.elements and answer the index number that is assigned
        to it. If index < 0, just answer None and do nothing.

        >>> e1 = Element(name='Child1')
        >>> e2 = Element(name='Child2')
        >>> e3 = Element(name='Child3')
        >>> e = Element(name='Parent', elements=[e1, e2])
        >>> index = e.setElementByIndex(e3, 1) #
        >>> e.elements[1] is e3, index == 1
        (True, True)
        >>> e.setElementByIndex(e2, 20) # Add at end
        2
        >>> e4 = Element(name='Child4')
        >>> e.setElementByIndex(e2, -2) is None
        True
        """
        if index < 0:
            return None # Don't accept.
        if index < len(self.elements):
            self._elements[index] = e
            if self.eId:
                self._eIds[e.eId] = e
            return index
        return self.appendElement(e)

    def appendElement(self, e):
        """Add element to the list of child elements. Note that elements can be
        added multiple times. If the element is already placed in another
        container, then remove it from its current parent. The parent relation
        and the position are lost. The position `e` is supposed to be filled
        already in local position.

        >>> e = Element(name='Parent')
        >>> e1 = Element(name='Child1', parent=e)
        >>> e2 = Element(name='Child2', parent=e)
        >>> e3 = Element(name='Child3', parent=e)
        >>> e.elements[-1] is e3
        True
        >>> i = e.appendElement(e1) # Append elements that is already child of e
        >>> # Now e1 is at end of list
        >>> e.elements[0] is e2, e.elements[-1] is e1, e.elements[1] is e3
        (True, True, True)
        """
        eParent = e.parent
        if not eParent is None:
            eParent.removeElement(e) # Remove from current parent, if there is one.
        self._elements.append(e) # Possibly add to self again, will move it to the top of the element stack.
        e.setParent(self) # Set parent of element without calling this method again.
        if e.eId: # Store the element by unique element id, if it is defined.
            self._eIds[e.eId] = e
        return len(self._elements)-1 # Answer the element index for e.

    append = appendElement # Add alternative method name for conveniece of high-level element additions.

    def removeElement(self, e):
        """If the element is placed in self, then remove it. Don't touch the
        position.

        >>> e = Element(name='Parent')
        >>> e1 = Element(name='Child1', parent=e)
        >>> e2 = Element(name='Child2', parent=e)
        >>> e3 = Element(name='Child3', parent=e)
        >>> e.removeElement(e2)
        <Element:Child2 (0pt, 0pt, 100pt, 100pt)>
        >>> e.elements[0] is e1, e.elements[1] is e3, e2.parent is None # e2 has no parent now.
        (True, True, True)
        """
        assert e.parent is self
        e.setParent(None) # Unlink the parent reference of e
        if e.eId in self._eIds:
            del self._eIds[e.eId]
        if e in self._elements:
            self._elements.remove(e)
        return e # Answer the unlinked elements for convenience of the caller.

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
        >>> e.getElementsAtPoint((None, 40)) == [e2] # Search on wildcard x
        True
        >>> e.getElementsAtPoint((20, None)) == [e1, e2] # Find both on wildcard y
        True
        """
        elements = []
        px, py, pz = point3D(point) # Add z if tuple is only (x,y)
        for e in self.elements:
            ex, ey, ez = e.xyz
            if (ex == px or px is None) and (ey == py or py is None) and (ez == pz or pz is None):
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
        >>> e3 = Element(name='Child3', x=20, y=40, w=200) # Same position, different size.
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
            rxyz = rv(e.xyz) # Point needs to be tuple to be used a key.
            if rxyz not in positions:
                positions[rxyz] = []
            positions[rxyz].append(e)
        return positions

    #   F L O W

    # If the element is part of a flow, then answer the squence.

    def _get_next(self):
        """If self if part of a flow, answer the next element, defined by self.nextElement.
        If self.nextPage is defined too, then search on the indicated page.

        >>> from pagebot.document import Document
        >>> doc = Document(autoPages=3)
        >>> page = doc[1]
        >>> e1_1 = Element(parent=page, name='e1', nextElement='e2')
        >>> e1_2 = Element(parent=page, name='e2', nextElement='e1', nextPage=2)
        >>> page = doc[2]
        >>> e2_1 = Element(parent=page, name='e1', nextElement='e2')
        >>> e2_2 = Element(parent=page, name='e2', nextElement='e3')
        >>> e2_3 = Element(parent=page, name='e3', nextElement='e1', nextPage=3)
        >>> page = doc[3]
        >>> e3_1 = Element(parent=page, name='e1', nextElement='e2')
        >>> e3_2 = Element(parent=page, name='e2', nextElement='e3')
        >>> e3_3 = Element(parent=page, name='e3')
        >>> e1_1.next.name
        'e2'
        >>> e1_1.next.next == e2_1 # Crosses page borders.
        True
        >>> e2_2.next.next.next.next == e3_3 # Crosses page borders
        True
        >>> e3_2.next.next is None # End of flow
        True
        >>> e3_2.prevElement # Gets repaired by the e3_2.next usage
        'e1'
        >>> e3_1.prevPage # Get repaired by the e3_1.next usage.
        (2, 0)
        """
        nextElement = None
        if self.nextElement is not None: # If there is a next element reference defined.
            if isinstance(self.nextPage, Element):
                page = self.nextPage
            elif self.nextPage: # then check if we also make reference to a another page.
                page = self.doc[self.nextPage]
            else: # If no next page reference, then refoer to the page of self.
                page = self.page
            if page is not None: # Only if a page was found for this element
                nextElement = page.select(self.nextElement)
                if nextElement is not None:
                    nextElement.prevElement = self.name # Repair in case it is broken
                    if self.nextPage:
                        nextElement.prevPage = self.page.pn

        return nextElement
    next = property(_get_next)

    def _get_isFlow(self):
        """Answers if self is part of a flow, which means that
        either self.prevElement or self.nextElement is not None.

        >>> e = Element()
        >>> e.isFlow
        False
        >>> e.nextElement = 'e1'
        >>> e.isFlow
        True
        """
        return bool(self.prevElement or self.nextElement)
    isFlow = property(_get_isFlow)

    def getFlow(self, flow=None):
        """Answers the list of flow element sequences starting on self. In case self.nextPage
        is defined, then

        >>> from pagebot.document import Document
        >>> doc = Document(autoPages=3)
        >>> page = doc[1]
        >>> e1_1 = Element(parent=page, name='e1', nextElement='e2')
        >>> e1_2 = Element(parent=page, name='e2', nextElement='e1', nextPage=2)
        >>> page = doc[2]
        >>> e2_1 = Element(parent=page, name='e1', nextElement='e2')
        >>> e2_2 = Element(parent=page, name='e2', nextElement='e3')
        >>> e2_3 = Element(parent=page, name='e3')
        >>> flow = e1_1.getFlow() # Identical to e1_1.flow
        >>> len(flow)
        5
        >>> flow[1].page.pn
        (1, 0)
        >>> flow[3].page.pn # Cross page border
        (2, 0)

        """
        if flow is None:
            flow = []  # List of elementa.
        e = self
        while e is not None:
            flow.append(e)
            e = e.next
        return flow

    def _get_flow(self):
        """Answers the list of flow element sequences starting on self.
        As property identical to calling self.getFlow()
        """
        return self.getFlow()
    flow = property(_get_flow)

    #   If self.nextElement is defined, then check the condition if there is overflow.

    def isOverflow(self, tolerance):
        """Answers if this element needs overflow to be solved.
        This method is typically called by conditions such as Overflow2Next.
        This method is redefined by inheriting classed, such as TextBox, that
        can have overflow of text."""
        return False

    def overflow2Next(self):
        """Try to fix if there is overflow. Default behavior is to do nothing.
        This method is redefined by inheriting classed, such as TextBox, that
        can have overflow of text."""
        return False

    def _get_baselineColor(self):
        """Answer the current setting of the baseline color for this element."""
        return self.css('baselineColor', DEFAULT_BASELINE_COLOR)
    def _set_baselineColor(self, baselineColor):
        self.style['baselineColor'] = baselineColor
    baselineColor = property(_get_baselineColor, _set_baselineColor)

    def _get_baselineWidth(self):
        """Answer the current setting of the baseline width for this element."""
        return self.css('baselineWidth', DEFAULT_BASELINE_WIDTH)
    def _set_baselineWidth(self, baselineWidth):
        self.style['baselineWidth'] = baselineWidth
    baselineWidth = property(_get_baselineWidth, _set_baselineWidth)

    def _get_baselineGrid(self):
        """Answers the baseline grid distance, as defined in the (parent)style.

        >>> from pagebot.toolbox.units import mm, p
        >>> e = Element()
        >>> e.baselineGrid is None # Undefined without style or parent style.
        True
        >>> e.baselineGrid = 12
        >>> e.baselineGrid
        12pt
        >>> e.baselineGrid = mm(13.5)
        >>> e.baselineGrid
        13.5mm
        >>> e = Element(style=dict(baselineGrid=14))
        >>> e.baselineGrid
        14pt
        """
        base = dict(base=self.parentH, em=self.em) # In case relative units, use this as base for %
        return units(self.css('baselineGrid'), base=base)
    def _set_baselineGrid(self, baselineGrid):
        self.style['baselineGrid'] = units(baselineGrid)
    baselineGrid = property(_get_baselineGrid, _set_baselineGrid)

    def _get_baselineGridStart(self):
        """Answers the baseline grid startf, as defined in the (parent)style.

        >>> e = Element()
        >>> e.baselineGridStart is None # Undefined without style or parent style.
        True
        >>> e.baselineGridStart = 17
        >>> e.baselineGridStart
        17pt
        >>> e = Element(style=dict(baselineGridStart=15))
        >>> e.baselineGridStart
        15pt
        """
        base = dict(base=self.parentH, em=self.em) # In case relative units, use this as base for %
        return units(self.css('baselineGridStart'), base=base)
    def _set_baselineGridStart(self, baselineGridStart):
        self.style['baselineGridStart'] = units(baselineGridStart)
    baselineGridStart = property(_get_baselineGridStart, _set_baselineGridStart)

    def baseY(self, lineIndex=0):
        """Answer the vertical position of line by lineIndex, starting at the top of the element.
        Note that this top-down measure is independent from the overall doc.originTop settings,
        as the baseline grid always runs from top of the element or page.

        >>> e = Element(baselineGrid=pt(12), baselineGridStart=pt(22))
        >>> e.baselineGrid, e.baselineGridStart
        (12pt, 22pt)
        """

        """
        >>> e.baseY()
        22pt
        >>> e.baseY(23)
        298pt
        """
        return self.h - self.baselineGrid * lineIndex + self.baselineGridStart

    # Text conditions, always True for non-text elements.

    def getDistance2Grid(self, y):
        """Answers the distance between y and y rounded to baseline grid.
        This can be a negative number showing the direction of rounding

        >>> e = Element(h=500, baselineGridStart=100, baselineGrid=10, originTop=False)
        >>> e.getDistance2Grid(pt(40))
        0pt
        >>> e.getDistance2Grid(45)
        -5pt
        >>> e.getDistance2Grid(38)
        2pt
        """
        if self.originTop:
            dy = y - self.baselineGridStart
        else:
            # Calculate the position of top of the grid
            gridTopY = self.h - (self.baselineGridStart or self.pt)
            # Calculate distance of the line to top of the grid
            gy = gridTopY - y
            dy = gy - round(gy/self.baselineGrid) * self.baselineGrid

        # Now we can answer the difference of y to the nearest grid line
        return dy


    def isTopOnGrid(self, tolerance=0):
        """Answer True if self.top is on the parent grid.
        >>> e1 = Element(baselineGridStart=100, baselineGrid=10, h=1000, originTop=False)
        >>> e2 = Element(y=100, h=200, parent=e1)
        >>> e2.isTopOnGrid()
        True
        >>> e2.y = 102
        >>> e2.isTopOnGrid()
        False
        """
        return abs(self.getDistance2Grid(self.top)) <= tolerance

    def isBottomOnGrid(self, tolerance=0):
        """Answer True if self.bottom is on the parent grid.
        >>> e1 = Element(baselineGridStart=100, baselineGrid=10, h=1000, originTop=False)
        >>> e2 = Element(y=100, h=200, parent=e1)
        >>> e2.isBottomOnGrid()
        True
        >>> e2.y = 102
        >>> e2.isBottomOnGrid()
        False
        """
        return abs(self.getDistance2Grid(self.bottom)) <= tolerance

    def isMiddleOnGrid(self, tolerance=0):
        """Answer True if self.middle is on the parent grid.
        >>> e1 = Element(baselineGridStart=100, baselineGrid=10, h=1000, originTop=False)
        >>> e2 = Element(y=100, h=200, parent=e1)
        >>> e2.isMiddleOnGrid()
        True
        >>> e2.y = 102
        >>> e2.isMiddleOnGrid()
        False
        """
        return abs(self.getDistance2Grid(self.middle)) <= tolerance

    def isBaselineOnGrid(self, tolerance=0, index=0):
        # Implemented for elements that support text boxes.
        # Default is True for non-text elements, so the calling condition is satisfied.
        return True

    def isBaselineOnTop(self, tolerance=0, index=0):
        # Implemented for elements that support text boxes.
        # Default is True for non-text elements, so the calling condition is satisfied.
        return True

    def isBaselineOnBottom(self, tolerance=0, index=0):
        # Implemented for elements that support text boxes.
        # Default is True for non-text elements, so the calling condition is satisfied.
        return True

    def isAscenderOnGrid(self, tolerance=0, index=0):
        # Implemented for elements that support text boxes.
        # Default is True for non-text elements, so the calling condition is satisfied.
        return True

    def isAscenderOnTop(self, tolerance=0, index=0):
        # Implemented for elements that support text boxes.
        # Default is True for non-text elements, so the calling condition is satisfied.
        return True

    def isAscenderOnBottom(self, tolerance=0, index=0):
        # Implemented for elements that support text boxes.
        # Default is True for non-text elements, so the calling condition is satisfied.
        return True

    def isCapHeightOnGrid(self, tolerance=0, index=0):
        # Implemented for elements that support text boxes.
        # Default is True for non-text elements, so the calling condition is satisfied.
        return True

    def isCapHeightOnTop(self, tolerance=0, index=0):
        # Implemented for elements that support text boxes.
        # Default is True for non-text elements, so the calling condition is satisfied.
        return True

    def isCapHeightOnBottom(self, tolerance=0, index=0):
        # Implemented for elements that support text boxes.
        # Default is True for non-text elements, so the calling condition is satisfied.
        return True

    def isXHeightOnGrid(self, tolerance=0, index=0):
        # Implemented for elements that support text boxes.
        # Default is True for non-text elements, so the calling condition is satisfied.
        return True

    def isXHeightOnTop(self, tolerance=0, index=0):
        # Implemented for elements that support text boxes.
        # Default is True for non-text elements, so the calling condition is satisfied.
        return True

    def isXHeightOnBottom(self, tolerance=0, index=0):
        # Implemented for elements that support text boxes.
        # Default is True for non-text elements, so the calling condition is satisfied.
        return True

    def isDescenderOnGrid(self, tolerance=0, index=0):
        # Implemented for elements that support text boxes.
        # Default is True for non-text elements, so the calling condition is satisfied.
        return True

    def isDescenderOnTop(self, tolerance=0, index=0):
        # Implemented for elements that support text boxes.
        # Default is True for non-text elements, so the calling condition is satisfied.
        return True

    def isDescenderOnBottom(self, tolerance=0, index=0):
        # Implemented for elements that support text boxes.
        # Default is True for non-text elements, so the calling condition is satisfied.
        return True

    #   S T Y L E

    # Answer the cascaded style value, looking up the chain of ancestors, until style value is defined.

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

    def getNamedStyle(self, styleName):
        """In case we are looking for a named style (e.g. used by the
        Typesetter to build a stack of cascading tag style, then query the
        ancestors for the named style. Default behavior of all elements is that
        they pass the request on to the root, which is normally the document.
        Use force attribute to overwrite an existing style with the same name.

        >>> from pagebot.document import Document
        >>> from pagebot.toolbox.color import color
        >>> doc = Document()
        >>> doc.addStyle('body', force=True, style=dict(name='body', fill=color('red'))) # Add named style to document
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
        for key in getRootStyle().keys():
            flattenedStyle[key] = self.css(key)
        return flattenedStyle

    def getBlendedStyle(self, t=None):
        """Answers the blended style for self, blended between the current time
        marks on position t or self.t. If style values are not in the time
        marks, then their values

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
        """Answers the current font instance as defined in style. Text based inheriting
        elements may want to implement as the font of the last added text.

        >>> e = Element(style=dict(font='Roboto-Regular'))
        >>> e.font
        <Font Roboto-Regular>
        >>> e.font.info.cssName
        'Roboto-Regular'
        """
        font = self.css('font', DEFAULT_FONT_PATH)
        if isinstance(font, str):
            font = findFont(font)
        return font
    def _set_font(self, font):
        """Store the font in the local style. This can be a path, name or Font instance"""
        self.style['font'] = font
    font = property(_get_font, _set_font)

    def _get_lib(self):
        """Answer the local element.lib dictionary by property, used for custom
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
        >>> from pagebot.elements.pbpage import Page
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
            return parent.docLib # Either parent element or document.docLib.
        return None # Document cannot be found, or there is there is no parent defined in the element.
    docLib = property(_get_docLib)

    def _get_doc(self):
        """Answers the root Document of this element by property, looking upward
        in the ancestor tree."""
        if self.parent is not None:
            return self.parent.doc
        return None
    doc = property(_get_doc)

    def _get_view(self):
        """Answers the self.doc.view, currently set for reference and building
        this element."""
        doc = self.doc
        if doc is not None:
            return doc.view
        return None
    view = property(_get_view)

    def _get_context(self):
        """Answers the context of this element. In general the self._context
        will be None, to allow searching the parents --> document --> view. But
        there may be exceptions where elements+children need their own."""
        if self._context is not None:
            return self._context
        # Context not defined for this element, try parent.
        if self.parent is not None:
            return self.parent.context
        # No context defined and no parent, we cannot do any better now than answering None here.
        return None
    def _set_context(self, context):
        self._context = context
    context = property(_get_context, _set_context)

    def _get_builder(self):
        return self.context.b
    b = builder = property(_get_builder)

    def newString(self, bs, e=None, style=None, w=None, h=None, pixelFit=True):
        """Create a new BabelString, using the current type of self.doc.context,
        or pagebot.contexts.getContext() if not self.doc or self.doc.view defined,
        if bs is a plain string. Otherwise just answer the BabelString unchanged.
        In case of a BabelString, is has to be the same as the current context would
        create, otherwise an error is raised. In other words, there is no BabelString
        conversion defined (no reliable way of doing that, they should be created
        in the right context from the beginning).

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> e = Element(context=context)
        """

        """
        TODO: Get more docTests to work
        >>> bs = e.newString('ABC')
        >>> str(bs.s)
        'ABC'
        >>> from pagebot.contexts.flatcontext import FlatContext
        >>> context = FlatContext()
        >>> e = Element(context=context)
        >>> bs = e.newString('ABC')
        >>> #str(bs.s)
        'ABC'
        """
        if e is None:
            e = self
        if self.context is not None:
            return self.context.newString(bs, e=e, style=style, w=w, h=h, pixelFit=pixelFit)
        return None

    # Most common properties

    def setParent(self, parent):
        """Set the parent of self as weakref if it is not None. Don't call
        self.appendElement(). Calling setParent is not the main way to add an
        element to a parent, because the original parent would not know that
        the element disappeared. Call self.appendElement(e), which will call
        this method. """
        if parent is not None:
            parent = weakref.ref(parent)
        self._parent = parent # Can be None if self needs to be unlinked from a parent tree. E.g. when moving it.

    def _get_parent(self):
        """Answers the parent of the element, if it exists, by weakref
        reference. Answer None of there is not parent defined or if the parent
        not longer exdef ists."""
        if self._parent is not None:
            return self._parent()
        return None
    def _set_parent(self, parent):
        # Note that the caller must add self to its elements.
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
        """Normal elements don't know the left/right orientation of the page
        that they are on. Pass the request on to the parent, until a page is
        reached."""
        if self.parent is not None:
            return self.parent.isRight
        return False
    isRight = property(_get_isRight)

    def _get_gridX(self):
        """Answers the grid, depending on the left/right orientation of self.

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
        definition [(wx, gutter), ...] If there is one or more None in the grid
        definition, then try to fit equally on self.cw.  If gutter is left
        None, then the default style gutter is filled there.

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

        if gridX is not None: # If there is a non-linear grid sequence defined, use that.
            undefined = 0
            usedWidth = 0
            # Make a first pass to see how many columns (None) need equal division and what total width spare we have.
            for gridValue in gridX:
                if not isinstance(gridValue, (list, tuple)):
                    gridValue = (gridValue, None) # Only single column width defined, force fill in with default gw gutter
                cw, gutter = gridValue
                if cw is None:
                    undefined += 1
                else:
                    usedWidth += cw
                if gutter is None:
                    gutter = gw
                usedWidth += gutter
            equalWidth = (pw - usedWidth) / (undefined or 1)
            # Now we know the divide width, scan through the grid list again, building x coordinates.
            x = 0
            for gridValue in gridX:
                if not isinstance(gridValue, (list, tuple)):
                    gridValue = (gridValue, None) # Only single column width defined, force fill in with default gw gutter
                cw, gutter = gridValue
                if cw is None:
                    cw = equalWidth
                if gutter is None:
                    gutter = gw
                gridColumns.append((x, cw))
                x += cw + gutter

        elif self.cw: # If no grid defined, and there is a general grid width, then run the squence for cw + gw gutter
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
        definition [(wx, gutter), ...] If there is one or more None in the grid
        definition, then try to fit equally on self.cw. If gutter is left
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

        if gridY is not None: # If there is a non-linear grid sequence defined, use that.
            undefined = 0
            usedHeight = 0
            #usedWidth = 0
            # Make a first pass to see how many columns (None) need equal division.
            for gridValue in gridY:
                if not isinstance(gridValue, (list, tuple)):
                    gridValue = (gridValue, None) # Only single column height defined, force fill in with default gh gutter
                ch, gutter = gridValue
                if ch is None:
                    undefined += 1
                #else:
                #    usedWidth += ch
                if gutter is None:
                    gutter = gh
                usedHeight += gutter
            usedHeight = (ph - usedHeight) / (undefined or 1)
            # Now we know the divide width, scane through the grid list again, building x coordinates.
            y = 0
            for gridValue in gridY:
                if not isinstance(gridValue, (list, tuple)):
                    gridValue = (gridValue, None) # Only single column height defined, force fill in with default gutter
                ch, gutter = gridValue
                if ch is None:
                    ch = usedHeight
                if gutter is None:
                    gutter = gh
                gridRows.append((y, ch))
                y += ch + gutter
        elif self.ch: # If no grid defined, and there is a general grid height, then run the squence for ch + gh gutter
            ch = self.ch
            y = 0
            for index in range(int(ph/ch)): # Roughly the amount of columns to expect. Avoid while loop
                if y + ch > ph:
                    break
                gridRows.append((y, ch))
                y += ch + gh # Next column start position.
        return gridRows

    # No getGrid in Z-direction for now.

    # Properties for unit access.

    def _get_parentW(self):
        """Answers the width if the parent element. If there is not parent,
        answer DEFAULT_WIDTH.

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
        return self.parent.w # Answer total width as reference for relative units.
    parentW = property(_get_parentW)

    def _get_parentH(self):
        """Answers the height if the parent element. If there is no parent,
        answer DEFAULT_HEIGHT.

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
        return self.parent.h # Answer total height as reference for relative units.
    parentH = property(_get_parentH)

    def _get_parentD(self):
        """Answers the depth if the parent element. If there is no parent,
        answer DEFAULT_DEPTH.

        >>> e0 = Element(d=502)
        >>> e1 = Element()
        >>> e1.parentD # No parent, answer default value
        100pt
        >>> e1.parent = e0 # Set parent, now width of parent is answered.
        >>> e1.parentD
        502pt
        """
        if self.parent is None:
            return DEFAULT_DEPTH
        return self.parent.d # Answer total depth as reference for relative units.
    parentD = property(_get_parentD)

    # Plain coordinates

    def _get_x(self):
        """Answers the `x` position of self as Unit instance. In case it is a
        relative unit (such as Fr, Perc or Em), we just set the current parent
        total and em as reference. By not freezing or rendering the value yet,
        the caller can decide to change parent value, and then render the value
        as with `u.get(optionalTotal)`. Some situations require the rendered
        value, but in case of CSS, the relative value should be maintained. Then
        the current parent total reference is not important.

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
        >>> child.x.pt # 40% of 400
        160
        >>> e.w = 500 # Child percentage changes dynamically from parent
        >>> child.x.pt # 40% of 500
        200
        >>> child.x = fr(0.5)
        >>> child.x
        0.5fr
        """
        # Retrieve as Unit instance and adjust attributes to current settings.
        base = dict(base=self.parentW, em=self.em) # In case relative units, use this as base.
        return units(self.style.get('x'), base=base)

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
        >>> child.y, child.y.pt # 40% of 400
        (40%, 160)
        >>> e.h = 500
        >>> child.y, child.y.pt # 40% of 500 dynamic calculation
        (40%, 200)
        """
        # Retrieve as Unit instance and adjust attributes to current settings.
        base = dict(base=self.parentH, em=self.em) # In case relative units, use this as base.
        return units(self.style.get('y'), base=base)
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
        >>> child.z, child.z.base, child.z.rv, child.z.ru # 40% of 400
        (40%, 400pt, 160, 160pt)
        >>> e.d = 500
        >>> child.z, child.z.pt # 40% of 500 dynamic calculation. Should have value or pt as result?
        (40%, 200)
        """
        # Retrieve as Unit instance and adjust attributes to current settings.
        base = dict(base=self.parentD, em=self.em) # In case relative units, use this as base.
        return units(self.style.get('z'), base=base)

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
        >>> child.xy, ru(child.xy), rv(child.xy) # Position in middle of parent square
        ((50%, 50%), (200pt, 200pt), (200, 200))
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
        >>> child.xyz, ru(child.xyz), rv(child.xyz) # Position in middle of parent cube
        ((112%, 22pt, 32pt), (448pt, 22pt, 32pt), (448, 22, 32))
        """
        return self.x, self.y, self.z
    def _set_xyz(self, p):
        assert len(p) == 3
        self.x = p[0]
        self.y = p[1]
        self.z = p[2]
    xyz = property(_get_xyz, _set_xyz)

    def _get_origin(self):
        """Answers the self.xyz, where y can be flipped, depending on the
        self.originTop flag."""
        return self._applyOrigin(self.xyz)

    origin = property(_get_origin)

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
        base = dict(base=self.parentW, em=self.em) # In case relative units, use this as base.
        return units(self.style.get('rx', 0), base=base)

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
        base = dict(base=self.parentH, em=self.em) # In case relative units, use this as base.
        return units(self.style.get('ry', 0), base=base)

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
        base = dict(base=self.parentD, em=self.em) # In case relative units, use this as base.
        return units(self.style.get('rz', 0), base=base)

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

    # @@@ NOT YET
    # FIX-ME: The 'timers' var below is undefined. Was it intended to be self.timeMarks perhaps ?
    #
    #def NOTNOW_getExpandedTimeMarks(self, t):
    #    """Answers a new interpolated TimeState instance, from the enclosing time states for t."""
    #    timeValueNames = self.timeKeys
    #    rootStyleKeys = self.timeMarks[0].keys()
    #    for n in range(1, len(timers)):
    #        tm0 = self.timeMarks[timers[n-1]]
    #        if t < tm0.t:
    #            continue
    #        tm1 = self.timeMarks[timers[n]]
    #        futureTimers = timers[n:]
    #        pastTimers = timers[:n-1]
    #        for rootStyleKey in rootStyleKeys:
    #            if not rootStyleKey in tm1.style:
    #                for futureTime in futureTimers:
    #                    futureTimeMark = self.timeMarks[futureTime]
    #                    if rootStyleKey in futureTimeMark.style:
    #                        tm1.style[rootStyleKey] = futureTimeMark.style[rootStyleKey]
    #
    #        return tm0, tm1
    #    raise ValueError

    # Origin compensated by alignment. This is used for easy solving of conditions,
    # where the positioning can be compenssaring the element alignment type.

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
        """Answer left position, including left margin of self

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
            if self.originTop:
                return self.y - self.h/2
            return self.y + self.h/2
        if yAlign == BOTTOM:
            if self.originTop:
                return self.y - self.h
            return self.y + self.h
        # yAlign must be TOP or None
        return self.y
    def _set_top(self, y):
        """Shift the element so `self.top == y`. Where the "top" is, depends on
        the setting of `self.yAlign`. If `self.isTextBox`, then vertical
        position can also be defined by the top or bottom position of the
        baseline."""
        yAlign = self.yAlign

        if yAlign == MIDDLE:
            if self.originTop:
                self.y = units(y) + self.h/2
            else:
                self.y = units(y) - self.h/2
        elif yAlign == BOTTOM:
            if self.originTop:
                self.y = units(y) + self.h
            else:
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
        if self.originTop:
            return   - self.mt
        return self.top + self.mt
    def _set_mTop(self, y):
        if self.originTop:
            self.top = units(y) + self.mt
        else:
            self.top = units(y) - self.mt
    mTop = property(_get_mTop, _set_mTop)

    def _get_middle(self):
        """On bounding box, not including margins.

        >>> e = Element(y=100, h=248, yAlign=TOP, originTop=True)
        >>> e.middle
        224pt
        >>> e.yAlign = BOTTOM
        >>> e.middle
        -24pt
        >>> e.yAlign = MIDDLE
        >>> e.middle
        100pt

        >>> e = Element(y=100, h=248, yAlign=TOP, originTop=False)
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
            if self.originTop:
                return self.y + self.h/2
            return self.y - self.h/2
        if yAlign == BOTTOM:
            if self.originTop:
                return self.y - self.h/2
            return self.y + self.h/2
        return self.y
    def _set_middle(self, y):
        yAlign = self.yAlign
        if yAlign == TOP:
            if self.originTop:
                self.y = y - self.h/2
            else:
                self.y = y + self.h/2
        elif yAlign == BOTTOM:
            if self.originTop:
                self.y = y + self.h/2
            else:
                self.y = y - self.h/2
        else:
            self.y = y
    middle = property(_get_middle, _set_middle)

    def _get_bottom(self):
        """On bounding box, not including margins.

        >>> e = Element(h=500, originTop=True, yAlign=TOP)
        >>> e.bottom
        500pt
        >>> e.yAlign = MIDDLE
        >>> e.bottom
        250pt
        >>> e.yAlign = BOTTOM
        >>> e.bottom
        0pt
        >>> e.bottom = 300
        >>> e.bottom
        300pt
        """
        yAlign = self.yAlign
        if yAlign == TOP:
            if self.originTop:
                return self.y + self.h
            return self.y - self.h
        if yAlign == MIDDLE:
            if self.originTop:
                return self.y + self.h/2
            return self.y - self.h/2
        return self.y
    def _set_bottom(self, y):
        yAlign = self.yAlign
        if yAlign == TOP:
            if self.originTop:
                self.y = units(y) - self.h
            else:
                self.y = units(y) + self.h
        elif yAlign == MIDDLE:
            if self.originTop:
                self.y = units(y) - self.h/2
            else:
                self.y = units(y) + self.h/2
        else:
            self.y = y
    bottom = property(_get_bottom, _set_bottom)

    def _get_mBottom(self): # Bottom, including bottom margin
        if self.originTop:
            return self.bottom + self.mb
        return self.bottom - self.mb
    def _set_mBottom(self, y):
        if self.originTop:
            self.bottom = units(y) - self.mb
        else:
            self.bottom = units(y) + self.mb
    mBottom = property(_get_mBottom, _set_mBottom)

    # Depth, running  in vertical z-axis dirction. Viewer is origin, positive
    # value is perpendicular into the screen.
    # Besides future usage in real 3D rendering, the z-axis is used to compare
    # conditional status in element layers.

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

    def _get_mBack(self): # Front, including front margin
        return self.back - self.css('mzb')
    def _set_mBack(self, z):
        self.back = units(z) - self.css('mzb')
    mBack = property(_get_mBack, _set_mBack)

    # Colors for fill and stroke

    def _get_fill(self):
        u"""Fill color property in style, using self.css to query cascading values.
        Setting the color will overwrite the cascade, by storing as local value.

        >>> e = Element(fill=color('red'))
        >>> e.fill
        Color(name="red")
        >>> e.fill = 1, 0, 0 # Construct color from tuple
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
        u"""Fill color property in style, using self.css to query cascading values.
        Setting the color will overwrite the cascade, by storing as local value.

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
        u"""Stroke width property in style, using self.css to query cascading values.
        Setting the color will overwrite the cascade, by storing as local value.

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

    # Borders (equivalent for element stroke and strokWidth)

    def getBorderDict(self, stroke=None, strokeWidth=None, line=None, dash=None, border=None):
        """Internal method to create a dictionary with border info. If no valid
        border dictionary is defined, then use optional stroke and strokeWidth
        to create one. Otherwise answer *None*."""

        if border is False:
            return {}
        if isinstance(border, dict):
            return border
        if isinstance(border, (int, float)): # If number, assume it is strokeWidth
            strokeWidth = units(border)

        if stroke is None:
            stroke = self.css('stroke', blackColor)
        #if strokeWidth is None:
        #    strokeWidth = self.strokeWidth # Take current stroke width setting in css
        if line is None:
            line = ONLINE
        # Dash can be None
        if not strokeWidth: # If 0, then answer an empty dict
            return {}
        return dict(stroke=stroke, strokeWidth=units(strokeWidth), line=line, dash=dash)

    def _get_borders(self):
        u"""Set all borders of the element.

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

    def _validateXAlign(self, xAlign): # Check and answer value
        assert xAlign in XALIGNS, '[%s.xAlign] Alignment "%s" not valid in %s' % (self.__class__.__name__, xAlign, XALIGNS)
        return xAlign
    def _validateYAlign(self, yAlign): # Check and answer value
        assert yAlign in YALIGNS, '[%s.yAlign] Alignment "%s" not valid in %s' % (self.__class__.__name__, yAlign, YALIGNS)
        return yAlign
    def _validateZAlign(self, zAlign): # Check and answer value
        assert zAlign in ZALIGNS, '[%s.zAlign] Alignment "%s" not valid in %s' % (self.__class__.__name__, zAlign, ZALIGNS)
        return zAlign

    def _get_xAlign(self): # Answer the type of x-alignment. For compatibility allow align and xAlign as equivalents.
        return self._validateXAlign(self.css('xAlign'))
    def _set_xAlign(self, xAlign):
        self.style['xAlign'] = self._validateXAlign(xAlign) # Save locally, blocking CSS parent scope for this param.
    xAlign = property(_get_xAlign, _set_xAlign)

    def _get_yAlign(self): # Answer the type of y-alignment.
        return self._validateYAlign(self.css('yAlign'))
    def _set_yAlign(self, yAlign):
        self.style['yAlign'] = self._validateYAlign(yAlign) # Save locally, blocking CSS parent scope for this param.
    yAlign = property(_get_yAlign, _set_yAlign)

    def _get_zAlign(self): # Answer the type of z-alignment.
        return self._validateZAlign(self.css('zAlign'))
    def _set_zAlign(self, zAlign):
        self.style['zAlign'] = self._validateZAlign(zAlign) # Save locally, blocking CSS parent scope for this param.
    zAlign = property(_get_zAlign, _set_zAlign)


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
        Elements will take care of the reposition/scaling themselves

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
        Elements will take care of the reposition/scaling themselves.

        >>> from pagebot.toolbox.units import mm
        >>> e = Element(bleedTop=20)
        >>> e.bleedTop
        20pt
        >>> e.bleed = 6
        >>> e.bleedTop = mm(5)
        >>> e.bleed
        (5mm, 6pt, 6pt, 6pt)
        """
        base = dict(base=self.h, em=self.em) # In case relative units, use this as base.
        return units(self.css('bleedTop', 0), base=base)
    def _set_bleedTop(self, bleed):
        self.style['bleedTop'] = units(bleed, default=0)
    bleedTop = property(_get_bleedTop, _set_bleedTop)

    def _get_bleedBottom(self):
        """Answers the value for bleed over the sides of parent or page objects.
        Elements will take care of the reposition/scaling themselves.

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
        """Answers the value for bleed over the sides of parent or page objects.
        Elements will take care of the reposition/scaling themselves.

        >>> from pagebot.toolbox.units import mm
        >>> e = Element(bleedLeft=20)
        >>> e.bleedLeft
        20pt
        >>> e.bleed = 6
        >>> e.bleedLeft = mm(5)
        >>> e.bleed
        (6pt, 6pt, 6pt, 5mm)
        """
        base = dict(base=self.w, em=self.em) # In case relative units, use this as base.
        return units(self.css('bleedLeft', 0), base=base)
    def _set_bleedLeft(self, bleed):
        self.style['bleedLeft'] = units(bleed, default=0)
    bleedLeft = property(_get_bleedLeft, _set_bleedLeft)

    def _get_bleedRight(self):
        """Answers the value for bleed over the sides of parent or page objects.
        Elements will take care of the reposition/scaling themselves.

        >>> from pagebot.toolbox.units import mm
        >>> e = Element(bleedRight=20)
        >>> e.bleedRight
        20pt
        >>> e.bleed = 21
        >>> e.bleedRight = mm(5)
        >>> e.bleed
        (21pt, 5mm, 21pt, 21pt)
        """
        base = dict(base=self.w, em=self.em) # In case relative units, use this as base.
        return units(self.css('bleedRight', 0), base=base)
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

        >>> from pagebot.toolbox.units import p
        >>> e = Element(bleed=p(1), xAlign=LEFT, yAlign=TOP, originTop=True)
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
            if self.originTop:
                oy -= self.bleedTop
            else:
                oy += self.bleedTop
        elif self.yAlign == BOTTOM:
            if self.originTop:
                oy += self.bleedBottom
            else:
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
            return self.z + parent.rootZ # Add relative self to parents position.
        return self.z
    rootZ = property(_get_rootZ)

    # (w, h, d) size of the element.

    def _get_proportional(self):
        """Get/set the proportional style flag as property. If True, setting self.w or self.h
        will keep the original proportions, but setting the other side as well.
        By default the self.proportional flag is False for most types of elements.

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
        >>> child.w, child.w.pt
        (4.5em, 45)
        """
        base = dict(base=self.parentW, em=self.em) # In case relative units, use this as base.
        return units(self.css('w'), base=base)
    def _set_w(self, w):
        w = units(w or DEFAULT_WIDTH)
        if self.proportional:
            if self.w:
                self.style['h'] = w * self.h.pt/self.w.pt
                self.style['d'] = w * self.d.pt/self.w.pt
        self.style['w'] = w # Overwrite element local style from here, parent css becomes inaccessable.

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
        >>> child.h.base
        440pt
        >>> #FIX child.h, child.h.ru, child.h.rv
        (20%, 88pt, 88)
        >>> e.style['fontSize'] = 12
        >>> child.h = '4.5em' # Multiplication with current e.style['fontSize']
        >>> child.h, child.h.pt
        (4.5em, 54)
        >>> e.h = 0 # Zero height expands to DEFAULT_HEIGHT (100)
        >>> e.h, e.h == DEFAULT_HEIGHT
        (100pt, True)
        """
        base = dict(base=self.parentH, em=self.em) # In case relative units, use this as base.
        return units(self.css('h', 0), base=base)
    def _set_h(self, h):
        h = units(h or DEFAULT_HEIGHT)
        if self.proportional:
            if self.h:
                self.style['w'] = h * self.w.pt/self.h.pt
                self.style['d'] = h * self.d.pt/self.h.pt
        self.style['h'] = h # Overwrite element local style from here, parent css becomes inaccessable.
    h = property(_get_h, _set_h)

    def _get_mh(self): # Height, including margins
        """Height property for self.mh style.
        Note that since the margins are not considered by the self.proportional flag,
        changed in self.mw, self.mh and self.md may not stay proportional.

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
        >>> e.d # Default value
        100pt
        >>> e = Element(d=100) # Set min/max of element with constructor
        >>> e.d = 101 # Set depth value
        >>> e.d
        101pt
        """
        base = dict(base=self.parentD, em=self.em) # In case relative units, use this as base.
        return units(self.css('d', 0), base=base)
    def _set_d(self, d):
        self.style['d'] = units(d or DEFAULT_DEPTH) # Overwrite element local style from here, parent css becomes inaccessable.
        d = units(d or DEFAULT_DEPTH)
        if self.proportional:
            if self.d:
                self.style['w'] = d * self.w.pt/self.d.pt
                self.style['h'] = d * self.h/self.d
        self.style['d'] = d # Overwrite element local style from here, parent css becomes inaccessable.
    d = property(_get_d, _set_d)

    def _get_md(self): # Depth, including margin front and margin back in z-axis.
        """Width property for self.md style.
        Note that since the margins are not considered by the self.proportional flag,
        changed in self.mw, self.mh and self.md may not stay proportional.

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
        """List if [(x, y), ...] (one of them can be None) that indicate the position of folding lines
        on a page. In general this is a view parameter (applying to all pages), but it can
        be overwritten by individual pages or other elements, if their folding pattern is different.
        The position of folds is ignored by self.w and self.h. It is mostly to show folding markers
        by PageView. The fold property is stored ins tyle and not inherited."""
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
        base = dict(base=self.h, em=self.em) # In case relative units, use this as base.
        return units(self.css('mt', 0), base=base)
    def _set_mt(self, mt):
        self.style['mt'] = units(mt or 0)  # Overwrite element local style from here, parent css becomes inaccessable.
    mt = property(_get_mt, _set_mt)

    def _get_mb(self): # Margin bottom
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
        base = dict(base=self.w, em=self.em) # In case relative units, use this as base.
        return units(self.css('mr', 0), base=base)
    def _set_mr(self, mr):
        self.style['mr'] = units(mr) # Overwrite element local style from here, parent css becomes inaccessable.
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
        base = dict(base=self.d, em=self.em) # In case relative units, use this as base.
        return units(self.css('mzb', 0), base=base)
    def _set_mzb(self, mzb):
        self.style['mzb'] = units(mzb)  # Overwrite element local style from here, parent css becomes inaccessable.
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
        >>> e.padding, ru(e.padding), rv(e.padding)
        ((10%, 10%, 10%, 10%), (50pt, 50pt, 50pt, 50pt), (50, 50, 50, 50))
        >>> e.padding = perc(15)
        >>> e.padding, ru(e.padding), rv(e.padding)
        ((15%, 15%, 15%, 15%), (75pt, 75pt, 75pt, 75pt), (75, 75, 75, 75))
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
        >>> e.padding3D, ru(e.padding3D), rv(e.padding3D)
        ((10%, 10%, 10%, 10%, 10%, 10%), (50pt, 50pt, 50pt, 50pt, 50pt, 50pt), (50, 50, 50, 50, 50, 50))
        >>> e.padding3D = perc(15)
        >>> e.padding3D, ru(e.padding3D), rv(e.padding3D)
        ((15%, 15%, 15%, 15%, 15%, 15%), (75pt, 75pt, 75pt, 75pt, 75pt, 75pt), (75, 75, 75, 75, 75, 75))
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
        >>> e.pt = 13 # Default conversion from numberts to points
        >>> e.pt
        13pt
        >>> e.pt = pt(14)
        >>> e.pt
        14pt
        >>> e.padding # Verify that other padding did not change.
        (14pt, 0pt, 0pt, 0pt)
        >>> e.pt = '10%'
        >>> e.pt, e.pt.pt # e.pt is abbreviation for padding-top. .pt is the property that converts to points.
        (10%, 50)
        """
        base = dict(base=self.h, em=self.em) # In case relative units, use this as base.
        return units(self.css('pt', 0), base=base)
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
        >>> e.pb.pt # 10% of base 500pt
        50
        """
        base = dict(base=self.h, em=self.em) # In case relative units, use this as base.
        return units(self.css('pb', 0), base=base)
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
        base = dict(base=self.w, em=self.em) # In case relative units, use this as base.
        return units(self.css('pl', 0), base=base)
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
        >>> e.pr.pt # Get padding-right, cast to points
        50
        """
        base = dict(base=self.w, em=self.em) # In case relative units, use this as base.
        return units(self.css('pr', 0), base=base)
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
        >>> e2.pzf.pt # Padding-front, cast to point
        50
        """
        base = dict(base=self.d, em=self.em) # In case relative units, use this as base.
        return units(self.css('pzf', 0), base=base)
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
        >>> e2.pzb.pt
        50
        """
        base = dict(base=self.d, em=self.em) # In case relative units, use this as base.
        return units(self.css('pzb', 0), base=base)
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
        >>> e.pl, e.pl.pt, e.pr, e.pr.pt
        (10%, 40, 10%, 40)
        >>> e.pw
        320pt
        """
        return self.w - self.pl - self.pr
    pw = property(_get_pw)

    def _get_ph(self):
        """Padded height (space between the vertical paddings) read-only property of the element block.

        >>> e = Element(h=400, pb=22, pt=33)
        >>> e.ph
        345pt
        >>> e.pb = e.pt = '10%'
        >>> e.pb, e.pb.pt, e.pt, e.pt.pt # e.pt is Abbreviation of padding-top, .pt is points
        (10%, 40, 10%, 40)
        >>> e.ph
        320pt
        """
        return self.h - self.pb - self.pt
    ph = property(_get_ph)

    def _get_pd(self):
        """Padded depth read-only property of the element block. Answer the distance between depth padding.

        >>> e = Element(d=400, pzf=22, pzb=33)
        >>> e.pd
        345pt
        >>> e.pzf = e.pzb = '10%'
        >>> e.pzf, e.pzf.pt, e.pzb, e.pzb.pt
        (10%, 40, 10%, 40)
        >>> e.pd
        320pt
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
        """Property answer the element frameDuration parameters, used for speed
        when exporting animated gifs. Normally only set in page or document."""
        return self.css('frameDuration')
    def _set_frameDuration(self, frameDuration):
        self.style['frameDuration'] = frameDuration # Overwrite as local value.
    frameDuration = property(_get_frameDuration, _set_frameDuration)

    def _get_originTop(self):
        """Answers the style flag if all point y values should measure top-down
        (typographic page orientation), instead of bottom-up (mathematical
        orientation). For Y-axis only. The axes in X and Z directions are
        fixed. The value is stored on page level, so there is no origin top/down
        switching possible inside the element tree of a page.
        Note that by changing, the position of existing glyphs does NOT change,
        so their (x,y) position changes (unless referred to by side positions
        such as e.top and e.center, etc.).

        Position of origin. DrawBot has y on bottom-left. In PageBot it is
        optional. Default is top-left. Note that the direcion of display is
        always upwards. This means that the position of text and elements
        goes downward from the top, they are not flipped vertical. It is up
        to the caller to make sure there is enough space for elements to show
        themselves on top of a given position. originTop often goes with

        >>> e1 = Element()
        >>> e1.originTop # Undefined by default, means that origin is at bottom left.
        False
        >>> e1 = Element(originTop=True)
        >>> e1.originTop
        True
        >>> e2 = Element(parent=e1, originTop=False)
        >>> e2.originTop # Overwritten by inherited parent.originTop
        True
        """
        if self.parent is not None: # Only interested in the flag on top of tree or on page level
            return self.parent.originTop
        return self._originTop
    originTop = property(_get_originTop)

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
        >>> child.w.pt, child.size[0].pt # Render to pt by 20% of parent.w --> 0.2 * 660 = 132
        (132, 132)
        """
        return self.w, self.h
    def _set_size(self, size):
        saveFlag = self.proportional # Disable the flag, we want to set the values independently
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
    size3D = property(_get_size3D, _set_size) # Setting is idential for self.size3D and self.size

    #   S H A D O W   &  G R A D I E N T

    def _get_shadow(self):
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
        if self.originTop:
            y = self.y + mt
        else:
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
        >>> e.paddedBox
        ((50pt, 50pt), (400pt, 400pt))
        >>> ru(e.paddedBox)
        ((50pt, 50pt), (400pt, 400pt))
        >>> rv(e.paddedBox)
        ((50, 50), (400, 400))
        """
        pl = self.pl
        pt = self.pt # pt is abbreviation from padding-top here, not points.
        pb = self.pb
        if self.originTop:
            y = self.y - pt
        else:
            y = self.y + pb
        return (self.x + pl, y), (self.w - pl - self.pr, self.h - pt - pb)
    paddedBox = property(_get_paddedBox)

    def _get_paddedBox3D(self):
        """Calculate the padded position and padded resized box in 3D of the lement, after applying
        the style padding. Answered format (x, y, z, w, h, d).

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
        >>> e.paddedBox3D
        ((50pt, 50pt, 50pt), (400pt, 400pt, 400pt))
        >>> ru(e.paddedBox3D)
        ((50pt, 50pt, 50pt), (400pt, 400pt, 400pt))
        >>> rv(e.paddedBox3D)
        ((50, 50, 50), (400, 400, 400))
        """
        (x, y), (w, h) = self.paddedBox
        pzf = self.pzf
        return (x, y, self.z + pzf), (w, h, self.d - pzf - self.pzb)
    paddedBox3D = property(_get_paddedBox3D)

    # PDF naming: MediaBox is highlighted with a magenta rectangle, the BleedBox with a cyan
    # one while dark blue is used for the TrimBox.
    # https://www.prepressure.com/pdf/basics/page-boxes

    # "Box" is bounding box on a single element.
    # "Block" is here used as bounding box of a group of elements or otherwise the wrapped bounding box on self context.

    def _get_block3D(self):
        """Answers the vacuum 3D bounding box around all child elements, including margin.

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
            # No element, answer vacuum block (x, y, z), (w, h, d)
            return pt(0, 0, 0), pt(0, 0, 0)
        for e in self.elements:
            x1 = min(x1, e.left)
            x2 = max(x2, e.right)
            if e.originTop:
                y1 = min(y1, e.mTop)
                y2 = max(y2, e.mBottom)
            else:
                y1 = min(y1, e.mBottom)
                y2 = max(y2, e.mTop)
            z1 = min(z1, e.front)
            z2 = max(z2, e.back)

        return (x1, y1, z1), (x2 - x1, y2 - y1, z2 - z1)
    block3D = property(_get_block3D)

    def _get_block(self):
        """Answers the vacuum bounding box around all child elements in 2D, including margin

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
            # No element, answer vacuum block (x, y, z), (w, h, d)
            return pt(0, 0, 0), pt(0, 0, 0)
        for e in self.elements:
            x1 = max(x1, e.left + e.pl)
            x2 = min(x2, e.right - e.pl)
            if e.originTop:
                y1 = max(y1, e.top + e.pt)
                y2 = min(y2, e.bottom - e.pb)
            else:
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
        """Answer the 2-tuple of (self.scaleX, self.scaleY)
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

    def getFloatTopSide(self, previousOnly=True, tolerance=0):
        """Answers the max y that can float to top, without overlapping previous
        sibling elements. This means we are just looking at the vertical
        projection between (self.mLeft, self.mRight). Note that the y may be
        outside the parent box. Only elements with identical z-value are
        compared. Comparison of available space, includes the margins of the
        elements."""
        if self.originTop:
            y = 0
        else:
            y = self.parent.h
        for e in self.parent.elements:
            if previousOnly and e is self: # Only look at siblings that are previous in the list.
                break
            if abs(e.z - self.z) > tolerance or e.mRight < self.mLeft or self.mRight < e.mLeft:
                continue # Not equal z-layer or not in window of vertical projection.
            if self.originTop:
                y = max(y, e.mBottom)
            else:
                y = min(y, e.mBottom)
        return y

    def getFloatBottomSide(self, previousOnly=True, tolerance=0):
        """Answers the max y that can float to bottom, without overlapping
        previous sibling elements. This means we are just looking at the
        vertical projection of (self.mLeft, self.mRight). Note that the y may be
        outside the parent box. Only elements with identical z-value are
        compared. Comparison of available space, includes the margins of the
        elements."""
        if self.originTop:
            y = self.parent.h
        else:
            y = 0
        for e in self.parent.elements: # All elements that share self.parent, except self.
            if previousOnly and e is self: # Only look at siblings that are previous in the list.
                break
            if abs(e.z - self.z) > tolerance or e.mRight < self.mLeft or self.mRight < e.mLeft:
                continue # Not equal z-layer or not in window of vertical projection.
            if self.originTop:
                y = min(y, e.mTop)
            else:
                y = max(y, e.mTop)
        return y

    def getFloatLeftSide(self, previousOnly=True, tolerance=0):
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
            if self.originTop: # not in window of horizontal projection.
                if e.mBottom <= self.mTop or self.mBottom <= e.mTop:
                    continue
            else:
                if e.mBottom >= self.mTop or self.mBottom >= e.mTop:
                    continue
            x = max(e.mRight, x)
        return x

    def getFloatRightSide(self, previousOnly=True, tolerance=0):
        """Answers the max Y that can float to the right, without overlapping
        previous sibling elements.  This means we are just looking at the
        vertical projection of (self.mLeft, self.mRight).  Note that the y may be
        outside the parent box. Only elements with identical z-value are
        compared.  Comparison of available space, includes the margins of the
        elements."""
        x = self.parent.w
        for e in self.parent.elements: # All elements that share self.parent, except self.
            if previousOnly and e is self: # Only look at siblings that are previous in the list.
                break
            if abs(e.z - self.z) > tolerance:
                continue # Not equal z-layer
            if self.originTop: # not in window of horizontal projection.
                if e.mBottom <= self.mTop or self.mBottom <= e.mTop:
                    continue
            else:
                if e.mBottom >= self.mTop or self.mBottom >= e.mTop:
                    continue
            x = min(e.mLeft, x)
        return x

    def _applyAlignment(self, p):
        """Answers the p according to the alignment status in the css."""
        px, py, pz = point3D(p)
        # Horizontal
        xAlign = self.xAlign
        if xAlign == CENTER:
            px -= self.w/2/self.scaleX
        elif xAlign == RIGHT:
            px -= self.w/self.scaleX
        # Vertical
        yAlign = self.yAlign
        if yAlign == MIDDLE:
            py -= self.h/2/self.scaleY
        elif yAlign == TOP:
            py -= self.h/self.scaleY
        # Currently no alignment in z-axis implemented
        return px, py, pz

    def _applyOrigin(self, p):
        """If self.originTop is False, then the y-value is interpreted as
        mathematics, starting at the bottom of the parent element, moving up.
        If the flag is True, then move from top down, where the origin of the
        element becomes top-left of the parent."""
        px, py, pz = point3D(p)
        if self.originTop and self.parent:
            py = self.parent.h - py
        return px, py, pz

    def _applyRotation(self, view, p):
        """Apply the rotation for angle, where (mx, my) is the rotation center."""
        if self.angle:
            px, py, _ = point3D(p)
            self.context.rotate(self.angle, center=(px+self.rx, py+self.ry))

    def _restoreRotation(self, view, p):
        """Reset graphics state from rotation mode."""
        if self.angle:
            px, py, _ = point3D(p)
            self.context.rotate(-self.angle, center=(px+self.rx, py+self.ry))

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
            self.context.saveGraphicState()
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
        if sx and sy and sz and (sx != 1 or sy != 1 or sz != 1): # Make sure these are value scale values.
            self.context.restoreGraphicState()

    #   S P E L L  C H E C K

    def _spellCheckWords(self, languages, unknown, minLength):
        """Spellcheck the words of self. Default behavior is to do nothing.
        Inheriting classes can redefined this method.
        """
        pass

    def spellCheck(self, languages=None, unknown=None, minLength=3):
        """Recursively spellcheck all child elements for the given languages. Answer a list with
        unknown words. Default is to do nothing and just pass the call on to child elements.
        Inheriting classes can redefine _spellCheckWords to check on their on text content.
        Words with a length smaller than minLength are skipped."""
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
        """Recursively compose Publication, Pages and Elements to compose the document of a publication.
        Default behavior is to just pass it on to the chidren.
        """
        for e in self.elements:
            e.compose(doc, publication)

    #   D R A W I N G  S U P P O R T

    def getMetricsString(self, view=None):
        """Answers a single string with metrics info about the element. Default
        is to show the posiiton and size (in points and columns). This method
        can be redefined by inheriting elements that want to show additional
        information."""
        s = '%s\nPosition: %s, %s, %s\nSize: %s, %s' % \
            (self.__class__.__name__ + ' ' + (self.name or ''),
                asFormatted(self.x), asFormatted(self.y), asFormatted(self.z),
                asFormatted(self.w), asFormatted(self.h)
            )
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
        """Draw fill of the rectangular element space. The self.css('fill')
        defines the color of the element background. Instead of the DrawBot
        stroke and strokeWidth attributes, use borders or (borderTop,
        borderRight, borderBottom, borderLeft) attributes.
        """
        c = view.context
        eShadow = self.shadow

        if eShadow:
            c.saveGraphicState()
            c.setShadow(eShadow)
            c.rect(p[0], p[1], self.w, self.h)
            c.restoreGraphicState()

        eFill = self.fill # Default is npColor
        eStroke = self.css('stroke', default=noColor)
        eGradient = self.gradient

        if eStroke is not noColor or eFill is not noColor or eGradient:
            c.saveGraphicState()

            # Drawing element fill and/or frame
            if eGradient: # Gradient overwrites setting of fill.
                # TODO: Make bleed work here too.
                c.setGradient(eGradient, p, self.w, self.h) # Add self.w and self.h to define start/end from relative size.
            else:
                c.fill(eFill)

            if eStroke is not noColor: # Separate from border behavior if set.
                c.stroke(eStroke, self.css('strokeWidth', pt(1)))

            if self.framePath is not None: # In case defined, use instead of bounding box.
                c.drawPath(self.framePath)
            c.rect(p[0], p[1], self.w, self.h) # Ignore bleed, should already have been applied on position and size.

            c.restoreGraphicState()

        # Instead of full frame drawing, check on separate border settings.
        borderTop = self.borderTop
        borderBottom = self.borderBottom
        borderRight = self.borderRight
        borderLeft = self.borderLeft

        if borderTop is not None:
            c.saveGraphicState()
            c.lineDash(borderTop.get('dash')) # None for no dash
            c.stroke(borderTop.get('stroke', noColor), borderTop.get('strokeWidth', 0))

            oLeft = 0 # Extra offset on left, if there is a left border.

            if borderLeft and (borderLeft.get('strokeWidth') or pt(0)) > 1:
                if borderLeft.get('line') == ONLINE:
                    oLeft = borderLeft.get('strokeWidth', 0)/2
                elif borderLeft.get('line') == OUTLINE:
                    oLeft = borderLeft.get('strokeWidth', 0)

            oRight = 0 # Extra offset on right, if there is a right border.

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

            if self.originTop:
                c.line((p[0]-oLeft, p[1]-oTop), (p[0]+self.w+oRight, p[1]-oTop))
            else:
                c.line((p[0]-oLeft, p[1]+self.h+oTop), (p[0]+self.w+oRight, p[1]+self.h+oTop))
            c.restoreGraphicState()

        if borderBottom is not None:
            c.saveGraphicState()
            c.lineDash(borderBottom.get('dash')) # None for no dash
            c.stroke(borderBottom.get('stroke', noColor), borderBottom.get('strokeWidth', 0))

            oLeft = 0 # Extra offset on left, if there is a left border.
            if borderLeft and (borderLeft.get('strokeWidth') or pt(0)) > 1:
                if borderLeft.get('line') == ONLINE:
                    oLeft = borderLeft.get('strokeWidth', 0)/2
                elif borderLeft.get('line') == OUTLINE:
                    oLeft = borderLeft.get('strokeWidth', 0)

            oRight = 0 # Extra offset on right, if there is a right border.
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

            if self.originTop:
                c.line((p[0]-oLeft, p[1]+self.h+oBottom), (p[0]+self.w+oRight, p[1]+self.h+oBottom))
            else:
                c.line((p[0]-oLeft, p[1]-oBottom), (p[0]+self.w+oRight, p[1]-oBottom))
            c.restoreGraphicState()

        if borderRight is not None:
            c.saveGraphicState()
            c.lineDash(borderRight.get('dash')) # None for no dash
            c.stroke(borderRight.get('stroke', noColor), borderRight.get('strokeWidth', 0))

            oTop = 0 # Extra offset on top, if there is a top border.
            if borderTop and (borderTop.get('strokeWidth') or pt(0)) > 1:
                if borderTop.get('line') == ONLINE:
                    oTop = borderTop.get('strokeWidth', 0)/2
                elif borderLeft.get('line') == OUTLINE:
                    oTop = borderTop.get('strokeWidth', 0)

            oBottom = 0 # Extra offset on bottom, if there is a bottom border.
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

            if self.originTop:
                c.line((p[0]+self.w+oRight, p[1]-oTop), (p[0]+self.w+oRight, p[1]+self.h+oBottom))
            else:
                c.line((p[0]+self.w+oRight, p[1]-oBottom), (p[0]+self.w+oRight, p[1]+self.h+oTop))
            c.restoreGraphicState()

        if borderLeft is not None:
            c.saveGraphicState()
            c.lineDash(borderLeft.get('dash')) # None for no dash
            c.stroke(borderLeft.get('stroke', noColor), borderLeft.get('strokeWidth', 0))

            oTop = 0 # Extra offset on top, if there is a top border.
            if borderTop and (borderTop.get('strokeWidth') or pt(0)) > 1:
                if borderTop.get('line') == ONLINE:
                    oTop = borderTop.get('strokeWidth', 0)/2
                elif borderLeft.get('line') == OUTLINE:
                    oTop = borderTop.get('strokeWidth', 0)

            oBottom = 0 # Extra offset on bottom, if there is a bottom border.
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

            if self.originTop:
                c.line((p[0]-oLeft, p[1]-oTop), (p[0]-oLeft, p[1]+self.h+oBottom))
            else:
                c.line((p[0]-oLeft, p[1]-oBottom), (p[0]-oLeft, p[1]+self.h+oTop))
            c.restoreGraphicState()

    #   D R A W B O T / F L A T  S U P P O R T

    def prepare(self, view):
        """Respond to the top-down element broadcast to prepare for build.
        If the original image needs scaling, then prepare the build by letting the context
        make a new cache file with the scaled images.
        If the cache file already exists, then ignore, just continue the broadcast
        towards the child elements.
        Default behavior is to do nothing. Inheriting Element classes can redefine.
        """
        for e in self.elements:
            e.prepare(view)

    def build(self, view, origin, drawElements=True, **kwargs):
        """Default drawing method just drawing the frame.
        Probably will be redefined by inheriting element classes."""
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        self._applyRotation(view, p)

        self.buildFrame(view, p) # Draw optional frame or borders.

        # Let the view draw frame info for debugging, in case view.showFrame == True
        # and self.isPage or if self.showFrame. Mark that we are drawing background here.
        view.drawPageMetaInfo(self, p, background=True)

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        # Draw the actual element content.
        # Inheriting elements classes can redefine just this method to fill in drawing behavior.
        # @p is the transformed position to draw in the main canvas.
        self.buildElement(view, p, drawElements, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        # Let the view draw frame info for debugging, in case view.showFrame == True
        # and self.isPage or if self.showFrame. Mark that we are drawing foreground here.
        view.drawPageMetaInfo(self, p, background=False)

        self._restoreRotation(view, p)
        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on flag 'view.showElementInfo'

    def buildElement(self, view, p, drawElements=True, **kwargs):
        """Main drawing method for elements to draw their content and the content
        of their children if they exist.
        @p is the transformed position of the context canvas.
        To be redefined by inheriting element classes that need to draw more than
        just their chold elements.
        """
        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, p, **kwargs)

    def buildChildElements(self, view, origin=None, **kwargs):
        """Draws child elements, dispatching depends on the implementation of
        context specific build elements.

        If no specific builder_<context.b.PB_ID> is implemented, call default
        e.build(view, origin)

        """
        hook = 'build_' + view.context.b.PB_ID

        for e in self.elements:
            if not e.show:
                continue
            if hasattr(e, hook):
                getattr(e, hook)(view, origin, **kwargs)
            else: # No implementation for this context, call default building method for this element.
                e.build(view, origin, **kwargs)

    #   H T M L  /  S C S S / S A S S  S U P P O R T

    # Sass syntax is not supported yet. It does not appear to be standard and cannot be easily
    # converted from existing CSS. Meanwhile, many CSS designers can extend easier to SCSS.

    def prepare_html(self, view):
        """Respond to the top-down view-->element broadcast in preparation for build_html.
        Default behavior is to do nothing other than recursively broadcast to all child element.
        Inheriting Element classes can redefine.
        """
        for e in self.elements:
            e.prepare_html(view)

    def prepare_zip(self, view):
        """Respond to the top-down view-->element broadcast in preparation for build_zip.
        Default behavior is to do nothing other than recursively broadcast to all child element.
        Inheriting Element classes can redefine.
        """
        for e in self.elements:
            e.prepare_zip(view)

    def build_scss(self, view):
        """Build the scss variables for this element."""
        b = self.context.b
        b.build_scss(self, view)
        for e in self.elements:
            if e.show:
                e.build_scss(view)


    def asNormalizedJSON(self):
        """Build self and all child elements as regular dict and add
        it to the list of siblings. Path points to the folder where
        elements can copy additional files, such as images, fonts,
        CSS, JS, etc.). This path will later be converted to zip file,
        as main storage of the current document.

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

    def build_html(self, view, path, drawElements=True, **kwargs):
        """Build the HTML/CSS code through WebBuilder (or equivalent) that is
        the closest representation of self. If there are any child elements,
        then also included their code, using the level recursive indent. For
        HTML builder the origin is ignored, as all position is relative.
        """
        b = view.context.b # Use the current context builder to write the HTML/CSS code.
        if self.htmlCode is not None:
            b.addHtml(self.htmlCode) # Add chunk of defined HTML to output.
        elif self.htmlPaths is not None:
            for htmlPath in self.htmlPaths:
                b.importHtml(htmlPath) # Add HTML content from file, if path is not None and the file exists.
        else:
            b.div(cssClass=self.cssClass, cssId=self.cssId) # No default class, ignore if not defined.

            if self.drawBefore is not None: # Call if defined
                self.drawBefore(self, view)

            # Build child elements, dispatch if they implemented generic or
            # context specific build method.
            if drawElements:
                self.buildChildElements(view, path, **kwargs)

            if self.drawAfter is not None: # Call if defined
                self.drawAfter(self, view)

            b._div()

    #   V A L I D A T I O N

    def evaluate(self, score=None):
        """Evaluate the content of element e with the total sum of conditions."""
        if score is None:
            score = Score()
        if self.conditions: # Can be None or empty
            for condition in self.conditions: # Skip in case there are no conditions in the style.
             condition.evaluate(self, score)
        for e in self.elements: # Also works if showing element is not a container.
            if e.show:
                e.evaluate(score)
        return score

    def solve(self, score=None):
        """Evaluate the content of element e with the total sum of conditions.
        The view is passed, as it (or its builder) may be needed to solve
        specific text conditions, such as run length of text and overflow of
        text boxes."""
        if score is None:
            score = Score()

        # Can be None or empty list. Skip in case there are no conditions in
        # the style.
        if self.conditions:

            for condition in self.conditions:
                condition.solve(self, score)

        # Also works if showing element is not a container.
        for e in self.elements:
            if e.show:
                e.solve(score)

        return score

    #   C O N D I T I O N S

    def isBottomOnBottom(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.h - self.parent.pb - self.mBottom) <= tolerance
        return abs(self.parent.pb - self.mBottom) <= tolerance

    def isBottomOnBottomSide(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.h - self.mBottom) <= tolerance
        return abs(self.mBottom) <= tolerance

    def isBottomOnBottomBleed(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.h - self.mBottom + self.bleedBottom) <= tolerance
        return abs(self.mBottom - self.bleedBottom) <= tolerance

    def isBottomOnTop(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.pt - self.mBottom) <= tolerance
        return abs(self.parent.h - self.parent.pt - self.mBottom) <= tolerance

    def isCenterOnCenter(self, tolerance=0):
        pl = self.parent.pl # Get parent padding left
        center = (self.parent.w - self.parent.pr - pl)/2
        return abs(pl + center - self.center) <= tolerance

    def isCenterOnCenterSides(self, tolerance=0):
        return abs(self.parent.w/2 - self.center) <= tolerance

    def isCenterOnLeft(self, tolerance=0):
        return abs(self.parent.pl - self.center) <= tolerance

    def isCenterOnRight(self, tolerance=0):
        return abs(self.parent.w - self.parent.pr - self.center) <= tolerance

    def isCenterOnRightSide(self, tolerance=0):
        return abs(self.parent.w - self.center) <= tolerance

    def isMiddleOnBottom(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.h - self.parent.pb - self.middle) <= tolerance
        return abs(self.parent.pb - self.middle) <= tolerance

    def isMiddleOnBottomSide(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.h - self.middle) <= tolerance
        return abs(self.middle) <= tolerance

    def isMiddleOnTop(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.pt - self.middle) <= tolerance
        return abs(self.parent.h - self.parent.pt - self.middle) <= tolerance

    def isMiddleOnTopSide(self, tolerance=0):
        if self.originTop:
            return abs(self.middle) <= tolerance
        return abs(self.parent.h - self.middle) <= tolerance

    def isMiddleOnMiddle(self, tolerance=0):
        pt = self.parent.pt # Get parent padding top
        pb = self.parent.pb
        middle = (self.parent.h - pt - pb)/2
        if self.originTop:
            return abs(pt + middle - self.middle) <= tolerance
        return abs(pb + middle - self.middle) <= tolerance

    def isMiddleOnMiddleSides(self, tolerance=0):
        if self.originTop:
            return abs(self.middle) <= tolerance
        return abs(self.parent.h - self.middle) <= tolerance

    def isLeftOnCenter(self, tolerance=0):
        pl = self.parent.pl # Get parent padding left
        center = (self.parent.w - self.parent.pr - pl)/2
        return abs(pl + center - self.mLeft) <= tolerance

    def isLeftOnCenterSides(self, tolerance=0):
        return abs(self.parent.w/2 - self.mLeft) <= tolerance

    def isLeftOnLeft(self, tolerance=0):
        return abs(self.parent.pl - self.mLeft) <= tolerance

    def isLeftOnLeftSide(self, tolerance=0):
        return abs(self.mLeft) <= tolerance

    def isLeftOnLeftBleed(self, tolerance=0):
        return abs(self.mLeft + self.bleedLeft) <= tolerance

    def isLeftOnRight(self, tolerance=0):
        return abs(self.parent.w - self.parent.pr - self.mLeft) <= tolerance

    def isLeftOnRightSide(self, tolerance=0):
        return abs(self.parent.w - self.mLeft) <= tolerance

    def isCenterOnLeftSide(self, tolerance=0):
        return abs(self.parent.mLeft - self.center) <= tolerance

    def isTopOnMiddle(self, tolerance=0):
        pt = self.parent.pt # Get parent padding top
        pb = self.parent.pb
        middle = (self.parent.h - pb - pt)/2
        if self.originTop:
            return abs(pt + middle - self.mTop) <= tolerance
        return abs(pb + middle - self.mTop) <= tolerance

    def isTopOnMiddleSides(self, tolerance=0):
        return abs(self.parent.h/2 - self.mTop) <= tolerance

    def isOriginOnBottom(self, tolerance=0):
        pb = self.parent.pb # Get parent padding left
        if self.originTop:
            return abs(self.parent.h - pb - self.y) <= tolerance
        return abs(pb - self.y) <= tolerance

    def isOriginOnBottomSide(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.h - self.y) <= tolerance
        return abs(self.y) <= tolerance

    def isOriginOnCenter(self, tolerance=0):
        pl = self.parent.pl # Get parent padding left
        center = (self.parent.w - self.parent.pr - pl)/2
        return abs(pl + center - self.x) <= tolerance

    def isOriginOnCenterSides(self, tolerance=0):
        return abs(self.parent.w/2 - self.x) <= tolerance

    def isOriginOnLeft(self, tolerance=0):
        return abs(self.parent.pl - self.x) <= tolerance

    def isOriginOnLeftSide(self, tolerance=0):
        return abs(self.x) <= tolerance

    def isOriginOnRight(self, tolerance=0):
        return abs(self.parent.w - self.parent.pr - self.x) <= tolerance

    def isOriginOnRightSide(self, tolerance=0):
        return abs(self.parent.w - self.x) <= tolerance

    def isOriginOnTop(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.pt - self.y) <= tolerance
        return abs(self.parent.h - self.parent.pt - self.y) <= tolerance

    def isOriginOnTopSide(self, tolerance=0):
        """Answers the boolean test if the origin of self is on the top side of
        self.parent.

        >>> e1 = Element(w=200, h=400)
        >>> e2 = Element(w=50, h=50, parent=e1)
        >>> #FIX e1.isOriginOnTopSide()
        False
        >>> #FIX e2.isOriginOnTopSide()
        False
        >>> e2.y = e1.top
        >>> #FIX e2.isOriginOnTopSide(), e2.y, e1.top
        (True, 500pt, 500pt)
        """
        if self.parent is None:
            return False
        return abs(self.parent.top - self.y) <= tolerance

    def isOriginOnMiddle(self, tolerance=0):
        """Answers the boolean test if the origin of self is on the top side of
        self.parent.

        >>> e1 = Element(w=200, h=400)
        >>> e2 = Element(w=50, h=50, parent=e1)
        >>> e1.isOriginOnMiddle()
        False
        >>> #FIX e2.isOriginOnMiddle()
        False
        >>> e2.y = e1.middle
        >>> #FIX e2.isOriginOnMiddle(), e2.y, e1.middle
        (True, 500pt, 500pt)
        """
        if self.parent is None:
            return False
        return abs(self.parent.middle - self.y) <= tolerance

    def isOriginOnMiddleSides(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.h/2 - self.y) <= tolerance
        return abs(self.parent.h/2 - self.y) <= tolerance

    def isRightOnCenter(self, tolerance=0):
        """Answers if the right size of `self` is on the middle of the parent.

        >>> e1 = Element(x=100, w=200) # e1.right == 300
        >>> e2 = Element(w=600, elements=[e1])

        """
        return abs(self.parent.pl + self.parent.pw/2 - self.mRight) <= tolerance

    def isRightOnCenterSides(self, tolerance=0):
        return abs(self.parent.w/2 - self.mRight) <= tolerance

    def isRightOnLeft(self, tolerance=0):
        return abs(self.parent.pl - self.mRight) <= tolerance

    def isRightOnRight(self, tolerance=0):
        return abs(self.parent.w - self.parent.pr - self.mRight) <= tolerance

    def isRightOnRightSide(self, tolerance=0):
        return abs(self.parent.w - self.mRight) <= tolerance

    def isRightOnRightBleed(self, tolerance=0):
        return abs(self.parent.w + self.bleedLeft) <= tolerance

    def isBottomOnMiddle(self, tolerance=0):
        pt = self.parent.pt # Get parent padding top
        pb = self.parent.pb
        middle = (self.parent.h - pb - pt)/2
        if self.originTop:
            return abs(pt + middle - self.mBottom) <= tolerance
        return abs(pb + middle - self.mBottom) <= tolerance

    def isBottomOnMiddleSides(self, tolerance=0):
        return abs(self.parent.h/2 - self.mBottom) <= tolerance

    def isTopOnBottom(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.h - self.parent.pb - self.mTop) <= tolerance
        return abs(self.parent.pb - self.mTop) <= tolerance

    def isTopOnTop(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.pt - self.mTop) <= tolerance
        return abs(self.parent.h - self.parent.pt - self.mTop) <= tolerance

    def isTopOnTopSide(self, tolerance=0):
        if self.originTop:
            return abs(self.mTop) <= tolerance
        return abs(self.parent.h - self.mTop) <= tolerance

    def isTopOnTopBleed(self, tolerance=0):
        if self.originTop:
            return abs(self.mTop - self.bleedTop) <= tolerance
        return abs(self.parent.h - self.mTop + self.bleedTop) <= tolerance

    # Shrink block conditions

    def isSchrunkOnBlockLeft(self, tolerance):
        boxX, _, _, _ = self.marginBox
        return abs(self.mLeft + self.pl - boxX) <= tolerance

    def isShrunkOnBlockRight(self, tolerance):
        boxX, _, boxW, _ = self.marginBox
        return abs(self.mRight - self.pr - (boxX + boxW)) <= tolerance

    def isShrunkOnBlockTop(self, tolerance):
        _, boxY, _, boxH = self.marginBox
        if self.originTop:
            return abs(self.mTop + self.pt - boxY) <= tolerance
        return self.mTop - self.pt - (boxY + boxH) <= tolerance

    def isShrunkOnBlockBottom(self, tolerance):
        """Test if the bottom of self is shrunk to the bottom position of the block."""
        _, boxY, _, boxH = self.marginBox
        if self.originTop:
            return abs(self.h - self.pb - (boxY + boxH)) <= tolerance
        return abs(self.pb - boxY) <= tolerance

    def isShrunkOnBlockLeftSide(self, tolerance):
        boxX, _, _, _ = self.box
        return abs(self.mLeft - boxX) <= tolerance

    def isShrunkOnBlockRightSide(self, tolerance):
        boxX, _, boxW, _ = self.mbox
        return abs(self.mRight - (boxX + boxW)) <= tolerance

    def isShrunkOnBlockTopSide(self, tolerance):
        _, boxY, _, boxH = self.box
        if self.originTop:
            return abs(self.mTop - boxY) <= tolerance
        return self.mTop - (boxY + boxH) <= tolerance

    def isShrunkOnBlockBottomSide(self, tolerance):
        _, boxY, _, boxH = self.marginBox
        if self.originTop:
            return abs(self.mBottom - (boxY + boxH)) <= tolerance
        return abs(self.mBottom - boxY) <= tolerance

    # Unimplemented here for text operations

    def isShrunkOnTextHeight(self, tolerance=0):
        """For non-text elements, this is always True to satisfy the calling condition."""
        return True

    def shrink2TextHeight(self, tolerance=0):
        """For non-text elements, this is always True to satisfy the calling condition."""
        return True

    def isShrunkOnTextWidth(self, tolerance=0):
        """For non-text elements, this is always True to satisfy the calling condition."""
        return True

    def shrink2TextWidth(self, tolerance=0):
        """For non-text elements, this is always True to satisfy the calling condition."""
        return True

    # Float conditions to page padding

    def isFloatOnTop(self, tolerance=0):
        if self.originTop:
            return abs(max(self.getFloatTopSide(), self.parent.pt) - self.mTop) <= tolerance
        return abs(min(self.getFloatTopSide(), self.parent.h - self.parent.pt) - self.mTop) <= tolerance

    def isFloatOnBottom(self, tolerance=0):
        if self.originTop:
            return abs(min(self.getFloatBottomSide(), self.parent.h - self.parent.pb) - self.mBottom) <= tolerance
        return abs(max(self.getFloatBottomSide(), self.parent.pb) - self.mBottom) <= tolerance

    def isFloatOnLeft(self, tolerance=0):
        return abs(max(self.getFloatLeftSide(), self.parent.pl) - self.mLeft) <= tolerance

    def isFloatOnRight(self, tolerance=0):
        return abs(min(self.getFloatRightSide(), self.parent.w - self.parent.pr) - self.mRight) <= tolerance

    # Float conditions to page sides

    def isFloatOnTopSide(self, tolerance=0):
        return abs(self.getFloatTopSide() - self.mTop) <= tolerance

    def isFloatOnBottomSide(self, tolerance=0):
        return abs(self.getFloatBottomSide() - self.mBottom) <= tolerance

    def isFloatOnLeftSide(self, tolerance=0):
        return abs(self.getFloatLeftSide() - self.mLeft) <= tolerance

    def isFloatOnRightSide(self, tolerance=0):
        return abs(self.getFloatRightSide() - self.mRight) <= tolerance

    #   Column/Row conditions

    def isLeftOnCol(self, col, tolerance):
        """Move top of the element to col index position."""
        gridColumns = self.getGridColumns()
        if col in range(len(gridColumns)):
            return abs(self.mLeft - gridColumns[col][0]) <= tolerance
        return False # row is not in range of gridColumns

    def isRightOnCol(self, col, tolerance):
        """Move top of the element to col index position."""
        gridColumns = self.getGridColumns()
        if col in range(len(gridColumns)):
            return abs(self.mRight - gridColumns[col][0] - self.gw) <= tolerance
        return False # row is not in range of gridColumns

    def isFitOnColSpan(self, col, colSpan, tolerance):
        """Answer the boolean flag if the self.w is the same as the total of
        column widths between col and col+colSpan

        >>> from pagebot.toolbox.units import pt
        >>> gridX = (pt(100, 10), pt(200, 20), pt(300, 30), pt(400, 40), pt(500, 50))
        >>> e1 = Element(padding=30, w=600, gridX=gridX)
        >>> e1.getGridColumns()
        [(0, 100pt), (110pt, 200pt), (330pt, 300pt), (660pt, 400pt), (1100pt, 500pt)]
        >>> e2 = Element(w=100, parent=e1)
        >>> e1.getGridColumns()
        [(0, 100pt), (110pt, 200pt), (330pt, 300pt), (660pt, 400pt), (1100pt, 500pt)]
        >>> e2.isFitOnColSpan(0, 1, 0)
        True
        >>> e2.w = 310
        >>> e2.isFitOnColSpan(0, 2, 0)
        True
        >>> e2.w = 950
        >>> e2.isFitOnColSpan(1, 3, 0)
        True
        """
        gridColumns = self.getGridColumns()
        if col >= 0 and col+colSpan <= len(gridColumns):
            c1 = gridColumns[col]
            c2 = gridColumns[col + colSpan - 1]
            #print(self.w, c2[0] - c1[0] + c2[1])
            return abs(self.w - (c2[0] - c1[0] + c2[1])) <= tolerance
        return False

    def isTopOnRow(self, row, tolerance):
        """Move top of the element to row."""
        gridRows = self.getGridRows()
        if row in range(len(gridRows)):
            return abs(self.mTop - gridRows[row][0]) <= tolerance
        return False # row is not in range of gridColumns

    def isBottomOnRow(self, row, tolerance):
        """Move top of the element to row."""
        gridRows = self.getGridRows()
        if row in range(len(gridRows)):
            return abs(self.mBottom - gridRows[row][0]) <= tolerance
        return False # row is not in range of gridColumns

    def isFitOnRowSpan(self, row, rowSpan, tolerance):
        gridRows = self.getGridRows()
        if row >= 0 and row+rowSpan < len(gridRows):
            r1 = gridRows[row]
            r2 = gridRows[row + rowSpan - 1]
            return abs(self.h - (r2[0] - r1[0] + r2[1])) <= tolerance
        return False

    #   T R A N S F O R M A T I O N S

    #   Column/Row alignment

    def left2Col(self, col):
        """Move top of the element to col index position."""
        gridColumns = self.getGridColumns()
        if col in range(len(gridColumns)):
            self.mLeft = self.parent.pl + gridColumns[col][0] # @@@ FIX GUTTER
            return True
        return False # Row is not in range of available gridColumns

    def right2Col(self, col):
        """Move right of the element to col index position."""
        gridColumns = self.getGridColumns()
        if col in range(len(gridColumns)):
            self.mRight = self.parent.pl + gridColumns[col][0] - self.gw
            return True
        return False # Row is not in range of available gridColumns

    def fit2ColSpan(self, col, colSpan):
        """Fit the width of self to colSpan (can run over several columns),
        starting at column index col.

        >>> from pagebot.toolbox.units import pt
        >>> gridX = (pt(100, 10), pt(200, 20), pt(300, 30), pt(400, 40), pt(500, 50))
        >>> e1 = Element(padding=30, w=600, gridX=gridX)
        >>> e1.getGridColumns()
        [(0, 100pt), (110pt, 200pt), (330pt, 300pt), (660pt, 400pt), (1100pt, 500pt)]
        >>> e2 = Element(w=100, parent=e1)
        >>> e2.isFitOnColSpan(1, 3, 0), e2.w
        (False, 100pt)
        >>> e2.fit2ColSpan(1, 3)
        True
        >>> e2.isFitOnColSpan(1, 3, 0), e2.w
        (True, 950pt)
        """
        gridColumns = self.getGridColumns()
        if col >= 0 and col+colSpan <= len(gridColumns):
            c1 = gridColumns[col]
            c2 = gridColumns[col + colSpan - 1]
            self.w = c2[0] - c1[0] + c2[1]
            return True
        return False

    def top2Row(self, row):
        """Move top of the element to row."""
        gridRows = self.getGridRows()
        if row in range(len(gridRows)):
            self.mTop = self.parent.pb + gridRows[row][0] # @@@ FIX GUTTER
            return True
        return False # row is not in range of gridColumns

    def bottom2Row(self, row):
        """Move top of the element to row."""
        gridRows = self.getGridRows()
        if row in range(len(gridRows)):
            self.mBottom = self.parent.pb + gridRows[row][0] # @@@ FIX GUTTER
            return True
        return False # row is not in range of gridColumns

    def fit2RowSpan(self, row, rowSpan):
        gridRows = self.getGridRows()
        indices = range(len(gridRows))
        if row in indices and row + rowSpan in indices:
            r1 = gridRows[row]
            r2 = gridRows[row + rowSpan - 1]
            self.h = r2[0] - r1[0] + r2[1]
            return True
        return False

    def top2Grid(self):
        """Move the top of self to rounded grid

        >>> e1 = Element(baselineGridStart=100, baselineGrid=10, h=1000, originTop=False)
        >>> e2 = Element(y=105, h=200, parent=e1)
        >>> e2.top
        105pt
        >>> e2.top2Grid()
        >>> e2.y
        100pt
        >>> e2.y = 101
        >>> e2.top2Grid()
        >>> e2.y
        100pt
        >>> e2.y = 106
        >>> e2.top2Grid()
        >>> e2.y
        110pt
        """
        self.top += self.getDistance2Grid(self.top)

    def bottom2Grid(self):
        """Move the top of self to rounded grid

        >>> e1 = Element(baselineGridStart=100, baselineGrid=10, h=1000, originTop=False)
        >>> e2 = Element(y=105, h=200, parent=e1)
        >>> e2.bottom
        105pt
        >>> e2.bottom2Grid()
        >>> e2.y
        100pt
        >>> e2.y = 101
        >>> e2.bottom2Grid()
        >>> e2.y
        100pt
        >>> e2.y = 106
        >>> e2.bottom2Grid()
        >>> e2.y
        110pt
        """
        self.bottom += self.getDistance2Grid(self.bottom)

    def _get_distance2Grid(self):
        """Answer the distance to the parent grid, where vertical alignment decides where is measured.

        >>> e1 = Element(baselineGridStart=100, baselineGrid=50, h=1000, originTop=False)
        >>> e2 = Element(y=130, h=200, parent=e1)
        >>> e2.distance2Grid
        20pt
        >>> e2.y = pt(140)
        >>> e2.distance2Grid
        10pt
        >>> e2.y = pt(150)
        >>> e2.distance2Grid
        0pt
        """
        return self.parent.getDistance2Grid(self.y)
    distance2Grid = property(_get_distance2Grid)

    #   Page block and Page side alignments

    #   Horizontal alignments

    def center2Center(self):
        """Move center of self to padding center position of parent.
        Note that this different from self.center2CenterSides if the left
        and right padding of parent is not identical.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetry
        >>> e1.center2Center() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.center2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2 - 120/2
        (165pt, 165.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.center2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2
        (225pt, 225.0)
        >>> e2.xAlign = RIGHT
        >>> success = e2.center2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2 + 120/2
        (285pt, 285.0)
        """
        if self.parent is None:
            return False
        self.center = self.parent.pl + self.parent.pw/2
        return True

    def center2CenterSides(self):
        """Move center of self to center of sides of parent.
        Note that this different from self.center2Center if the left
        and right padding of parent is not identical.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetry
        >>> e1.center2CenterSides() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.center2CenterSides()
        >>> e2.x, 500/2 - 120/2
        (190pt, 190.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.center2CenterSides()
        >>> e2.x, 500/2
        (250pt, 250.0)
        >>> e2.xAlign = RIGHT
        >>> success = e2.center2CenterSides()
        >>> e2.x, 500/2 + 120/2
        (310pt, 310.0)
        """
        if self.parent is None:
            return False
        self.center = self.parent.w/2
        return True

    def center2Left(self):
        """Move center of self to left padding of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetry
        >>> e1.center2Left() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.center2Left()
        >>> e2.x, 30 - 120/2
        (-30pt, -30.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.center2Left()
        >>> e2.x, 30
        (30pt, 30)
        >>> e2.xAlign = RIGHT
        >>> success = e2.center2Left()
        >>> e2.x, 30 + 120/2
        (90pt, 90.0)
        """
        if self.parent is None:
            return False
        self.center = self.parent.pl # Padding left
        return True

    def center2LeftSide(self):
        """Move center of self to left side of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetry
        >>> e1.center2LeftSide() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.center2LeftSide()
        >>> e2.x, -120/2
        (-60pt, -60.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.center2LeftSide()
        >>> e2.x
        0pt
        >>> e2.xAlign = RIGHT
        >>> success = e2.center2LeftSide()
        >>> e2.x, 120/2
        (60pt, 60.0)
        """
        if self.parent is None:
            return False
        self.center = 0
        return True

    def center2Right(self):
        """Move center of self to the right padding of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetry
        >>> e1.center2Right() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.center2Right()
        >>> e2.x, 500 - 80 - 120/2
        (360pt, 360.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.center2Right()
        >>> e2.x, 500 - 80
        (420pt, 420)
        >>> e2.xAlign = RIGHT
        >>> success = e2.center2Right()
        >>> e2.x, 500 - 80 + 120/2
        (480pt, 480.0)
        """
        if self.parent is None:
            return False
        self.center = self.parent.w - self.parent.pr
        return True

    def center2RightSide(self):
        """Move center of self to the right side of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetry
        >>> e1.center2RightSide() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.center2RightSide()
        >>> e2.x, 500 - 120/2
        (440pt, 440.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.center2RightSide()
        >>> e2.x, 500
        (500pt, 500)
        >>> e2.xAlign = RIGHT
        >>> success = e2.center2RightSide()
        >>> e2.x, 500 + 120/2
        (560pt, 560.0)
        """
        if self.parent is None:
            return False
        self.center = self.parent.w
        return True

    def left2Center(self):
        """Move left of self to the padding center of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetry
        >>> e1.left2Center() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.left2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2
        (225pt, 225.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.left2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2 + 120/2
        (285pt, 285.0)
        >>> e2.xAlign = RIGHT
        >>> success = e2.left2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2 + 120
        (345pt, 345.0)
        """
        if self.parent is None:
            return False
        self.mLeft = self.parent.pl + self.parent.pw/2
        return True

    def left2CenterSides(self):
        """Move left of self to the sides center of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetry
        >>> e1.left2Center() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.left2CenterSides()
        >>> e2.x, 500/2
        (250pt, 250.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.left2CenterSides()
        >>> e2.x, 500/2 + 120/2
        (310pt, 310.0)
        >>> e2.xAlign = RIGHT
        >>> success = e2.left2CenterSides()
        >>> e2.x, 500/2 + 120
        (370pt, 370.0)
        """
        if self.parent is None:
            return False
        self.mLeft = self.parent.w/2
        return True

    def left2Left(self):
        """Move left of self to padding left position of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> e1 = Element(w=500, pl=50)
        >>> e1.left2Left() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.left2Left()
        >>> e2.x
        50pt
        >>> e2.xAlign = CENTER
        >>> success = e2.left2Left()
        >>> e2.x
        110pt
        >>> e2.xAlign = RIGHT
        >>> success = e2.left2Left()
        >>> e2.x
        170pt
        """
        if self.parent is None:
            return False
        self.mLeft = self.parent.pl # Padding left
        return True

    def left2LeftSide(self):
        """Move left of self to left position of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> e1 = Element(w=500, pl=50)
        >>> e1.left2LeftSide() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.left2LeftSide()
        >>> e2.x
        0pt
        >>> e2.xAlign = CENTER
        >>> success = e2.left2LeftSide()
        >>> e2.x
        60pt
        >>> e2.xAlign = RIGHT
        >>> success = e2.left2LeftSide()
        >>> e2.x
        120pt
        """
        if self.parent is None:
            return False
        self.mLeft = 0
        return True

    def left2LeftBleed(self):
        """Move left of self to left bleed position of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.
        """
        if self.parent is None:
            return False
        self.mLeft = -self.bleedLeft
        return True

    def left2Right(self):
        """Move left of self to padding right position of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> e1 = Element(w=500, padding=50)
        >>> e1.left2Right() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=RIGHT)
        >>> success = e2.left2Right()
        >>> e2.x
        570pt
        >>> e2.xAlign = CENTER
        >>> success = e2.left2Right()
        >>> e2.x
        510pt
        >>> e2.xAlign = LEFT
        >>> success = e2.left2Right()
        >>> e2.x
        450pt
        """
        if self.parent is None:
            return False
        self.mLeft = self.parent.w - self.parent.pr
        return True

    def left2RightSide(self):
        """Move left of self to full width (right position) of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> e1 = Element(w=500, padding=50)
        >>> e1.left2RightSide() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=RIGHT)
        >>> success = e2.left2RightSide()
        >>> e2.x
        620pt
        >>> e2.xAlign = CENTER
        >>> success = e2.left2RightSide()
        >>> e2.x
        560pt
        >>> e2.xAlign = LEFT
        >>> success = e2.left2RightSide()
        >>> e2.x
        500pt
        """
        if self.parent is None:
            return False
        self.mLeft = self.parent.w
        return True

    def right2Center(self):
        """Position the right side centered on the padding of the parent.
        Note that this different from self.right2Center if the left
        and right padding of parent is not identical.

        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetric padding
        >>> e1.right2Center() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.right2Center()
        >>> e2.x, e1.pl, e1.pw/2, 30 + (500 - 30 - 80)/2 - 120
        (105pt, 30pt, 195pt, 105.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.right2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2 - 120/2
        (165pt, 165.0)
        >>> e2.xAlign = RIGHT
        >>> success = e2.right2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2
        (225pt, 225.0)
        """
        if self.parent is None:
            return False
        self.mRight = self.parent.pl + self.parent.pw/2
        return True

    def right2CenterSides(self):
        """Position the right side centered on the sides of the parent.
        Note that this different from self.right2Center if the left
        and right padding of parent is not identical.

        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetric padding
        >>> e1.right2CenterSides() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.right2CenterSides()
        >>> e2.x # 500/2 - 120
        130pt
        >>> e2.xAlign = CENTER
        >>> success = e2.right2CenterSides()
        >>> e2.x # 500/2 - 120/2
        190pt
        >>> e2.xAlign = RIGHT
        >>> success = e2.right2CenterSides()
        >>> e2.x # 500/2
        250pt
        """
        if self.parent is None:
            return False
        self.mRight = self.parent.w/2
        return True

    def right2Left(self):
        """Move right of self to padding left position of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> e1 = Element(w=500, padding=50)
        >>> e1.right2Left() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.right2Left()
        >>> e2.x # 50 - 120
        -70pt
        >>> e2.xAlign = CENTER
        >>> success = e2.right2Left()
        >>> e2.x # 50 - 120/2
        -10pt
        >>> e2.xAlign = RIGHT
        >>> success = e2.right2Left()
        >>> e2.x
        50pt
        """
        if self.parent is None:
            return False
        self.mRight = self.parent.pl # Padding left
        return True

    def right2LeftSide(self):
        """Move right of self to left position of parent. The position of e2
        element origin depends on the horizontal alignment type.

        >>> e1 = Element(w=500, padding=50)
        >>> e1.right2LeftSide() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.right2LeftSide()
        >>> e2.x
        -120pt
        >>> e2.xAlign = CENTER
        >>> success = e2.right2LeftSide()
        >>> e2.x, -120/2
        (-60pt, -60.0)
        >>> e2.xAlign = RIGHT
        >>> success = e2.right2LeftSide()
        >>> e2.x
        0pt
        """
        if self.parent is None:
            return False
        self.mRight = 0 # Left side of parent position
        return True

    def right2Right(self):
        """Move right of self to padding right position of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> e1 = Element(w=500, pl=30, pr=80)
        >>> e1.right2Right() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.right2Right()
        >>> e2.x, 500 - 80 - 120
        (300pt, 300)
        >>> e2.xAlign = CENTER
        >>> success = e2.right2Right()
        >>> e2.x, 500 - 80 - 120/2
        (360pt, 360.0)
        >>> e2.xAlign = RIGHT
        >>> success = e2.right2Right()
        >>> e2.x, 500 - 80
        (420pt, 420)
        """
        if self.parent is None:
            return False
        self.mRight = self.parent.w - self.parent.pr
        return True

    def right2RightSide(self):
        """Move right of self to right width position of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> e1 = Element(w=500, padding=50)
        >>> e1.right2RightSide() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.right2RightSide()
        >>> e2.x, 500 - 120
        (380pt, 380)
        >>> e2.xAlign = CENTER
        >>> success = e2.right2RightSide()
        >>> e2.x, 500 - 120/2
        (440pt, 440.0)
        >>> e2.xAlign = RIGHT
        >>> success = e2.right2RightSide()
        >>> e2.x
        500pt
        """
        if self.parent is None:
            return False
        self.mRight = self.parent.w
        return True

    def right2RightBleed(self):
        """Move right of self to right bleed width position of parent. The
        position of e2 element origin depends on the horizontal alignment
        type."""
        if self.parent is None:
            return False
        self.mRight = self.parent.w + self.bleedRight
        return True

    def origin2Center(self):
        """Move origin of the element to the padding center of the parent.

        >>> e1 = Element(w=500, pl=30, pr=80)
        >>> e1.origin2Center() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.origin2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2
        (225pt, 225.0)
        """
        if self.parent is None:
            return False
        self.x = self.parent.pl + self.parent.pw/2
        return True

    def origin2CenterSides(self):
        """Move origin of the element to the sides center of the parent.

        >>> e1 = Element(w=500, pl=30, pr=80)
        >>> e1.origin2CenterSides() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.origin2CenterSides()
        >>> e2.x, 500/2
        (250pt, 250.0)
        """
        if self.parent is None:
            return False
        self.x = self.parent.w/2
        return True

    def origin2Left(self):
        """Move origin of the element to the padding left of the parent.

        >>> e1 = Element(w=500, pl=30, pr=80)
        >>> e1.origin2Left() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.origin2Left()
        >>> e2.x, 30
        (30pt, 30)
        """
        if self.parent is None:
            return False
        self.x = self.parent.pl # Padding left
        return True

    def origin2LeftSide(self):
        """Move origin of the element to the left side of the parent.

        >>> e1 = Element(w=500, pl=30, pr=80)
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.origin2LeftSide()
        >>> e2.x
        0pt
        """
        self.x = 0
        return True

    def origin2Right(self):
        """Move origin of the element to the right padding of the parent.

        >>> e1 = Element(w=500, pl=30, pr=80)
        >>> e1.origin2Right() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.origin2Right()
        >>> e2.x, 500 - 80
        (420pt, 420)
        """
        if self.parent is None:
            return False
        self.x = self.parent.w - self.parent.pr
        return True

    def origin2RightSide(self):
        """Move origin of the element to the right padding of the parent.

        >>> e1 = Element(w=500, pl=30, pr=80)
        >>> e1.origin2RightSide() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.origin2RightSide()
        >>> e2.x, 500
        (500pt, 500)
        """
        if self.parent is None:
            return False
        self.x = self.parent.w
        return True


    #   Vertical alignments

    def bottom2Bottom(self):
        """Move bottom of the element to the bottom of the parent block.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.bottom2Bottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop
        (True, True)
        >>> success = e2.bottom2Bottom()
        >>> e2.y, 500 - 80 - 120
        (300pt, 300)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2Bottom()
        >>> e2.y, 500 - 80 - 120/2, e1.h - e1.pb - e2.h/2
        (360pt, 360.0, 360pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2Bottom()
        >>> e2.y, 500 - 80
        (420pt, 420)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.bottom2Bottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop
        (False, False)
        >>> success = e2.bottom2Bottom()
        >>> e2.y, 80 + 120
        (200pt, 200)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2Bottom()
        >>> e2.y, 80 + 120/2, e1.pb + e2.h/2
        (140pt, 140.0, 140pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2Bottom()
        >>> e2.y, 80
        (80pt, 80)

        """
        if self.parent is None:
            return False
        if self.parent.originTop:
            self.mBottom = self.parent.h - self.parent.pb
        else:
            self.mBottom = self.parent.pb
        return True

    def bottom2BottomSide(self):
        """Move bottom of the element to the bottom side of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.bottom2BottomSide() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (True, True)
        >>> success = e2.bottom2BottomSide()
        >>> e2.y, 500 - 120
        (380pt, 380)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2BottomSide()
        >>> e2.y, 500 - 120/2, e1.h - e2.h/2
        (440pt, 440.0, 440pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2BottomSide()
        >>> e2.y, 500
        (500pt, 500)

         >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.bottom2BottomSide() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (False, False)
        >>> success = e2.bottom2BottomSide()
        >>> e2.y, 120
        (120pt, 120)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2BottomSide()
        >>> e2.y, 120/2, e2.h/2
        (60pt, 60.0, 60pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2BottomSide()
        >>> e2.y, 0
        (0pt, 0)
        """
        if self.parent is None:
            return False
        if self.originTop:
            self.mBottom = self.parent.h
        else:
            self.mBottom = 0
        return True

    def bottom2BottomBleed(self):
        """Move bottom of the element to the bottom side of the parent,
        overshooting by bleed. The position of e2 element origin depends on
        the vertical alignment type.
        """
        if self.parent is None:
            return False
        if self.originTop:
            self.mBottom = self.parent.h + self.bleedBottom
        else:
            self.mBottom = -self.bleedBottom
        return True

    def bottom2Top(self):
        """Move bottom of the element to the top padding of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.bottom2Top() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (True, True)
        >>> success = e2.bottom2Top()
        >>> e2.y, 30 - 120
        (-90pt, -90)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2Top()
        >>> e2.y, 30 - 120/2
        (-30pt, -30.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2Top()
        >>> e2.y, 30
        (30pt, 30)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.bottom2Top() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (False, False)
        >>> success = e2.bottom2Top()
        >>> e2.y, 500 - 30 + 120, e1.h - e1.pt + e2.h
        (590pt, 590, 590pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2Top()
        >>> e2.y, 500 - 30 + 120/2, e1.h - e1.pt + e2.h/2
        (530pt, 530.0, 530pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2Top()
        >>> e2.y, 500 - 30, e1.h - e1.pt
        (470pt, 470, 470pt)
        """
        if self.parent is None:
            return False
        if self.originTop:
            self.mBottom = self.parent.pt
        else:
            self.mBottom = self.parent.h - self.parent.pt
        return True

    def middle2Bottom(self):
        """Move middle of the element to the bottom padding of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.middle2Bottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (True, True)
        >>> success = e2.middle2Bottom()
        >>> e2.y, 500 - 80 - 120/2
        (360pt, 360.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2Bottom()
        >>> e2.y, 500 - 80
        (420pt, 420)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2Bottom()
        >>> e2.y, 500 - 80 + 120/2
        (480pt, 480.0)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.middle2Bottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (False, False)
        >>> success = e2.middle2Bottom()
        >>> e2.y, 80 + 120/2, e1.pb + e2.h/2
        (140pt, 140.0, 140pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2Bottom()
        >>> e2.y, 80, e1.pb
        (80pt, 80, 80pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2Bottom()
        >>> e2.y, 80 - 120/2, e1.pb - e2.h/2
        (20pt, 20.0, 20pt)

        """
        if self.parent is None:
            return False
        if self.originTop:
            self.middle = self.parent.h - self.parent.pb
        else:
            self.middle = self.parent.pb
        return True

    def middle2BottomSide(self):
        """Move middle of the element to the bottom side of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.middle2BottomSide() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (True, True)
        >>> success = e2.middle2BottomSide()
        >>> e2.y, 500 - 120/2
        (440pt, 440.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2BottomSide()
        >>> e2.y, 500
        (500pt, 500)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2BottomSide()
        >>> e2.y, 500 + 120/2
        (560pt, 560.0)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.middle2BottomSide() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (False, False)
        >>> success = e2.middle2BottomSide()
        >>> e2.y, 120/2, e2.h/2
        (60pt, 60.0, 60pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2BottomSide()
        >>> e2.y, 0
        (0pt, 0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2BottomSide()
        >>> e2.y, -120/2, -e2.h/2
        (-60pt, -60.0, -60pt)
        """
        if self.parent is None:
            return False
        if self.originTop:
            self.middle = self.parent.h
        else:
            self.middle = 0
        return True


    def middle2Top(self):
        """Move middle of the element to the top side of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.middle2Top() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (True, True)
        >>> success = e2.middle2Top()
        >>> e2.y, 30 - 120/2
        (-30pt, -30.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2Top()
        >>> e2.y, 30
        (30pt, 30)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2Top()
        >>> e2.y, 30 + 120/2
        (90pt, 90.0)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.middle2Top() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (False, False)
        >>> success = e2.middle2Top()
        >>> e2.y, 500 - 30 + 120/2, e1.h - e1.pt + e2.h/2
        (530pt, 530.0, 530pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2Top()
        >>> e2.y, 500 - 30, e1.h - e1.pt
        (470pt, 470, 470pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2Top()
        >>> e2.y, 500 - 30 - 120/2, e1.h - e1.pt - e2.h/2
        (410pt, 410.0, 410pt)
        """
        if self.parent is None:
            return False
        if self.originTop:
            self.middle = self.parent.pt
        else:
            self.middle = self.parent.h - self.parent.pt
        return True

    def middle2TopSide(self):
        """Move middle of the element to the top side of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.middle2TopSide() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (True, True)
        >>> success = e2.middle2TopSide()
        >>> e2.y, -120/2
        (-60pt, -60.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2TopSide()
        >>> e2.y
        0pt
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2TopSide()
        >>> e2.y, 120/2
        (60pt, 60.0)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.middle2TopSide() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (False, False)
        >>> success = e2.middle2TopSide()
        >>> e2.y, 500 + 120/2, e1.h + e2.h/2
        (560pt, 560.0, 560pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2TopSide()
        >>> e2.y, 500, e1.h
        (500pt, 500, 500pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2TopSide()
        >>> e2.y, 500 - 120/2, e1.h - e2.h/2
        (440pt, 440.0, 440pt)
        """
        if self.parent is None:
            return False
        if self.originTop:
            self.middle = 0
        else:
            self.middle = self.parent.h
        return True

    def middle2Middle(self): # Vertical center, following CSS naming.
        """Move middle of the element to the padding middle of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.middle2Middle() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (True, True)
        >>> success = e2.middle2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2 - 120/2
        (165pt, 165.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2
        (225pt, 225.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2 + 120/2
        (285pt, 285.0)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.middle2Middle() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (False, False)
        >>> success = e2.middle2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2 + 120/2, e1.pb + (e1.h - e1.pb - e1.pt)/2 + e2.h/2
        (335pt, 335.0, 335pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2, e1.pb + (e1.h - e1.pb - e1.pt)/2
        (275pt, 275.0, 275pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2 - 120/2, e1.pb + (e1.h - e1.pb - e1.pt)/2 - e2.h/2
        (215pt, 215.0, 215pt)
        """
        if self.parent is None:
            return False
        if self.originTop:
            self.middle = self.parent.pt + self.parent.ph/2
        else:
            self.middle = self.parent.pb + self.parent.ph/2
        return True

    def middle2MiddleSides(self):
        """Move middle of the element to the sides middle of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.middle2MiddleSides() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (True, True)
        >>> success = e2.middle2MiddleSides()
        >>> e2.y, 500/2 - 120/2
        (190pt, 190.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2MiddleSides()
        >>> e2.y, 500/2
        (250pt, 250.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2MiddleSides()
        >>> e2.y, 500/2 + 120/2
        (310pt, 310.0)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.middle2MiddleSides() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (False, False)
        >>> success = e2.middle2MiddleSides()
        >>> e2.y, 500/2 + 120/2, e1.h/2 + e2.h/2
        (310pt, 310.0, 310pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2MiddleSides()
        >>> e2.y, 500/2, e1.h/2
        (250pt, 250.0, 250pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2MiddleSides()
        >>> e2.y, 500/2 - 120/2, e1.h/2 - e2.h/2
        (190pt, 190.0, 190pt)
        """
        if self.parent is None:
            return False
        self.middle = self.parent.h/2


    def top2Middle(self):
        """Move top of the element to the padding middle of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.top2Middle() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (True, True)
        >>> success = e2.top2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2
        (225pt, 225.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2 + 120/2
        (285pt, 285.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2 + 120
        (345pt, 345.0)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.top2Middle() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (False, False)
        >>> success = e2.top2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2, e1.pb + (e1.h - e1.pb - e1.pt)/2
        (275pt, 275.0, 275pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2 - 120/2, e1.pb + (e1.h - e1.pb - e1.pt)/2 - e2.h/2
        (215pt, 215.0, 215pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2 - 120, e1.pb + (e1.h - e1.pb - e1.pt)/2 - e2.h
        (155pt, 155.0, 155pt)
        """
        if self.parent is None:
            return False
        if self.originTop:
            self.mTop = self.parent.pt + self.parent.ph/2
        else:
            self.mTop = self.parent.pb + self.parent.ph/2
        return True

    def top2MiddleSides(self):
        """Move top of the element to the middle between sides of the parent.
        The position of e2 element origin depends on the vertical alignment
        type.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.top2MiddleSides() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (True, True)
        >>> success = e2.top2MiddleSides()
        >>> e2.y, 500/2
        (250pt, 250.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2MiddleSides()
        >>> e2.y, 500/2 + 120/2
        (310pt, 310.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2MiddleSides()
        >>> e2.y, 500/2 + 120
        (370pt, 370.0)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.top2MiddleSides() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (False, False)
        >>> success = e2.top2MiddleSides()
        >>> e2.y, 500/2
        (250pt, 250.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2MiddleSides()
        >>> e2.y, 500/2 - 120/2, e1.h/2 - e2.h/2
        (190pt, 190.0, 190pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2MiddleSides()
        >>> e2.y, 500/2 - 120, e1.h/2 - e2.h
        (130pt, 130.0, 130pt)
        """
        if self.parent is None:
            return False
        self.mTop = self.parent.h/2
        return True

    def origin2Bottom(self):
        """Move origin of the element to the padding bottom of the parent.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.origin2Bottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (True, True)
        >>> success = e2.origin2Bottom()
        >>> e2.y, 500 - 80
        (420pt, 420)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.origin2Bottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (False, False)
        >>> success = e2.origin2Bottom()
        >>> e2.y, 80, e1.pb
        (80pt, 80, 80pt)
        """
        if self.parent is None:
            return False
        if self.originTop:
            self.y = self.parent.h - self.parent.pb
        else:
            self.y = self.parent.pb
        return True

    def origin2BottomSide(self):
        """Move origin of the element to the padding bottom of the parent.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.origin2BottomSide() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (True, True)
        >>> success = e2.origin2BottomSide()
        >>> e2.y
        500pt

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.origin2BottomSide() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> e1.originTop, e2.originTop # Inherited property
        (False, False)
        >>> success = e2.origin2BottomSide()
        >>> e2.y, 0
        (0pt, 0)
        """
        if self.parent is None:
            return False
        if self.originTop:
            self.y = self.parent.h
        else:
            self.y = 0
        return True

    def origin2Top(self):
        """Move origin of the element to the top padding of the parent.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.origin2Top() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1)
        >>> success = e2.origin2Top()
        >>> e2.y, 30
        (30pt, 30)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.origin2Top() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1)
        >>> success = e2.origin2Top()
        >>> e2.y, 30
        (30pt, 30)

        """
        if self.parent is None:
            return False
        if self.originTop:
            self.y = self.parent.pt
        else:
            self.y = self.parent.h - self.parent.pt
        return True

    def origin2TopSide(self):
        """Move origin of the element to the top side of the parent.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.origin2TopSide() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1)
        >>> success = e2.origin2TopSide()
        >>> e2.y
        0pt

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.origin2TopSide() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1)
        >>> success = e2.origin2TopSide()
        >>> e2.y, e1.h
        (500pt, 500pt)
        """
        if self.parent is None:
            return False
        if self.originTop:
            self.y = 0
        else:
            self.y = self.parent.h
        return True

    def origin2Middle(self):
        """Move origin of the element to the top side of the parent.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.origin2Middle() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1)
        >>> success = e2.origin2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2
        (225pt, 225.0)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.origin2Middle() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1)
        >>> success = e2.origin2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2
        (275pt, 275.0)
        """
        if self.parent is None:
            return False
        if self.originTop:
            self.y = self.parent.pt + self.parent.ph/2
        else:
            self.y = self.parent.pb + self.parent.ph/2
        return True

    def origin2MiddleSides(self):
        """Move origin of the element to the sides middle of the parent.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.origin2MiddleSides() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1)
        >>> success = e2.origin2MiddleSides()
        >>> e2.y, 500/2
        (250pt, 250.0)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.origin2MiddleSides() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1)
        >>> success = e2.origin2MiddleSides()
        >>> e2.y, 500/2
        (250pt, 250.0)
        """
        if self.parent is None:
            return False
        self.y = self.parent.h/2
        return True

    def bottom2Middle(self):
        """Move margin bottom of the element to the padding middle of the parent.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.bottom2Middle() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.bottom2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2 - 120
        (105pt, 105.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2 - 120/2
        (165pt, 165.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2
        (225pt, 225.0)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.bottom2Middle() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.bottom2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2 + 120, e1.pb + (e1.h - e1.pb - e1.pt)/2 + e2.h
        (395pt, 395.0, 395pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2 + 120/2, e1.pb + (e1.h - e1.pb - e1.pt)/2 + e2.h/2
        (335pt, 335.0, 335pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2, e1.pb + (e1.h - e1.pb - e1.pt)/2
        (275pt, 275.0, 275pt)
        """
        if self.parent is None:
            return False
        if self.originTop:
            self.mBottom = self.parent.pt + self.parent.ph/2
        else:
            self.mBottom = self.parent.pb + self.parent.ph/2
        return True

    def bottom2MiddleSides(self):
        """Move margin bottom of the element to the sides middle of the parent.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.bottom2MiddleSides() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.bottom2MiddleSides()
        >>> e2.y, 500/2 - 120
        (130pt, 130.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2MiddleSides()
        >>> e2.y, 500/2 - 120/2
        (190pt, 190.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2MiddleSides()
        >>> e2.y, 500/2
        (250pt, 250.0)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.bottom2MiddleSides() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.bottom2MiddleSides()
        >>> e2.y, 500/2 + 120, e1.h/2 + e2.h
        (370pt, 370.0, 370pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2MiddleSides()
        >>> e2.y, 500/2 + 120/2, e1.h/2 + e2.h/2
        (310pt, 310.0, 310pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2MiddleSides()
        >>> e2.y, 500/2, e1.h/2
        (250pt, 250.0, 250pt)
        """
        if self.parent is None:
            return False
        self.mBottom = self.parent.h/2
        return True

    def top2Bottom(self):
        """Move margin top of the element to the padding bottom of the parent.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.top2Bottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.top2Bottom()
        >>> e2.y, 500 - 80
        (420pt, 420)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2Bottom()
        >>> e2.y, 500 - 80 + 120/2
        (480pt, 480.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2Bottom()
        >>> e2.y, 500 - 80 + 120
        (540pt, 540)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.top2Bottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.top2Bottom()
        >>> e2.y, 80, e1.pb
        (80pt, 80, 80pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2Bottom()
        >>> e2.y, 80 - 120/2, e1.pb - e2.h/2
        (20pt, 20.0, 20pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2Bottom()
        >>> e2.y, 80 - 120, e1.pb - e2.h
        (-40pt, -40, -40pt)
        """
        if self.parent is None:
            return False
        if self.originTop:
            self.mTop = self.parent.h - self.parent.pb
        else:
            self.mTop = self.parent.pb
        return True

    def top2Top(self):
        """Move margin top of the element to the padding top of the parent.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.top2Top() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.top2Top()
        >>> e2.y, 30
        (30pt, 30)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2Top()
        >>> e2.y, 30 + 120/2
        (90pt, 90.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2Top()
        >>> e2.y, 30 + 120
        (150pt, 150)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.top2Top() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.top2Top()
        >>> e2.y, 500 - 30, e1.h - e1.pt
        (470pt, 470, 470pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2Top()
        >>> e2.y, 500 - 30 - 120/2, e1.h - e1.pt - e2.h/2
        (410pt, 410.0, 410pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2Top()
        >>> e2.y, 500 - 30 - 120, e1.h - e1.pt - e2.h
        (350pt, 350, 350pt)
        """
        if self.parent is None:
            return False
        if self.originTop:
            self.mTop = self.parent.pt
        else:
            self.mTop = self.parent.h - self.parent.pt
        return True

    def top2TopSide(self):
        """Move margin top of the element to the top side of the parent.

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=True)
        >>> e1.top2TopSide() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.top2TopSide()
        >>> e2.y
        0pt
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2TopSide()
        >>> e2.y, 120/2
        (60pt, 60.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2TopSide()
        >>> e2.y, 120
        (120pt, 120)

        >>> e1 = Element(h=500, pt=30, pb=80, originTop=False)
        >>> e1.top2TopSide() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.top2TopSide()
        >>> e2.y, 500, e1.h
        (500pt, 500, 500pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2TopSide()
        >>> e2.y, 500 - 120/2, e1.h - e2.h/2
        (440pt, 440.0, 440pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2TopSide()
        >>> e2.y, 500 - 120, e1.h - e2.h
        (380pt, 380, 380pt)
        """
        if self.parent is None:
            return False
        if self.originTop:
            self.mTop = 0
        else:
            self.mTop = self.parent.h
        return True

    def top2TopBleed(self):
        """Move margin top of the element to the top side of the parent, overshooting
        by bleed."""
        if self.parent is None:
            return False
        if self.originTop:
            self.mTop = -self.bleedTop
        else:
            self.mTop = self.parent.h + self.bleedTop
        return True

    # Floating parent padding

    def float2Top(self):
        """Float the element upward, until top hits the parent top padding or
        "hooks" into another element at the same z-layer position. Include
        margin to decide if it fits."""
        if self.originTop:
            self.mTop = min(self.getFloatTopSide(), self.parent.pt)
        else:
            self.mTop = min(self.getFloatTopSide(), self.parent.h - self.parent.pt)
        return True

    def float2Bottom(self):
        if self.originTop:
            self.mBottom = min(self.getFloatBottomSide(), self.parent.h - self.parent.pb)
        else:
            self.mBottom = min(self.getFloatBottomSide(), self.parent.pb)
        return True

    def float2Left(self):
        self.mLeft = max(self.getFloatLeftSide(), self.parent.pl) # padding left
        return True

    def float2Right(self):
        self.mRight = min(self.getFloatRightSide(), self.parent.w - self.parent.pr)
        return True

    # Floating to parent sides, go as far as there are no other elements in the
    # same z-layer

    def float2TopSide(self):
        self.mTop = self.getFloatTopSide()
        return True

    def float2BottomSide(self):
        """Float margin bottom to bottom side."""
        self.mBottom = self.getFloatBottomSide()
        return True

    def float2LeftSide(self):
        """Float margin left to left side."""
        self.mLeft = self.getFloatLeftSide()
        return True

    def float2RightSide(self):
        """Float margin right to right side."""
        self.mRight = self.getFloatRightSide()
        return True

    # With fitting (and shrinking) we need to change the actual size of the
    # element. This can have implications on it's content, and we need to take
    # the min/max sizes into conderantion: setting the self.w and self.h to a
    # value, does not mean that the size really got that value, if exceeding a
    # min/max limit.

    def fit2Bottom(self):
        if self.originTop:
            self.h += self.parent.h - self.parent.pb - self.mBottom
        else:
            self.h = self.mTop - self.parent.pb
            self.mBottom = self.parent.pb
        return True

    def fit2BottomSide(self):
        if self.originTop:
            self.h += self.parent.h - self.mBottom
        else:
            top = self.mTop
            self.mBottom = 0
            self.h = top
        return True

    def fit2BottomBleed(self):
        if self.originTop:
            self.h += self.parent.h - self.mBottom + self.bleedBottom
        else:
            top = self.mTop
            self.mBottom = -self.bleedBottom
            self.h = top + self.bleedBottom
        return True

    def fit2Left(self):
        u"""Fit to left, inlcuding margin left and margin right."""
        right = self.mRight
        self.mLeft = self.parent.pl # Padding left
        self.w += right - self.mRight
        return True

    def fit2LeftSide(self):
        u"""Fit to left, including margin left and margin right."""
        right = self.mRight
        self.mLeft = 0
        self.w += right - self.mRight
        return True

    def fit2Right(self):
        """Make the right side of self fit the right padding of the parent,
        without moving the left position. TextBox implements it's own method
        to make the text fit by adjusting the size.

        >>> e1 = Element(x=100, y=20, w=100, h=50)
        >>> e2 = Element(w=300, h=300, elements=[e1], padding=10)
        >>> e1.x, e1.y, e1.w, e1.h # Default position and size
        (100pt, 20pt, 100pt, 50pt)
        >>> success = e1.fit2Right()
        >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent on padding
        (100pt, 20pt, 190pt, 50pt)
        >>>
        """
        self.w = self.parent.w - self.parent.pr - self.x
        return True

    def scale2Right(self):
        """Make the right side of self fit the right padding of the parent,
        without moving the left position. The scale the height according to the
        original ratio.

        >>> e1 = Element(x=100, y=20, w=100, h=50)
        >>> e2 = Element(w=300, h=300, elements=[e1], padding=10)
        >>> e1.x, e1.y, e1.w, e1.h # Default position and size
        (100pt, 20pt, 100pt, 50pt)
        >>> success = e1.scale2Right()
        >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent on padding
        (100pt, 20pt, 190pt, 95pt)
        >>>
        """
        orgW = self.w
        if orgW:
            self.w = self.parent.w - self.parent.pr - self.x
            self.h = self.h * self.w.pt / orgW.pt
            return True
        return False # No original width, cannot calculate due to zero division.

    def fit2RightSide(self):
        """Make the right side of self fit the right side of the parent,
        without moving the left position.

        >>> e1 = Element(x=100, y=20, w=100, h=50)
        >>> e2 = Element(w=300, h=300, elements=[e1], padding=10)
        >>> e1.x, e1.y, e1.w, e1.h # Default position and size
        (100pt, 20pt, 100pt, 50pt)
        >>> success = e1.fit2RightSide()
        >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent on padding
        (100pt, 20pt, 200pt, 50pt)
        >>>
        """
        self.w = self.parent.w - self.x
        return True

    def fit2RightBleed(self):
        """Make the right side of self fit the right bleed side of the parent,
        without moving the left position."""
        self.w = self.parent.w - self.x + self.bleedRight
        return True

    def fit2Top(self):
        """Make the top side of self fit the top padding of the parent, without
        moving the bottom position.

        >>> e1 = Element(x=100, y=20, w=100, h=50)
        >>> e2 = Element(w=300, h=300, elements=[e1], padding=10)
        >>> e1.x, e1.y, e1.w, e1.h # Default position and size
        (100pt, 20pt, 100pt, 50pt)
        >>> success = e1.fit2Top()
        >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent on padding
        (100pt, 20pt, 100pt, 320pt)
        >>>
        """
        if self.originTop:
            bottom = self.mBottom
            self.mTop = self.parent.pt
            self.h += bottom - self.mBottom
        else:
            self.h += self.parent.h - self.parent.pt - self.mTop
        return True

    def fit2TopSide(self):
        if self.originTop:
            bottom = self.mBottom
            self.mTop = 0
            self.h += bottom - self.mBottom
        else:
            self.h += self.parent.h - self.mTop
        return True

    def fit2TopBleed(self):
        if self.originTop:
            bottom = self.mBottom
            self.mTop = -self.bleedTop
            self.h += bottom - self.mBottom
        else:
            self.h += self.parent.h - self.mTop + self.bleedTop
        return True

    #   Shrinking

    def shrink2BlockBottom(self):
        _, boxY, _, boxH = self.box
        if self.originTop:
            self.h = boxH
        else:
            top = self.mTop
            self.mBottom = boxY
            self.h += top - self.mTop
        return True

    def shrink2BlockBottomSide(self):
        if self.originTop:
            self.h += self.parent.h - self.mBottom
        else:
            top = self.mTop
            self.mBottom = 0 # Parent botom
            self.h += top - self.mTop
        return True

    def shrink2BlockLeft(self):
        right = self.MRight
        self.mLeft = self.parent.pl # Padding left
        self.w += right - self.mRight
        return True

    def shrink2BlockLeftSide(self):
        right = self.mRight
        self.mLeft = 0
        self.w += right - self.mRight
        return True

    def shrink2BlockRight(self):
        self.w += self.parent.w - self.parent.pr - self.mRight
        return True

    def shrink2BlockRightSide(self):
        self.w += self.parent.w - self.mRight
        return True

    def shrink2BlockTop(self):
        if self.originTop:
            bottom = self.mBottom
            self.mTop = self.parent.pt
            self.h += bottom - self.mBottom
        else:
            self.h += self.parent.h - self.parent.pt - self.mTop
        return True

    def shrink2BlockTopSide(self):
        if self.originTop:
            bottom = self.mBottom
            self.mTop = 0
            self.h += bottom - self.mBottom
        else:
            self.h += self.parent.h - self.mTop
        return True

    #    Text conditions

    def baseline2Top(self):
        # Implemented for elements that support text boxes.
        # Default is to do nothing for non-text elements
        pass

    def baseline2Middle(self):
        # Implemented for elements that support text boxes.
        # Default is to do nothing for non-text elements
        pass

    def baseline2Bottom(self):
        # Implemented for elements that support text boxes.
        # Default is to do nothing for non-text elements
        pass

    def capHeight2Top(self):
        # Implemented for elements that support text boxes.
        # Default is to do nothing for non-text elements
        pass

    def capHeight2Middle(self):
        # Implemented for elements that support text boxes.
        # Default is to do nothing for non-text elements
        pass

    def capHeight2Bottom(self):
        # Implemented for elements that support text boxes.
        # Default is to do nothing for non-text elements
        pass

    def xHeight2Top(self):
        # Implemented for elements that support text boxes.
        # Default is to do nothing for non-text elements
        pass

    def xHeight2Middle(self):
        # Implemented for elements that support text boxes.
        # Default is to do nothing for non-text elements
        pass

    def xHeight2Bottom(self):
        # Implemented for elements that support text boxes.
        # Default is to do nothing for non-text elements
        pass

    def ascender2Top(self):
        # Implemented for elements that support text boxes.
        # Default is to do nothing for non-text elements
        pass

    def ascender2Middle(self):
        # Implemented for elements that support text boxes.
        # Default is to do nothing for non-text elements
        pass

    def ascender2Bottom(self):
        # Implemented for elements that support text boxes.
        # Default is to do nothing for non-text elements
        pass

    def descender2Top(self):
        # Implemented for elements that support text boxes.
        # Default is to do nothing for non-text elements
        pass

    def descender2Middle(self):
        # Implemented for elements that support text boxes.
        # Default is to do nothing for non-text elements
        pass

    def descender2Bottom(self):
        # Implemented for elements that support text boxes.
        # Default is to do nothing for non-text elements
        pass

    #   S H O W I N G  P R O P E R T I E S (stored as style attribute, mostly used by views)

    #   Note that the viewing property values are NOT inherited by self.css(...) following
    #   the element tree upwards. Instead they are local parameters for each element, page
    #   or view.

    def setShowings(self, *args):
        """Set the showing flags of self (often a View instance) to predefined
        flags, depending on a type of stage of usage."""
        setNames = set(args)

        self.show = True
        self.showSpread = False
        self.viewMinInfoPadding = 0
        self.showCropMarks = False
        self.showRegistrationMarks = False
        self.showColorBars = False
        self.showOrigin = False
        self.showPadding = False # Show the (inside) frame of padding
        self.showFrame = False # Showing the element boundaries.
        self.showMargin = False # Showing the (outside) frame of margin.
        self.showNameInfo = False
        self.showElementInfo = False
        self.showMissingElement = False
        self.showGrid = False
        self.showBaselineGrid = False
        self.showTextLeading = False
        self.showFlowConnections = False
        self.showTextOverflowMarker = False
        self.showImageReference = False
        self.cssVerbose = False

        if VIEW_PRINT in setNames:
            # View settings flags to True for print (such as crop marks and
            # registration marks).
            self.showSpread = True
            self.viewMinInfoPadding = DEFAULT_MININFOPADDING
            self.showCropMarks = DEFAULT_CROPMARKS
            self.showRegistrationMarks = DEFAULT_REGISTRATIONMARKS
            self.showNameInfo = True
            if self.isView:
                self.padding = DEFAULT_MININFOPADDING

        if VIEW_PRINT2 in setNames:
            # Extended show options for printing
            self.showColorBars = True

        if VIEW_DEBUG in setNames:
            # View settings flags to True that are useful for debugging a document
            self.showPadding = True
            self.showMargin = True
            self.showFrame = True
            self.showGrid = DEFAULT_GRID
            self.showBaselineGrid = DEFAULT_BASELINE
            self.showTextLeading = True

        if VIEW_DEBUG2 in setNames:
            self.showOrigin = True
            self.showElementInfo = True
            self.showMissingElement = True
            self.cssVerbose = True

        if VIEW_FLOW in setNames:
            self.showFlowConnections = True
            self.showTextOverflowMarker = True
            self.showImageReference = True

        #else VIEW_NONE in setNames: # View settings are all off.

    def _get_show(self):
        """Set flag for drawing or interpretation with conditional.

        >>> e = Element(show=False) # Set a separate attribute
        >>> e.show
        False
        >>> e.show = True
        >>> e.show
        True
        >>> e = Element(style=dict(show=False)) # Set through local style
        >>> e.show
        False
        >>> e1 = Element()
        >>> e1.show # Default is True
        True
        >>> i = e.appendElement(e1) # Add to parent, inheriting show == False
        >>> e1.show
        False
        """
        return self.css('show', True) # Inherited
    def _set_show(self, showFlag):
        self.style['show'] = showFlag # Hiding rest of css for this value.
    show = property(_get_show, _set_show)

    def _get_showSpread(self):
        """Boolean value. If True, show even pages on left of fold, odd on the right.
        Gap distance between the spread pages is defined by the page margins."""
        return self.style.get('showSpread', False) # Not inherited
    def _set_showSpread(self, spread):
        self.style['showSpread'] = bool(spread)
    showSpread = property(_get_showSpread, _set_showSpread)

    # Document/page stuff
    def _get_viewMinInfoPadding(self):
        """Unit value. # Minimum padding needed to show meta info. Otherwise truncated
        to 0 and not showing meta info."""
        base = dict(base=self.parentW, em=self.em) # In case relative units, use this as base for %
        return units(self.style.get('viewMinInfoPadding', 0), base=base) # Not inherited
    def _set_viewMinInfoPadding(self, viewMinInfoPadding):
        self.style['viewMinInfoPadding'] = units(viewMinInfoPadding)
    viewMinInfoPadding = property(_get_viewMinInfoPadding, _set_viewMinInfoPadding)

    def _get_showCropMarks(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding, show crop marks
        around the elemment."""
        return self.style.get('showCropMarks') or {} # Not inherited
    def _set_showCropMarks(self, showCropMarks):
        if not showCropMarks:
            showCropMarks = {}
        elif not isinstance(showCropMarks, (set, list, tuple, dict)):
            showCropMarks = DEFAULT_CROPMARKS
        assert isinstance(showCropMarks, (set, list, tuple, dict))
        self.style['showCropMarks'] = showCropMarks
    showCropMarks = property(_get_showCropMarks, _set_showCropMarks)

    def _get_showRegistrationMarks(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding, show
        registration  marks around the elemment."""
        return self.style.get('showRegistrationMarks') or {} # Not inherited
    def _set_showRegistrationMarks(self, showRegistrationMarks):
        if not showRegistrationMarks:
            showRegistrationMarks = {}
        elif not isinstance(showRegistrationMarks, (set, list, dict, tuple)):
            showRegistrationMarks = DEFAULT_REGISTRATIONMARKS
        assert isinstance(showRegistrationMarks, (set, list, tuple, dict))
        self.style['showRegistrationMarks'] = showRegistrationMarks
    showRegistrationMarks = property(_get_showRegistrationMarks, _set_showRegistrationMarks)

    def _get_showColorBars(self):
        """Set value, containing the selection of color bars that should be shown.
        See pagebot.constants for the names of the options."""
        return set(self.style.get('showColorBars') or []) # Not inherited
    def _set_showColorBars(self, showColorBars):
        if not showColorBars:
            showColorBars = []
        elif not isinstance(showColorBars, (set, list, tuple)):
            if isinstance(showColorBars, str):
                showColorBars = [showColorBars]
            elif showColorBars:
                showColorBars = DEFAULT_COLOR_BARS
            else:
                showColorBars = [] # Don't show them
        self.style['showColorBars'] = set(showColorBars)
    showColorBars = property(_get_showColorBars, _set_showColorBars)

    def _get_showOrigin(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding, show
        origin cross hair marker of the page or other elements."""
        return self.style.get('showOrigin', False) # Not inherited
    def _set_showOrigin(self, showOrigin):
        self.style['showOrigin'] = bool(showOrigin)
    showOrigin = property(_get_showOrigin, _set_showOrigin)

    def _get_showPadding(self):
        """Boolean value. If True show padding of the page or other elements."""
        return self.style.get('showPadding', False) # Not inherited
    def _set_showPadding(self, showPadding):
        self.style['showPadding'] = bool(showPadding)
    showPadding = property(_get_showPadding, _set_showPadding)

    def _get_showMargin(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding, show
        margin of the page or other elements."""
        return self.style.get('showMargin', False) # Not inherited
    def _set_showMargin(self, showMargin):
        self.style['showMargin'] = bool(showMargin)
    showMargin = property(_get_showMargin, _set_showMargin)

    def _get_showFrame(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding, show
        frame of the page or other elements as self.size."""
        return self.style.get('showFrame', False) # Not inherited
    def _set_showFrame(self, showFrame):
        self.style['showFrame'] = bool(showFrame)
    showFrame = property(_get_showFrame, _set_showFrame)

    def _get_showNameInfo(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding, show
        the name of the page or other elements."""
        return self.style.get('showNameInfo', False) # Not inherited
    def _set_showNameInfo(self, showNameInfo):
        self.style['showNameInfo'] = bool(showNameInfo)
    showNameInfo = property(_get_showNameInfo, _set_showNameInfo)

    def _get_showElementInfo(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding, show
        the meta info of the page or other elements."""
        return self.style.get('showElementInfo', False) # Not inherited
    def _set_showElementInfo(self, showElementInfo):
        self.style['showElementInfo'] = bool(showElementInfo)
    showElementInfo = property(_get_showElementInfo, _set_showElementInfo)

    def _get_showIdClass(self):
        """Boolean value. If True show the element.cssId and element.cssClass,
        if they are defined.
        """
        return self.style.get('showIdClass', False) # Not inherited
    def _set_showIdClass(self, showIdClass):
        self.style['showIdClass'] = bool(showIdClass)
    showIdClass = property(_get_showIdClass, _set_showIdClass)

    def _get_showDimensions(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding, show
        the dimensions of the page or other elements."""
        return self.style.get('showDimensions', False) # Not inherited
    def _set_showDimensions(self, showDimensions):
        self.style['showDimensions'] = bool(showDimensions)
    showDimensions = property(_get_showDimensions, _set_showDimensions)

    def _get_showMissingElement(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding, show
        the MissingElement of the page or other elements."""
        return self.style.get('showMissingElement', False) # Not inherited
    def _set_showMissingElement(self, showMissingElement):
        self.style['showMissingElement'] = bool(showMissingElement)
    showMissingElement = property(_get_showMissingElement, _set_showMissingElement)

    def _get_showSourceCode(self):
        """Boolean value. If True elements can show their source code on export."""
        return self.style.get('showSourceCode', False) # Not inherited
    def _set_showSourceCode(self, showSourceCode):
        self.style['showSourceCode'] = bool(showSourceCode)
    showSourceCode = property(_get_showSourceCode, _set_showSourceCode)

    #   Grid stuff using a selected set of (GRID_COL, GRID_ROW, GRID_SQR)

    def _get_showGrid(self):
        """Set value, containing the parts of grid that should be shown. See pagebot.constants
        for the names of the options."""
        return set(self.style.get('showGrid') or []) # Not inherited
    def _set_showGrid(self, showGrid):
        if not showGrid:
            showGrid = []
        elif not isinstance(showGrid, (set, list, tuple)):
            if showGrid in GRID_OPTIONS: # In case of single valid option, make into set
                showGrid = set([showGrid])
            else:
                showGrid = DEFAULT_GRID
        self.style['showGrid'] = set(showGrid)
    showGrid = property(_get_showGrid, _set_showGrid)

    #   Types of baseline grid to be drawn using conbination set of (BASE_LINE, BASE_INDEX_LEFT)

    def _get_showBaselineGrid(self):
        """Set value, containing the parts of baseline that should be shown. See pagebot.constants
        for the names of the options."""
        return set(self.style.get('showBaselineGrid') or []) # Not inherited
    def _set_showBaselineGrid(self, showBaselineGrid):
        if not showBaselineGrid:
            showBaselineGrid = []
        elif not isinstance(showBaselineGrid, (set, tuple, list)):
            if showBaselineGrid in BASE_OPTIONS: # In case of single valid option, make into set
                showBaselineGrid = set([showBaselineGrid])
            else:
                showBaselineGrid = DEFAULT_BASELINE
        self.style['showBaselineGrid'] = set(showBaselineGrid)
    showBaselineGrid = property(_get_showBaselineGrid, _set_showBaselineGrid)

    def _get_showTextLeading(self):
        """Boolean value. If True show the vertical distance between text lines."""
        return self.style.get('showTextLeading', False) # Not inherited
    def _set_showTextLeading(self, showTextLeading):
        self.style['showTextLeading'] = bool(showTextLeading)
    showTextLeading = property(_get_showTextLeading, _set_showTextLeading)

    #   Flow stuff

    def _get_showFlowConnections(self):
        """Boolean value. If True show connection between elements the overflow text lines."""
        return self.style.get('showFlowConnections', False) # Not inherited
    def _set_showFlowConnections(self, showFlowConnections):
        self.style['showFlowConnections'] = bool(showFlowConnections)
    showFlowConnections = property(_get_showFlowConnections, _set_showFlowConnections)

    def _get_showTextOverflowMarker(self):
        """Boolean value. If True a [+] marker is shown where text boxes have overflow,
        while not connected to another element."""
        return self.style.get('showTextOverflowMarker', False) # Not inherited
    def _set_showTextOverflowMarker(self, showTextOverflowMarker):
        self.style['showTextOverflowMarker'] = bool(showTextOverflowMarker)
    showTextOverflowMarker = property(_get_showTextOverflowMarker, _set_showTextOverflowMarker)

    #   Image stuff

    def _get_showImageReference(self):
        """Boolean value. If True, the name/reference of an image element is show."""
        return self.style.get('showImageReference', False) # Not inherited
    def _set_showImageReference(self, showImageReference):
        self.style['showImageReference'] = bool(showImageReference)
    showImageReference = property(_get_showImageReference, _set_showImageReference)

    def _get_showImageLoresMarker(self):
        """Boolean value. If True, show lores-cache marker on images. This property inherits cascading. """
        return self.css('showImageLoresMarker', False) # Inherited
    def _set_showImageLoresMarker(self, showImageLoresMarker):
        self.style['showImageLoresMarker'] = bool(showImageLoresMarker)
    showImageLoresMarker = property(_get_showImageLoresMarker, _set_showImageLoresMarker)

    def _get_scaleImage(self):
        """Boolean value. If True, save images as cached scaled. """
        return self.css('scaleImage', True) # Inherited
    def _set_scaleImage(self, scaleImage):
        self.style['scaleImage'] = bool(scaleImage)
    scaleImage = property(_get_scaleImage, _set_scaleImage)

    def _get_scaledImageFactor(self):
        """If >= (default) 0.8 then don't save cached. Cached images should never enlarge. """
        return self.css('scaledImageFactor', True) # Inherited
    def _set_scaledImageFactor(self, scaledImageFactor):
        self.style['scaledImageFactor'] = bool(scaledImageFactor)
    scaledImageFactor = property(_get_scaledImageFactor, _set_scaledImageFactor)

    def _get_defaultImageWidth(self):
        """If set, then use this as default width for scaling images.
        Used as target for HTML context image scaling.
        """
        return self.css('defaultImageWidth') # Inherited. Can be None
    def _set_defaultImageWidth(self, defaultImageWidth):
        self.style['defaultImageWidth'] = defaultImageWidth # Can be None.
    defaultImageWidth = property(_get_defaultImageWidth, _set_defaultImageWidth)

    def _get_defaultImageHeight(self):
        """If set, then use this as default height for scaling images.
        Used as target for HTML context image scaling.
        """
        return self.css('defaultImageHeight') # Inherited. Can be None
    def _set_defaultImageHeight(self, defaultImageHeight):
        self.style['defaultImageHeight'] = defaultImageHeight # Can be None.
    defaultImageHeight = property(_get_defaultImageHeight, _set_defaultImageHeight)

    #   Spread stuff

    def _get_showImageReference(self):
        """Boolean value. If True, the name/reference of an image element is show."""
        return self.style.get('showImageReference', False) # Not inherited
    def _set_showImageReference(self, showImageReference):
        self.style['showImageReference'] = bool(showImageReference)
    showImageReference = property(_get_showImageReference, _set_showImageReference)

    #   CSS flags

    def _get_cssVerbose(self):
        """Boolean value. If True, adds information comments with original values to
        CSS export."""
        return self.css('cssVerbose', False) # Inherited
    def _set_cssVerbosee(self, cssVerbose):
        self.style['cssVerbose'] = bool(cssVerbose)
    cssVerbose = property(_get_cssVerbose, _set_cssVerbosee)

    #   Exporting

    def _get_saveUrlAsDirectory(self):
        """Boolean value. Flag to turn off saving self.url pages as directory.
        Instead, all "/" is replaced by "-". This choice is made for exprot .html
        paths, where a flat directory is less of a problem than adjusting all relative urls
        for images/CSS/JS
        """
        return self.css('saveUrlAsDirectory', False) # Inherited
    def _set_saveUrlAsDirectory(self, saveUrlAsDirectory):
        self.style['saveUrlAsDirectory'] = saveUrlAsDirectory
    saveUrlAsDirectory = property(_get_saveUrlAsDirectory, _set_saveUrlAsDirectory)

    def _get_doExport(self):
        """Boolean value. Flag to turn off any export, for view, e.g. in case of testing with docTest."""
        return self.css('doExport', False)
    def _set_doExport(self, doExport):
        self.style['doExport'] = bool(doExport)
    doExport = property(_get_doExport, _set_doExport)


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
