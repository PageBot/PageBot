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
#     element.py
#
from __future__ import division

import weakref
import copy
from pagebot.contexts import defaultContext
from pagebot.conditions.score import Score
from pagebot import x2cx, cx2x, y2cy, cy2y, z2cz, cz2z  
from pagebot.toolbox.transformer import point3D, pointOffset, uniqueID
from pagebot.style import (makeStyle, MIDDLE, CENTER, RIGHT, TOP, BOTTOM,
                           LEFT, FRONT, BACK, XALIGNS, YALIGNS, ZALIGNS,
                           MIN_WIDTH, MAX_WIDTH, MIN_HEIGHT, MAX_HEIGHT,
                           MIN_DEPTH, MAX_DEPTH, DEFAULT_WIDTH,
                           DEFAULT_HEIGHT, DEFAULT_DEPTH, XXXL,
                           INTERPOLATING_TIME_KEYS, ONLINE, INLINE,
                           OUTLINE)
from pagebot.toolbox.transformer import asFormatted, uniqueID
from pagebot.toolbox.timemark import TimeMark
from pagebot.contexts.builders.buildinfo import BuildInfo # Container with Builder flags and data/parametets

class Element(object):

    # Initialize the default Element behavior flags.
    # These flags can be overwritten by inheriting classes, or dynamically in instances,
    # e.g. where the settings of TextBox.nextBox and TextBox.nextPage define if a TextBox
    # instance can operate as a flow.
    isText = False
    isTextBox = False
    isFlow = False # Value is True if self.next if defined.
    isPage = False # Set to True by Page-like elements.
    isView = False


    def __init__(self, point=None, x=0, y=0, z=0, w=DEFAULT_WIDTH, h=DEFAULT_HEIGHT, d=DEFAULT_DEPTH, 
            t=0, parent=None, context=None, name=None, class_=None, title=None, description=None, language=None,
            style=None, conditions=None, info=None, framePath=None, 
            elements=None, template=None, nextElement=None, prevElement=None, nextPage=None, prevPage=None, 
            isLeftPage=None, isRightPage=None, bleed=None, 
            padding=None, pt=0, pr=0, pb=0, pl=0, pzf=0, pzb=0, 
            margin=None, mt=0, mr=0, mb=0, ml=0, mzf=0, mzb=0, 
            borders=None, borderTop=None, borderRight=None, borderBottom=None, borderLeft=None, 
            shadow=None, gradient=None, 
            drawBefore=None, drawAfter=None, 
            **kwargs):  
        u"""Basic initialize for every Element constructor. Element always have a location, even if not defined here.
        If values are added to the contructor parameter, instead of part in **kwargs, this forces them to have values,
        not inheriting from one of the parent styles.
        Ignore setting of setting eId as attribute, guaranteed to be unique.
        
        >>> import sys
        >>> e = Element(name='TestElement', x=10, y=20, w=100, h=120, maxH=1000, pl=11, pt=22, margin=(33,44,55,66))
        >>> e.name, e.info.description is None
        ('TestElement', True)
        >>> e.maxW == sys.maxint, e.maxH
        (True, 1000)
        >>> e.x, e.y, e.w, e.h, e.padding, e.margin
        (10, 20, 100, 120, (22, 0, 0, 11), (33, 44, 55, 66))
        >>> e = Element()
        >>> e.x, e.y, e.w, e.h, e.padding, e.margin
        (0, 0, 100, 100, (0, 0, 0, 0), (0, 0, 0, 0))

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.document import Document
        >>> c = DrawBotContext()
        >>> w, h = 300, 400
        >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=c)
        >>> page = doc[0]
        >>> e = Element(parent=page, x=0, y=20, w=page.w, h=3)
        >>> e.build(doc.getView(), (0, 0))
        >>> e.xy
        (0, 20)
        >>> e.size
        (300, 3, 1)
        >>> view = doc.getView()
        >>> e.build(view, (0, 0))

        >>> from pagebot.contexts.flatcontext import FlatContext 
        >>> from pagebot.document import Document
        >>> c = FlatContext()
        >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=c)
        >>> page = doc[0]
        >>> e = Element(parent=page, x=0, y=20, w=page.w, h=3)
        >>> # Allow the context to create a new document and page canvas. Normally view does it.
        >>> c.newPage(w, h) 
        >>> e.build(doc.getView(), (0, 0))
        >>> e.xy
        (0, 20)
        >>> e.size
        (300, 3, 1)

        """  
        assert point is None or isinstance(point, (tuple, list))
        
        # Set the property for elements that need their own context. If None the property will query parent and root.
        self.context = context 

        # Initilialize self._elements and self._eIds
        self.clearElements()

        self.style = makeStyle(style, **kwargs) # Make default style for t == 0
        # Initialize style values that are not supposed to inherite from parent styles.
        # Always store point in style as separate (x, y, z) values. Missing values are 0
        self.point3D = point or (x, y, z)
        self.w = w
        self.h = h
        self.d = d
        self.padding = padding or (pt, pr, pb, pl, pzf, pzb)
        self.margin = margin or (mt, mr, mb, ml, mzf, mzb)
        if bleed is not None:
            self.bleed = bleed # Property ignores to expand if None
        # Border info dict have format: 
        # dict(line=ONLINE, dash=None, stroke=0, strokeWidth=borderData)
        # If not borders defined, then drawing will use the stroke and strokeWidth (if defined)
        # for intuitive compatibility with DrawBot.
        self.borders = borders or (borderTop, borderRight, borderBottom, borderLeft)

        # Drawing hooks is same for 3 types of view/builders. Seperation must be done by caller.
        # Optional method to draw before child elements are drawn.
        self.drawBefore = drawBefore 
        # Optional method to draw right after child elements are drawn.
        self.drawAfter = drawAfter

        # Shadow and gradient, if defined
        self.shadow = shadow
        self.gradient = gradient
        self.framePath = framePath # Optiona frame path to draw instead of bounding box element rectangle.

        # Set timer of this element.
        self.timeMarks = [TimeMark(0, self.style), TimeMark(XXXL, self.style)] # Default TimeMarks from t == 0 until infinite of time.
        self._tm0 = self._tm1 = None # Boundary timemarks, where self._tm0.t <= t <= self._tm1.t, with expanded styles.
        self.t = t # Initialize self.style from t = 0
        self.timeKeys = INTERPOLATING_TIME_KEYS # List of names of style entries that can interpolate in time.

        if padding is not None:
            self.padding = padding # Expand by property
        if margin is not None:
            self.margin = margin

        self.name = name # Optional name of an element. Used as base for # id in case of HTML/CSS export.
        self.class_ = class_ # Optional class name. Ignored if None, not to overwrite CSS of parents.
        self.title = title or name # Optional to make difference between title name, style property
        self._eId = uniqueID(self) # Direct set property with guaranteed unique persistent value. 
        self._parent = None # Preset, so it exists for checking when appending parent.
        if parent is not None:
            # Add and set weakref to parent element or None, if it is the root. Caller must add self to its elements separately.
            self.parent = parent # Set referecnes in both directions. Remove any previous parent links
        # Conditional placement stuff
        if not conditions is None and not isinstance(conditions, (list, tuple)): # Allow singles
            conditions = [conditions]
        self.conditions = conditions # Explicitedly stored local in element, not inheriting from ancesters. Can be None.
        self.report = [] # Area for conditions and drawing methods to report errors and warnings.
        # Optional description of this element or its content. Otherwise None. Can be string or BabelString
        self.description = description 
        self.language = language # Optional language code from HTML standard. Otherwise None.
        # Save flow reference names
        self.prevElement = prevElement # Name of the prev flow element
        self.nextElement = nextElement # Name of the next flow element
        self.nextPage = nextPage # Name ot identifier of the next page that nextElement refers to,
        self.prevPage = prevPage # if a flow must run over page boundaries.
        self._isLeftPage = isLeftPage # True/False/None. In case None, parent will be queried
        self._isRightPage = isRightPage
        # Copy relevant info from template: w, h, elements, style, conditions, next, prev, nextPage
        # Initialze self.elements, add template elements and values, copy elements if defined.
        self.applyTemplate(template, elements) 
        # Initialize the default Element behavior tags, in case this is a flow.
        self.isFlow = not None in (prevElement, nextElement, nextPage)
        # Instance to hold details flags and data to direct the builder of this element.
        # Reference directory paths for source files, as used by building Html/Css templates and self.build
        self.info = info or BuildInfo()

    def __repr__(self):
        u"""Object as string.

        >>> e = Element(name='TestElement', x=10, y=20, w=100, h=120)
        >>> `e`
        'Element:TestElement (10, 20)'
        >>> e.title = 'MyTitle'
        >>> e.x, e.y = 100, 200
        >>> `e`
        'Element:MyTitle (100, 200)'
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
        return '%s%s (%d, %d)%s' % (self.__class__.__name__, name, int(round(self.point[0])), int(round(self.point[1])), elements)

    def __len__(self):
        u"""Answer total amount of elements, placed or not.

        >>> e = Element(name='TestElement', x=100, y=200, w=100, h=120)
        >>> childE1 = Element(name='E1', x=0, y=0, w=21, h=22)
        >>> childE2 = Element(name='E2', x=100, y=0, w=11, h=12)
        >>> i1 = e.appendElement(childE1)
        >>> i2 = e.appendElement(childE2)
        >>> i1, i2, len(e) # Index of appended elements and length of parent
        (0, 1, 2)
        """
        return len(self.elements) 

    #   T E M P L A T E

    def applyTemplate(self, template, elements=None):
        u"""Copy relevant info from template: w, h, elements, style, conditions when element is created.
        Don't call later.

        >>> from pagebot.elements import Template
        >>> e = Element(name='TestElement')
        >>> t = Template(x=11, y=12, w=100, h=200)
        >>> e.applyTemplate(t)
        >>> e.x, e.y, e.w, e.h
        (11, 12, 100, 200)
        """
        self.template = template # Set template value by property call, copying all template elements and attributes.
        if elements is not None:
            # Add optional list of additional elements.
            for e in elements or []: 
                self.appendElement(e) # Add cross reference searching for eId of elements.
            
    def _get_template(self):
        u"""Property get/set for e.template.

        >>> from pagebot.elements import Template
        >>> e = Element(name='TestElement')
        >>> t = Template(name='MyTemplate', x=11, y=12, w=100, h=200)
        >>> e.applyTemplate(t)
        >>> e.template
        Template:MyTemplate (11, 12)
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
            self.info = copy.copy(template.info)
            # Copy style items
            for  name, value in template.style.items():
                self.style[name] = value
            # Copy condition list. Does not have to be deepCopy, condition instances are multi-purpose.
            self.conditions = copy.copy(template.conditions)
            for e in template.elements:
                self.appendElement(e.copy(parent=self))
    template = property(_get_template, _set_template)

    #   E L E M E N T S
    #   Every element is potentioally a container of other elements.

    def __getitem__(self, eIdOrName):
        u"""Answer the element with eIdOrName. Answer None if the element does not exist.
        Elements behave as a semi-dictionary for child elements. 
        For retrieval by index, use e.elements[index]

        >>> e = Element(name='TestElement', x=100, y=200, w=100, h=120)
        >>> childE1 = Element(name='E1', x=0, y=0, w=21, h=22)
        >>> i = e.appendElement(childE1)
        >>> e['E1'] is childE1
        True
        """
        return self.get(eIdOrName)

    def __setitem__(self, eId, e):
        if not e in self.elements:
            self.elements.append(e)
        self._eIds[eId] = e

    def _get_eId(self):
        u"""Answer the unique element Id. Cannot set self._eId through self.eId property. 
        Set self._eId if really necessary, as hex string.

        >>> from pagebot.toolbox.transformer import hex2dec
        >>> e = Element(name='TestElement', x=100, y=200, w=100, h=120)
        >>> isinstance(hex2dec(e.eId), (int, long)) # Answers unique hex string in self._eId, such as '234FDC09FC10A0FA790'
        True
        """
        return self._eId
    eId = property(_get_eId)

    def _get_elements(self):
        u"""Property to get/set elements to parent self.

        >>> e = Element()
        >>> len(e), len(e.elements)
        (0, 0)
        >>> e.elements = (Element(), Element(), Element())
        >>> len(e), len(e.elements)
        (3, 3)
        """
        return self._elements
    def _set_elements(self, elements):
        self.clearElements() # Clear all existing child elements of self.
        for e in elements:
            self.appendElement(e) # Make sure to set all references.
    elements = property(_get_elements, _set_elements)

    def _get_elementIds(self): # Answer the x-ref dictionary with elements by their e.eIds
        u"""Answer the list with child.eId

        >>> e = Element()
        >>> e.elements = (Element(), Element(), Element())
        >>> len(e.elementIds)
        3
        """
        return self._eIds
    elementIds = property(_get_elementIds)

    def get(self, eIdOrName, default=None):
        u"""Answer the element by eId or name. Answer the same selection for default, if the element cannot be found.
        Answer None if it does not exist.

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
        u"""Answer the page element, if it has a unique element Id. Answer None if the eId does not exist as child.

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
        u"""Recursively answer the page of this element. This can be several layers above self.
        If there element has not a parent in the line of parents, then answer None.

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

    def getElementByName(self, name):
        u"""Answer the first element in the offspring list that fits the name. Answer None if it cannot be found.

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

    def clearElements(self):
        u"""Properly initializes self._elements and self._eIds. 
        Any existing elements get their parent weakrefs become None and will garbage collect.        >>> e1 = Element(name='Child')

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

    def copy(self, parent=None):
        u"""Answer a full copy of self, where the "unique" fields are set to default. 
        Also perform a deep copy on all child elements.

        >>> e1 = Element(name='Child', w=100)
        >>> e = Element(name='Parent', elements=[e1], w=200)
        >>> copyE = e.copy()
        >>> len(copyE) == len(e) == 1
        True
        >>> copyE is e, copyE['Child'] is e['Child'] # Element tree is copied
        (False, False)
        >>> copyE.name == e.name, copyE.w == e.w == 200, copyE['Child'].w == e['Child'].w == 100 # Values are copied
        (True, True, True)
        """
        # This also initializes the child element tree as empty list.
        # Style is supposed to be a deep-copyable dictionary.
        # self._eId is automatically created, guaranteed unique Id for every element.
        # Ignore original **kwargs, as these values are supposed to be in style now.
        # Inheriting classes are responsible to add their own specific values.
        e = self.__class__(x=self.x, y=self.y, z=self.z, w=self.w, h=self.h, d=self.d,
            t=self.t, # Copy type frame.
            parent=parent, # Allow to keep reference to current parent context and style.
            context=self._context, # Copy local context, None most cases, where reference to parent->doc context is required.
            name=self.name, class_=self.class_, title=self.title, description=self.description, language=self.language,
            style=copy.deepcopy(self.style), # Style is supposed to be a deep-copyable dictionary.
            conditions=copy.deepcopy(self.conditions), # Conditions may be modified by the element of ascestors.
            info=copy.deepcopy(self.info), # Info may be modified by the element of ascestors.
            framePath=self.framePath, 
            elements=None, # Will be copied separately.
            template=self.template, nextElement=self.nextElement, prevElement=self.prevElement, 
            nextPage=self.nextPage, prevPage=self.prevPage, 
            padding=self.padding, # Copies all padding values at once
            margin=self.margin, # Copies all margin values at once, 
            borders=self.borders, # Copies all borders at once.
            shadow=self.shadow, # Needs to be copied?
            gradient=self.gradient, # Needs to be copied? 
            drawBefore=self.drawBefore,
            drawAfter=self.drawAfter)
        # Now do the same for each child element and append it to self.
        for child in self.elements:
            e.appendElement(child.copy()) # Add the element to child list and update self._eId dictionary
        return e

    def setElementByIndex(self, e, index):
        u"""Replace the element, if there is already one at index. Otherwise append it to self.elements
        and answer the index number that it got. If index < 0, just answer None and do nothing.

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
            self.elements[index] = e
            if self.eId:
                self._eIds[e.eId] = e
            return index
        return self.appendElement(e)

    def appendElement(self, e):
        u"""Add element to the list of child elements. Note that elements can be added multiple times.
        If the element is alread placed in another container, then remove it from its current parent.
        This relation and position is lost. The position e is supposed to be filled already in local position.

        >>> e1 = Element(name='Child1')
        >>> e2 = Element(name='Child2')
        >>> e3 = Element(name='Child3')
        >>> e = Element(name='Parent', elements=[e1, e2])
        >>> i = e.appendElement(e3)
        >>> e.elements[-1] is e3, i
        (True, 2)
        >>> i = e.appendElement(e1) # Append elements that is already child of e
        >>> e.elements[0] is e2, e.elements[1] is e3, e.elements[2] is e1 # Now e1 is at end of list
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

    def removeElement(self, e):
        u"""If the element is placed in self, then remove it. Don't touch the position.

        >>> e1 = Element(name='Child1')
        >>> e2 = Element(name='Child2')
        >>> e3 = Element(name='Child3')
        >>> e = Element(name='Parent', elements=[e1, e2, e3])
        >>> removedE = e.removeElement(e2)
        >>> e.elements[0] is e1, e.elements[1] is e3, e2.parent is None
        (True, True, True)
        """
        assert e.parent is self
        e.setParent(None) # Unlink the parent reference of e
        if e.eId in self._eIds:
            del self._eIds[e.eId]
        if e in self._elements:
            self._elements.remove(e)
        return e # Answer the unlinked elements for convenience of the caller.

    def _get_show(self):
        u"""Set flag for drawing or interpretation with conditional.
        
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
        return self.css('show', True)
    def _set_show(self, showFlag):
        self.style['show'] = showFlag # Hiding rest of css for this value.
    show = property(_get_show, _set_show)

    #   C H I L D  E L E M E N T  P O S I T I O N S

    def getElementsAtPoint(self, point):
        u"""Answer the list with elements that fit the point. Note None in the point will match any
        value in the element position. Where None in the element position with not fit any xyz of the point.

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
        px, py, pz = point3D(point) 
        for e in self.elements:
            ex, ey, ez = point3D(e.point)
            if (ex == px or px is None) and (ey == py or py is None) and (ez == pz or pz is None):
                elements.append(e)
        return elements

    def getElementsPosition(self):
        u"""Answer the dictionary of element Ids as key and their position as value.

        >>> e1 = Element(name='Child1', x=20, y=30)
        >>> e2 = Element(name='Child2', x=20, y=40)
        >>> e = Element(name='Parent', elements=[e1, e2])
        >>> d = e.getElementsPosition()
        >>> len(d)
        2
        >>> d[e1.eId], d[e2.eId]
        ((20, 30), (20, 40))
        """
        elements = {}
        for e in self.elements:
            if e.eId:
                elements[e.eId] = e.point
        return elements

    def getPositions(self):
        u""""Answer the dictionary of positions of elements. 
        Key is the local point of the child element. Value is list of elements.

        >>> e1 = Element(name='Child1', x=20, y=30)
        >>> e2 = Element(name='Child2', x=20, y=40)
        >>> e = Element(name='Parent', elements=[e1, e2])
        >>> d = e.getPositions()
        >>> sorted(d.keys())
        [(20, 30), (20, 40)]
        >>> d[(20, 30)] == [e1], d[(20, 40)] == [e2]
        (True, True)
        """
        positions = {}
        for e in self.elements:
            point = tuple(e.point) # Point needs to be tuple to be used a key.
            if point not in positions:
                positions[point] = []
            positions[point].append(e)
        return positions


    #   F L O W

    # If the element is part of a flow, then answer the squence.
    
    def NOTNOW_getFlows(self):
        u"""Answer the set of flow element sequences on the page."""
        flows = {} # Key is nextBox of first textBox. Values is list of TextBox instances.
        for e in self.elements:
            if not e.isFlow:
                continue
            # Now we know that this element has a e.nextBox and e.nextPage
            # There should be a flow with that name in our flows yet
            found = False
            for nextId, seq in flows.items():
                if seq[-1].nextElement == e.name: # Glue to the end of the sequence.
                    seq.append(e)
                    found = True
                elif e.nextElement == seq[0].name: # Add at the start of the list.
                    seq.insert(0, e)
                    found = True
            if not found: # New entry
                flows[e.next] = [e]
        return flows

    def NOTNOW_getNextFlowBox(self, tb, makeNew=True):
        u"""Answer the next textBox that tb is pointing to. This can be on the same page or a next
        page, depending how the page (and probably its template) is defined."""
        if tb.nextPage: # Page number or name
            # The flow textBox is pointing to another page. Try to get it, and otherwise create one,
            # if makeNew is set to True.
            page = self.doc.getPage(tb.nextPage)
            if page is None and makeNew:
                page = self.doc.newPage(name=tb.nextPage)
            # Hard check. Otherwise something must be wrong in the template flow definition.
            # or there is more content than we can handle, while not allowing to create new pages.
            assert page is not None
            assert not page is self # Make sure that we got a another page than self.
            # Get the element on the next page that
            tb = page.getElementByName(tb.nextElement)
            # Hard check. Otherwise something must be wrong in the template flow definition.
            assert tb is not None and not tb
        else:
            page = self # Staying on the same page, flowing into another column.
            tb = self.getElementByName(tb.nextElement)
            # Hard check. Make sure that this one is empty, otherwise mistake in template
            assert not tb
        return page, tb

    #   If self.nextElement is defined, then check the condition if there is overflow.

    def isOverflow(self, tolerance):
        u"""Answer the boolean flag if this element needs overflow to be solved.
        This method is typically called by conditions such as Overflow2Next.
        This method is redefined by inheriting classed, such as
        TextBox, that can have overflow of text."""
        return True

    def overflow2Next(self):
        u"""Try to fix if there is overflow. Default behavior is to do nothing. This method
        is redefined by inheriting classed, such as TextBox, that can have overflow of text."""
        return True

    def _get_baselineGrid(self):
        u"""Answer the baseline grid distance, as defined in the (parent)style. 

        >>> e = Element()
        >>> e.baselineGrid is None # Undefined without style or parent style.
        True
        >>> e.baselineGrid = 12
        >>> e.baselineGrid
        12
        >>> e = Element(style=dict(baselineGrid=14))
        >>> e.baselineGrid
        14
        """
        return self.css('baselineGrid')
    def _set_baselineGrid(self, baselineGrid):
        self.style['baselineGrid'] = baselineGrid
    baselineGrid = property(_get_baselineGrid, _set_baselineGrid)

    def _get_baselineGridStart(self):
        u"""Answer the baseline grid startf, as defined in the (parent)style. 

        >>> e = Element()
        >>> e.baselineGridStart is None # Undefined without style or parent style.
        True
        >>> e.baselineGridStart = 17
        >>> e.baselineGridStart
        17
        >>> e = Element(style=dict(baselineGridStart=15))
        >>> e.baselineGridStart
        15
        """
        return self.css('baselineGridStart')
    def _set_baselineGridStart(self, baselineGridStart):
        self.style['baselineGridStart'] = baselineGridStart
    baselineGridStart = property(_get_baselineGridStart, _set_baselineGridStart)

    # Text conditions, always True for non-text elements.

    def isBaselineOnTop(self, tolerance):
        return True

    def isBaselineOnBottom(self, tolerance):
        return True

    def isBaselineOnTop(self, tolerance):
        return True

    def isAscenderOnTop(self, tolerance):
        return True

    def isCapHeightOnTop(self, tolerance):
        return True

    def isXHeightOnTop(self, tolerance):
        return True

    #   S T Y L E

    # Answer the cascaded style value, looking up the chain of ancestors, until style value is defined.

    def css(self, name, default=None):
        u"""In case we are looking for a plain css value, cascading from the main ancestor styles
        of self, then follow the parent links until document or root, if self does not contain
        the requested value."""
        if name in self.style:
            return self.style[name]
        if self.parent is not None:
            return self.parent.css(name, default)
        return default

    def getNamedStyle(self, styleName):
        u"""In case we are looking for a named style (e.g. used by the Typesetter to build a stack
        of cascading tag style, then query the ancestors for the named style. Default behavior
        of all elements is that they pass the request on to the root, which is nornally the document."""
        if self.parent:
            return self.parent.getNamedStyle(styleName)
        return None

    #   L I B --> Document.lib

    def _get_lib(self):
        u"""Answer the shared document.lib dictionary by property, used for share global entry by elements.
        Elements query their self.parent.lib until the root document is reached.

        >>> from pagebot.document import Document
        >>> from pagebot.elements.pbpage import Page
        >>> e = Element(name='Child')
        >>> page = Page(elements=[e])
        >>> doc = Document(pages=[page])
        >>> e.lib.get('MyValue') == None # Get undefined value
        True
        >>> doc.lib['MyValue'] = (1, 2, 3)
        >>> e.lib.get('MyValue') # Get defined value, up parent tree.
        (1, 2, 3)
        """
        parent = self.parent
        if parent is not None:
            return parent.lib # Either parent element or document.lib.
        return None # Document cannot be found, or there is there is no parent defined in the element.
    lib = property(_get_lib)

    def _get_doc(self):
        u"""Answer the root Document of this element by property, looking upward in the ancestor tree."""
        if self.parent is not None:
            return self.parent.doc
        return None
    doc = property(_get_doc)

    def _get_view(self):
        u"""Answer the self.doc.view, currently set for reference and building this element."""
        doc = self.doc
        if doc is not None:
            return doc.view
        return None
    view = property(_get_view)

    def _get_context(self):
        u"""Answer the context of this element. In general the self._context will be None, to allow
        searching the parent-->doc tree. But there may be exceptions where elements+children need their own."""
        if self._context is not None:
            return self._context
        # Context not defined for this element, try parent.
        if self.parent is not None:
            return self.parent.context
        # No context defined and no parent, we only can answer the default context here.
        return defaultContext
    def _set_context(self, context):
        self._context = context
    context = property(_get_context, _set_context)

    def _get_builder(self):
        return self.context.b
    b = builder = property(_get_builder)

    def newString(self, bs, e=None, style=None, w=None, h=None, fontSize=None, 
            styleName=None, tagName=None):
        u"""Create a new BabelString, using the current type of self.doc.context,
        or pagebot.contexts.defaultContext if not self.doc or self.doc.view defined, 
        if bs is a plain string. Otherwise just answer the BabelString unchanged.
        In case of a BabelString, is has to be the same as the current context would
        create, otherwise an error is raised. In other words, there is no BabelString
        conversion defined (no reliable way of doing that, they should be created 
        in the right context from the beginning)."""
        return self.context.newString(bs, e=e, style=style, w=w, h=h, fontSize=fontSize, 
            styleName=styleName, tagName=tagName)
        
    # Most common properties

    def setParent(self, parent):
        u"""Set the parent of self as weakref if it is not None. Don't call self.appendElement().
        Calling setParent is not the main way to add an element to a parent, because the original
        parent would not know that the element disappeared. Call self.appendElement(e), which will
        call this method. """
        if parent is not None:
            parent = weakref.ref(parent)
        self._parent = parent # Can be None if self needs to be unlinked from a parent tree. E.g. when moving it.

    def _get_parent(self):
        u"""Answer the parent of the element, if it exists, by weakref reference. Answer None of there
        is not parent defined or if the parent not longer exists."""
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
        u"""Answer all elements that share self.parent, not including self in the list."""
        siblings = []
        for e in self.parent.elements:
            if not e is self:
                siblings.append(e)
        return siblings
    siblings = property(_get_siblings)

    def _get_ancestors(self):
        u"""Answer the list of anscestors of self, including the document root. Self is not included."""
        ancestors = []
        parent = self.parent
        while parent is not None:
            assert not parent in ancestors, '[%s.%s] Illegal loop in parent->ancestors reference.' % (self.__class__.__name__, self.name)
            ancestors.append(parent)
            parent = parent.parent
        return ancestors
    ancestors = property(_get_ancestors)

    def _get_point(self):
        u"""Answer the 2D point tuple of the relative local position of self."""
        return self.x, self.y # Answer as 2D
    def _set_point(self, point):
        self.x = point[0]
        self.y = point[1]
    point = property(_get_point, _set_point)

    def _get_point3D(self):
        u"""Answer the 3D point tuple of the relative local position of self."""
        return self.x, self.y, self.z
    def _set_point3D(self, point):
        self.x, self.y, self.z = point3D(point) # Always store as 3D-point, z = 0 if missing.
    point3D = property(_get_point3D, _set_point3D)

    def _get_oPoint(self): 
        u"""Answer the self.point, where y can be flipped, depending on the self.originTop flag."""
        return self._applyOrigin(self.point)
    oPoint3D = oPoint = property(_get_oPoint)

    # Orientation of elements (and pages)

    def isLeftPage(self):
        u"""Normal elements don't know the left/right orientation of the page that they are on.
        Pass the request on to the parent, until a page is reachted."""
        if self._isLeftPage is not None:
            return self._isLeftPage
        if self.parent is not None:
            return self.parent.isLeftPage() 
        return False

    def isRightPage(self):
        u"""Normal elements don't know the left/right orientation of the page that they are on.
        Pass the request on to the parent, until a page is reachted."""
        if self._isRightPage is not None:
            return self._isRightPage
        if self.parent is not None:
            return self.parent.isRightPage()
        return False

    def _get_gridX(self):
        u"""Answer the grid, depending on the left/right orientation of self.

        >>> e = Element(gridX=(10,20,30))
        >>> e.gridX
        (10, 20, 30)
        >>> e.gridX = 40, 50, 60
        >>> e.gridX
        (40, 50, 60)
        """
        if self.isLeftPage():
            return self.css('gridL') or self.css('gridX')
        if self.isRightPage():
            return self.css('gridR') or self.css('gridX')
        return self.css('gridX')
    def _set_gridX(self, gridX):
        if self.isLeftPage():
            self.style['gridL'] = gridX  # Save locally, blocking CSS parent scope for this param.
        elif self.isRightPage():
            self.style['gridR'] = gridX
        else:
            self.style['gridX'] = gridX
    gridX = property(_get_gridX, _set_gridX)

    def _get_gridY(self):
        u"""Answer the vertical grid, depending on the top/bottom orientation of self.

        >>> e = Element(gridY=(10,20,30))
        >>> e.gridY
        (10, 20, 30)
        >>> e.gridY = 40, 50, 60
        >>> e.gridY
        (40, 50, 60)
        """
        return self.css('gridY')
    def _set_gridY(self, gridY):
        self.style['gridY'] = gridY  # Save locally, blocking CSS parent scope for this param.
    gridY = property(_get_gridY, _set_gridY)

    def _get_gridZ(self):
        u"""Answer the grid, depending on the left/right orientation of self.

        >>> e = Element(gridZ=(10,20,30))
        >>> e.gridZ
        (10, 20, 30)
        >>> e.gridZ = 40, 50, 60
        >>> e.gridZ
        (40, 50, 60)
        """
        return self.css('gridZ')
    def _set_gridZ(self, gridZ):
        self.style['gridZ'] = gridZ  # Save locally, blocking CSS parent scope for this param.
    gridZ = property(_get_gridZ, _set_gridZ)

    def getGridColumns(self):
        u"""Answer the constructed sequence of [(columnX, columnW), ...] in the block of the element.
        Note that this is different from the gridX definition [(wx, gutter), ...]
        If there is one or more None in the grid definition, then try to fit equally on self.cw.
        If gurtter is left None, then the default style gutter is filled there.

        >>> column, gutter = 48, 8 # Preset padding
        >>> e = Element(w=300, h=100, cw=column, gw=gutter, isLeftPage=True)
        >>> e.getGridColumns() # Equal devided column widths
        [(0, 48), (56, 48), (112, 48), (168, 48), (224, 48)]
        >>> e.cw = 64 # Change column width
        >>> e.gw = 12 # Change gutter 
        >>> e.getGridColumns() # Changed equal deviced columns
        [(0, 64), (76, 64), (152, 64), (228, 64)]
        >>> e.gridX = (30, 40, 50, 60) 
        >>> e.getGridColumns() # Columns from value list
        [(0, 30), (42, 40), (94, 50), (156, 60)]
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

    def getGridRows(self):
        u"""Answer the constructed sequence of [(columnX, columnW), ...] in the block of the element.
        Note that this is different from the gridX definition [(wx, gutter), ...]
        If there is one or more None in the grid definition, then try to fit equally on self.cw.
        If gutter is left None, then the default style gutter is filled there.

        >>> column, gutter = 48, 8 # Preset padding
        >>> e = Element(w=100, h=300, ch=column, gh=gutter, isLeftPage=True)
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

    # Plain coordinates

    def _get_x(self):
        u"""Answer the x position of self.

        >>> e = Element(x=100)
        >>> e.x, e.y, e.z
        (100, 0, 0)
        >>> e.x = 101
        >>> e.x, e.y, e.z
        (101, 0, 0)
        """
        return self.style['x'] # Direct from style. Not CSS lookup.
    def _set_x(self, x):
        self.style['x'] = x
    x = property(_get_x, _set_x)
    
    def _get_y(self):
        u"""Answer the y position of self.

        >>> e = Element(y=100)
        >>> e.x, e.y, e.z
        (0, 100, 0)
        >>> e.y = 101
        >>> e.x, e.y, e.z
        (0, 101, 0)
        """
        return self.style['y'] # Direct from style. Not CSS lookup.
    def _set_y(self, y):
        self.style['y'] = y
    y = property(_get_y, _set_y)
    
    def _get_z(self):
        u"""Answer the z position of self.

        >>> e = Element(z=100)
        >>> e.x, e.y, e.z
        (0, 0, 100)
        >>> e.z = 101
        >>> e.x, e.y, e.z
        (0, 0, 101)
        """
        return self.style['z'] # Direct from style. Not CSS lookup.
    def _set_z(self, z):
        self.style['z'] = z
    z = property(_get_z, _set_z)
    
    def _get_xy(self):
        u"""Answer ther Point2D tuple.

        >>> e = Element(x=10, y=20)
        >>> e.xy
        (10, 20)
        >>> e.xy = 11, 21
        >>> e.xy
        (11, 21)
        >>> e.xy = 12, 22, 32 # Ignore the z-value
        >>> e.xy
        (12, 22)
        >>> e.y += 100
        >>> e.xy
        (12, 122)
        """
        return self.x, self.y
    def _set_xy(self, p):
        self.x = p[0]
        self.y = p[1] # Ignore any z
    xy = property(_get_xy, _set_xy)

    def _get_xyz(self):
        u"""Answer ther Point3D tuple.

        >>> e = Element(x=10, y=20, z=30)
        >>> e.xyz
        (10, 20, 30)
        >>> e.xyz = 11, 21, 31
        >>> e.xyz
        (11, 21, 31)
        >>> e.xyz = 12, 22, 32 
        >>> e.xyz
        (12, 22, 32)
        >>> e.x += 100
        >>> e.xyz
        (112, 22, 32)
        """
        return self.x, self.y, self.z
    def _set_xyz(self, p):
        self.x = p[0]
        self.y = p[1] 
        self.z = p[2] 
    xyz = property(_get_xyz, _set_xyz)


    #   T I M E

    def _get_t(self):
        u"""The self._t status is the time status, interpolating between the values in 
        self.tStyles[t1] and self.tStyles[t2] where t1 <= t <= t2 and these styles contain
        the requested parameters.

        >>> e = Element()
        >>> e.t
        0
        >>> e.t = 16
        >>> e.t
        16
        """
        return self._t
    def _set_t(self, t):
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
    #    u"""Answer a new interpolated TimeState instance, from the enclosing time states for t."""
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
        u"""Answer the position of the left side of the element, depending on alignment.

        >>> e = Element(x=100, w=248, xAlign=LEFT)
        >>> e.left
        100
        >>> e.left = 100
        >>> e.left
        100
        >>> e.xAlign = CENTER
        >>> int(e.left)
        -24
        >>> e.xAlign = RIGHT
        >>> e.left
        -148
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

    def _get_mLeft(self): # Left, including left margin
        return self.left - self.css('ml')
    def _set_mLeft(self, x):
        self.left = x + self.css('ml')
    mLeft = property(_get_mLeft, _set_mLeft)

    def _get_center(self):
        u"""Answer the position of the horizontal center of the element, depending on alignment.

        >>> e = Element(x=100, w=248, xAlign=LEFT)
        >>> int(e.center)
        224
        >>> e.center = 224
        >>> int(e.center)
        224
        >>> e.xAlign = CENTER
        >>> int(e.center)
        100
        >>> e.xAlign = RIGHT
        >>> int(e.center)
        -24
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
            self.x = x - self.w/2
        elif xAlign == RIGHT:
            self.x = x + self.w/2
        else:
            self.x = x
    center = property(_get_center, _set_center)

    def _get_right(self):
        u"""Answer the position of the right side of the element, depending on alignment.

        >>> e = Element(x=100, w=248, xAlign=LEFT)
        >>> e.right
        348
        >>> e.xAlign = CENTER
        >>> int(e.right)
        224
        >>> e.xAlign = RIGHT
        >>> e.right
        100
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
            self.x = x - self.w
        elif xAlign == CENTER:
            self.x = x - self.w/2
        else:
            self.x = x
    right = property(_get_right, _set_right)

    def _get_mRight(self):
        u"""Right position, including right margin.

        >>> e = Element(x=100, w=248, mr=44, xAlign=LEFT)
        >>> e.mRight
        304
        >>> e.xAlign = RIGHT
        >>> e.mRight
        56
        >>> e.xAlign = CENTER
        >>> int(e.mRight)
        180
        """
        return self.right - self.mr
    def _set_mRight(self, x):
        self.right = x + self.mr
    mRight = property(_get_mRight, _set_mRight)

    # Vertical

    def _get_top(self):
        u"""Answer the top position (relative to self.parent) of self.

        >>> e = Element(y=100, h=248, yAlign=TOP)
        >>> e.top
        100
        >>> e.yAlign = BOTTOM
        >>> e.top
        348
        >>> e.yAlign = MIDDLE
        >>> int(e.top)
        -24
        """
        yAlign = self.yAlign
        if yAlign == MIDDLE:
            return self.y - self.h/2
        if yAlign == BOTTOM:
            if self.originTop:
                return self.y - self.h
            return self.y + self.h
        return self.y
    def _set_top(self, y):
        u"""Shift the element so self.top == y."""
        yAlign = self.yAlign
        if yAlign == MIDDLE:
            self.y = y + self.h/2
        elif yAlign == BOTTOM:
            if self.originTop:
                self.y = y + self.h
            else:
                self.y = y - self.h
        else:
            self.y = y
    top = property(_get_top, _set_top)

    def _get_mTop(self): # Top, including top margin
        if self.originTop:
            return self.top - self.mt
        return self.top + self.mt
    def _set_mTop(self, y):
        if self.originTop:
            self.top = y + self.mt
        else:
            self.top = y - self.mt
    mTop = property(_get_mTop, _set_mTop)

    def _get_middle(self): 
        u"""On bounding box, not including margins.
        
        >>> e = Element(y=100, h=248, yAlign=TOP)
        >>> int(e.middle)
        -24
        >>> e.yAlign = BOTTOM
        >>> int(e.middle)
        224
        >>> e.yAlign = MIDDLE
        >>> int(e.middle)
        100
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
        u"""On bounding box, not including margins.

        >>> e = Element(y=100, h=248, yAlign=TOP)
        >>> e.bottom
        -148
        >>> e.yAlign = BOTTOM
        >>> e.bottom
        100
        >>> e.yAlign = MIDDLE
        >>> int(e.bottom)
        224
        """
        yAlign = self.yAlign
        if yAlign == TOP:
            if self.originTop:
                return self.y + self.h
            return self.y - self.h
        if yAlign == MIDDLE:
            return self.y + self.h/2
        return self.y
    def _set_bottom(self, y):
        yAlign = self.yAlign
        if yAlign == TOP:
            if self.originTop:
                self.y = y - self.h
            else:
                self.y = y + self.h
        elif yAlign == MIDDLE:
            self.y = y - self.h/2
        else:
            self.y = y
    bottom = property(_get_bottom, _set_bottom)

    def _get_mBottom(self): # Bottom, including bottom margin
        if self.originTop:
            return self.bottom + self.mb
        return self.bottom - self.mb
    def _set_mBottom(self, y):
        if self.originTop:
            self.bottom = y - self.mb
        else:
            self.bottom = y + self.mb
    mBottom = property(_get_mBottom, _set_mBottom)

    # Depth, running  in vertical z-axis dirction. Viewer is origin, posistive value is perpendicular to the screen.
    # Besides future usage in real 3D rendering, the z-axis is used to compare conditional status in element layers.

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
            self.z = z + self.d/2
        elif zAlign == BACK:
            self.z = z + self.d
        else:
            self.z = z
    front = property(_get_front, _set_front)

    def _get_mFront(self): # Front, including front margin
        return self.front + self.css('mzf')
    def _set_mFront(self, z):
        self.front = z + self.css('mzf')
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
            self.z = z - self.d/2
        elif zAlign == FRONT:
            self.z = z - self.d
        else:
            self.z = z
    back = property(_get_back, _set_back)

    def _get_mBack(self): # Front, including front margin
        return self.back - self.css('mzb')
    def _set_mBack(self, z):
        self.back = z - self.css('mzb')
    mBack = property(_get_mBack, _set_mBack)

    # Borders

    def _borderDict(self, borderData):
        u"""Internal method to create a dictionary with border info. If no valid border
        dictionary is defined, then use optional stroke and strokeWidth to create one.
        Otherwise answer *None*."""
        if isinstance(borderData, (int, long, float)):
            return dict(line=ONLINE, dash=None, stroke=0, strokeWidth=borderData)
        if isinstance(borderData, dict):
            if not 'line' in borderData: # (ONLINE, INLINE, OUTLINE):
                borderData['line'] = ONLINE
            if not 'dash' in borderData:
                borderData['dash'] = None
            if not 'strokeWidth' in borderData:
                borderData['strokeWidth'] = 1
            if not 'stroke' in borderData:
                borderData['stroke'] = 0
            return borderData
        # TODO: Solve this, error on initialize of element, _parent does not yet exist.
        #stroke = self.css('stroke')
        #strokeWidth = self.css('strokeWidht')
        #if stroke is not None and strokeWidth:
        #     return dict(line=ONLINE, dash=None, stroke=stroke, strokeWidth=strokeWidth)
        return None

    def _get_borders(self):
        return self.borderTop, self.borderRight, self.borderBottom, self.borderLeft
    def _set_borders(self, borders):
        if not isinstance(borders, (list, tuple)):
            # Make copy, in case it is a dict, otherwise changes will be made in all.
            borders = copy.copy(borders), copy.copy(borders), copy.copy(borders), copy.copy(borders)
        elif len(borders) == 2:
            borders = borders*2
        elif len(borders) == 1:
            borders = borders*4
        self.borderTop, self.borderRight, self.borderBottom, self.borderLeft = borders
    # Seems to be onfusing having only one of the two. So allow both property names for the same.
    border = borders = property(_get_borders, _set_borders)

    def _get_borderTop(self):
        return self.css('borderTop')
    def _set_borderTop(self, border):
        self.style['borderTop'] = self._borderDict(border)
    borderTop = property(_get_borderTop, _set_borderTop)

    def _get_borderRight(self):
        return self.css('borderRight')
    def _set_borderRight(self, border):
        self.style['borderRight'] = self._borderDict(border)
    borderRight = property(_get_borderRight, _set_borderRight)

    def _get_borderBottom(self):
        return self.css('borderBottom')
    def _set_borderBottom(self, border):
        self.style['borderBottom'] = self._borderDict(border)
    borderBottom = property(_get_borderBottom, _set_borderBottom)

    def _get_borderLeft(self):
        return self.css('borderLeft')
    def _set_borderLeft(self, border):
        self.style['borderLeft'] = self._borderDict(border)
    borderLeft = property(_get_borderLeft, _set_borderLeft)

    # Alignment types, defines where the origin of the element is located.

    def _validateXAlign(self, xAlign): # Check and answer value
        assert xAlign in XALIGNS, '[%s.xAlign] Alignment "%s" not valid in %s' % (self.__class__.__name__, xAlign, sorted(XALIGNS))
        return xAlign
    def _validateYAlign(self, yAlign): # Check and answer value
        assert yAlign in YALIGNS, '[%s.yAlign] Alignment "%s" not valid in %s' % (self.__class__.__name__, yAlign, sorted(YALIGNS))
        return yAlign
    def _validateZAlign(self, zAlign): # Check and answer value
        assert zAlign in ZALIGNS, '[%s.zAlign] Alignment "%s" not valid in %s' % (self.__class__.__name__, zAlign, sorted(ZALIGNS))
        return zAlign

    def _get_xAlign(self): # Answer the type of x-alignment. For compatibility allow align and xAlign as equivalents.
        return self._validateXAlign(self.css('xAlign'))
    def _set_xAlign(self, xAlign):
        self.style['xAlign'] = self._validateXAlign(xAlign) # Save locally, blocking CSS parent scope for this param.
    xAlign = property(_get_xAlign, _set_xAlign)
     
    def _get_yAlign(self): # Answer the type of x-alignment.
        return self._validateYAlign(self.css('yAlign'))
    def _set_yAlign(self, yAlign):
        self.style['yAlign'] = self._validateYAlign(yAlign) # Save locally, blocking CSS parent scope for this param.
    yAlign = property(_get_yAlign, _set_yAlign)
     
    def _get_zAlign(self): # Answer the type of x-alignment.
        return self._validateZAlign(self.css('zAlign'))
    def _set_zAlign(self, zAlign):
        self.style['zAlign'] = self._validateZAlign(zAlign) # Save locally, blocking CSS parent scope for this param.
    zAlign = property(_get_zAlign, _set_zAlign)
     
    # Position by column + gutter size index.

    def _get_cx(self): # Answer the x-position, defined in columns. Can be fractional for elements not on grid.
        return x2cx(self.x, self)
    def _set_cx(self, cx): # Set the x-position, defined in columns.
        x = cx2x(cx, self)
        if x is not None:
            self.x = x
    cx = property(_get_cx, _set_cx)

    def _get_cy(self): # Answer the y-position, defined in columns. Can be fractional for elements not on grid.
        return y2cy(self.y, self)
    def _set_cy(self, cy): # Set the x-position, defined in columns.
        y = cy2y(cy, self)
        if y is not None:
            self.y = y
    cy = property(_get_cy, _set_cy)

    def _get_cz(self): # Answer the z-position, defined in columns. Can be fractional for elements not on 3D-grid.
        return z2cz(self.y, self)
    def _set_cz(self, cz): # Set the z-position, defined in style['cz'] columns.
        z = cz2z(cz, self)
        if z is not None:
            self.z = z
    cz = property(_get_cz, _set_cz)

    # TODO: Make this work
    """
    def _get_cols(self): # Number of columns in the given self.w and self.colW
        return w2cols(self.w, self) # Using self.cw and self.gw
    def _set_cols(self, cols):
        w = cols2w(cw, self)
        if w is not None:
            self.w = w
    cols = property(_get_cols, _set_cols)

    def _get_rows(self): # Number of vertical rows, in the given self.h and self.colH
        return h2rows(self.h, self) # Using self.ch and self.gw
    def _set_rows(self, rows):
        h = rows2h(ch, self)
        if h is not None:
            self.h = h
    rows = property(_get_rows, _set_rows)

    def _get_lanes(self): # z-axis name for rows and cols.
        return d2lanes(self.d, self) # Using self.cd and self.gw
    def _set_lanes(self, cd):
        d = lanes2d(cd, self)
        if d is not None:
            self.d = d
    lanes = property(_get_lanes, _set_lanes)
    """

    def _get_cw(self): # Column width
        return self.css('cw')
    def _set_cw(self, cw):
        self.style['cw'] = cw
    cw = property(_get_cw, _set_cw)

    def _get_ch(self): # Column height (row height)
        return self.css('ch')
    def _set_ch(self, ch):
        self.style['ch'] = ch
    ch = property(_get_ch, _set_ch)

    def _get_cd(self): # Column depth (slice?)
        return self.css('cd')
    def _set_cd(self, cd):
        self.style['cd'] = cd
    cd = property(_get_cd, _set_cd)


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
        u"""Gutter property for (e.gw, e.gh) 

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
        if isinstance(gutter, (long, int, float)):
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
        u"""Gutter 3D property for (e.gw, e.gh, e.gd) 

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
        if isinstance(gutter3D, (long, int, float)):
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
        u"""Answer the value for bleed over the sides of parent or page objects.
        Elements will take of the reposition/scaling themselves"""
        return self.bleedTop, self.bleedRight, self.bleedBottom, self.bleedLeft
    def _set_bleed(self, bleed):
        if isinstance(bleed, (list, tuple)):
            if len(bleed) == 4:
                self.bleedTop, self.bleedRight, self.bleedBottom, self.bleedLeft = bleed
            elif len(bleed) == 2:
                self.bleedTop, self.bleedRight = self.bleedBottom, self.bleedLeft = bleed
            else: # Length  
                self.bleedTop = self.bleedRight = self.bleedBottom = self.bleedLeft = bleed[0]
        else:
            self.bleedTop = self.bleedRight = self.bleedBottom = self.bleedLeft = bleed
    bleed = property(_get_bleed, _set_bleed)

    def _get_bleedTop(self):
        u"""Answer the value for bleed over the sides of parent or page objects.
        Elements will take of the reposition/scaling themselves"""
        return self.css('bleedTop', 0)
    def _set_bleedTop(self, bleed):
        assert isinstance(bleed, (int, float))
        self.style['bleedTop'] = bleed
    bleedTop = property(_get_bleedTop, _set_bleedTop)

    def _get_bleedBottom(self):
        u"""Answer the value for bleed over the sides of parent or page objects.
        Elements will take of the reposition/scaling themselves"""
        return self.css('bleedBottom', 0)
    def _set_bleedBottom(self, bleed):
        assert isinstance(bleed, (int, float))
        self.style['bleedBottom'] = bleed
    bleedBottom = property(_get_bleedBottom, _set_bleedBottom)

    def _get_bleedLeft(self):
        u"""Answer the value for bleed over the sides of parent or page objects.
        Elements will take of the reposition/scaling themselves"""
        return self.css('bleedLeft', 0)
    def _set_bleedLeft(self, bleed):
        assert isinstance(bleed, (int, float))
        self.style['bleedLeft'] = bleed
    bleedLeft = property(_get_bleedLeft, _set_bleedLeft)

    def _get_bleedRight(self):
        u"""Answer the value for bleed over the sides of parent or page objects.
        Elements will take of the reposition/scaling themselves"""
        return self.css('bleedRight', 0)
    def _set_bleedRight(self, bleed):
        assert isinstance(bleed, (int, float))
        self.style['bleedRight'] = bleed
    bleedRight = property(_get_bleedRight, _set_bleedRight)

    # Absolute positions

    def _get_rootX(self): 
        u"""Answer the read-only property root value of local self.x, 
        from the whole tree of ancestors.

        >>> e1 = Element(x=10)
        >>> e2 = Element(x=20, elements=[e1])
        >>> e3 = Element(x=44, elements=[e2])
        >>> e1.x, e1.rootX, e2.x, e2.rootX, e3.x, e3.rootX
        (10, 74, 20, 64, 44, 44)
        """
        parent = self.parent
        if parent is not None:
            return self.x + parent.rootX # Add relative self to parents position.
        return self.x
    rootX = property(_get_rootX)

    def _get_rootY(self): 
        u"""Answer the read-only property root value of local self.y, 
        from the whole tree of ancestors.

        >>> e1 = Element(y=10)
        >>> e2 = Element(y=20, elements=[e1])
        >>> e3 = Element(y=44, elements=[e2])
        >>> e1.y, e1.rootY, e2.y, e2.rootY, e3.y, e3.rootY
        (10, 74, 20, 64, 44, 44)
        """
        parent = self.parent
        if parent is not None:
            return self.y + parent.rootY # Add relative self to parents position.
        return self.y
    rootY = property(_get_rootY)

    def _get_rootZ(self): 
        u"""Answer the read-only property root value of local self.z, 
        from the whole tree of ancestors.

        >>> e1 = Element(z=10)
        >>> e2 = Element(z=20, elements=[e1])
        >>> e3 = Element(z=44, elements=[e2])
        >>> e1.z, e1.rootZ, e2.z, e2.rootZ, e3.z, e3.rootZ
        (10, 74, 20, 64, 44, 44)
        """
        parent = self.parent
        if parent is not None:
            return self.z + parent.rootZ # Add relative self to parents position.
        return self.z
    rootZ = property(_get_rootZ)

    # (w, h, d) size of the element.

    def _get_w(self): 
        u"""Answer the width of the element.

        >>> e = Element(w=100, maxW=1000)
        >>> e.w
        100
        >>> e.w = 101
        >>> e.w
        101
        >>> e.w = e.maxW + 10000
        >>> e.w
        1000
        >>> e.w = 0
        >>> e.w, e.w == DEFAULT_WIDTH
        (100, True)
        """ 
        return min(self.maxW, max(self.minW, self.style['w'], MIN_WIDTH)) # From self.style, don't inherit.
    def _set_w(self, w):
        self.style['w'] = w or DEFAULT_WIDTH # Overwrite element local style from here, parent css becomes inaccessable.
    w = property(_get_w, _set_w)

    def _get_mw(self): # Width, including margins
        u"""Width property for self.mw style.

        >>> e = Element(w=10, ml=22, mr=33)
        >>> e.mw
        65
        >>> e = Element()
        >>> e.w = 10
        >>> e.ml = 22
        >>> e.mr = 33
        >>> e.mw
        65
        """
        return self.w + self.ml + self.mr # Add margins to width
    def _set_mw(self, w):
        self.style['w'] = max(0, w - self.ml - self.mr) # Cannot become < 0
    mw = property(_get_mw, _set_mw)

    def _get_h(self):
        u"""Answer the height of the element.

        >>> e = Element(h=100, maxH=1000)
        >>> e.h
        100
        >>> e.h = 101
        >>> e.h
        101
        >>> e.h = e.maxH + 10000
        >>> e.h
        1000
        >>> e.h = 0
        >>> e.h, e.h == DEFAULT_HEIGHT
        (100, True)
        """ 
        return min(self.maxH, max(self.minH, self.style['h'], MIN_HEIGHT)) # From self.style, don't inherit.
    def _set_h(self, h):
        self.style['h'] = h or DEFAULT_HEIGHT # Overwrite element local style from here, parent css becomes inaccessable.
    h = property(_get_h, _set_h)

    def _get_mh(self): # Height, including margins
        u"""Width property for self.mh style.

        >>> e = Element(h=10, mt=22, mb=33)
        >>> e.mh
        65
        >>> e = Element()
        >>> e.h = 10
        >>> e.mt = 22
        >>> e.mb = 33
        >>> e.mh
        65
        """
        return self.h + self.mt + self.mb # Add margins to height
    def _set_mh(self, h):
        self.style['h'] = max(0, h - self.mt - self.mb) # Cannot become < 0
    mh = property(_get_mh, _set_mh)

    def _get_d(self): 
        u"""Answer the depth of the element.

        >>> e = Element(d=100, maxD=1000)
        >>> e.d
        100
        >>> e.d = 101
        >>> e.d
        101
        >>> e.d = e.maxD + 10000
        >>> e.d
        1000
        >>> e.d = 0
        >>> e.d, e.d == MIN_DEPTH
        (1, True)
        """ 
        return min(self.maxD, max(self.minD, self.style['d'], MIN_DEPTH)) # From self.style, don't inherit.
    def _set_d(self, d):
        self.style['d'] = d or MIN_DEPTH # Overwrite element local style from here, parent css becomes inaccessable.
    d = property(_get_d, _set_d)

    def _get_md(self): # Depth, including margin front and margin back in z-axis.
        u"""Width property for self.md style.

        >>> e = Element(d=10, mzb=22, mzf=33)
        >>> e.md
        65
        >>> e = Element()
        >>> e.d = 10
        >>> e.mzb = 22
        >>> e.mzf = 33
        >>> e.md
        65
        """
        return self.d + self.mzb + self.mzf # Add front and back margins to depth
    def _set_md(self, d):
        self.style['d'] = max(0, d - self.mzf - self.mzb) # Cannot become < 0, behind viewer?
    md = property(_get_md, _set_md)

    # Margin properties

    # TODO: Add support of "auto" values, doing live centering.

    def _get_margin(self): 
        u"""Tuple of paddings in CSS order, direction of clock
        Can be 123, [123], [123, 234], [123, 234, 345], [123, 234, 345, 456] 
        or [123, 234, 345, 456, 567, 678]

        >>> e = Element(margin=(10, 20, 30, 40))
        >>> e.mt, e.mr, e.mb, e.ml
        (10, 20, 30, 40)
        >>> e.ml = 123
        >>> e.margin
        (10, 20, 30, 123)
        >>> e.margin = 11
        >>> e.margin
        (11, 11, 11, 11)
        >>> e.margin = (11, 22)
        >>> e.margin
        (11, 22, 11, 22)
        >>> e.margin = (11, 22, 33)
        >>> e.margin
        (11, 22, 33, 11)
        >>> e.margin = (11, 22, 33, 44)
        >>> e.margin
        (11, 22, 33, 44)
        >>> e.mt, e.mr, e.mb, e.ml
        (11, 22, 33, 44)
        >>> e.margin = (11, 22, 33, 44, 55, 66)
        >>> e.margin
        (11, 22, 33, 44)
        """
        return self.mt, self.mr, self.mb, self.ml
    def _set_margin(self, margin):
        # Can be 123, [123], [123, 234] or [123, 234, 345, 4565, ]
        if isinstance(margin, (long, int, float)):
            margin = [margin]
        if len(margin) == 1: # All same value
            margin = (margin[0], margin[0], margin[0], margin[0], margin[0], margin[0])
        elif len(margin) == 2: # mt == mb, ml == mr, mzf == mzb
            margin = (margin[0], margin[1], margin[0], margin[1], margin[0], margin[1])
        elif len(margin) == 3: # mt == ml == mzf, mb == mr == mzb
            margin = (margin[0], margin[1], margin[2], margin[0], margin[1], margin[2])
        elif len(margin) == 4: # mt, mr, mb, ml, 0, 0
            margin = (margin[0], margin[1], margin[2], margin[3], 0, 0)
        elif len(margin) == 6:
            pass
        else:
            raise ValueError
        self.mt, self.mr, self.mb, self.ml, self.mzf, self.mzb = margin
    margin = property(_get_margin, _set_margin)

    def _get_margin3D(self): 
        u"""Tuple of margin in CSS order + (front, back), direction of clock
        
        >>> e = Element(margin=(10, 20, 30, 40))
        >>> e.mt, e.mr, e.mb, e.ml
        (10, 20, 30, 40)
        >>> e.ml = 123
        >>> e.margin3D
        (10, 20, 30, 123, 0, 0)
        >>> e.margin3D = 11
        >>> e.margin3D
        (11, 11, 11, 11, 11, 11)
        >>> e.margin3D = (11, 22)
        >>> e.margin3D
        (11, 22, 11, 22, 11, 22)
        >>> e.margin3D = (11, 22, 33)
        >>> e.margin3D
        (11, 22, 33, 11, 22, 33)
        >>> e.margin3D = (11, 22, 33, 44)
        >>> e.margin3D
        (11, 22, 33, 44, 0, 0)
        >>> e.margin3D = (11, 22, 33, 44, 55, 66)
        >>> e.margin3D
        (11, 22, 33, 44, 55, 66)
        """
        return self.mt, self.mr, self.mb, self.ml, self.mzf, self.mzb
    margin3D = property(_get_margin3D, _set_margin)

    def _get_mt(self): 
        u"""Margin top property

        >>> e = Element(mt=12)
        >>> e.mt
        12
        >>> e.mt = 13
        >>> e.mt
        13
        >>> e.style = dict(mt=14)
        >>> e.mt
        14
        """
        return self.style['mt'] # Don't inherit
    def _set_mt(self, mt):
        self.style['mt'] = mt  # Overwrite element local style from here, parent css becomes inaccessable.
    mt = property(_get_mt, _set_mt)
    
    def _get_mb(self): # Margin bottom
        u"""Margin bottom property

        >>> e = Element(mb=12)
        >>> e.mb
        12
        >>> e.mb = 13
        >>> e.mb
        13
        >>> e.style = dict(mb=14)
        >>> e.mb
        14
        """
        return self.style['mb'] # Don't inherit
    def _set_mb(self, mb):
        self.style['mb'] = mb  # Overwrite element local style from here, parent css becomes inaccessable.
    mb = property(_get_mb, _set_mb)
    
    def _get_ml(self): # Margin left
        u"""Margin left property

        >>> e = Element(ml=12)
        >>> e.ml
        12
        >>> e.ml = 13
        >>> e.ml
        13
        >>> e.style = dict(ml=14)
        >>> e.ml
        14
        """
        return self.style['ml'] # Don't inherit
    def _set_ml(self, ml):
        self.style['ml'] = ml # Overwrite element local style from here, parent css becomes inaccessable.
    ml = property(_get_ml, _set_ml)
    
    def _get_mr(self): # Margin right
        u"""Margin right property

        >>> e = Element(mr=12)
        >>> e.mr
        12
        >>> e.mr = 13
        >>> e.mr
        13
        >>> e.style = dict(mr=14)
        >>> e.mr
        14
        """
        return self.style['mr'] # Don't inherit
    def _set_mr(self, mr):
        self.style['mr'] = mr  # Overwrite element local style from here, parent css becomes inaccessable.
    mr = property(_get_mr, _set_mr)

    def _get_mzf(self): # Margin z-axis front
        u"""Margin z-axis front property (closest to view point)

        >>> e = Element(mzf=12)
        >>> e.mzf
        12
        >>> e.mzf = 13
        >>> e.mzf
        13
        >>> e.style = dict(mzf=14)
        >>> e.mzf
        14
        """
        return self.style['mzf'] # Don't inherit
    def _set_mzf(self, mzf):
        self.style['mzf'] = mzf  # Overwrite element local style from here, parent css becomes inaccessable.
    mzf = property(_get_mzf, _set_mzf)
    
    def _get_mzb(self): # Margin z-axis back
        u"""Margin z-axis back property (most distant to view point)

        >>> e = Element(mzb=12)
        >>> e.mzb
        12
        >>> e.mzb = 13
        >>> e.mzb
        13
        >>> e.style = dict(mzb=14)
        >>> e.mzb
        14
        """
        return self.style['mzb'] # Don't inherit
    def _set_mzb(self, mzb):
        self.style['mzb'] = mzb  # Overwrite element local style from here, parent css becomes inaccessable.
    mzb = property(_get_mzb, _set_mzb)
        
    # Padding properties

    # TODO: Add support of "auto" values, doing live centering.
 
    def _get_padding(self): 
        u"""Tuple of paddings in CSS order, direction of clock starting on top
        Can be 123, [123], [123, 234], [123, 234, 345], [123, 234, 345, 456] 
        or [123, 234, 345, 456, 567, 678]

        >>> e = Element(padding=(10, 20, 30, 40))
        >>> e.pt, e.pr, e.pb, e.pl
        (10, 20, 30, 40)
        >>> e.pl = 123
        >>> e.padding
        (10, 20, 30, 123)
        >>> e.padding = 11
        >>> e.padding
        (11, 11, 11, 11)
        >>> e.padding = (11, 22)
        >>> e.padding
        (11, 22, 11, 22)
        >>> e.padding = (11, 22, 33)
        >>> e.padding
        (11, 22, 33, 11)
        >>> e.padding = (11, 22, 33, 44)
        >>> e.padding
        (11, 22, 33, 44)
        >>> e.pt, e.pr, e.pb, e.pl
        (11, 22, 33, 44)
        >>> e.padding = (11, 22, 33, 44, 55, 66)
        >>> e.padding
        (11, 22, 33, 44)
        >>> e.padding3D
        (11, 22, 33, 44, 55, 66)
        """
        return self.pt, self.pr, self.pb, self.pl
    def _set_padding(self, padding):
        # Can be 123, [123], [123, 234] or [123, 234, 345, 4565]
        assert padding is not None
        if isinstance(padding, (long, int, float)):
            padding = [padding]
        if len(padding) == 1: # All same value
            padding = (padding[0], padding[0], padding[0], padding[0], padding[0], padding[0])
        elif len(padding) == 2: # pt == pb, pl == pr, pzf == pzb
            padding = (padding[0], padding[1], padding[0], padding[1], padding[0], padding[1])
        elif len(padding) == 3: # pt == pl == pzf, pb == pr == pzb
            padding = (padding[0], padding[1], padding[2], padding[0], padding[1], padding[2])
        elif len(padding) == 4: # pt, pr, pb, pl, 0, 0
            padding = (padding[0], padding[1], padding[2], padding[3], 0, 0)
        elif len(padding) == 6:
            pass
        else:
            raise ValueError
        self.pt, self.pr, self.pb, self.pl, self.pzf, self.pzb = padding
    padding = property(_get_padding, _set_padding)

    def _get_padding3D(self): 
        u"""Tuple of padding in CSS order + (front, back), direction of clock
        
        >>> e = Element(padding=(10, 20, 30, 40))
        >>> e.pt, e.pr, e.pb, e.pl
        (10, 20, 30, 40)
        >>> e.pl = 123
        >>> e.padding3D
        (10, 20, 30, 123, 0, 0)
        >>> e.padding3D = 11
        >>> e.padding3D
        (11, 11, 11, 11, 11, 11)
        >>> e.padding3D = (11, 22)
        >>> e.padding3D
        (11, 22, 11, 22, 11, 22)
        >>> e.padding3D = (11, 22, 33)
        >>> e.padding3D
        (11, 22, 33, 11, 22, 33)
        >>> e.padding3D = (11, 22, 33, 44)
        >>> e.padding3D
        (11, 22, 33, 44, 0, 0)
        >>> e.padding3D = (11, 22, 33, 44, 55, 66)
        >>> e.padding3D
        (11, 22, 33, 44, 55, 66)
        """
        return self.pt, self.pr, self.pb, self.pl, self.pzf, self.pzb
    padding3D = property(_get_padding3D, _set_padding)

    def _get_pt(self): 
        u"""Padding top property

        >>> e = Element(pt=12)
        >>> e.pt
        12
        >>> e.pt = 13
        >>> e.pt
        13
        >>> e.style = dict(pt=14)
        >>> e.pt
        14
        >>> e.padding # Make sure other did not change.
        (14, 0, 0, 0)
        """
        return self.css('pt', 0)
    def _set_pt(self, pt):
        self.style['pt'] = pt  # Overwrite element local style from here, parent css becomes inaccessable.
    pt = property(_get_pt, _set_pt)

    def _get_pb(self): # Padding bottom
        u"""Padding bottom property

        >>> e = Element(padding=(10, 20, 30, 40))
        >>> e.pb
        30
        >>> e = Element(pb=12)
        >>> e.pb
        12
        >>> e.pb = 13
        >>> e.pb
        13
        >>> e.style = dict(pb=14)
        >>> e.pb
        14
        >>> e.padding # Make sure other did not change.
        (0, 0, 14, 0)
        """
        return self.css('pb', 0)
    def _set_pb(self, pb):
        self.style['pb'] = pb  # Overwrite element local style from here, parent css becomes inaccessable.
    pb = property(_get_pb, _set_pb)
    
    def _get_pl(self): 
        u"""Padding left property

        >>> e = Element(padding=(10, 20, 30, 40))
        >>> e.pl
        40
        >>> e = Element(pl=12)
        >>> e.pl
        12
        >>> e.pl = 13
        >>> e.pl
        13
        >>> e.style = dict(pl=14)
        >>> e.pl
        14
        >>> e.padding # Make sure other did not change.
        (0, 0, 0, 14)
        """
        return self.css('pl', 0)
    def _set_pl(self, pl):
        self.style['pl'] = pl # Overwrite element local style from here, parent css becomes inaccessable.
    pl = property(_get_pl, _set_pl)
    
    def _get_pr(self): # Margin right
        u"""Padding right property

        >>> e = Element(padding=(10, 20, 30, 40))
        >>> e.pr
        20
        >>> e = Element(pr=12)
        >>> e.pr
        12
        >>> e.pr = 13
        >>> e.pr
        13
        >>> e.style = dict(pr=14)
        >>> e.pr
        14
        >>> e.padding # Make sure other did not change.
        (0, 14, 0, 0)
        """
        return self.css('pr', 0)
    def _set_pr(self, pr):
        self.style['pr'] = pr  # Overwrite element local style from here, parent css becomes inaccessable.
    pr = property(_get_pr, _set_pr)

    def _get_pzf(self): 
        u"""Padding z-axis front property

        >>> e = Element(pzf=12)
        >>> e.pzf
        12
        >>> e.pzf = 13
        >>> e.pzf
        13
        >>> e.style = dict(pzf=14)
        >>> e.pzf
        14
        >>> e.padding3D # Make sure other did not change.
        (0, 0, 0, 0, 14, 0)
        """
        return self.css('pzf', 0)
    def _set_pzf(self, pzf):
        self.style['pzf'] = pzf  # Overwrite element local style from here, parent css becomes inaccessable.
    pzf = property(_get_pzf, _set_pzf)
    
    def _get_pzb(self): 
        u"""Padding z-axis back property

        >>> e = Element(pzb=12)
        >>> e.pzb
        12
        >>> e.pzb = 13
        >>> e.pzb
        13
        >>> e.style = dict(pzb=14)
        >>> e.pzb
        14
        >>> e.padding3D # Make sure other did not change.
        (0, 0, 0, 0, 0, 14)
        """
        return self.css('pzb', 0)
    def _set_pzb(self, pzb):
        self.style['pzb'] = pzb  # Overwrite element local style from here, parent css becomes inaccessable.
    pzb = property(_get_pzb, _set_pzb)

    def _get_pw(self): 
        u"""Padded width read-only property of the element block.

        >>> e = Element(w=400, pl=22, pr=33)
        >>> e.pw
        345
        """
        return self.w - self.pl - self.pr
    pw = property(_get_pw)
    
    def _get_ph(self):
        u"""Padded height read-only property of the element block. 

        >>> e = Element(h=400, pb=22, pt=33)
        >>> e.ph
        345
        """
        return self.h - self.pb - self.pt
    ph = property(_get_ph)
    
    def _get_pd(self):
        u"""Padded depth read-only property of the element block.

        >>> e = Element(d=400, pzf=22, pzb=33)
        >>> e.pd
        345
        """
        return self.d - self.pzf - self.pzb
    pd = property(_get_pd)

    def _get_originTop(self):
        u"""Answer the style flag if all point y values should measure top-down (typographic page
        orientation), instead of bottom-up (mathematical orientation). For Y-axis only. 
        The axes in X and Z directions are fixed.

        >>> e = Element()
        >>> e.originTop is None
        True
        >>> e = Element(originTop=True)
        >>> e.originTop
        True
        >>> e.originTop = False
        >>> e.originTop
        False
        """
        return self.css('originTop')
    def _set_originTop(self, flag):
        if flag:
            self.style['originTop'] = True # Overwrite element local style from here, parent css becomes inaccessable.
            self.style['yAlign'] = TOP
        else:
            self.style['originTop'] = False
            self.style['yAlign'] = BOTTOM
    originTop = property(_get_originTop, _set_originTop)

    def _get_size(self):
        u"""Answer the 3D size tuple.

        >>> e = Element(w=100, h=200)
        >>> e.size
        (100, 200, 1)
        >>> e.d = 111
        >>> e.size
        (100, 200, 111)
        >>> e.d = 300
        >>> e.size
        (100, 200, 300)
        >>> e.size = (101, 201, 301)
        >>> e.size
        (101, 201, 301)
        """
        return self.getSize3D()  
    def _set_size(self, size):
        self.setSize(size)
    size = property(_get_size, _set_size)

    def getSize(self):
        u"""Answer the size of the element by calling properties self.w and self.h.
        This allows element to dynamically calculate the size if necessary, by redefining the
        self.w and/or self.h properties.
        
        >>> e = Element(w=100, h=200)
        >>> e.getSize()
        (100, 200)
        """
        return self.w, self.h

    def getSize3D(self):
        u"""Answer the 3D size of the element.

        >>> e = Element(w=100, h=200, d=300)
        >>> e.getSize3D() # Same as e.size
        (100, 200, 300)
        """
        return self.w, self.h, self.d

    def setSize(self, w, h=0, d=0):
        u"""Set the size of the element by calling by properties self.w and self.h. 
        If set, then overwrite access from style width and height. self.d is optional attribute.

        >>> e = Element()
        >>> e.setSize(100, 200, 300)
        >>> e.size
        (100, 200, 300)
        >>> e.setSize(101) # Set h to default and d to 1
        >>> e.size
        (101, 100, 1)
        >>> e.setSize(101, 201)
        >>> e.size
        (101, 201, 1)
        >>> e.setSize((101, 201, 301)) # Set by size tuple
        >>> e.size
        (101, 201, 301)
        >>> e.setSize((101, 201)) # Set by size tuple
        >>> e.size
        (101, 201, 1)
        """
        if isinstance(w, (list, tuple)):
            if len(w) == 2:
                w, h = w
            elif len(w) == 3:
                w, h, d = w
            else:
                raise ValueError
        self.w = w # Set by property
        self.h = h 
        self.d = d # By default elements have 0 depth.

    #   S H A D O W   &  G R A D I E N T

    def _get_shadow(self):
        return self.css('shadow')
    def _set_shadow(self, shadow):
        self.style['shadow'] = shadow
    shadow = property(_get_shadow, _set_shadow)

    def _get_textShadow(self):
        return self.css('textShadow')
    def _set_textShadow(self, textShadow):
        self.style['textShadow'] = textShadow
    textShadow = property(_get_textShadow, _set_textShadow)

    def _get_gradient(self):
        return self.css('gradient')
    def _set_gradient(self, gradient):
        self.style['gradient'] = gradient
    gradient = property(_get_gradient, _set_gradient)

    def _get_textGradient(self):
        return self.css('textGradient')
    def _set_textGradient(self, textGradient):
        self.style['textGradient'] = textGradient
    textGradient = property(_get_textGradient, _set_textGradient)

    def _get_box3D(self):
        u"""Answer the 3D bounding box of self from (self.x, self.y, self.w, self.h) properties."""
        return self.x or 0, self.y or 0, self.z or 0, self.w or 0, self.h or 0, self.d or 0
    box3D = property(_get_box3D)

    def _get_box(self):
        u"""Construct the bounding box from (self.x, self.y, self.w, self.h) properties."""
        return self.x or 0, self.y or 0, self.w or 0, self.h or 0
    box = property(_get_box)

    def _get_marginBox(self):
        u"""Calculate the margin position and margin resized box of the element, after applying the
        option style margin."""
        mt = self.mt
        mb = self.mb
        ml = self.ml
        if self.originTop:
            y = self.y - mt
        else:
            y = self.y - mb
        return (self.x - ml, y,
            self.w + ml + self.mr, 
            self.h + mt - mb)
    marginBox = property(_get_marginBox)

    def _get_paddedBox(self):
        u"""Calculate the padded position and padded resized box of the element, after applying the
        style padding. Answered format (x, y, w, h)."""
        pl = self.pl
        pt = self.pt
        pb = self.pb
        if self.originTop:
            y = self.y + pt
        else:
            y = self.y + pb
        return (self.x + pl, y, self.w - pl - self.pr, self.h - pt - pb)
    paddedBox = property(_get_paddedBox)

    def _get_paddedBox3D(self):
        u"""Calculate the padded position and padded resized box in 3D of the lement, after applying
        the style padding. Answered format (x, y, z, w, h, d)."""
        x, y, w, h = self.paddedBox
        pzf = self.pzf
        return x, y, self.z + pzf, w, h, self.d - pzf - self.pzb
    paddedBox3D = property(_get_paddedBox3D)

    # PDF naming: MediaBox is highlighted with a magenta rectangle, the BleedBox with a cyan 
    # one while dark blue is used for the TrimBox.
    # https://www.prepressure.com/pdf/basics/page-boxes

    # "Box" is bounding box on a single element.
    # "Block" is here used as bounding box of a group of elements.

    def _get_block3D(self):
        u"""Answer the vacuum 3D bounding box around all child elements.

        >>> e1 = Element(x=10, y=10, z=10, w=100, h=100, d=101)
        >>> e2 = Element(x=50, y=50, z=50, w=200, h=100, d=401)
        >>> e3 = Element(x=70, y=30, z=50, w=801, h=10, d=100)
        >>> #e1.w, e1.h

        >>> e = Element(elements=[e1, e2, e3])
        >>> #e1.left, e1.right

        >>> #e.block3D
        """
        x1 = y1 = z1 = XXXL
        x2 = y2 = z2 = -XXXL
        if not self.elements:
            return 0, 0, 0, 0, 0, 0
        for e in self.elements:
            x1 = min(x1, e.left)
            x2 = max(x2, e.right)
            if e.originTop:
                y1 = min(y1, e.top)
                y2 = max(y2, e.bottom)
            else:
                y1 = min(y1, e.bottom)
                y2 = max(y2, e.top)
            z1 = min(z1, e.front)
            z2 = max(z2, e.back)

        return x1, y1, z1, x2 - x1, y2 - y1, z2 - z1
    block3D = property(_get_block3D)

    def _get_block(self):
        u"""Answer the vacuum bounding box around all child elements in 2D

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

    def _get_marginBlock3D(self):
        u"""Answer the vacuum 3D bounding box around all child elements."""
        x1 = y1 = z1 = XXXL
        x2 = y2 = z2 = -XXXL
        if not self.elements:
            return 0, 0, 0, 0, 0, 0
        for e in self.elements:
            x1 = min(x1, e.left - e.ml)
            x2 = max(x2, e.right + e.mr)
            if e.originTop:
                y1 = min(y1, e.top - e.mt)
                y2 = max(y2, e.bottom + e.mb)
            else:
                y1 = min(y1, e.bottom - e.mb)
                y2 = max(y2, e.top + e.mt)
            z1 = min(z1, e.front - e.zmf)
            z2 = max(z2, e.back - e.zmb)

        return x1, y1, z1, x2 - x1, y2 - y1, z2 - z1
    marginBlock3D = property(_get_marginBlock3D)

    def _get_marginBlock(self):
        u"""Answer the vacuum bounding box around all child elements in 2D"""
        x, y, _, w, h, _ = self._get_marginBlock3D()
        return x, y, w, h
    marginBlock = property(_get_marginBlock)

    def _get_paddedBlock3D(self):
        u"""Answer the vacuum 3D bounding box around all child elements, 
        subtracting their paddings. Sizes cannot become nextive."""
        x1 = y1 = z1 = XXXL
        x2 = y2 = z2 = -XXXL
        if not self.elements:
            return 0, 0, 0, 0, 0, 0
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
        return x1, y1, z1, x2 - x1, y2 - y1, z2 - z1
    paddedBlock3D = property(_get_paddedBlock3D)

    def _get_paddedBlock(self):
        u"""Answer the vacuum bounding box around all child elements in 2D"""
        x, y, _, w, h, _ = self._get_paddedBlock3D()
        return x, y, w, h
    paddedBlock = property(_get_paddedBlock)

    def _get_originsBlock3D(self):
        u"""Answer (minX, minY, maxX, maxY, minZ, maxZ) for all element origins."""
        minX = minY = XXXL
        maxX = maxY = -XXXL
        for e in self.elements:
            minX = min(minX, e.x)
            maxX = max(maxX, e.x)
            minY = min(minY, e.y)
            maxY = max(maxY, e.y)
            minZ = min(minZ, e.z)
            maxZ = max(maxZ, e.z)
        return minX, minY, minZ, maxX, maxY, maxZ
    originsBlock3D = property(_get_originsBlock3D)

    def _get_originsBlock(self):
        minX, minY, _, maxX, maxY, _ = self._get_originsBlock3D()
        return minX, minY, maxX, maxY
    originsBlock = property(_get_originsBlock)

    # Size limits

    def _get_minW(self):
        return self.css('minW') or MIN_WIDTH
    def _set_minW(self, minW): # Clip values
        self.style['minW'] = max(MIN_WIDTH, min(MAX_WIDTH, minW)) # Set on local style, shielding parent self.css value.
    minW = property(_get_minW, _set_minW)

    def _get_minH(self):
        return self.css('minH') or MIN_HEIGHT
    def _set_minH(self, minH):
        self.style['minH'] = max(MIN_HEIGHT, min(MAX_HEIGHT, minH)) # Set on local style, shielding parent self.css value.
    minH = property(_get_minH, _set_minH)

    def _get_minD(self): # Set/get the minimal depth, in case the element has 3D dimensions.
        return self.css('minD') or MIN_DEPTH
    def _set_minD(self, minD):
        self.style['minD'] = max(MIN_DEPTH, min(MAX_DEPTH, minD)) # Set on local style, shielding parent self.css value.
    minD = property(_get_minD, _set_minD)

    def getMinSize(self):
        u"""Answer the (minW, minH) of this element.

        >>> e = Element()
        >>> e.getMinSize()
        (1, 1)
        """
        return self.minW, self.minH

    def getMinSize3D(self):
        u"""Answer the (minW, minH, minD) of this element.

        >>> e = Element()
        >>> e.getMinSize3D()
        (1, 1, 1)
        """
        return self.minW, self.minH, self.minD

    def setMinSize(self, minW, minH=None, minD=None):
        u"""Set the min size vaues.

        >>> e = Element()
        >>> e.getMinSize()
        (1, 1)
        >>> e.setMinSize(100, 200, 300)
        >>> e.getMinSize()
        (100, 200)
        >>> e.getMinSize3D()
        (100, 200, 300)
        """
        if minW and minH is None and minD is None:
            if isinstance(minW, (int, float, long)):
                self.minW = self.minH = self.minD = minW
            elif isinstance(minH, (tuple, list)):
                if len(minH) == 1:
                    self.minW = self.minH = self.minD = minW
                elif len(minH) == 2:
                    self.minW = self.minH = minW
                    self.minD = 0
                elif len(minH) == 3:
                    self.minW, self.minH, self.minD = minW
        else:
            self.minW = minW
            self.minH = minH
            self.minD = minD or 0 # Optional minimum depth of the element.

    def _get_maxW(self):
        maxW = self.style.get('maxW')
        if self.parent:
            maxW = maxW or self.parent.w
        return maxW or MAX_WIDTH # Unless defined local, take current parent.w as maxW
    def _set_maxW(self, maxW):
        self.style['maxW'] = max(MIN_WIDTH, min(MAX_WIDTH, maxW)) # Set on local style, shielding parent self.css value.
    maxW = property(_get_maxW, _set_maxW)

    def _get_maxH(self):
        maxH = self.style.get('maxH')
        if self.parent:
            maxH = maxH or self.parent.h
        return maxH or MAX_HEIGHT # Unless defined local, take current parent.w as maxW
    def _set_maxH(self, maxH):
        self.style['maxH'] = max(MIN_HEIGHT, min(MAX_HEIGHT, maxH)) # Set on local style, shielding parent self.css value.
    maxH = property(_get_maxH, _set_maxH)

    def _get_maxD(self):
        maxD = self.style.get('maxD')
        if self.parent:
            maxD = maxD or self.parent.d
        return maxD or MAX_DEPTH # Unless defined local, take current parent.w as maxW
    def _set_maxD(self, maxD):
        self.style['maxD'] = max(MIN_DEPTH, min(MAX_DEPTH, maxD)) # Set on local style, shielding parent self.css value.
    maxD = property(_get_maxD, _set_maxD)

    def getMaxSize(self):
        return self.maxW, self.maxH, self.maxD # No limit if value is None

    def setMaxSize(self, maxW, maxH=None, maxD=None):
        if maxW and maxH is None and maxD is None:
            if isinstance(maxW, (int, float, long)):
                self.maxW = self.maxH = self.maxD = maxW
            elif isinstance(maxH, (tuple, list)):
                if len(maxH) == 1:
                    self.maxW = self.maxH = self.maxD = maxW
                elif len(maxH) == 2:
                    self.maxW = self.maxH = maxW
                    self.maxD = 0
                elif len(maxH) == 3:
                    self.maxW, self.maxH, self.maxD = maxW
        else:
            self.maxW = maxW
            self.maxH = maxH
            self.maxD = maxD or 0 # Optional maximum depth of the element.

    def _get_scaleX(self):
        return self.css('scaleX', 1)
    def _set_scaleX(self, scaleX):
        assert scaleX != 0
        self.style['scaleX'] = scaleX # Set on local style, shielding parent self.css value.
    scaleX = property(_get_scaleX, _set_scaleX)

    def _get_scaleY(self):
        return self.css('scaleX', 1)
    def _set_scaleY(self, scaleY):
        assert scaleY != 0
        self.style['scaleY'] = scaleY # Set on local style, shielding parent self.css value.
    scaleY = property(_get_scaleY, _set_scaleY)

    def _get_scaleZ(self):
        return self.css('scaleZ', 1)
    def _set_scaleZ(self, scaleZ):
        assert scaleZ != 0
        self.style['scaleZ'] = scaleZ # Set on local style, shielding parent self.css value.
    scaleZ = property(_get_scaleZ, _set_scaleZ)

    def getFloatTopSide(self, previousOnly=True, tolerance=0):
        u"""Answer the max y that can float to top, without overlapping previous sibling elements.
        This means we are just looking at the vertical projection between (self.left, self.right).
        Note that the y may be outside the parent box. Only elements with identical z-value are compared.
        Comparison of available spave, includes the margins of the elements."""
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
        u"""Answer the max y that can float to bottom, without overlapping previous sibling elements.
        This means we are just looking at the vertical projection of (self.left, self.right).
        Note that the y may be outside the parent box. Only elements with identical z-value are compared.
        Comparison of available spave, includes the margins of the elements."""
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
        u"""Answer the max x that can float to the left, without overlapping previous sibling elements.
        This means we are just looking at the horizontal projection of (self.top, self.bottom).
        Note that the x may be outside the parent box. Only elements with identical z-value are compared.
        Comparison of available spave, includes the margins of the elements."""
        x = 0
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
            x = max(e.mRight, x)
        return x

    def getFloatRightSide(self, previousOnly=True, tolerance=0):
        u"""Answer the max Y that can float to the right, without overlapping previous sibling elements.
        This means we are just looking at the vertical projection of (self.left, self.right).
        Note that the y may be outside the parent box. Only elements with identical z-value are compared.
        Comparison of available spave, includes the margins of the elements."""
        x = self.parent.w
        for e in self.parent.elements: # All elements that share self.parent, except self.
            if previousOnly and e is self: # Only look at siblings that are previous in the list.
                break 
            if abs(e.z - self.z) > tolerance or e.mBottom < self.mTop or self.mBottom < e.mTop:
                continue # Not equal z-layer or not in window of horizontal projection.
            x = min(e.mLeft, x)
        return x

    def _applyAlignment(self, p):
        u"""Answer the p according to the alignment status in the css.""" 
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
        u"""If self.originTop is False, then the y-value is interpreted as mathematics, 
        starting at the bottom of the parent element, moving up.
        If the flag is True, then move from top down, where the origin of the element becomes
        top-left of the parent."""
        px, py, pz = point3D(p)
        if self.originTop and self.parent:
            py = self.parent.h - py
        return px, py, pz

    def _applyRotation(self, view, mx, my, angle):
        u"""Apply the rotation for angle, where (mx, my) is the rotation center."""
        view.saveGraphicState()
        # TODO: Working on this.

    def _restoreRotation(self, view):
        u"""Reset graphics state from rotation mode."""
        if self.css('rotationX') and self.css('rotationY') and self.css('rotationAngle'):
            view.restoreGraphicState()

    def _applyScale(self, view, p):
        u"""Internal method to apply the scale, if both *self.scaleX* and *self.scaleY* are set. Use this
        method paired with self._restoreScale(). The (x, y) answered as reversed scaled tuple,
        so drawing elements can still draw on "real size", while the other element is in scaled mode."""
        sx = self.scaleX
        sy = self.scaleY
        sz = self.scaleZ
        p = point3D(p)
        if sx and sy and sz and (sx != 1 or sy != 1 or sz != 1): # Make sure these are value scale values.
            view.saveGraphicState()
            view.scale(sx, sy)
            p = (p[0] / sx, p[1] / sy, p[2] / sz) # Scale point in 3 dimensions.
        return p

    def _restoreScale(self, view):
        u"""Reset graphics state from svaed scale mode. Make sure to match the call of self._applyScale.
        If one of (self.scaleX, self.scaleY, self.scaleZ) is not 0 or 1, then do the restore."""
        sx = self.scaleX
        sy = self.scaleY
        sz = self.scaleZ
        if sx and sy and sz and (sx != 1 or sy != 1 or sz != 1): # Make sure these are value scale values.
            view.restoreGraphicState()

    #   D R A W I N G  S U P P O R T 

    def getMetricsString(self, view=None):
        u"""Answer a single string with metrics info about the element. Default is to show the posiiton
        and size (in points and columns). This method can be redefined by inheriting elements
        that want to show additional information."""
        s = '%s\nPosition: %s, %s, %s\nSize: %s, %s\nColumn point: %s, %s\nColumn size: %s, %s' % \
            (self.__class__.__name__ + ' ' + (self.name or ''), asFormatted(self.x), asFormatted(self.y), asFormatted(self.z), 
             asFormatted(self.w), asFormatted(self.h), 
             asFormatted(self.cx), asFormatted(self.cy), asFormatted(self.cw), asFormatted(self.ch),
            )
        if self.xAlign or self.yAlign:
            s += '\nAlign: %s, %s' % (self.xAlign, self.yAlign)
        if self.conditions:
            if view is None:
                view = self.doc.view
            score = self.evaluate(view)
            s += '\nConditions: %d | Evaluate %d' % (len(self.conditions), score.result)
            if score.fails:
                s += ' Fails: %d' % len(score.fails)
                for eFail in score.fails:
                    s += '\n%s %s' % eFail
        return s

    def buildFrame(self, view, p):
        u"""Draw fill of the rectangular element space.
        The self.css('fill') defines the color of the element background.
        Instead of the DrawBot stroke and strokeWidth attributes, use
        borders or (borderTop, borderRight, borderBottom, borderLeft) attributes.
        If one of the self.bleed is defined, then shift and resize background by that size.
        """
        c = view.context
        b = c.b # Get builder from context

        eShadow = self.shadow
        if eShadow:
            c.saveGraphicState()
            c.setShadow(eShadow) 
            c.rect(p[0], p[1], self.w, self.h)
            c.restoreGraphicState()

        eFill = self.css('fill', None)
        eStroke = self.css('stroke', None)
        eGradient = self.gradient
        if eStroke is not None or eFill is not None or eGradient:
            c.saveGraphicState()
            # Drawing element fill and/or frame
            if eGradient: # Gradient overwrites setting of fill.
                # TODO: Make bleed work here too.
                c.setGradient(eGradient, p, self.w, self.h) # Add self.w and self.h to define start/end from relative size.
            else:
                c.setFillColor(eFill)
            c.setStrokeColor(eStroke, self.css('strokeWidth', 1))
            if self.framePath is not None: # In case defined, use instead of bounding box. 
                c.drawPath(self.framePath)
            elif self.originTop:
                c.rect(p[0] - self.bleedLeft, p[1] - self.bleedTop, 
                    self.w + self.bleedLeft + self.bleedRight, self.h + self.bleedTop + self.bleedBottom)
            else:
                c.rect(p[0] - self.bleedLeft, p[1] - self.bleedBottom, 
                    self.w + self.bleedLeft + self.bleedRight, self.h + self.bleedTop + self.bleedBottom)
            c.restoreGraphicState()

        # Instead of full frame drawing, check on separate border settings.
        borderTop = self.borderTop
        borderBottom = self.borderBottom
        borderRight = self.borderRight
        borderLeft = self.borderLeft

        if borderTop is not None:
            c.saveGraphicState()
            if borderTop['dash']:
                c.lineDash(*borderTop['dash'])
            c.setStrokeColor(borderTop['stroke'], borderTop['strokeWidth'])

            oLeft = 0 # Extra offset on left, if there is a left border.
            if borderLeft and (borderLeft['strokeWidth'] or 0) > 1:
                if borderLeft['line'] == ONLINE:
                    oLeft = borderLeft['strokeWidth']/2
                elif borderLeft['line'] == OUTLINE:
                    oLeft = borderLeft['strokeWidth']

            oRight = 0 # Extra offset on right, if there is a right border.
            if borderRight and (borderRight['strokeWidth'] or 0) > 1:
                if borderRight['line'] == ONLINE:
                    oRight = borderRight['strokeWidth']/2
                elif borderRight['line'] == OUTLINE:
                    oRight = borderRight['strokeWidth']

            if borderTop['line'] == OUTLINE:
                oTop = borderTop['strokeWidth']/2
            elif borderTop['line'] == INLINE:
                oTop = -borderTop['strokeWidth']/2
            else:
                oTop = 0

            if self.originTop:
                c.line((p[0]-oLeft, p[1]-oTop), (p[0]+self.w+oRight, p[1]-oTop))
            else:
                c.line((p[0]-oLeft, p[1]+self.h+oTop), (p[0]+self.w+oRight, p[1]+self.h+oTop))
            c.restoreGraphicState()

        if borderBottom is not None:
            c.saveGraphicState()
            if borderBottom['dash']:
                c.lineDash(*borderBottom['dash'])
            c.setStrokeColor(borderBottom['stroke'], borderBottom['strokeWidth'])

            oLeft = 0 # Extra offset on left, if there is a left border.
            if borderLeft and (borderLeft['strokeWidth'] or 0) > 1:
                if borderLeft['line'] == ONLINE:
                    oLeft = borderLeft['strokeWidth']/2
                elif borderLeft['line'] == OUTLINE:
                    oLeft = borderLeft['strokeWidth']

            oRight = 0 # Extra offset on right, if there is a right border.
            if borderRight and (borderRight['strokeWidth'] or 0) > 1:
                if borderRight['line'] == ONLINE:
                    oRight = borderRight['strokeWidth']/2
                elif borderRight['line'] == OUTLINE:
                    oRight = borderRight['strokeWidth']

            if borderBottom['line'] == OUTLINE:
                oBottom = borderBottom['strokeWidth']/2
            elif borderBottom['line'] == INLINE:
                oBottom = -borderBottom['strokeWidth']/2
            else:
                oBottom = 0

            if self.originTop:
                c.line((p[0]-oLeft, p[1]+self.h+oBottom), (p[0]+self.w+oRight, p[1]+self.h+oBottom))
            else:
                c.line((p[0]-oLeft, p[1]-oBottom), (p[0]+self.w+oRight, p[1]-oBottom))
            c.restoreGraphicState()
        
        if borderRight is not None:
            c.saveGraphicState()
            if borderRight['dash']:
                c.lineDash(*borderRight['dash'])
            c.setStrokeColor(borderRight['stroke'], borderRight['strokeWidth'])

            oTop = 0 # Extra offset on top, if there is a top border.
            if borderTop and (borderTop['strokeWidth'] or 0) > 1:
                if borderTop['line'] == ONLINE:
                    oTop = borderTop['strokeWidth']/2
                elif borderLeft['line'] == OUTLINE:
                    oTop = borderTop['strokeWidth']

            oBottom = 0 # Extra offset on bottom, if there is a bottom border.
            if borderBottom and (borderBottom['strokeWidth'] or 0) > 1:
                if borderBottom['line'] == ONLINE:
                    oBottom = borderBottom['strokeWidth']/2
                elif borderBottom['line'] == OUTLINE:
                    oBottom = borderBottom['strokeWidth']

            if borderRight['line'] == OUTLINE:
                oRight = borderRight['strokeWidth']/2
            elif borderLeft['line'] == INLINE:
                oRight = -borderRight['strokeWidth']/2
            else:
                oRight = 0

            if self.originTop:
                c.line((p[0]+self.w+oRight, p[1]-oTop), (p[0]+self.w+oRight, p[1]+self.h+oBottom))
            else:
                c.line((p[0]+self.w+oRight, p[1]-oBottom), (p[0]+self.w+oRight, p[1]+self.h+oTop))
            c.restoreGraphicState()

        if borderLeft is not None:
            c.saveGraphicState()
            if borderLeft['dash']:
                c.lineDash(*borderLeft['dash'])
            c.setStrokeColor(borderLeft['stroke'], borderLeft['strokeWidth'])

            oTop = 0 # Extra offset on top, if there is a top border.
            if borderTop and (borderTop['strokeWidth'] or 0) > 1:
                if borderTop['line'] == ONLINE:
                    oTop = borderTop['strokeWidth']/2
                elif borderLeft['line'] == OUTLINE:
                    oTop = borderTop['strokeWidth']

            oBottom = 0 # Extra offset on bottom, if there is a bottom border.
            if borderBottom and (borderBottom['strokeWidth'] or 0) > 1:
                if borderBottom['line'] == ONLINE:
                    oBottom = borderBottom['strokeWidth']/2
                elif borderBottom['line'] == OUTLINE:
                    oBottom = borderBottom['strokeWidth']

            if borderLeft['line'] == OUTLINE:
                oLeft = borderLeft['strokeWidth']/2
            elif borderLeft['line'] == INLINE:
                oLeft = -borderLeft['strokeWidth']/2
            else:
                oLeft = 0

            if self.originTop:
                c.line((p[0]-oLeft, p[1]-oTop), (p[0]-oLeft, p[1]+self.h+oBottom))
            else:
                c.line((p[0]-oLeft, p[1]-oBottom), (p[0]-oLeft, p[1]+self.h+oTop))
            c.restoreGraphicState()

    #   D R A W B O T / F L A T  S U P P O R T

    def build(self, view, origin, drawElements=True):
        u"""Default drawing method just drawing the frame. 
        Probably will be redefined by inheriting element classes."""
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        self.buildFrame(view, p) # Draw optional frame or borders.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin) # Depends on flag 'view.showElementInfo'

    def buildChildElements(self, view, origin):
        u"""Draw child elements, dispatching depending on the implementation of context specific build elements.
        If not specific builder_<context.b.PB_ID> is implemented, call default. e.build(view, origin)"""
        hook = 'build_' + self.context.b.PB_ID
        for e in self.elements:
            if not e.show:
                continue
            if hasattr(e, hook):
                getattr(e, hook)(view, origin)
            else: # No implementation for this context, call default building method for this element.
                e.build(view, origin)

    #   H T M L  /  C S S  S U P P O R T

    def build_css(self, view, origin=None):
        u"""Build the css for this element. Default behavior is to import the content of the file
        if there is a path reference, otherwise build the CSS from the available values and parameters
        in self.style and self.css()."""
        b = view.context.b # Get the build of the current context.
        if self.info.cssPath is not None:
            b.importCss(self.info.cssPath) # Add CSS content of file, if path is not None and the file exists.
        elif self.class_: # For now, we only can generate CSS if the element has a class name defined.
            b.css('.'+self.class_, self.style)
        else:
            b.css(message='No CSS for element %s\n' % self.__class__.__name__)

    def build_html(self, view, origin=None, drawElements=True):
        u"""Build the HTML/CSS code through WebBuilder (or equivalent) that is the closest representation of self. 
        If there are any child elements, then also included their code, using the
        level recursive indent."""

        # REVIEW THIS!
        # Since the 'p' variable in the drawBefor and drawAfter
        # calls bellow was undefined, I have added here the three following
        # lines of code copied from the Element.build method implementation:
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)
        p = self._applyAlignment(p)

        self.build_css(view)
        b = self.context.b # Use the current context builder to write the HTML/CSS code.
        info = self.info # Contains builder parameters and flags for Builder "b"
        if info.htmlPath is not None:
            b.importHtml(info.htmlPath) # Add HTML content of file, if path is not None and the file exists.
        else:
            b.div(class_=self.class_) # No default class, ignore if not defined.
            
            if self.drawBefore is not None: # Call if defined
                self.drawBefore(self, view, p)

            if drawElements: # Build child elements, dispatch if they implemented generic or context specific build method.
                self.buildChildElements(view, origin)

            if self.drawAfter is not None: # Call if defined
                self.drawAfter(self, view, p)

            b._div()

    #   V A L I D A T I O N

    def evaluate(self, score=None):
        u"""Evaluate the content of element e with the total sum of conditions."""
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
        u"""Evaluate the content of element e with the total sum of conditions.
        The view is passed, as it (or its builder) may be needed to solve specific text 
        conditions, such as run length of text and overflow of text boxes."""
        if score is None:
            score = Score()
        if self.conditions: # Can be None or empty
            for condition in self.conditions: # Skip in case there are no conditions in the style.
                condition.solve(self, score)
        for e in self.elements: # Also works if showing element is not a container.
            if e.show:
                e.solve(score)
        return score
         
    #   C O N D I T I O N S

    def isBottomOnBottom(self, view, tolerance=0):
        if self.originTop:
            return abs(self.parent.h - self.parent.pb - self.bottom) <= tolerance
        return abs(self.parent.pb - self.bottom) <= tolerance

    def isBottomOnBottomSide(self, view, tolerance=0):
        if self.originTop:
            return abs(self.parent.h - self.bottom) <= tolerance
        return abs(self.bottom) <= tolerance
        
    def isBottomOnTop(self, view, tolerance=0):
        if self.originTop:
            return abs(self.parent.pt - self.bottom) <= tolerance
        return abs(self.parent.h - self.parent.pt - self.bottom) <= tolerance

    def isCenterOnCenter(self, view, tolerance=0):
        pl = self.parent.pl # Get parent padding left
        center = (self.parent.w - self.parent.pr - pl)/2
        return abs(pl + center - self.center) <= tolerance

    def isCenterOnCenterSides(self, view, tolerance=0):
        return abs(self.parent.w/2 - self.center) <= tolerance
  
    def isCenterOnLeft(self, view, tolerance=0):
        return abs(self.parent.pl - self.center) <= tolerance

    def isCenterOnRight(self, view, tolerance=0):
        return abs(self.parent.w - self.parent.pr - self.center) <= tolerance
   
    def isCenterOnRightSide(self, view, tolerance=0):
        return abs(self.parent.w - self.center) <= tolerance

    def isMiddleOnBottom(self, view, tolerance=0):
        if self.originTop:
            return abs(self.parent.h - self.parent.pb - self.middle) <= tolerance
        return abs(self.parent.pb - self.middle) <= tolerance

    def isMiddleOnBottomSide(self, view, tolerance=0):
        if self.originTop:
            return abs(self.parent.h - self.middle) <= tolerance
        return abs(self.middle) <= tolerance

    def isMiddleOnTop(self, view, tolerance=0):
        if self.originTop:
            return abs(self.parent.pt - self.middle) <= tolerance
        return abs(self.parent.h - self.parent.pt - self.middle) <= tolerance

    def isMiddleOnTopSide(self, tolerance=0):
        if self.originTop:
            return abs(self.middle) <= tolerance
        return abs(self.parent.h - self.middle) <= tolerance

    def isMiddleOnMiddle(self, view, tolerance=0):
        pt = self.parent.pt # Get parent padding top
        pb = self.parent.pb 
        middle = (self.parent.h - pt - pb)/2
        if self.originTop:
            return abs(pt + middle - self.middle) <= tolerance
        return abs(pb + middle - self.middle) <= tolerance

    def isMiddleOnMiddleSides(self, view, tolerance=0):
        if self.originTop:
            return abs(self.middle) <= tolerance
        return abs(self.parent.h - self.middle) <= tolerance
  
    def isLeftOnCenter(self, view, tolerance=0):
        pl = self.parent.pl # Get parent padding left
        center = (self.parent.w - self.parent.pr - pl)/2
        return abs(pl + center - self.left) <= tolerance

    def isLeftOnCenterSides(self, view, tolerance=0):
        return abs(self.parent.w/2 - self.left) <= tolerance

    def isLeftOnLeft(self, view, tolerance=0):
        return abs(self.parent.pl - self.left) <= tolerance

    def isLeftOnLeftSide(self, view, tolerance=0):
        return abs(self.left) <= tolerance

    def isLeftOnRight(self, view, tolerance=0):
        return abs(self.parent.w - self.parent.pr - self.left) <= tolerance

    def isCenterOnLeftSide(self, view, tolerance=0):
        return abs(self.parent.left - self.center) <= tolerance

    def isTopOnMiddle(self, view, tolerance=0):
        pt = self.parent.pt # Get parent padding top
        pb = self.parent.pb 
        middle = (self.parent.h - pb - pt)/2
        if self.originTop:
            return abs(pt + middle - self.top) <= tolerance
        return abs(pb + middle - self.top) <= tolerance

    def isTopOnMiddleSides(self, view, tolerance=0):
        return abs(self.parent.h/2 - self.top) <= tolerance

    def isOriginOnBottom(self, view, tolerance=0):
        pb = self.parent.pb # Get parent padding left
        if self.originTop:
            return abs(self.parent.h - pb - self.y) <= tolerance
        return abs(pb - self.y) <= tolerance

    def isOriginOnBottomSide(self, view, tolerance=0):
        if self.originTop:
            return abs(self.parent.h - self.y) <= tolerance
        return abs(self.y) <= tolerance

    def isOriginOnCenter(self, view, tolerance=0):
        pl = self.parent.pl # Get parent padding left
        center = (self.parent.w - self.parent.pr - pl)/2
        return abs(pl + center - self.x) <= tolerance

    def isOriginOnCenterSides(self, view, tolerance=0):
        return abs(self.parent.w/2 - self.x) <= tolerance

    def isOriginOnLeft(self, view, tolerance=0):
        return abs(self.parent.pl - self.x) <= tolerance

    def isOriginOnLeftSide(self, view, tolerance=0):
        return abs(self.x) <= tolerance

    def isOriginOnRight(self, view, tolerance=0):
        return abs(self.parent.w - self.parent.pr - self.x) <= tolerance

    def isOriginOnRightSide(self, view, tolerance=0):
        return abs(self.parent.w - self.x) <= tolerance

    def isOriginOnTop(self, view, tolerance=0):
        if self.originTop:
            return abs(self.parent.pt - self.y) <= tolerance
        return abs(self.parent.h - self.parent.pt - self.y) <= tolerance

    def isOriginOnTopSide(self, view, tolerance=0):
        u"""Answer the boolean test if the origin of self is on the top side of self.parent.

        >>> e1 = Element(w=200, h=200, x=0, y=500)
        >>> e2 = Element(w=500, h=500, elements=[e1])
        >>> e1.isOriginOnTopSide(None)
        True
        >>> e1.y = 400
        >>> e1.isOriginOnTopSide(None)
        False
        >>> 
        """
        if self.originTop:
            return abs(self.y) <= tolerance
        return abs(self.parent.h - self.y) <= tolerance

    def isOriginOnMiddle(self, view, tolerance=0):
        if self.originTop:
            return abs(self.parent.mt + (self.parent.h - self.parent.pb - self.parent.pt)/2 - self.y) <= tolerance
        return abs(self.parent.mb + (self.parent.h - self.parent.pb - self.parent.pt)/2 - self.y) <= tolerance
 
    def isOriginOnMiddleSides(self, view, tolerance=0):
        if self.originTop:
            return abs(self.parent.h/2 - self.y) <= tolerance
        return abs(self.parent.h/2 - self.y) <= tolerance
 
    def isRightOnCenter(self, view=None, tolerance=0):
        u"""Answer the boolean flag if the right size of self is on the middle of the parent.

        >>> e1 = Element(x=100, w=200) # e1.right == 300
        >>> e2 = Element(w=600, elements=[e1])

        """
        return abs(self.parent.w - self.x) <= tolerance

    def isRightOnCenterSides(self, view, tolerance=0):
        return abs(self.parent.w/2 - self.right) <= tolerance

    def isRightOnLeft(self, view, tolerance=0):
        return abs(self.parent.pl - self.right) <= tolerance

    def isRightOnRight(self, view, tolerance=0):
        return abs(self.parent.w - self.parent.pr - self.right) <= tolerance

    def isRightOnRightSide(self, view, tolerance=0):
        return abs(self.parent.w - self.right) <= tolerance

    def isBottomOnMiddle(self, view, tolerance=0):
        pt = self.parent.pt # Get parent padding top
        pb = self.parent.pb
        middle = (self.parent.h - pb - pt)/2
        if self.originTop:
            return abs(pt + middle - self.bottom) <= tolerance
        return abs(pb + middle - self.bottom) <= tolerance

    def isBottomOnMiddleSides(self, tolerance=0):
        return abs(self.parent.h/2 - self.bottom) <= tolerance

    def isTopOnBottom(self, view, tolerance=0):
        if self.originTop:
            return abs(self.parent.h - self.parent.pb - self.top) <= tolerance
        return abs(self.parent.pb - self.top) <= tolerance

    def isTopOnTop(self, view, tolerance=0):
        if self.originTop:
            return abs(self.parent.pt - self.top) <= tolerance
        return abs(self.parent.h - self.parent.pt - self.top) <= tolerance

    def isTopOnTopSide(self, view, tolerance=0):
        if self.originTop:
            return abs(self.top) <= tolerance
        return abs(self.parent.h - self.top) <= tolerance

    # Shrink block conditions

    def isSchrunkOnBlockLeft(self, view, tolerance):
        boxX, _, _, _ = self.marginBox
        return abs(self.left + self.pl - boxX) <= tolerance

    def isShrunkOnBlockRight(self, view, tolerance):
        boxX, _, boxW, _ = self.marginBox
        return abs(self.right - self.pr - (boxX + boxW)) <= tolerance
     
    def isShrunkOnBlockTop(self, view, tolerance):
        _, boxY, _, boxH = self.marginBox
        if self.originTop:
            return abs(self.top + self.pt - boxY) <= tolerance
        return self.top - self.pt - (boxY + boxH) <= tolerance

    def isShrunkOnBlockBottom(self, view, tolerance):
        u"""Test if the bottom of self is shrunk to the bottom position of the block."""
        _, boxY, _, boxH = self.marginBox
        if self.originTop:
            return abs(self.h - self.pb - (boxY + boxH)) <= tolerance
        return abs(self.pb - boxY) <= tolerance

    def isShrunkOnBlockLeftSide(self, view, tolerance):
        boxX, _, _, _ = self.box
        return abs(self.left - boxX) <= tolerance

    def isShrunkOnBlockRightSide(self, view, tolerance):
        boxX, _, boxW, _ = self.mbox
        return abs(self.right - (boxX + boxW)) <= tolerance
     
    def isShrunkOnBlockTopSide(self, view, tolerance):
        _, boxY, _, boxH = self.box
        if self.originTop:
            return abs(self.top - boxY) <= tolerance
        return self.top - (boxY + boxH) <= tolerance

    def isShrunkOnBlockBottomSide(self, view, tolerance):
        _, boxY, _, boxH = self.marginBox
        if self.originTop:
            return abs(self.bottom - (boxY + boxH)) <= tolerance
        return abs(self.bottom - boxY) <= tolerance

    # Float conditions to page padding

    def isFloatOnTop(self, view, tolerance=0):
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

    def isFloatOnTopSide(self, view, tolerance=0):
        return abs(self.getFloatTopSide() - self.mTop) <= tolerance

    def isFloatOnBottomSide(self, tolerance=0):
        return abs(self.getFloatBottomSide() - self.mBottom) <= tolerance

    def isFloatOnLeftSide(self, tolerance=0):
        return abs(self.getFloatLeftSide() - self.mLeft) <= tolerance

    def isFloatOnRightSide(self, tolerance=0):
        return abs(self.getFloatRightSide() - self.mRight) <= tolerance

    #   Column/Row conditions

    def isLeftOnCol(self, col, tolerance):
        u"""Move top of the element to col index position."""
        gridColumns = self.getGridColumns()
        if col in range(len(gridColumns)):
            return abs(self.left - gridColumns[col][0]) <= tolerance
        return False # row is not in range of gridColumns 

    def isRightOnCol(self, col, tolerance):
        u"""Move top of the element to col index position."""
        gridColumns = self.getGridColumns()
        if col in range(len(gridColumns)):
            return abs(self.right - gridColumns[col][0]) <= tolerance
        return False # row is not in range of gridColumns 

    def isFitOnColspan(self, col, colSpan, tolerance):
        gridColumns = self.getGridColumns()
        indices = range(len(gridColumns))
        if col in indices and col + colSpan in indices:
            c1 = gridColumns[col]
            c2 = gridColumns[col + colSpan - 1]
            return abs(self.w - (c2[0] - c1[0] + c2[1])) <= tolerance
        return False

    def isTopOnRow(self, row, tolerance):
        u"""Move top of the element to row."""
        gridRows = self.getGridRows()
        if row in range(len(gridRows)):
            return abs(self.top - gridRows[row][0]) <= tolerance
        return False # row is not in range of gridColumns 

    def isBottomOnRow(self, row, tolerance):
        u"""Move top of the element to row."""
        gridRows = self.getGridRows()
        if row in range(len(gridRows)):
            return abs(self.bottom - gridRows[row][0]) <= tolerance
        return False # row is not in range of gridColumns 

    def isFitOnRowspan(self, row, rowSpan, tolerance):
        gridRows = self.getGridRows()
        indices = range(len(gridRows))
        if row in indices and row + rowSpan in indices:
            r1 = gridRows[row]
            r2 = gridRows[row + rowSpan - 1]
            return abs(self.h - (r2[0] - r1[0] + r2[1])) <= tolerance
        return False

    #   T R A N S F O R M A T I O N S 

    #   Column/Row alignment

    def left2Col(self, col):
        u"""Move top of the element to col index position."""
        gridColumns = self.getGridColumns()
        if col in range(len(gridColumns)):
            self.left = self.parent.pl + gridColumns[col][0] # @@@ FIX GUTTER
            return True
        return False # row is not in range of gridColumns 

    def right2Col(self, col):
        u"""Move right of the element to col index position."""
        gridColumns = self.getGridColumns()
        if col in range(len(gridColumns)):
            self.right = self.parent.pl + gridColumns[col][0] # @@@ FIX GUTTER
            return True
        return False # row is not in range of gridColumns 

    def fit2ColSpan(self, col, colSpan):
        gridColumns = self.getGridColumns()
        indices = range(len(gridColumns))
        if col in indices and col + colSpan in indices:
            c1 = gridColumns[col]
            c2 = gridColumns[col + colSpan - 1]
            self.w = c2[0] - c1[0] + c2[1]
            return True
        return False

    def top2Row(self, row):
        u"""Move top of the element to row."""
        gridRows = self.getGridRows()
        if row in range(len(gridRows)):
            self.top = self.parent.pb + gridRows[row][0] # @@@ FIX GUTTER
            return True
        return False # row is not in range of gridColumns 

    def bottom2Row(self, row):
        u"""Move top of the element to row."""
        gridRows = self.getGridRows()
        if row in range(len(gridRows)):
            self.bottom = self.parent.pb + gridRows[row][0] # @@@ FIX GUTTER
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
    
    #   Page block and Page side alignments

    def bottom2Bottom(self):
        u"""Move bottom of the element to the bottom of the parent block.

        >>> e1 = Element(y=300)
        >>> e2 = Element(elements=[e1], pb=20)
        >>> success = e1.bottom2Bottom()
        >>> e1.bottom # Move bottom of e1 down to padding-bottom position of e2
        20
        """
        if self.originTop:
            self.bottom = self.parent.h - self.parent.pb
        else:
            self.bottom = self.parent.pb
        return True

    def bottom2BottomSide(self):
        u"""Move bottom of the element to the bottom of the parent side.

        >>> e1 = Element(y=300)
        >>> e2 = Element(elements=[e1])
        >>> success = e1.bottom2BottomSide()
        >>> e1.bottom # Move bottom of e1 down to padding-bottom position of e2
        0
        """
        if self.originTop:
            self.bottom = self.parent.h
        else:
            self.bottom = 0
        return True

    def bottom2Top(self):
        u"""Move bottom of the element to the top of the parent block."""
        if self.originTop:
            self.bottom = self.parent.pt 
        else:
            self.bottom = self.parent.h - self.parent.pt
        return True
    
    def middle2Bottom(self):
        u"""Move middle of the element to the bottom of the parent block."""
        if self.originTop:
            self.middle = self.parent.h - self.parent.pb
        else:
            self.middle = self.parent.pb
        return True
    
    def middle2BottomSide(self):
        u"""Move middle of the element to the bottom parent side."""
        if self.originTop:
            self.middle = self.parent.h
        else:
            self.middle = 0
        return True

    def center2Center(self):
        pl = self.parent.pl # Get parent padding left
        self.center = pl + (self.parent.w - self.parent.pr - pl)/2
        return True
    
    def center2CenterSides(self):
        self.center = self.parent.w/2
        return True

    def center2Left(self):
        self.center = self.parent.pl # Padding left
        return True

    def center2LeftSide(self):
        self.center = 0
        return True

    def center2Right(self):
        self.center = self.parent.w - self.parent.pr
        return True

    def center2RightSide(self):
        self.center = self.parent.w
        return True

    def middle2Top(self):
        if self.originTop:
            self.middle = self.parent.pt
        else:
            self.middle = self.parent.h - self.parent.pt
        return True       

    def middle2TopSide(self):
        if self.originTop:
            self.middle = 0
        else:
            self.middle = self.parent.h
        return True       

    def middle2Middle(self): # Vertical center, following CSS naming.
        pt = self.parent.pt # Get parent padding top
        pb = self.parent.pb
        middle = (self.parent.h - pb - pt)/2
        if self.originTop:
            self.middle = pt + middle
        else:
            self.middle = pb + middle
        return True

    def middle2MiddleSides(self):
        self.middle = self.parent.h/2

    def left2Center(self):
        pl = self.parent.pl # Get parent padding left
        self.left = pl + (self.parent.w - self.parent.pr - pl)/2
        return True       

    def left2CenterSides(self):
        self.left = self.parent.w/2
        return True       

    def left2Left(self):
        self.left = self.parent.pl # Padding left
        return True       

    def left2Right(self):
        self.left = self.parent.w - self.parent.pr
        return True       

    def left2LeftSide(self):
        self.left = 0
        return True       

    def top2Middle(self):
        pt = self.parent.pt # Get parent padding left
        pb = self.parent.pb
        middle = (self.parent.h - pb - pt)/2
        if self.originTop:
            self.top = pt + middle
        else:
            self.top = pb + middle
        return True       

    def top2MiddleSides(self):
        self.top = self.parent.h/2
        return True       

    def origin2Bottom(self):
        if self.originTop:
            self.y = self.parent.h - self.parent.pb
        else:
            self.y = self.parent.pb
        return True

    def origin2BottomSide(self):
        if self.originTop:
            self.y = self.parent.h
        else:
            self.y = 0
        return True       

    def origin2Center(self):
        self.x = self.parent.ml + (self.parent.w - self.parent.pr - self.parent.pl)/2
        return True       

    def origin2CenterSides(self):
        self.x = self.parent.w/2
        return True       

    def origin2Left(self):
        self.x = self.parent.pl # Padding left
        return True       

    def origin2LeftSide(self):
        self.x = 0
        return True       

    def origin2Right(self):
        self.x = self.parent.w - self.parent.pr
        return True

    def origin2RightSide(self):
        self.x = self.parent.w
        return True

    def origin2Top(self):
        if self.originTop:
            self.y = self.parent.pt
        else:
            self.y = self.parent.h - self.parent.pt
        return True

    def origin2TopSide(self):
        if self.originTop:
            self.y = 0
        else:
            self.y = self.parent.h
        return True

    def origin2Middle(self):
        pt = self.parent.pt # Get parent padding top
        pb = self.parent.pb
        middle = (self.parent.h - pb - pt)/2
        if self.originTop:
            self.y = pt + middle
        else:
            self.y = pb + middle
        return True
 
    def origin2MiddleSides(self):
        self.y = self.parent.h/2
        return True

    def right2Center(self):
        pl = self.parent.pl # Get parent padding left
        self.right = pl + (self.parent.w - self.parent.pr - pl)/2
        return True

    def right2CenterSides(self):
        self.right = self.parent.w/2
        return True

    def right2Left(self):
        self.right = self.parent.pl # Padding left
        return True

    def right2Right(self):
        self.right = self.parent.w - self.parent.pr
        return True
    
    def right2RightSide(self):        
        self.right = self.parent.w
        return True

    def bottom2Middle(self):
        pt = self.parent.pt # Get parent padding top
        pb = self.parent.pb
        middle = (self.parent.h - pb - pt)/2
        if self.originTop:
            self.bottom = pt + middle
        else:
            self.bottom = pb + middle
        return True

    def bottom2MiddleSides(self):
        self.bottom = self.parent.h/2
        return True

    def top2Bottom(self):
        if self.originTop:
            self.top = self.parent.h - self.parent.pb
        else:
            self.top = self.parent.pb
        return True
    
    def top2Top(self):
        if self.originTop:
            self.top = self.parent.pt
        else:
            self.top = self.parent.h - self.parent.pt
        return True
    
    def top2TopSide(self):
        if self.originTop:
            self.mTop = 0
        else:
            self.mTop = self.parent.h
        return True

    # Floating parent padding

    def float2Top(self):
        u"""Float the element upward, until top hits the parent top padding.
        Include margin to decide if it fits."""
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

    # Floating parent sides

    def float2TopSide(self):
        self.mTop = self.getFloatTopSide()
        return True

    def float2BottomSide(self):
        self.mBottom = self.getFloatBottomSide()
        return True

    def float2LeftSide(self):
        self.mLeft = self.getFloatLeftSide()
        return True

    def float2RightSide(self):
        self.mRight = self.getFloatRightSide()
        return True

    # With fitting (and shrinking) we need to change the actual size of the element.
    # This can have implications on it's content, and we need to take the min/max
    # sizes into conderantion: setting the self.w and self.h to a value, does not mean
    # that the size really got that value, if exceeding a min/max limit.
    
    def fit2Bottom(self):
        if self.originTop:
            self.h += self.parent.h - self.parent.pb - self.bottom
        else:
            self.h = self.top - self.parent.pb
            self.bottom = self.parent.pb
        return True

    def fit2BottomSide(self):
        if self.originTop:
            self.h += self.parent.h - self.bottom
        else:
            top = self.top
            self.bottom = 0
            self.h += top - self.top
        return True

    def fit2Left(self):
        right = self.right
        self.left = self.parent.pl # Padding left
        self.w += right - self.right
        return True

    def fit2LeftSide(self):
        right = self.right
        self.left = 0
        self.w += right - self.right
        return True

    def fit2Right(self):
        u"""Make the right side of self fit the right padding of the parent, without
        moving the left position.

        >>> e1 = Element(x=100, y=20, w=100, h=50)
        >>> e2 = Element(w=300, h=300, elements=[e1], padding=10)
        >>> e1.x, e1.y, e1.w, e1.h # Default position and size
        (100, 20, 100, 50)
        >>> success = e1.fit2Right()
        >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent on padding
        (100, 20, 190, 50)
        >>> 
        """
        self.w = self.parent.w - self.parent.pr - self.x
        return True

    def fit2RightSide(self):
        u"""Make the right side of self fit the right side of the parent, without
        moving the left position.

        >>> e1 = Element(x=100, y=20, w=100, h=50)
        >>> e2 = Element(w=300, h=300, elements=[e1], padding=10)
        >>> e1.x, e1.y, e1.w, e1.h # Default position and size
        (100, 20, 100, 50)
        >>> success = e1.fit2RightSide()
        >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent on padding
        (100, 20, 200, 50)
        >>> 
        """
        self.w = self.parent.w - self.x
        return True

    def fit2Top(self):
        u"""Make the top side of self fit the top padding of the parent, without
        moving the bottom position.

        >>> e1 = Element(x=100, y=20, w=100, h=50)
        >>> e2 = Element(w=300, h=300, elements=[e1], padding=10)
        >>> e1.x, e1.y, e1.w, e1.h # Default position and size
        (100, 20, 100, 50)
        >>> success = e1.fit2Top()
        >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent on padding
        (100, 20, 100, 300)
        >>> 
        """
        if self.originTop:
            bottom = self.bottom
            self.top = self.parent.pt
            self.h += bottom - self.bottom
        else:
            self.h += self.parent.h - self.parent.pt - self.top
        return True

    def fit2TopSide(self):
        if self.originTop:
            bottom = self.bottom
            self.top = 0
            self.h += bottom - self.bottom
        else:
            self.h += self.parent.h - self.top
        return True

    #   Shrinking
    
    def shrink2BlockBottom(self):
        _, boxY, _, boxH = self.box
        if self.originTop:
            self.h = boxH
        else:
            top = self.top
            self.bottom = boxY
            self.h += top - self.top
        return True

    def shrink2BlockBottomSide(self):
        if self.originTop:
            self.h += self.parent.h - self.bottom
        else:
            top = self.top
            self.bottom = 0 # Parent botom 
            self.h += top - self.top
        return True

    def shrink2BlockLeft(self):
        right = self.right
        self.left = self.parent.pl # Padding left
        self.w += right - self.right
        return True

    def shrink2BlockLeftSide(self):
        right = self.right
        self.left = 0
        self.w += right - self.right
        return True

    def shrink2BlockRight(self):
        self.w += self.parent.w - self.parent.pr - self.right
        return True

    def shrink2BlockRightSide(self):
        self.w += self.parent.w - self.right
        return True

    def shrink2BlockTop(self):
        if self.originTop:
            bottom = self.bottom
            self.top = self.parent.pt
            self.h += bottom - self.bottom
        else:
            self.h += self.parent.h - self.parent.pt - self.top
        return True

    def shrink2BlockTopSide(self):
        if self.originTop:
            bottom = self.bottom
            self.top = 0
            self.h += bottom - self.bottom
        else:
            self.h += self.parent.h - self.top
        return True

    #    Text conditions

    def baseline2Top(self):
        # ...
        return True
        
    def baseline2Bottom(self):
        # ...
        return True

    def floatBaseline2Top(self):
        # ...
        return True

    def floatAscender2Top(self):
        # ...
        return True

    def floatCapHeight2Top(self):
        # ...
        return True

    def floatXHeight2Top(self):
        # ...
        return True


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
