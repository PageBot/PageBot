#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------

#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     document.py
#
import copy
from pagebot.stylelib import styleLib # Library with named, predefined style dicts.
from pagebot.conditions.score import Score
from pagebot.elements.pbpage import Page, Template
from pagebot.elements.views import viewClasses, defaultViewClass
from pagebot.style import getRootStyle, TOP, BOTTOM
from pagebot.toolbox.transformer import obj2StyleId

class Document(object):
    u"""A Document is just another kind of container.

    Doctest: https://docs.python.org/2/library/doctest.html
    Run doctest in Sublime: cmd-B

    >>> doc = Document(name='TestDoc', autoPages=50)
    >>> len(doc), min(doc.pages.keys()), max(doc.pages.keys())
    (50, 1, 50)
    
    >>> doc = Document(name='TestDoc', w=300, h=400, autoPages=2, padding=(30, 40, 50, 60))
    >>> doc.name, doc.w, doc.h, doc.originTop, len(doc)
    ('TestDoc', 300, 400, True, 2)
    >>> doc.padding
    (30, 40, 50, 60)
    >>> page = doc[1] # First page is on the right
    >>> page.padding = 20
    >>> page.w, page.h, page.pw, page.ph, page.pt, page.pr, page.pb, page.pl, page.title
    (300, 400, 260, 360, 20, 20, 20, 20, 'default')

    >>> pages = (Page(), Page(), Page())
    >>> doc = Document(name='TestDoc', w=300, h=400, pages=pages, autoPages=0, viewId='Mamp')
    >>> len(doc)
    3
    >>> doc.context
    <HtmlContext>

    """    
    PAGE_CLASS = Page # Allow inherited versions of the Page class.
    
    DEFAULT_VIEWID = defaultViewClass.viewId

    def __init__(self, styles=None, theme=None, viewId=None, name=None, title=None, pages=None, autoPages=1, 
            template=None, templates=None, originTop=True, startPage=1, w=None, h=None, 
            padding=None, lib=None, context=None, exportPaths=None, **kwargs):
        u"""Contains a set of Page elements and other elements used for display in thumbnail mode. 
        Allows to compose the pages without the need to send them directly to the output for 
        "asynchronic" page filling."""

        # Apply the theme if defined or create default styles, to make sure they are there.
        self.rootStyle = self.makeRootStyle(**kwargs)
        self.initializeStyles(theme, styles) # May or may not overwrite the root style.

        self.originTop = originTop # Set as property in rootStyle and also change default rootStyle['yAlign'] to right side.
        self.w = w or 1000 # Always needs a value. Take 1000 if 0 or None defined.
        self.h = h or 1000 # These values overwrite the self.rootStyle['w'] and self.rootStyle['h']
        if padding is not None:
            self.padding = padding

        self.name = name or title or 'Untitled'
        self.title = title or self.name

        self.pages = {} # Key is pageNumber, Value is row list of pages: self.pages[pn][index] = page
        for page in pages or []: # In case there are pages defined on init, add them.
            self.appendPage(page, startPage)

        # Initialize the current view of this document. All conditional checking and building
        # is done through this view. The defaultViewClass is set either to an in stance of PageView.
        self.views = {} # Key is the viewId. Value is a view instance.
        # Set the self.view to an instance of viewId or defaultViewClass.viewId and store in self.views.
        # Add the optional context, if defined. Otherwise use the result of default getContext.
        # A context is an instance of e.g. one of DrawBotContext, FlatContext or HtmlContext, which then
        # hold the instance of a builder (respectively DrawBot, Flat and one of the HtmlBuilders, such
        # as GitBuilder or MampBuilder)
        self.newView(viewId or self.DEFAULT_VIEWID, context=context)

        # Template is name or instance default template.
        self.initializeTemplates(templates, template) 

        # Property self.lib for storage of collected content while typesetting and composing, 
        # referring to the pages they where placed on during composition. The lib can optionally
        # be defined when constructing self.
        if lib is None:
            lib = {}
        self._lib = lib

        # Document (w, h) size is default from page, but will modified by the type of display mode. 
        if autoPages:
            self.makePages(pageCnt=autoPages, pn=startPage, w=self.w, h=self.h, **kwargs)

        # Call generic initialize method, allowing inheriting publication classes to initialize their stuff.
        # This can be the creation of templates, pages, adding/altering styles and view settings.
        # Default is to do nothing.
        self.initialize(**kwargs)

    def initialize(self, **kwargs):
        u"""Default implementation of publication initialized. Can be redefined by inheriting classed.
        All **kwargs are available to allow access for inheriting Publication documents."""
        pass

    def _get_lib(self):
        u"""Answer the global storage dictionary, used by TypeSetter and others to keep track of footnotes,
        table of content, etc. Some common entries are predefined.

        >>> doc = Document(name='TestDoc', w=300, h=400, lib=dict(a=12, b=34))
        >>> doc.lib
        {'a': 12, 'b': 34}
        """
        return self._lib 
    lib = property(_get_lib)

    def __len__(self):
        u"""Answer the amount of pages in the document."""
        return len(self.pages)

    def __repr__(self):
        u"""Answering the string representation of the document.

        >>> doc = Document(name='TestDoc', w=300, h=400, lib=dict(a=12, b=34))
        >>> str(doc)
        '[Document-Document "TestDoc"]'
        """
        return '[Document-%s "%s"]' % (self.__class__.__name__, self.name)

    def _get_doc(self):
        u"""Root of the chain of element properties, searching upward in the ancestors tree.

        >>> doc = Document(name='TestDoc')
        >>> doc.doc is doc
        True
        """
        return self
    doc = property(_get_doc)
    
    def _get_context(self):
        u"""Answer the context of the current view, to allow searching the parents --> document --> view. """
        return self.view.context
    context = property(_get_context)

    # Document[12] answers a list of pages where page.y == 12
    # This behaviour is different from regular elements, who want the page.eId as key.
    def __getitem__(self, pnIndex):
        u"""Answer the pages with pageNumber equal to page.y. 
        
        >>> doc = Document(name='TestDoc', w=300, h=400, autoPages=100)
        >>> page = doc[66]
        >>> doc.getPageNumber(page)
        '66'
        """
        if isinstance(pnIndex, (list, tuple)):
            pn, index = pnIndex
        else:
            pn, index = pnIndex, 0 # Default is left page on pn row.
        return self.pages[pn][index]
    def __setitem__(self, pn, page):
        if not pn in self.pages:
            self.pages[pn] = []
        self.pages[pn].append(page)
   
    def _get_ancestors(self):
        u"""Root of the chain of element properties, searching upward in the ancestors tree.
        As the document, by definition, is the top of the tree, an empty list is answered.

        >>> doc = Document(name='TestDoc')
        >>> len(doc.ancestors) == 0
        True
        """
        return []
    ancestors = property(_get_ancestors)
    
    def _get_parent(self):
        u"""Root of the chain of element properties, searching upward in the ancestors tree.
        As the document, by definition, is the top of the tree, None is answered as parent.

        >>> doc = Document(name='TestDoc')
        >>> doc.parent is None
        True
        """
        return None
    parent = property(_get_parent)

    def getGlossary(self):
        u"""Answer a string glossary with most representing info about the document.

        >>> doc = Document(name='DemoDoc')
        >>> doc.getGlossary().startswith('Document "DemoDoc"')
        True
        """
        glossary = []
        glossary.append('%s "%s"' % (self.__class__.__name__, self.name))
        glossary.append('\tPages: %d' % len(self.pages))
        glossary.append('\tTemplates: %s' % ', '.join(sorted(self.templates.keys())))
        glossary.append('\tStyles: %s' % ', '.join(sorted(self.styles.keys())))
        glossary.append('\tLib: %s' % ', '.join(self._lib.keys()))
        return '\n'.join(glossary)

    def _get_builder(self):
        u"""Answer the builder, as supposed to be available in the self.context.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> doc = Document(context=context, title='MySite')
        >>> doc, doc.context, doc.title
        ([Document-Document "MySite"], <DrawBotContext>, 'MySite')
        >>> from pagebot.contexts.flatcontext import FlatContext
        >>> context = FlatContext()
        >>> doc = Document(context=context)
        >>> doc.context
        <FlatContext>
        """
        return self.context.b
    b = builder = property(_get_builder)

    #   T E M P L A T E

    def initializeTemplates(self, templates, defaultTemplate):
        u"""Initialize the document templates.""" 
        self.templates = {} # Store defined dictionary of templates or empty dict.
        if templates is not None:
            for name, template in templates.items():
                self.addTemplate(name, template)
        # Used as default document master template if undefined in pages.
        if isinstance(defaultTemplate, str): # Make reference to existing template by name
            defaultTemplate = self.templates.get(defaultTemplate) # If it exists, otherwise it is None
        if defaultTemplate is None: # Only if we have one, overwrite existing default template if it was there.
            # Make sure there is at least a default template.
            defaultTemplate = Template(w=self.w, h=self.h, name='default', padding=self.padding)
        self.defaultTemplate = defaultTemplate

    def getTemplate(self, name=None):
        u"""Answer the named template. If it does not exist, then answer the default template. 
        Answer None of if there is no default.

        >>> doc = Document(name='TestDoc')
        >>> doc.getTemplate()
        <Template:default (0, 0)>
        >>> doc.getTemplate() == doc.defaultTemplate
        True
        """
        return self.templates.get(name, self.defaultTemplate)

    def addTemplate(self, name, template):
        u"""Add the template to the self.templates of dictionaries. There is no check, so the
        caller can overwrite existing templates. Answer the template as convenience of the caller.

        >>> from pagebot.elements.pbpage import Template
        >>> name ='TestTemplate'
        >>> t = Template(w=200, h=300, name=name)
        >>> doc = Document(name='TestDoc')
        >>> doc.addTemplate('myTemplate', t)
        <Template:TestTemplate (0, 0)>
        >>> doc.getTemplate('myTemplate').name == name
        True
        """
        template.parent = self
        self.templates[name] = template
        return template

    def _get_defaultTemplate(self):
        u"""Answer the default template of the document.

        >>> doc = Document(name='TestDoc')
        >>> doc.defaultTemplate
        <Template:default (0, 0)>
        """
        return self.templates.get('default')
    def _set_defaultTemplate(self, template):
        self.addTemplate('default', template)
    defaultTemplate = property(_get_defaultTemplate, _set_defaultTemplate)

    #   S T Y L E

    def initializeStyles(self, theme, styles):
        u"""Make sure that the default styles always exist."""
        if theme is not None:
            self.styles = copy.copy(theme.styles)
            # Additional styles defined? Let them overwrite the theme.
            for styleName, style in (styles or {}).items():
                self.addStyle(name, style)

        else: # No theme defined, use the styles, otherwise use defailt style.
            if styles is None:
                styles = copy.copy(styleLib['default'])
            self.styles = styles # Dictionary of styles. Key is XML tag name value is Style instance.
        # Make sure that the default styles for document and page are always there.
        name = 'root'
        if name not in self.styles:
            self.addStyle(name, self.rootStyle)
        name = 'document'
        if name not in self.styles: # Default dict styles as placeholder, if nothing is defined.
            self.addStyle(name, dict(name=name))
        name = 'page'
        if name not in self.styles: # Default dict styles as placeholder, if nothing is defined.
            self.addStyle(name, dict(name=name))

    def makeRootStyle(self, **kwargs):
        u"""Create a rootStyle, then set the arguments from **kwargs, if their entry name already exists.
        This is similar (but not identical) to the makeStyle in Elements. There any value entry is 
        copied, even if that is not defined in the root style."""
        rootStyle = getRootStyle()
        for name, v in kwargs.items():
            if name in rootStyle: # Only overwrite existing values.
                rootStyle[name] = v 
        return rootStyle

    def applyStyle(self, style):
        u"""Apply the key-value of the style onto the self.rootStyle. This overwrites existing style
        values inthe self.rootStyle by all values in style. Cannot be undone.

        >>> doc = Document(name='TestDoc', w=123)
        >>> doc.w
        123
        >>> doc.applyStyle(dict(w=1234))
        >>> doc.w
        1234
        """
        for key, value in style.items():
            self.rootStyle[key] = value

    # Answer the cascaded style value, looking up the chain of ancestors, until style value is defined.

    def css(self, name, default=None, styleId=None):
        u"""If optional sId is None or style cannot found, then use the root style. 
        If the style is found from the (cascading) sId, then use that to return the requested attribute.
        Note that self.css( ) is a generic query for a named CSS value, upwards the parent tree.
        This is different from the CSS functions as self.buildCss( ), that actually generate CSS code.

        >>> doc = Document(name='TestDoc', w=500, h=500, autoPages=10)
        >>> doc.css('w'), doc.css('h')
        (500, 500)
        """
        style = self.findStyle(styleId)
        if style is None:
            style = self.rootStyle
        return style.get(name, default)

    def findStyle(self, styleId):
        u"""Answer the style that fits the optional sequence naming of styleId.
        Answer None if no style can be found. styleId can have one of these formats:
        ('main h1', 'h1 b')
        """
        if styleId is None:
            return None
        styleId = obj2StyleId(styleId)
        while styleId and ' '.join(styleId) not in self.styles:
            styleId = styleId[1:]
        if styleId:
            return self.styles[styleId]
        return None

    def getNamedStyle(self, styleName):
        u"""In case we are looking for a named style (e.g. used by the Typesetter to build a stack
        of cascading tag style, then query the ancestors for the named style. Default behavior
        of all elements is that they pass the request on to the root, which is nornally the document."""
        return self.getStyle(styleName)

    def getStyle(self, name):
        u"""Answer the names style. If that does not exist, answer the default root style."""
        return self.styles.get(name)
    
    def getRootStyle(self):
        u"""Answer the default root style, used by the Typesetter as default for all other stacked styles."""
        return self.rootStyle

    def add2Style(self, name, addStyle):
        u"""Add (overwrite) the values in the existing style *name* with the values in *addStyle*.
        Raise an error if the *name* style does not exist. Answer the named target style for convenience of the caller."""
        assert name in self.styles
        style = self.styles[name]
        for key, value in addStyle.items():
            style[key] = value
        return style # Answer the style for convenience of the caller.

    def addStyle(self, name, style, force=False):
        u"""Add the style to the self.styles dictionary.  Make sure that styles don't get overwritten, if force is False. 
        Remove them first with *self.removeStyle* or use *self.replaceStyle(name, style)* instead."""
        if name in self.styles:
            assert force
            self.removeStyle(name)
        self.replaceStyle(name, style)
        
    def removeStyle(self, name):
        u"""Remove the style *name* if it exists. Raise an error if is does not exist."""
        del self.styles[name]

    def replaceStyle(self, name, style):
        u"""Set the style by name. Overwrite the style with that name if it already exists."""
        self.styles[name] = style
        # Force the name of the style to synchronize with the requested key.
        style['name'] = name
        return style # Answer the style for convenience of tha caller, e.g. when called by self.newStyle(args,...)

    def newStyle(self, **kwargs):
        u"""Create a new style with the supplied arguments as attributes. Force the style in self.styles,
        even if already exists. Forst the name of the style to be the same as the style key.
        Answer the new style."""
        return self.replaceStyle(kwargs['name'], dict(**kwargs))
    
    #   D E F A U L T  A T T R I B U T E S 

    def _get_originTop(self):
        u"""Answer the document flag if origin is on top.

        >>> doc = Document(name='TestDoc', originTop=True)
        >>> doc.originTop
        True
        >>> doc.rootStyle.get('originTop')
        True
        >>> doc.originTop = False
        >>> doc.originTop
        False
        >>> doc.rootStyle.get('originTop')
        False
        """
        return self.rootStyle.get('originTop')
    def _set_originTop(self, flag):
        rs = self.rootStyle
        rs['originTop'] = flag
        rs['yAlign'] = {True:TOP, False: BOTTOM}[bool(flag)]
    originTop = property(_get_originTop, _set_originTop)

    def _get_frameDuration(self):
        u"""Property answer the document frameDuration parameters, used for speed when
        exporting animated gifs.
        """
        return self.rootStyle.get('frameDuration')
    def _set_frameDuration(self, frameDuration):
        self.rootStyle['frameDuration'] = frameDuration
    frameDuration = property(_get_frameDuration, _set_frameDuration)

    # CSS property service to children.
    def _get_w(self): # Width
        u"""Property answering the global (intended) width of the document as defined by
        self.rootStyle['w']. This may not represent the actual width of the document, 
        which comes from the maximum width of all child pages together and if the current
        view is defined as spread.

        >>> doc = Document(name='TestDoc', w=100)
        >>> doc.w
        100
        >>> doc.rootStyle['w'] = 200
        >>> doc.w
        200
        >>> doc.w = 300
        >>> doc.w
        300
        """
        return self.rootStyle['w'] 
    def _set_w(self, w):
        self.rootStyle['w'] = w # Overwrite element local style from here, parent css becomes inaccessable.
    w = property(_get_w, _set_w)

    def _get_h(self): # Height
        u"""Property answering the global (intended) height of the document as defined by
        self.rootStyle['h']. This may not represent the actual height of the document, 
        which comes from the maximum height of all child pages together.

        >>> doc = Document(name='TestDoc', h=100)
        >>> doc.h
        100
        >>> doc.rootStyle['h'] = 200
        >>> doc.h
        200
        >>> doc.h = 300
        >>> doc.h
        300
        """
        return self.rootStyle['h'] 
    def _set_h(self, h):
        self.rootStyle['h'] = h # Overwrite element local style from here, parent css becomes inaccessable.
    h = property(_get_h, _set_h)

    def _get_d(self): # Depth
        u"""Property answering the global (intended) depth of the document as defined by
        self.rootStyle['d']. This may not represent the actual depth of the document, 
        which comes from the maximum depth of all child pages together.

        >>> doc = Document(name='TestDoc', d=100)
        >>> doc.d
        100
        >>> doc.rootStyle['d'] = 200
        >>> doc.d
        200
        >>> doc.d = 300
        >>> doc.d
        300
        """
        return self.rootStyle['d'] # From self.style, don't inherit.
    def _set_d(self, d):
        self.rootStyle['d'] = d # Overwrite element local style from here, parent css becomes inaccessable.
    d = property(_get_d, _set_d)

    def _get_padding(self): # Tuple of paddings in CSS order, direction of clock
        u"""Answer the document global padding, as defined in the root style.
        Intercace is identical to Element.padding

        >>> doc = Document(name='TestDoc', padding=(10, 20, 30, 40))
        >>> doc.padding
        (10, 20, 30, 40)
        >>> doc.padding = (11, 21, 31, 41)
        >>> doc.padding3D
        (11, 21, 31, 41, 0, 0)
        """
        return self.pt, self.pr, self.pb, self.pl
    def _set_padding(self, padding):
        # Can be 123, [123], [123, 234] or [123, 234, 345, 4565, ]
        if isinstance(padding, (int, float)):
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
        u"""Tuple of padding in CSS order + (front, back), direction of clock.
        Interface is identical to Element.padding3d.
        
        >>> doc = Document(name='TestDoc', padding=(10, 20, 30, 40, 50, 60))
        >>> doc.pt, doc.pr, doc.pb, doc.pl, doc.pzf, doc.pzb
        (10, 20, 30, 40, 50, 60)
        >>> doc.pl = 123
        >>> doc.padding3D
        (10, 20, 30, 123, 50, 60)
        >>> doc.padding3D = 11
        >>> doc.padding3D
        (11, 11, 11, 11, 11, 11)
        >>> doc.padding3D = (11, 22)
        >>> doc.padding3D
        (11, 22, 11, 22, 11, 22)
        >>> doc.padding3D = (11, 22, 33)
        >>> doc.padding3D
        (11, 22, 33, 11, 22, 33)
        >>> doc.padding3D = (11, 22, 33, 44)
        >>> doc.padding3D
        (11, 22, 33, 44, 0, 0)
        >>> doc.padding3D = (11, 22, 33, 44, 55, 66)
        >>> doc.padding3D
        (11, 22, 33, 44, 55, 66)
        """
        return self.pt, self.pr, self.pb, self.pl, self.pzf, self.pzb
    padding3D = property(_get_padding3D, _set_padding)

    def _get_pt(self): # Padding top
        u"""Padding top property
        Interface is identical to Element.pt.

        >>> doc = Document(name='TestDoc', pt=12)
        >>> doc.pt
        12
        >>> doc.pt = 13
        >>> doc.pt
        13
        >>> doc.padding # Taking over default value of root style.
        (13, 42, 42, 49)
        >>> doc.padding3D # Taking over default value of root style.
        (13, 42, 42, 49, 0, 0)
        """
        return self.css('pt', 0)
    def _set_pt(self, pt):
        self.rootStyle['pt'] = pt  
    pt = property(_get_pt, _set_pt)

    def _get_pb(self): # Padding bottom
        u"""Padding bottom property
        Interface is identical to Element.pb.

        >>> doc = Document(name='TestDoc', pb=12)
        >>> doc.pb
        12
        >>> doc.pb = 13
        >>> doc.pb
        13
        >>> doc.padding # Taking over default value of root style.
        (49, 42, 13, 49)
        >>> doc.padding3D # Taking over default value of root style.
        (49, 42, 13, 49, 0, 0)
        """
        return self.css('pb', 0)
    def _set_pb(self, pb):
        self.rootStyle['pb'] = pb  
    pb = property(_get_pb, _set_pb)
    
    def _get_pl(self): # Padding left
        u"""Padding left property
        Interface is identical to Element.pl.

        >>> doc = Document(name='Testoc', pl=12)
        >>> doc.pl
        12
        >>> doc.pl = 13
        >>> doc.pl
        13
        >>> doc.padding # Taking over default value of root style.
        (49, 42, 42, 13)
        >>> doc.padding3D # Taking over default value of root style.
        (49, 42, 42, 13, 0, 0)
        """
        return self.css('pl', 0)
    def _set_pl(self, pl):
        self.rootStyle['pl'] = pl 
    pl = property(_get_pl, _set_pl)
    
    def _get_pr(self): # Margin right
        u"""Padding right property
        Interface is identical to Element.pr.

        >>> doc = Document(name='Testoc', pr=12)
        >>> doc.pr
        12
        >>> doc.pr = 13
        >>> doc.pr
        13
        >>> doc.padding # Taking over default value of root style.
        (49, 13, 42, 49)
        >>> doc.padding3D # Taking over default value of root style.
        (49, 13, 42, 49, 0, 0)
        """
        return self.css('pr', 0)
    def _set_pr(self, pr):
        self.rootStyle['pr'] = pr  
    pr = property(_get_pr, _set_pr)

    def _get_pzf(self): # Padding z-axis front
        u"""Padding padding z-front property
        Interface is identical to Element.pzf.

        >>> doc = Document(name='Testoc', pzf=12)
        >>> doc.pzf
        12
        >>> doc.pzf = 13
        >>> doc.pzf
        13
        >>> doc.padding # Taking over default value of root style.
        (49, 42, 42, 49)
        >>> doc.padding3D # Taking over default value of root style.
        (49, 42, 42, 49, 13, 0)
        """
        return self.css('pzf', 0)
    def _set_pzf(self, pzf):
        self.rootStyle['pzf'] = pzf  
    pzf = property(_get_pzf, _set_pzf)
    
    def _get_pzb(self): # Padding z-axis back
        u"""Padding padding z-front property
        Interface is identical to Element.pzb.

        >>> doc = Document(name='Testoc', pzb=12)
        >>> doc.pzb
        12
        >>> doc.pzb = 13
        >>> doc.pzb
        13
        >>> doc.padding # Taking over default value of root style.
        (49, 42, 42, 49)
        >>> doc.padding3D # Taking over default value of root style.
        (49, 42, 42, 49, 0, 13)
        """
        return self.css('pzb', 0)
    def _set_pzb(self, pzb):
        self.rootStyle['pzb'] = pzb  
    pzb = property(_get_pzb, _set_pzb)

    #   P A G E S

    def appendPage(self, page, startPage=1):
        u"""Append page to the document. Assert that it is a page element.

        >>> from pagebot.elements.pbpage import Page
        >>> from pagebot.elements.views.pageview import PageView
        >>> doc = Document(name='TestDoc', autoPages=100)
        >>> len(doc)
        100
        >>> page = Page()
        >>> doc.appendPage(page)
        >>> len(doc)
        101
        >>> page = Page()
        >>> doc.appendElement(page)
        >>> len(doc)
        102
        >>> min(doc.pages.keys()), max(doc.pages.keys())
        (1, 102)
        """
        if page.isPage:
            page.setParent(self) # Set parent as weakref, without calling self.appendElement again.
            if self.pages.keys():
                pn = max(self.pages.keys())+1
            else:
                pn = startPage
            self[pn] = page
        else:
            raise TypeError('Cannot add element "%s" to document. Only "e.isPage == True" are supported.' % page)
    
    appendElement = appendPage

    def getPage(self, pnOrName, index=0):
        u"""Answer the page at (pn, index). Otherwise search for a page with this name. 
        Raise index errors if it does not exist."""
        if pnOrName in self.pages:
            if index >= len(self.pages[pnOrName]):
                return None
            return self.pages[pnOrName][index]
        pages = self.findPages(name=pnOrName) # In case searching by name, there is chance that multiple are answered as list.
        if pages:
            return pages[0]
        return None

    def getPages(self, pn):
        u"""Answer all pages that share the same page number. Rase KeyError if non exist.

        >>> from pagebot.elements.pbpage import Page
        >>> from pagebot.elements.views.pageview import PageView
        >>> doc = Document(name='TestDoc', autoPages=100)
        >>> doc[66] == doc.getPages(66)[0]
        True
        """
        return self.pages[pn]

    def findPages(self, eId=None, name=None, pattern=None, pageSelection=None):
        u"""Various ways to find pages from their attributes."""
        pages = []
        for pn, pnPages in sorted(self.pages.items()):
            if not pageSelection is None and not pn in pageSelection:
                continue
            for page in pnPages: # List of pages with identical pn
                if eId == page.eId:
                    return [page]
                if (name is not None and name == page.name) or \
                       pattern is not None and page.name is not None and pattern in page.name:
                    pages.append(page)
        return pages

    def isLeft(self):
        u"""This is reached for e.isleft() queries, when elements are not placed on a page.
        The Document cannot know the answer then. Always answer False.

        >>> doc = Document(name='TestDoc')
        >>> doc.isLeft
        False
        >>> doc.isRight
        False
        """
        return False
    isRight = isLeft = False
    
    def isLeftPage(self, page):
        u"""Answer the boolean flag if the page is currently defined as a left page. 
        Left page is even page number

        >>> doc = Document(name='TestDoc', autoPages=8)
        >>> page = doc[5]
        >>> doc.isLeftPage(page)
        False
        >>> page = doc[6]
        >>> doc.isLeftPage(page)
        True
        """
        for pn, pnPages in self.pages.items():
            if page in pnPages:
                return pn % 2 == 0 
        return False # Page not found

    def isRightPage(self, page):
        u"""Answer the boolean flag if the page is currently defined as a left page. 
        Right page is odd page number.

        >>> doc = Document(name='TestDoc', autoPages=8)
        >>> page = doc[5]
        >>> doc.isRightPage(page)
        True
        >>> page = doc[6]
        >>> doc.isRightPage(page)
        False
        """
        for pn, pnPages in self.pages.items():
            if page in pnPages:
                return pn % 2 == 1
        return False # Page not found

    def newPage(self, pn=None, template=None, w=None, h=None, name=None, **kwargs):
        u"""Create a new page with size (self.w, self.h) unless defined otherwise. 
        Add the pages in the row of pn, if defined. Otherwise create a new row of pages at pn. 
        If pn is undefined, add a new page row at the end.
        If template is undefined, then use self.defaultTemplate to initialize the new page."""
        if isinstance(template, str):
            template = self.templates.get(template)
        if template is None:
            template = self.defaultTemplate
        
        if not name and template is not None:
            name = template.name

        page = self.PAGE_CLASS(parent=self, w=None, h=None, name=name, **kwargs)
        page.applyTemplate(template)
        return page # Answer the new page 

    def makePages(self, pageCnt, pn=1, template=None, name=None, w=None, h=None, **kwargs):
        u"""If no "point" is defined as page number pn, then we'll continue after the maximum 
        value of page.y origin position. If template is undefined, then self.newPage will use 
        self.defaultTemplate to initialize the new pages.

        >>> doc = Document(autoPages=4)
        >>> len(doc.pages), sorted(doc.pages.keys())
        (4, [1, 2, 3, 4])
        """
        for n in range(pageCnt): # First page is n + pn
            # Parent is forced to self.
            self.newPage(pn=pn+n, template=template, name=name, w=w, h=h, **kwargs) 

    def getElementPage():
        u"""Search ancestors for the page element. This call can only happen here if elements 
        don't have a Page ancestor. Always return None to indicate that there is no Page 
        instance found amongst the ancesters."""
        return None

    def nextPage(self, page, nextPage=1, makeNew=True):
        u"""Answer the next page of page. If it does not exist, create a new page.

        >>> doc = Document(autoPages=4)
        >>> page = doc[2]
        >>> next = doc.nextPage(page)
        >>> doc.getPageNumber(next)
        '3'
        >>> next = doc.nextPage(next)
        >>> doc.getPageNumber(next)
        '4'
        >>> next = doc.nextPage(next) # Creating new page
        >>> doc.getPageNumber(next)
        '5'
        """
        found = False
        for pn, pnPages in sorted(self.pages.items()):
            for index, pg in enumerate(pnPages):
                if found:
                    return pg
                if pg.eId == page.eId:
                    found = True
        # Not found, create new one?
        if makeNew:
            return self.newPage()
        return None

    def getPageNumber(self, page):
        u"""Answer a string with the page number pn, if the page can be found. If the page has index > 0:
        then answer page format "pn-index". pn and index are incremented by 1.
        TODO: Make a reversed table if this squential search shows to be slow in the future with large docs.
        """
        for pn, pnPages in sorted(self.pages.items()):
            for index, pg in enumerate(pnPages):
                if pg is page:
                    if index:
                        return '%d-%d' % (pn, index)
                    return '%d' % (pn)
        return ''

    def getFirstPage(self):
        u"""Answer the list of pages with the lowest sorted page.y. Answer empty list if there are no pages."""
        for pn, pnPages in sorted(self.pages.items()):
            for index, page in enumerate(pnPages):
                return page
        return None

    def getLastPage(self):
        u"""Answer last page with the highest sorted page.y. Answer empty list if there are no pages."""
        pn = sorted(self.pages.keys())[-1]
        return self.pages[pn][-1]

    def getSortedPages(self, pageSelection=None):
        u"""Answer the dynamic list of pages, sorted by y, x and index."""
        pages = [] # List of (pn, pnPages) tuples of pages with the same page number.
        for pn, pnPages in sorted(self.pages.items()):
            if pageSelection is not None and not pn in pageSelection:
                continue
            pages.append((pn, pnPages))
        return pages

    def getMaxPageSizes(self, pageSelection=None):
        u"""Answer the (w, h, d) size of all pages together. If the optional pageSelection is defined (set of y-values),
        then only evaluate the selected pages.

        >>> doc = Document(name='TestDoc', w=500, h=500, autoPages=10, maxW=100000, maxH=100000)
        >>> doc.getMaxPageSizes()
        (500, 500, 1)
        >>> page = doc[1]
        >>> page.w, page.h
        (500, 500)
        >>> page.w = 2345
        >>> page, page.w
        (<Page:default (0, 0)>, 2345)
        >>> doc[4].h = 1111
        >>> doc.getMaxPageSizes()
        (2345, 1111, 1)
        """
        w = h = d = 0
        for pn, pnPages in self.pages.items():
            if not pageSelection is None and not pn in pageSelection:
                continue
            for page in pnPages:
                w = max(page.w, w)
                h = max(page.h, h)
                d = max(page.d, d)
        return w, h, d

    #   C O N D I T I O N S

    def solve(self, score=None):
        u"""Evaluate the content of all pages to return the total sum of conditions solving.
        If necessary, the builder for solving specific text conditions, such as
        run length of text and overflow of text boxes, is found by the current self.view.b.

        >>> doc = Document(name='TestDoc', w=300, h=400, autoPages=2, padding=(30, 40, 50, 60))
        >>> score = doc.solve()
        >>> score
        Score: 0 Fails: 0
        """
        score = Score()
        for pn, pnPages in sorted(self.pages.items()):
            for page in pnPages: # List of pages with identical pn, step through the pages.
                page.solve(score)
        return score

    #   V I E W S

    def getView(self, viewId=None, create=True):
        u"""Answer the view viewId exists. Otherwise if create is True and viewId is a known
        class of view, then create a new instance and answers it. Otherwise answer self.view.

        >>> doc = Document(name='TestDoc')
        >>> doc.getView().isView
        True
        >>> doc.view is doc.getView(), doc.view.name
        (True, 'Page')
        """
        if viewId in self.views:
            return self.views[viewId]
        return self.view

    def newView(self, viewId=None, name=None, context=None):
        u"""Create a new view instance and set self.view default view, that will be used for 
        checking on view parameters, before any element rendering is done, such as layout conditions 
        and creating the right type of strings. 
        If context is not defined, then use the result of getView()

        >>> from pagebot.elements.views import viewClasses
        >>> doc = Document(name='TestDoc', w=300, h=400, autoPages=2)
        >>> sorted(viewClasses.keys())
        ['Git', 'Mamp', 'Page', 'Site']
        >>> view = doc.newView('Page', 'myView')
        >>> str(view.context) in ('<DrawBotContext>', '<FlatContext>')
        True
        >>> view.w, view.h
        (300, 400)
        >>> view = doc.newView('Site')
        >>> view.context
        <HtmlContext>
        """
        if viewId is None:
            viewId = self.DEFAULT_VIEWID
        view = self.view = self.views[viewId] = viewClasses[viewId](name=name or viewId, w=self.w, h=self.h, context=context)
        view.setParent(self) # Just set parent, without all functionality of self.addElement()
        return view
    
    #   D R A W I N G  &  B U I L D I N G

    def build(self, path=None, pageSelection=None, multiPage=True):
        u"""Build the document as website, using the document.view for export.

        >>> doc = Document(name='TestDoc', w=300, h=400, autoPages=1, padding=(30, 40, 50, 60))
        >>> doc.view # PageView is default.
        <PageView:Page (0, 0)>
        >>> doc.build('_export/TestBuildDoc.pdf')        
        >>> view = doc.newView('Site')
        >>> doc.view
        <SiteView:Site (0, 0)>
        """
        self.view.build(path, pageSelection=pageSelection, multiPage=multiPage)

    def export(self, path=None, multiPage=True):
        u"""Export the document as website, using the document.view for export.

        >>> from pagebot.elements import newRect
        >>> from pagebot.conditions import *
        >>> w = h = 400
        >>> doc = Document(name='TestDoc', w=w, h=h, autoPages=1, padding=40)
        >>> r = newRect(fill=(1,0,0), parent=doc[1], conditions=[Fit()])
        >>> score = doc.solve()
        >>> doc.view # PageView is default.
        <PageView:Page (0, 0)>
        >>> doc.export('_export/TestExportDoc.pdf')        
        """
        self.build(path=path, multiPage=multiPage)

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
