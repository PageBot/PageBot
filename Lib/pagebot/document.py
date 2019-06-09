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
#     document.py
#
import copy
import codecs
from pagebot.stylelib import styleLib # Library with named, predefined style dicts.
from pagebot.conditions.score import Score
from pagebot.elements.pbpage import Page, Template
from pagebot.elements.views import viewClasses, defaultViewClass
from pagebot.constants import *
from pagebot.style import getRootStyle
from pagebot.themes import DEFAULT_THEME_CLASS
from pagebot.toolbox.transformer import obj2StyleId, path2Url, json2Dict, \
    dict2Json, asNormalizedJSON
from pagebot.toolbox.units import pt, units, isUnit, point3D

class Document:
    """A Document a container of pages.

    Doctest: https://docs.python.org/2/library/doctest.html
    Run doctest in Sublime: cmd-B

    >>> doc = Document(name='TestDoc', startPage=12, autoPages=50)
    >>> len(doc), min(doc.pages.keys()), max(doc.pages.keys())
    (50, 12, 61)

    >>> doc = Document(name='TestDoc', w=300, h=400, autoPages=2, padding=(30, 40, 50, 60))
    >>> doc.name, doc.w, doc.h, doc.originTop, len(doc)
    ('TestDoc', 300pt, 400pt, False, 2)
    >>> doc.padding
    (30pt, 40pt, 50pt, 60pt)
    >>> page = doc[1] # First page is on the right
    >>> page.padding = 20
    >>> page.w, page.h, page.pw, page.ph, page.pt, page.pr, page.pb, page.pl, page.title
    (300pt, 400pt, 260pt, 360pt, 20pt, 20pt, 20pt, 20pt, 'default')

    >>> pages = (Page(), Page(), Page())
    >>> doc = Document(name='TestDoc', w=300, h=400, pages=pages, autoPages=0, viewId='Mamp')
    >>> len(doc), sorted(doc.pages.keys()), len(doc.pages[1])
    (3, [1, 2, 3], 1)
    >>> doc.context
    <HtmlContext>

    """
    PAGE_CLASS = Page # Allow inherited versions of the Page class.
    DEFAULT_VIEWID = defaultViewClass.viewId

    def __init__(self, styles=None, theme=None, viewId=None, name=None, title=None, pages=None,
            autoPages=1, template=None, templates=None, originTop=False, startPage=None,
            sId=None, w=None, h=None, d=None, size=None, wh=None, whd=None, padding=None, 
            docLib=None, context=None, path=None, exportPaths=None, **kwargs):
        """Contains a set of Page elements and other elements used for display
        in thumbnail mode. Used to compose the pages without the need to send
        them directly to the output for asynchronous page filling."""

        if whd is not None:
            size = whd
        elif wh is not None:
            size = wh # Alternative ways to define size, making it intuitive to the caller.
        if size is not None: # For convenience of the caller, also accept size tuples.
            w, h, d = point3D(size) # Set 

        # Set position of origin and direction of y for self and all inheriting pages
        # and elements.
        self._originTop = originTop # Set as property. Ii is not supposed to change.

        # If no theme defined, then use the default theme class to create an instance.
        # Themes hold values and colors, combined in a theme.mood dictionary that matches
        # functions with parameters.
        if theme is None:
            theme = DEFAULT_THEME_CLASS()
        self.theme = theme

        # Adjust self.rootStyle['yAlign'] default value, based on self.origin, if not defined
        # as separate attribute in **kwargs.
        self.rootStyle = rs = self.makeRootStyle(**kwargs)
        self.initializeStyles(styles) # May or may not overwrite the root style.
        self.path = path # Optional source file path of the document, e.g. .sketch file.
        self.name = name or title or 'Untitled'
        self.title = title or self.name

        self.w = w or DEFAULT_DOC_WIDTH # Always needs a value. Take 1000 if 0 or None defined.
        self.h = h or DEFAULT_DOC_HEIGHT # These values overwrite the self.rootStyle['w'] and self.rootStyle['h']
        self.d = d # In case depth is 0, keep is as value

        self.sId = sId # Optional system id, used by an external application (e.g. Sketch). Can be None.

        if padding is not None:
            self.padding = padding

        # Initialize the dictionary of pages.
        self.pages = {} # Key is pageNumber, Value is row list of pages: self.pages[pn][index] = page
        for page in pages or []: # In case there are pages defined on init, add them.
            self.appendPage(page, startPage)

        # Initialize the current view of this document. All conditional
        # checking and building is done through this view. The defaultViewClass
        # is set either to an in stance of PageView.
        self.views = {} # Key is the viewId. Value is a view instance.

        # Set the self.view to an instance of viewId or defaultViewClass.viewId
        # and store in self.views. Add the optional context, if defined.
        # Otherwise use the result of default getContext. A context is an
        # instance of e.g. one of DrawBotContext, FlatContext or HtmlContext,
        # which then hold the instance of a builder (respectively DrawBot, Flat
        # and one of the HtmlBuilders, such as GitBuilder or MampBuilder)
        self.newView(viewId or self.DEFAULT_VIEWID, context=context)

        # Template is name or instance default template.
        self.initializeTemplates(templates, template)

        # Property self.docLib for storage of collected content while typesetting
        # and composing, referring to the pages they where placed on during
        # composition. The docLib can optionally be defined when constructing
        # self.
        if docLib is None:
            docLib = {}
        self._docLib = docLib

        # Document (w, h) size is default from page, but will modified by the type of display mode.
        if autoPages:
            self.makePages(pageCnt=autoPages, pn=startPage, w=self.w, h=self.h, d=self.d, **kwargs)

        # Call generic initialize method, allowing inheriting publication
        # classes to initialize their stuff. This can be the creation of
        # templates, pages, adding/altering styles and view settings. Default
        # is to do nothing.
        self.initialize(**kwargs)

    def initialize(self, **kwargs):
        """Default implementation of publication initialized. Can be redefined
        by inheriting classed. All **kwargs are available to allow access for
        inheriting Publication documents."""
        pass

    def _get_docLib(self):
        """Answers the global storage dictionary, used by TypeSetter and others
        to keep track of footnotes, table of content, etc. Some common entries
        are predefined. In the future this lib could be saved into JSON, in
        case it needs to be shared between documents. E.g. this could happen if
        a publication is generated from multiple independents documents, that
        need to exchange information across applications.

        >>> doc = Document(name='TestDoc', docLib=dict(a=12, b=34))
        >>> sorted(doc.docLib.items())
        [('a', 12), ('b', 34)]
        """
        return self._docLib
    docLib = property(_get_docLib)

    def __len__(self):
        """Answers the amount of pages in the document.

        >>> doc = Document(name='TestDoc', startPage=13, autoPages=42)
        >>> len(doc) == len(doc.pages) == 42
        True
        """
        return len(self.pages)

    def __repr__(self):
        """Answering the string representation of the document.

        >>> doc = Document(name='TestDoc', autoPages=41)
        >>> t = doc.addTemplate('Template1', Template())
        >>> v = doc.getView('Mamp') # Creating the view if it does not exist.
        >>> str(doc)
        '<Document "TestDoc" Pages=41 Templates=2 Views=1>'
        """
        s = '<%s "%s"' % (self.__class__.__name__, self.name)
        if self.pages:
            s += ' Pages=%d' % len(self.pages)
        if self.templates:
            s += ' Templates=%d' % len(self.templates)
        if self.views:
            s += ' Views=%d' % len(self.views)
        s += '>'
        return s

    def _get_doc(self):
        """Root of the chain of element properties, searching upward in the
        ancestors tree. It refers to itself to make the call compatible with
        any child page or element.

        >>> doc = Document(name='TestDoc')
        >>> doc.doc is doc
        True
        """
        return self
    doc = property(_get_doc)

    def _get_context(self):
        """Answers the context of the current view to allow searching the
        parents --> document --> view. """
        return self.view.context
    context = property(_get_context)

    # Document[12] answers a list of pages where page.y == 12
    # This behaviour is different from regular elements, who want the page.eId as key.
    def __getitem__(self, pnIndex):
        """Answers the pages with pageNumber equal to page.y.

        >>> doc = Document(name='TestDoc', w=300, h=400, autoPages=100)
        >>> page = doc[66]
        >>> page, page.pn
        (<Page #66 default (300pt, 400pt)>, (66, 0))
        >>> doc.getPageNumber(page)
        (66, 0)
        >>> doc[-10] is None and doc[10000] is None # Answer None if out of range.
        True
        """
        if isinstance(pnIndex, (list, tuple)):
            pn, index = pnIndex
        else:
            pn, index = pnIndex, 0 # Default is left page on pn row.
        if pn in self.pages:
            return self.pages[pn][index]
        return None
    def __setitem__(self, pn, page):
        if not pn in self.pages: # Add list as
            self.pages[pn] = []
        self.pages[pn].append(page)
        page.setParent(self)

    def _get_ancestors(self):
        """Root of the chain of element properties, searching upward in the
        ancestors tree. As the document, by definition, is the top of the
        tree, an empty list is answered.

        >>> doc = Document(name='TestDoc')
        >>> len(doc.ancestors) == 0
        True
        """
        return []
    ancestors = property(_get_ancestors)

    def _get_parent(self):
        """Root of the chain of element properties, searching upward in the
        ancestors tree. As the document, by definition, is the top of the
        tree, `None` is answered as parent.

        >>> doc = Document(name='TestDoc')
        >>> doc.parent is None
        True
        """
        return None
    parent = property(_get_parent)

    def getGlossary(self):
        """Answers a string glossary with most representing info about the
        document.

        >>> doc = Document(name='DemoDoc')
        >>> doc.getGlossary().startswith('Document "DemoDoc"')
        True
        """
        glossary = []
        glossary.append('%s "%s"' % (self.__class__.__name__, self.name))
        glossary.append('\tPages: %d' % len(self.pages))
        glossary.append('\tTemplates: %s' % ', '.join(sorted(self.templates.keys())))
        glossary.append('\tStyles: %s' % ', '.join(sorted(self.styles.keys())))
        glossary.append('\tLib: %s' % ', '.join(self.docLib.keys()))
        return '\n'.join(glossary)

    def _get_builder(self):
        """Answers the builder, which should be available from self.context.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> doc = Document(context=context, title='MySite')
        >>> doc, doc.context, doc.title
        (<Document "MySite" Pages=1 Templates=1 Views=1>, <DrawBotContext>, 'MySite')
        """

        """>>> from pagebot.contexts.flatcontext import FlatContext
        >>> context = FlatContext()
        >>> doc = Document(context=context)
        >>> doc.context
        <FlatContext>
        """
        return self.context.b
    b = builder = property(_get_builder)

    #   T E M P L A T E

    def initializeTemplates(self, templates, defaultTemplate):
        """Initialize the document templates."""
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
        """Answers the named template. If it does not exist, then answer the
        default template. Answer `None` if there is no default.

        >>> from pagebot.constants import A6
        >>> doc = Document(name='TestDoc', size=A6)
        >>> doc.getTemplate()
        <Template>
        >>> doc.getTemplate() == doc.defaultTemplate
        True
        """
        return self.templates.get(name, self.defaultTemplate)

    def addTemplate(self, name, template):
        """Adds the template to the self.templates of dictionaries. There is no
        check, so the caller can overwrite existing templates. Answer the
        template as convenience of the caller.

        >>> from pagebot.elements.pbpage import Template
        >>> name ='TestTemplate'
        >>> t = Template(w=200, h=300, name=name)
        >>> doc = Document(name='TestDoc')
        >>> doc.addTemplate('myTemplate', t)
        <Template>
        >>> doc.getTemplate('myTemplate').name == name
        True
        """
        template.parent = self
        self.templates[name] = template
        return template

    def _get_defaultTemplate(self):
        """Answers the default template of the document.

        >>> from pagebot.constants import Legal
        >>> doc = Document(name='TestDoc', size=Legal)
        >>> doc.defaultTemplate
        <Template>
        """
        return self.templates.get('default')
    def _set_defaultTemplate(self, template):
        self.addTemplate('default', template)
    defaultTemplate = property(_get_defaultTemplate, _set_defaultTemplate)

    #   S T Y L E

    def initializeStyles(self, styles):
        """Make sure that the default styles always exist."""

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
        """Creates a rootStyle, then set the arguments from **kwargs, if their
        entry name already exists. This is similar (but not identical) to the
        makeStyle in Elements. There any value entry is copied, even if that is
        not defined in the root style.

        >>> doc = Document()
        >>> page = doc[1] # Inheriting from doc
        >>> doc.originTop, doc.rootStyle['yAlign'], page.originTop, page.yAlign
        (False, 'bottom', False, 'bottom')
        >>> doc = Document(originTop=True)
        >>> page = doc[1] # Inheriting from doc
        >>> doc.originTop, doc.rootStyle['yAlign'], page.originTop, page.yAlign
        (True, 'top', True, 'top')
        >>> doc = Document(originTop=True, yAlign=BOTTOM)
        >>> page = doc[1] # Inheriting from doc, overwriting yAlign default.
        >>> doc.originTop, doc.rootStyle['yAlign'], page.originTop, page.yAlign
        (True, 'bottom', True, 'bottom')
        >>> doc = Document(yAlign=TOP)
        >>> page = doc[1] # Inheriting from doc, overwriting yAlign default.
        >>> doc.originTop, doc.rootStyle['yAlign'], page.originTop, page.yAlign
        (False, 'top', False, 'top')
        """
        rootStyle = getRootStyle()
        for name, v in kwargs.items():
            if name in rootStyle: # Only overwrite existing values.
                rootStyle[name] = v
        # Adjust the default vertical origin position from self.origin, if not already defined
        # by **kwargs
        if 'yAlign' not in kwargs:
            yAlign = {True: TOP, False: BOTTOM, None: BOTTOM}[self.originTop]
            rootStyle['yAlign'] = yAlign
        return rootStyle

    def applyStyle(self, style):
        """Apply the key-value of the style onto the self.rootStyle. This
        overwrites existing style values inthe self.rootStyle by all values in
        style. Cannot be undone.

        >>> doc = Document(name='TestDoc', w=123)
        >>> doc.w
        123pt
        >>> doc.applyStyle(dict(w=pt(1234)))
        >>> doc.w
        1234pt
        """
        for key, value in style.items():
            self.rootStyle[key] = value

    # Answer the cascaded style value, looking up the chain of ancestors, until style value is defined.

    def css(self, name, default=None, styleId=None):
        """If optional eId is None or style cannot found, then use the root
        style. If the style is found from the (cascading) eId, then use that
        to return the requested attribute.  Note that self.css( ) is a generic
        query for a named CSS value, upwards the parent tree.  This is
        different from the CSS functions as self.buildCss( ), that actually
        generate CSS code.

        >>> doc = Document(name='TestDoc', w=500, h=500, autoPages=10)
        >>> doc.css('w'), doc.css('h')
        (500pt, 500pt)
        """
        style = self.findStyle(styleId)
        if style is None:
            style = self.rootStyle
        return style.get(name, default)

    def findStyle(self, styleId):
        """Answers the style that fits the optional sequence naming of styleId.
        Answer `None` if no style can be found. styleId can have one of these
        formats:

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
        """In case we are looking for a named style (e.g. used by the
        Typesetter to build a stack of cascading tag style, then query the
        ancestors for the named style. Default behavior of all elements is that
        they pass the request on to the root, which is nornally the
        document."""
        return self.getStyle(styleName)

    def getStyle(self, name):
        """Answers the names style. If that does not exist, answer the default
        root style."""
        return self.styles.get(name)

    def getRootStyle(self):
        """Answers the default root style, used by the Typesetter as default for
        all other stacked styles."""
        return self.rootStyle

    def add2Style(self, name, addStyle):
        """Add (overwrite) the values in the existing style *name* with the
        values in *addStyle*. Raise an error if the *name* style does not
        exist. Answer the named target style for convenience of the caller."""
        assert name in self.styles
        style = self.styles[name]
        for key, value in addStyle.items():
            style[key] = value
        return style # Answer the style for convenience of the caller.

    def addStyle(self, name, style, force=False):
        """Add the style to the self.styles dictionary. Make sure that styles
        don't get overwritten, if force is False. Remove them first with
        *self.removeStyle* or use *self.replaceStyle(name, style)* instead."""
        if name in self.styles:
            assert force
            self.removeStyle(name)
        self.replaceStyle(name, style)

    def removeStyle(self, name):
        """Remove the style *name* if it exists. Raise an error if is does not
        exist."""
        del self.styles[name]

    def replaceStyle(self, name, style):
        """Set the style by name. Overwrite the style with that name if it
        already exists."""
        self.styles[name] = style
        # Force the name of the style to synchronize with the requested key.
        style['name'] = name
        return style # Answer the style for convenience of tha caller, e.g. when called by self.newStyle(args,...)

    def newStyle(self, **kwargs):
        """Create a new style with the supplied arguments as attributes. Force
        the style in self.styles, even if already exists. Forst the name of the
        style to be the same as the style key. Answer the new style."""
        return self.replaceStyle(kwargs['name'], dict(**kwargs))

    #   D E F A U L T  A T T R I B U T E S

    def _get_originTop(self):
        """Answers the document flag if origin is on top. This value is not supposed to change.

        >>> doc = Document(name='TestDoc', originTop=True)
        >>> doc.originTop
        True
        """
        return self._originTop
    originTop = property(_get_originTop)

    def _get_frameDuration(self):
        """Property answer the document frameDuration parameters, used for
        speed when exporting animated gifs.
        """
        return self.rootStyle.get('frameDuration')
    def _set_frameDuration(self, frameDuration):
        self.rootStyle['frameDuration'] = frameDuration
    frameDuration = property(_get_frameDuration, _set_frameDuration)

    # CSS property service to children.

    def _get_em(self):
        """Answers the current em value (for use in relative units), as value of
        self.css('fontSize', DEFAULT_FONT_SIZE)."""
        return self.rootStyle.get('fontSize', DEFAULT_FONT_SIZE)
    def _set_em(self, em):
        """Store the em size (as fontSize) in the local style."""
        self.rootStyle['fontSize'] = em
    em = property(_get_em, _set_em)

    def _get_w(self): # Width
        """Property answering the global (intended) width of the document as
        defined by self.rootStyle['w']. This may not represent the actual width
        of the document, which comes from the maximum width of all child pages
        together and if the current view is defined as spread.

        >>> doc = Document(name='TestDoc', w=100)
        >>> doc.w
        100pt
        >>> doc.rootStyle['w'] = 200
        >>> doc.w
        200pt
        >>> doc.w = 300
        >>> doc.w
        300pt
        """
        return units(self.rootStyle['w'])
    def _set_w(self, w):
        self.rootStyle['w'] = units(w) # Overwrite element local style from here, parent css becomes inaccessable.
    w = property(_get_w, _set_w)

    def _get_h(self): # Height
        """Property answering the global (intended) height of the document as
        defined by self.rootStyle['h']. This may not represent the actual
        height of the document, which comes from the maximum height of all
        child pages together.

        >>> doc = Document(name='TestDoc', h=100)
        >>> doc.h
        100pt
        >>> doc.rootStyle['h'] = 200
        >>> doc.h
        200pt
        >>> doc.h = 300
        >>> doc.h
        300pt
        """
        return units(self.rootStyle['h'])
    def _set_h(self, h):
        self.rootStyle['h'] = units(h) # Overwrite element local style from here, parent css becomes inaccessable.
    h = property(_get_h, _set_h)

    def _get_d(self): # Depth
        """Property answering the global (intended) depth of the document as
        defined by self.rootStyle['d']. This may not represent the actual depth
        of the document, which comes from the maximum depth of all child pages
        together.

        >>> doc = Document(name='TestDoc', d=100)
        >>> doc.d
        100pt
        >>> doc.rootStyle['d'] = 200
        >>> doc.d
        200pt
        >>> doc.d = 300
        >>> doc.d
        300pt
        """
        return units(self.rootStyle['d']) # From self.style, don't inherit.
    def _set_d(self, d):
        self.rootStyle['d'] = units(d) # Overwrite element local style from here, parent css becomes inaccessable.
    d = property(_get_d, _set_d)

    def _get_size(self):
        """Answer the (w, h) tuple of the document size."""
        return self.w, self.h
    size = property(_get_size)

    def _get_gridX(self):
        """Answer the style value for gridX as property

        >>> gridX = [(100,8),(100,8)]
        >>> doc = Document(gridX=gridX)
        >>> doc.gridX
        [(100, 8), (100, 8)]
        >>> doc.gridX = [(120,9),(120,9),(120,9)]
        >>> doc.gridX
        [(120, 9), (120, 9), (120, 9)]
        """
        return self.rootStyle['gridX']
    def _set_gridX(self, gridX):
        self.rootStyle['gridX'] = gridX
    gridX = property(_get_gridX, _set_gridX)

    def _get_gridY(self):
        """Answer the style value for gridY as property

        >>> gridY = [(100,8),(100,8)]
        >>> doc = Document(gridY=gridY)
        >>> doc.gridY
        [(100, 8), (100, 8)]
        >>> doc.gridY = [(120,9),(120,9),(120,9)]
        >>> doc.gridY
        [(120, 9), (120, 9), (120, 9)]
        """
        return self.rootStyle['gridY']

    def _set_gridY(self, gridY):
        self.rootStyle['gridY'] = gridY

    gridY = property(_get_gridY, _set_gridY)

    def _get_padding(self): # Tuple of paddings in CSS order, direction of clock
        """Answers the document global padding, as defined in the root style.
        Intercace is identical to Element.padding

        >>> doc = Document(name='TestDoc', padding=(10, 20, 30, 40))
        >>> doc.padding
        (10pt, 20pt, 30pt, 40pt)
        >>> doc.padding = (11, 21, 31, 41)
        >>> doc.padding3D
        (11pt, 21pt, 31pt, 41pt, 0pt, 0pt)
        """
        return self.pt, self.pr, self.pb, self.pl

    def _set_padding(self, padding):
        """
        Can be 123, [123], [123, 234] or [123, 234, 345, 4565, ]
        """
        if isUnit(padding) or isinstance(padding, (int, float)):
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
        """Tuple of padding in CSS order + (front, back), direction of clock.
        Interface is identical to Element.padding3D.

        >>> doc = Document(name='TestDoc', padding=(10, 20, 30, 40, 50, 60))
        >>> doc.pt, doc.pr, doc.pb, doc.pl, doc.pzf, doc.pzb
        (10pt, 20pt, 30pt, 40pt, 50pt, 60pt)
        >>> doc.pl = 123
        >>> doc.padding3D
        (10pt, 20pt, 30pt, 123pt, 50pt, 60pt)
        >>> doc.padding3D = 11
        >>> doc.padding3D
        (11pt, 11pt, 11pt, 11pt, 11pt, 11pt)
        >>> doc.padding3D = (11, 22)
        >>> doc.padding3D
        (11pt, 22pt, 11pt, 22pt, 11pt, 22pt)
        >>> doc.padding3D = (11, 22, 33)
        >>> doc.padding3D
        (11pt, 22pt, 33pt, 11pt, 22pt, 33pt)
        >>> doc.padding3D = (11, 22, 33, 44)
        >>> doc.padding3D
        (11pt, 22pt, 33pt, 44pt, 0pt, 0pt)
        >>> doc.padding3D = (11, 22, 33, 44, 55, 66)
        >>> doc.padding3D
        (11pt, 22pt, 33pt, 44pt, 55pt, 66pt)
        """
        return self.pt, self.pr, self.pb, self.pl, self.pzf, self.pzb

    padding3D = property(_get_padding3D, _set_padding)

    def _get_pt(self): # Padding top
        """Padding top property
        Interface is identical to Element.pt.
        In this method "pt" is abbreviation of padding-top, not units point.

        >>> doc = Document(name='TestDoc', pt=12)
        >>> doc.pt
        12pt
        >>> doc.pt = 13
        >>> doc.pt
        13pt
        >>> doc.padding # Taking over default value of root style.
        (13pt, 36pt, 36pt, 42pt)
        >>> doc.padding3D # Taking over default value of root style.
        (13pt, 36pt, 36pt, 42pt, 0pt, 0pt)
        """
        h = self.h
        base = dict(base=h, em=self.em) # In case relative units, use this as base.
        return units(self.rootStyle.get('pt'), base=base)

    def _set_pt(self, pt):
        self.rootStyle['pt'] = units(pt)

    pt = property(_get_pt, _set_pt)

    def _get_pb(self): # Padding bottom
        """Padding bottom property
        Interface is identical to Element.pb.

        >>> doc = Document(name='TestDoc', pb=12)
        >>> doc.pb
        12pt
        >>> doc.pb = 13
        >>> doc.pb
        13pt
        >>> doc.padding # Taking over default value of root style.
        (42pt, 36pt, 13pt, 42pt)
        >>> doc.padding3D # Taking over default value of root style.
        (42pt, 36pt, 13pt, 42pt, 0pt, 0pt)
        """
        h = self.h
        base = dict(base=h, em=self.em) # In case relative units, use this as base.
        return units(self.rootStyle.get('pb'), base=base)

    def _set_pb(self, pb):
        self.rootStyle['pb'] = units(pb)

    pb = property(_get_pb, _set_pb)

    def _get_pl(self): # Padding left
        """Padding left property. Interface is identical to Element.pl.

        >>> doc = Document(name='Testoc', pl=12)
        >>> doc.pl
        12pt
        >>> doc.pl = 13
        >>> doc.pl
        13pt
        >>> doc.padding # Taking over default value of root style.
        (42pt, 36pt, 36pt, 13pt)
        >>> doc.padding3D # Taking over default value of root style.
        (42pt, 36pt, 36pt, 13pt, 0pt, 0pt)
        """
        w = self.w
        base = dict(base=w, em=self.em) # In case relative units, use this as base.
        return units(self.rootStyle.get('pl'), base=base)

    def _set_pl(self, pl):
        self.rootStyle['pl'] = units(pl)

    pl = property(_get_pl, _set_pl)

    def _get_pr(self): # Margin right
        """Padding right property. Interface is identical to Element.pr.

        >>> doc = Document(name='Testoc', pr=12)
        >>> doc.pr
        12pt
        >>> doc.pr = 13
        >>> doc.pr
        13pt
        >>> doc.padding # Taking over default value of root style.
        (42pt, 13pt, 36pt, 42pt)
        >>> doc.padding3D # Taking over default value of root style.
        (42pt, 13pt, 36pt, 42pt, 0pt, 0pt)
        """
        w = self.w
        base = dict(base=w, em=self.em) # In case relative units, use this as base.
        return units(self.rootStyle.get('pr', 0), base=base)

    def _set_pr(self, pr):
        self.rootStyle['pr'] = units(pr)

    pr = property(_get_pr, _set_pr)

    def _get_pzf(self): # Padding z-axis front
        """Padding padding z-front property. Interface is identical to
        Element.pzf.

        >>> doc = Document(name='Testoc', d=100, pzf=12)
        >>> doc.d, doc.pzf # Needs some depth > 1, for padding not to be clipped.
        (100pt, 12pt)
        >>> doc.pzf = 13
        >>> doc.pzf
        13pt
        >>> doc.padding # Taking over default value of root style.
        (42pt, 36pt, 36pt, 42pt)
        >>> doc.padding3D # Taking over default value of root style.
        (42pt, 36pt, 36pt, 42pt, 13pt, 0pt)
        """
        d = self.d
        base = dict(base=d, em=self.em) # In case relative units, use this as base.
        return units(self.rootStyle.get('pzf', 0), base=base)

    def _set_pzf(self, pzf):
        self.rootStyle['pzf'] = units(pzf)

    pzf = property(_get_pzf, _set_pzf)

    def _get_pzb(self): # Padding z-axis back
        """Padding padding z-front property. Interface is identical to
        Element.pzb.

        >>> doc = Document(name='Testoc', d=100, pzb=12)
        >>> doc.d, doc.pzb # Needs some depth > 1, for padding not to be clipped.
        (100pt, 12pt)
        >>> doc.pzb = 13
        >>> doc.pzb
        13pt
        >>> doc.padding # Taking over default value of root style.
        (42pt, 36pt, 36pt, 42pt)
        >>> doc.padding3D # Taking over default value of root style.
        (42pt, 36pt, 36pt, 42pt, 0pt, 13pt)
        """
        d = self.d
        base = dict(base=self.d, em=self.em) # In case relative units, use this as base.
        return units(self.rootStyle.get('pzb', 0), base=base)

    def _set_pzb(self, pzb):
        self.rootStyle['pzb'] = units(pzb)

    pzb = property(_get_pzb, _set_pzb)

    #   P A G E S

    def appendPage(self, page, pn=None):
        """Append page to the document. Assert that it is a page element.

        >>> from pagebot.elements.pbpage import Page
        >>> from pagebot.elements.views.pageview import PageView
        >>> doc = Document(name='TestDoc', startPage=50, autoPages=100)
        >>> len(doc), min(doc.pages.keys()), max(doc.pages.keys())
        (100, 50, 149)
        >>> page = Page()
        >>> doc.appendPage(page)
        >>> len(doc)
        101
        >>> page = Page()
        >>> doc.appendElement(page)
        >>> len(doc)
        102
        >>> min(doc.pages.keys()), max(doc.pages.keys())
        (50, 151)
        """
        if page.isPage:
            if pn is None:
                if self.pages.keys():
                    pn = max(self.pages.keys())+1
                else:
                    pn = 1
            # Create self.pages[pn] = [] if not exists. Then append page to the list.
            # Also call page.setParent(self) as weakref, without calling self.appendElement again.
            self[pn] = page
        else:
            raise TypeError('Cannot add element "%s" to document. Only "e.isPage == True" are supported.' % page)

    appendElement = appendPage

    def getPage(self, pnOrName, index=0):
        """Answers the page at (pn, index). Otherwise search for a page with this name.
        Raise index errors if it does not exist."""
        if pnOrName in self.pages:
            if index >= len(self.pages[pnOrName]):
                return None
            return self.pages[pnOrName][index]
        pages = self.findPages(name=pnOrName) # In case searching by name, there is chance that multiple are answered as list.
        if pages:
            return pages[0]
        return None

    def removePage(self, page):
        """Remove the page from the document and return the object.

        >>> from pagebot.constants import A5
        >>> doc = Document(name='TestDoc', autoPages=5, size=A5)
        >>> page = doc[3]
        >>> page
        <Page #3 default (148mm, 210mm)>
        """

    def getPages(self, pn):
        """Answers all pages that share the same page number. Raise KeyError if
        none exist.

        >>> doc = Document(name='TestDoc', autoPages=100)
        >>> doc[66] == doc.getPages(66)[0]
        True
        """
        return self.pages[pn]

    def findPages(self, eId=None, name=None, pattern=None, pageSelection=None):
        """Various ways to find pages from their attributes."""
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

    def findPage(self, eId=None, name=None, pattern=None, pageSelection=None):
        """Answer the first page found from the self.findPages(...) call. Answer None
        if no page can be found matching the parameters."""
        pages = self.findPages(eId=eId, name=name, pattern=pattern, pageSelection=pageSelection)
        if pages:
            return pages[0]
        return None

    def findBysId(self, sId):
        """If defined, the system self.sId can be used to recursively find self or a child.
        Answer None if nothing can be found that is exactly matching.

        >>> from elements import *
        >>> doc = Document(sId=1234)
        >>> doc.view.sId = 7890
        >>> page = doc[1]
        >>> e1 = Element(parent=page, name='e1', sId=2345)
        >>> e2 = Element(parent=e1, name='e2', sId=3456)
        >>> doc.findBysId(3456)
        <Element:e2 (0pt, 0pt, 100pt, 100pt)>
        >>> doc.findBysId(2345)
        <Element:e1 (0pt, 0pt, 100pt, 100pt) E(1)>
        >>> doc.findBysId(1234)
        <Document "Untitled" Pages=1 Templates=1 Views=1>
        >>> doc.findBysId(7890)
        <PageView>
        """
        if sId is not None:
            if self.sId == sId:
                return self
            for _, pages in self.pages.items():
                for page in pages:
                    found = page.findBysId(sId)
                    if found is not None:
                        return found
            for _, view in self.views.items():
                found = view.findBysId(sId)
                if found is not None:
                    return found
        return None

    def deepFind(self, name=None, pattern=None):
        assert name or pattern
        for pn, pages in self.pages.items():
            for page in pages:
                found = page.deepFind(name=name, pattern=pattern)
                if found is not None:
                    return found
        return None
    select = deepFind

    def isLeft(self):
        """This is reached for `e.isleft()` queries, when elements are not
        placed on a page. The Document cannot know the answer then. Always
        answer False.

        >>> doc = Document(name='TestDoc')
        >>> doc.isLeft
        False
        >>> doc.isRight
        False
        """
        return False

    isRight = isLeft = False

    def newPage(self, pn=None, template=None, w=None, h=None, name=None,
            originTop=None, **kwargs):
        """Creates a new page with size `(self.w, self.h)` unless defined
        otherwise. Add the pages in the row of pn, if defined, otherwise create
        a new row of pages at pn. If `pn` is undefined, add a new page row at
        the end. If template is undefined, then use self.defaultTemplate to
        initialize the new page.

        >>> doc = Document(w=80, h=120, originTop=False)
        >>> page = doc[1]
        >>> page.size
        (80pt, 120pt)
        >>> page.originTop # Value copied into the new page setting
        False
        >>> doc = Document(originTop=True)
        >>> page = doc[1]
        >>> page.originTop
        True
        """
        if isinstance(template, str):
            template = self.templates.get(template)

        if isinstance(template, str): # Find the template with this name.
            template = self.getTemplate(template)
        if template is None: # Not defined or template not found, then use default
            template = self.defaultTemplate

        if not name and template is not None:
            name = template.name

        # If undefined, copy the new page size from the document preset size.
        if w is None:
            w = self.w

        if h is None:
            h = self.h

        # If not defined, then use the self.origin instead.
        if originTop is None:
            originTop = self.originTop

        # Don't set parent to self yet, as this will make the page create a #1.
        # Setting of page.parent is done by self.appendPage, for the right page
        # number.
        page = self.PAGE_CLASS(w=w, h=h, name=name, originTop=originTop, **kwargs)
        self.appendPage(page, pn) # Add the page to the document, before applying the template.
        page.applyTemplate(template)
        return page # Answer the new page for convenience of the caller.

    def removePage(self, pn):
        """Remove the page with index pn, keeping the page numbers of the remaining pages unchanged.

        >>> doc = Document(autoPages=3)
        >>> len(doc.pages), sorted(doc.pages.keys())
        (3, [1, 2, 3])
        >>> doc.removePage(2)
        >>> len(doc.pages), sorted(doc.pages.keys())
        (2, [1, 3])
        """
        del self.pages[pn]

    def makePages(self, pageCnt, pn=None, template=None, name=None, w=None,
            h=None, **kwargs):
        """If no "point" is defined as page number `pn`, then we'll continue
        after the maximum value of `page.y` origin position. If template is
        undefined, then `self.newPage` will use `self.defaultTemplate` to
        initialize the new pages.

        >>> doc = Document(autoPages=2)
        >>> doc.makePages(2)
        >>> len(doc.pages), sorted(doc.pages.keys())
        (4, [1, 2, 3, 4])
        """
        if pn is None:
            pn = max(self.pages.keys() or [0])+1
        for n in range(pageCnt): # First page is n + pn
            # Parent is forced to self.
            self.newPage(pn=pn+n, template=template, name=name, w=w, h=h, **kwargs)

    def getElementPage():
        """Search ancestors for the page element. This call can only happen
        here if elements don't have a Page ancestor. Always return None to
        indicate that there is no Page instance found amongst the ancesters."""
        return None

    def nextPage(self, page, nextPage=1, makeNew=True):
        """Answers the next page of page. If it does not exist, create a new
        page.

        >>> from pagebot.constants import Tabloid
        >>> doc = Document(autoPages=4, size=Tabloid, originTop=False)
        >>> len(doc.pages), len(doc)
        (4, 4)
        >>> page = doc[2]
        >>> next = doc.nextPage(page)
        >>> next
        <Page #3 default (11", 16.90")>
        >>> doc.getPageNumber(next)
        (3, 0)
        >>> next = doc.nextPage(next)
        >>> doc.getPageNumber(next)
        (4, 0)
        >>> doc.nextPage(next, makeNew=False) is None
        True
        >>> next = doc.nextPage(next) # Creating new page of makeNew is True
        >>> doc.getPageNumber(next)
        (5, 0)
        >>> next.originTop
        False
        """
        found = False
        for pn, pnPages in sorted(self.pages.items()):
            for index, pg in enumerate(pnPages):
                if found:
                    return pg
                if pg.eId == page.eId:
                    found = True # Trigger to select the next page in the loop.
        # Not found, create new one?
        if makeNew:
            return self.newPage() # Uses setting of self.originTop as page default.
        return None # No next page found and none created.

    def prevPage(self, page, prevPage=1):
        """Answers the previous page of page. If it does not exist, answer
        None.

        >>> from pagebot.constants import Tabloid
        >>> doc = Document(autoPages=4, size=Tabloid)
        >>> len(doc.pages), len(doc)
        (4, 4)
        >>> page = doc[2]
        >>> prev = doc.prevPage(page)
        >>> prev
        <Page #1 default (11", 16.90")>
        >>> doc.getPageNumber(prev)
        (1, 0)
        >>> prev = doc.prevPage(prev)
        >>> doc.getPageNumber(prev) is None
        True
        """
        previous = None
        for pn, pnPages in sorted(self.pages.items()):
            for index, pg in enumerate(pnPages):
                if pg.eId == page.eId:
                   return previous
                previous = pg
        return None # No previous page found.

    def getPageNumber(self, page):
        """Answers a string with the page number (pn, index), if the page can
        be found and there are multiple. Pages are organized as dict of lists
        (allowing multiple pages on the same page number)

        {1:[page, page, ...], 2}

        TODO: Make a reversed table if this squential search shows to be slow
        in the future with large docs.
        """
        for pn, pnPages in sorted(self.pages.items()):
            for index, pg in enumerate(pnPages):
                if page is pg:
                    return (pn, 0)
        return None # Cannot find this page

    def getFirstPage(self):
        """Answers the list of pages with the lowest sorted `page.y`. Answer
        empty list if there are no pages.

        >>> doc = Document(name='TestDoc', w=500, h=500, startPage=624, autoPages=10)
        >>> doc.getFirstPage()
        <Page #624 default (500pt, 500pt)>
        """
        for pn, pnPages in sorted(self.pages.items()):
            for index, page in enumerate(pnPages):
                return page
        return None

    def getLastPage(self):
        """Answers last page with the highest sorted `page.y`. Answer empty list
        if there are no pages.

        >>> doc = Document(name='TestDoc', w=500, h=500, startPage=5, autoPages=10)
        >>> doc.getLastPage()
        <Page #14 default (500pt, 500pt)>
        """
        pn = sorted(self.pages.keys())[-1]
        return self.pages[pn][-1]

    def getSortedPages(self, pageSelection=None):
        """Answers the dynamic list of pages, sorted by y, x and index."""
        pages = [] # List of (pn, pnPages) tuples of pages with the same page number.
        for pn, pnPages in sorted(self.pages.items()):
            if pageSelection is not None and not pn in pageSelection:
                continue
            pages.append((pn, pnPages))
        return pages

    def getPageTree(self, pageTree=None):
        """Answer a nested dict/list of pages, interpreting their tree-relation (e.g. as
        used for a website-navigation-menu structure) from their url-path.
        The keys in the dictionary are the "folder" names. The pages in each directory
        are collected in a list at key '@'.

        >>> doc = Document(autoPages=0)
        >>> p = doc.newPage(name='home', url='index.html')
        >>> p = doc.newPage(name='c', url='a/aa1/c.html')
        >>> p = doc.newPage(name='d', url='a/aa1/d.html')
        >>> p = doc.newPage(name='d', url='a/aa2/d.html')
        >>> p = doc.newPage(name='e', url='a/aa2/e.html')
        >>> p = doc.newPage(name='f', url='a/aa3/f.html')
        >>> p = doc.newPage(name='g', url='b/bb1/g.html')
        >>> p = doc.newPage(name='h', url='b/bb2/h.html')
        >>> p = doc.newPage(name='i', url='b/bb3/i.html')
        >>> p = doc.newPage(name='j', url='c/c c1/j.html')
        >>> p = doc.newPage(name='zzz', url='r/s/t/u/v/w/x/y/z/zzz.html')
        >>> p = doc.newPage(name='noUrlPage')
        >>> tree = doc.getPageTree()
        >>> tree['home']
        <PageNode path=home page=<Page #1 home (1000pt, 1000pt)> []>
        >>> tree.children[1]
        <PageNode path=a page=None ['a/aa1', 'a/aa2', 'a/aa3']>
        >>> tree['b']
        <PageNode path=b page=None ['b/bb1', 'b/bb2', 'b/bb3']>
        >>> tree['b']['bb1'].page is None
        True
        >>> tree['b']['bb1']['g'].page
        <Page #7 g (1000pt, 1000pt)>
        >>> tree['c'] # Show removed space in url
        <PageNode path=c page=None ['c/c_c1']>
        >>> tree['c']['c_c1']['j'].page.url # Removed space in the url
        'c/c_c1/j.html'
        >>> tree['c']['c_c1']['j'].page.flatUrl
        'c-c_c1-j.html'
        >>> tree['r']['s']['t']['u']['v']['w']['x'].page is None
        True
        >>> tree['r']['s']['t']['u']['v']['w']['x']['y']['z']['zzz'].page
        <Page #11 zzz (1000pt, 1000pt)>
        """
        class PageNode:
            def __init__(self, path=None, page=None):
                self.path = path2Url(path)
                self.page = page
                self.children = []
            def __getitem__(self, name):
                for child in self.children:
                    if child.path and child.path.split('/')[-1] == name:
                        return child
                return None
            def __len__(self):
                return len(self.children)
            def __repr__(self):
                l = []
                for child in self.children:
                    l.append(child.path)
                return '<%s path=%s page=%s %s>' % (self.__class__.__name__, self.path, self.page, l)
            def show(self, tab=0):
                print('\t'*tab, id(self), self)
                for child in self.children:
                    child.show(tab+1)
            def getNode(self, path): # Answer the node with this path, oatherwise add it.
                if path is None:
                    return None
                for child in self.children:
                    if path is not None and path == child.path:
                        return child

                node = PageNode(path)
                self.children.append(node)
                return node

        def addPageNode(page, node):
            if page.url:
                path = None
                for part in page.url.split('/')[:-1]:
                    if path is None:
                        path = part
                    else:
                        path += '/' + part
                    node = node.getNode(path)
                if not path:
                    path = page.name
                else:
                    path += '/' + page.name
                pageNode = PageNode(path, page)
                node.children.append(pageNode)

        root = PageNode('root')
        for pages in self.pages.values(): # For all pages in self
            for page in pages:
                addPageNode(page, root)
        #root.show()
        return root # Answer the full tree.

    def getMaxPageSizes(self, pageSelection=None):
        """Answers the (w, h, d) size of all pages together. If the optional
        pageSelection is defined (set of y-values), then only evaluate the
        selected pages. Clip the found values against the document min/max
        proportions.

        >>> doc = Document(name='TestDoc', w=500, h=500, autoPages=10)
        >>> doc.getMaxPageSizes()
        (500pt, 500pt, 100pt)
        >>> page = doc[1]
        >>> page.size
        (500pt, 500pt)
        >>> page.w = 1400
        >>> page
        <Page #1 default (1400pt, 500pt)>
        >>> doc[4].h = 850
        >>> doc.getMaxPageSizes() # Clipped to max size
        (1400pt, 850pt, 100pt)
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

    #   S P E L L  C H E C K

    def spellCheck(self, languages=None):
        """Recursively spellcheck all pages for the given languages. Answer a list with
        unknown words. Default is to do nothing and just pass the call on to child elements.
        Inheriting classes can redefine _spellCheckWords to check on their on text content."""
        unknownByPage = {}
        if isinstance(languages, str):
            languages = [languages]
        elif languages is None:
            languages = [self.language or DEFAULT_LANGUAGE]
        for pn, pnPages in sorted(self.pages.items()):
            unknown = []
            for page in pnPages:
                page.spellCheck(languages, unknown)
            if unknown:
                unknownByPage[pn] = unknown # Only add if there was somethning found
        return unknownByPage

    #   C O N D I T I O N S

    def solve(self, score=None):
        """Evaluate the content of all pages to return the total sum of
        conditions solving. If necessary, the builder for solving specific text
        conditions, such as run length of text and overflow of text boxes, is
        found by the current self.view.b.

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
        """Answers the view `viewId` exists. Otherwise if create is `True` and
        `viewId` is a known class of view, then creates a new instance and answers
        it. Otherwise answer `self.view`.

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
        """Create a new view instance and set self.view default view, that will
        be used for checking on view parameters, before any element rendering
        is done, such as layout conditions and creating the right type of
        strings. If context is not defined, then use the result of getView().

        >>> from pagebot.elements.views import viewClasses
        >>> doc = Document(name='TestDoc', w=300, h=400, autoPages=2)
        >>> sorted(viewClasses.keys())
        ['Git', 'Mamp', 'Page', 'Site']
        >>> view = doc.newView('Page', 'myView')
        >>> str(view.context) in ('<DrawBotContext>', '<FlatContext>')
        True
        >>> view.w, view.h
        (300pt, 400pt)
        >>> view = doc.newView('Site')
        >>> view.context
        <HtmlContext>
        """
        if viewId is None:
            viewId = self.DEFAULT_VIEWID
        view = self.view = self.views[viewId] = viewClasses[viewId](name=name or viewId, w=self.w, h=self.h, context=context)
        view.setParent(self) # Just set parent, without all functionality of self.addElement()
        return view

    #   S A V E  .  P B T

    
    @classmethod
    def open(cls, path):
        """Save the document in native json source code file, represenrinf all of the current
        settings, including the current dociment.view.
        """

        """
        >>> doc1 = Document(name='MyDoc', w=300, h=400)
        >>> path = '/tmp/pagebot.document.json'
        >>> doc1.save(path) # Save document as PageBot-native zip file.
        >>> doc2 = Document.open(path)
        >>> doc2

        """
        f = codecs.open(path, mode="r", encoding="utf-8") # Save the XML as unicode.
        json = f.read()
        f.close()
        d = json2Dict(json)
        doc = cls()
        return doc

    def save(self, path, **kwargs):
        """Save the document in native json source code file, represenrinf all of the current
        settings, including the current dociment.view.
        """

        """
        >>> doc = Document(w=300, h=400)
        >>> doc.save('/tmp/pagebot.document.json') # Save document as PageBot-native zip file.
        """
        normalizedPages = {}
        d = dict(
            class_=self.__class__.__name__,
            name=self.name,
            rootStyle=asNormalizedJSON(self.rootStyle),
            pages=asNormalizedJSON(self.pages),
            view=asNormalizedJSON(self.view),
        )
        json = dict2Json(d)
        f = codecs.open(path, mode="w", encoding="utf-8") # Save the XML as unicode.
        f.write(json)
        f.close()

    #   D R A W I N G  &  B U I L D I N G

    def build(self, path=None, pageSelection=None, multiPage=True, **kwargs):
        """Builds the document, using the `document.view` for export.

        >>> doc = Document(name='TestDoc', w=300, h=400, autoPages=1, padding=(30, 40, 50, 60))
        >>> doc.view # PageView is default.
        <PageView>
        >>> doc.build('/tmp/TestBuildDoc.pdf')
        >>> view = doc.newView('Site')
        >>> doc.view
        <SiteView:Site (0pt, 0pt, 300pt, 400pt)>
        """
        self.view.build(path, pageSelection=pageSelection, multiPage=multiPage, **kwargs)

    def export(self, path=None, multiPage=True, **kwargs):
        """Export the document, using the `document.view` for export.

        >>> from pagebot.elements import newRect
        >>> from pagebot.toolbox.color import redColor, noColor, color
        >>> from pagebot.conditions import *
        >>> w = h = 400 # Auto-convert plain numbers to default pt-units.
        >>> doc = Document(name='TestDoc', size=(w, h), autoPages=1, padding=40)
        >>> r = newRect(fill=color(1, 0, 0), stroke=noColor, parent=doc[1], conditions=[Fit()])
        >>> score = doc.solve()
        >>> doc.view # PageView is default.
        <PageView>
        >>> doc.export('_export/TestExportDoc.pdf')
        """
        self.build(path=path, multiPage=multiPage, **kwargs)

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
