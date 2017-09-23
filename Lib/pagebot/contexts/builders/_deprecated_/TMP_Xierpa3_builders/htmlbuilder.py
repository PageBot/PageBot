# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#   htmlbuilder.py
#
#   Following standard
#   https://google-styleguide.googlecode.com/svn/trunk/htmlcssguide.xml
#
from xierpa3.builders.builder import Builder
from xierpa3.builders.builderparts.xmltagbuilderpart import XmlTagBuilderPart
from xierpa3.builders.builderparts.htmlbuilderpart import HtmlBuilderPart
from xierpa3.builders.builderparts.xmltransformerpart import XmlTransformerPart
from xierpa3.builders.builderparts.svgbuilderpart import SvgBuilderPart
from xierpa3.builders.builderparts.canvasbuilderpart import CanvasBuilderPart
from xierpa3.toolbox.transformer import TX
from xierpa3.toolbox.stack import Stack

class HtmlBuilder(XmlTagBuilderPart, CanvasBuilderPart, SvgBuilderPart, 
        XmlTransformerPart, HtmlBuilderPart, Builder):
    u"""
    """
    # Used for dispatching component.build_sass, and builder.isType('html'),
    # for components that want to define builder dependent behavior. In normal
    # processing of a page, this should never happen. But it can be used to
    # select specific parts of code that should not be interpreted by other builders.

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Builder.C 

    ID = C.TYPE_HTML # Also the default extension of the output format.
    EXTENSION = ID
    ATTR_POSTFIX = ID # Postfix of dispatcher and attribute names above generic names.

    def initialize(self):
        Builder.initialize(self)
        # XmlTagBuilderPart support
        self._tagStack = Stack() # Stack with running tags for closing and XML validation
        self._svgMode = False # Some calls change behavior when in svg mode.
        self._canvasMode = False # Some calls change behavior in HTML5 canvas mode.

    def getUrl(self):
        u"""Answer the url of the current page. To be implemented by inheriting classes
        that actually knows about urls. Default behavior is to do nothing."""
        return self.e.getFullUrl()

    def theme(self, component):
        pass

    def _theme(self, component):
        pass 

    def page(self, component):
        u"""
        Builds the header of an HTML document.
        Note that the inheriting PhPBuilder uses the result of this method to generate
        the header.php file, as a separate result stream.
        """
        self.docType(self.ID)
        self.html()
        self.head()
        # Title depends on selected article. Otherwise show the path, if not available.
        path = self.getPath()
        title = component.getTitle(path=path) or path
        self.title_(title) # Search for the title in the component  tree
        self.ieExceptions()
        # self.supportMediaQueries() # Very slow, getting this from Google?
        self.setViewPort()
        self.buildFontLinks(component)
        self.buildCssLinks(component)
        self.ieExceptions()
        # Build required search engine info, if available in self.adapter
        self.buildMetaDescription(component)
        self.buildMetaKeyWords(component)
        
        self.link(rel="apple-touch-icon-precomposed", href="img/appletouchicon.png")
        self.buildJavascript(component)
        self.buildFavIconLinks(component)
        self._head()

        self.body()
        # Instead of calling the main self.block
        self.div(class_='page_' + component.name or component.class_ or self.C.CLASS_PAGE)
        self.comment(component.getClassName()) # Add reference  Python class name of this component
        if self.isEditor(): # In case we are live in /edit mode, make the whole page as form.
            self.editor(component) # Build top editor interface.

    def _page(self, component):
        u"""Build the tail of an HTML document.
        Note that the inheriting PhPBuilder uses the result of this method to generate
        the footer.php file, as a separate result stream."""
        # Instead of calling the main self._block
        if self.isEditor(): # In case we are live in /edit mode, make the whole page as form.
            self._editor(component)
        self._div(comment='.page_'+(component.name or component.class_ or self.C.CLASS_PAGE))
        self._body()
        self._html()

    def save(self, component, root=None, path=None, extension=None):
        u"""Save the file in path."""
        if path is None: # Allow full overwrite of complete path.
            path = self.getFilePath(component, root)
        dirPath = self.makeDirectory(path) # Make sure that the directory part of path exists.
        for template in component.getTemplates():
            filePath = dirPath + '/' + template.name + '.' + (extension or self.EXTENSION) # .html or .php
            template.build(self)
            self.saveAsFile(filePath, self.getResult()) # Directory already exists.
        return path
   
    def buildJavascript(self, component):
        if component.style and component.style.js:
            self.jsUrl(component.style.js)

    def buildFavIconLinks(self, component):
        u"""Build the favicon link, from the result of **component.adapter.getFavIcon()**.
        If the result is **None** then ignore."""
        data = component.adapter.getFavIcon()
        if data.url is not None:
            self.output("<link type='image/x-icon' rel='icon' href='%s'></link>" % data.url)

    def buildMetaDescription(self, component):
        u"""Build the meta tag with description of the site for search engines, if available in the adapter."""
        data = component.adapter.getDescription()
        if data.text is not None:
            self.meta(name=self.C.META_DESCRIPTION, content=data.text)
            
    def buildMetaKeyWords(self, component):
        u"""Build the meta tag with keywords of the site for search engines, if available in the adapter."""
        data = component.adapter.getKeyWords()
        if data.text is not None:
            self.meta(name=self.C.META_KEYWORDS, content=data.text)
            
    def XXXcssUrl(self, css):
        if not isinstance(css, (list, tuple)):
            css = [css]
        for url in css:
            self.link(href=url, rel="stylesheet", type="text/css")

    def jsUrl(self, js):
        u"""Alternative to jQuery: http://vanilla-js.com"""
        if not isinstance(js, (tuple, list)):
            js = [js]
        for url in js:
            self.script(type="text/javascript", src=url)

    def buildCssLinks(self, component):
        u"""
        Create the CSS links inside the head. /css-<SASS_STYLENAME> defines the type of CSS output from the Sass
        compiler. The CSS parameter must be one of ['nested', 'expanded', 'compact', 'compressed']
        """
        #urlName = component.root.urlName # Get the specific URL prefix for from root of this component.
        for cssUrl in component.css: # Should always be defined, default is an empty list
            #if not cssUrl.startswith('http://'):
            #    cssUrl = '/' + urlName + cssUrl
            self.link(href=cssUrl, type="text/css", charset="UTF-8", rel="stylesheet", media="screen")

    def buildFontLinks(self, component):
        u"""Build the webfont links of they are defined in **components.fonts**.
        Ignore if **self.C.useOnline()** is **False**."""
        if self.C.useOnline():
            for fontUrl in component.fonts: # Should always be defined, default is an empty list
                self.link(href=fontUrl, type="text/css", charset="UTF-8", rel="stylesheet", media="screen")

    def ieExceptions(self):
        self.comment("1140px Grid styles for <= IE9")
        self.newline()
        self.text("""<!--[if lte IE 9]><link rel="stylesheet" href="/cssie/ie9.css" type="text/css" media="screen" /><![endif]-->""")
        # self.text("""<link rel="stylesheet" href="cssie/ie9.css" type="text/css" media="screen,projection" />""")
        self.newline()

    def supportMediaQueries(self):
        self.comment("""Enables media queries in some unsupported browsers""")
        self.newline()
        self.script(type="text/javascript", src="http://code.google.com/p/css3-mediaqueries-js")

    def setViewPort(self):
        self.meta(name='viewport', content='width=device-width, initial-scale=1.0')

    # E D I T O R

    def isEditor(self):
        if not self.e:
            return False # Running batch mode, has no editor.
        return self.e.form[self.C.PARAM_EDIT]

    def editor(self, component):
        self.form(id='editor', method='post', action='/ajax')
        self.div(style='float:left;background-color:#D0D0D0;width:100%')
        self.input(type='hidden', name='edit', value=self.e.form[self.C.PARAM_EDIT]) # Keep edit open when in that mode.
        self.input(type='hidden', name='article', value=self.getCurrentArticleId()) # Keep edit open when in that mode.
        self.input(type='button', name='new', value='New', onclick='newArticle();')
        self.input(type='button', name='save', value='Save', onclick='saveArticle();')
        self._div()

    def _editor(self, component):
        # Add script to collect the editable texts from the html
        self._form()
        self.script()
        self.output("""
        function newArticle(){
            alert('New article');
        }
        function saveArticle(){
            alert('Save article');
            //alert(document.getElementById("article").html());
            document.getElementById("editor").submit();
        }
        function getContentEditableText(id) {
            var ce = $("<pre />").html($("#" + id).html());
            if ($.browser.webkit)
              ce.find("div").replaceWith(function() { return "\\n" + this.innerHTML; });
            if ($.browser.msie)
              ce.find("p").replaceWith(function() { return this.innerHTML + "<br>"; });
            if ($.browser.mozilla || $.browser.opera || $.browser.msie)
              ce.find("br").replaceWith("\\n");
            return ce.text();
        }
        """)
        self._script()

    # B L O C K

    def block(self, component):
        """Optional space for a component to build the opening of a block.
        This does **not** automatically build a **div</div> since that is not flexible enough.
        To be redefined by inheriting builder classed. Default behavior is to do nothing, except 
        showing the **component.selector** as comment/"""
        if component.selector:
            self.tabs()
            self.div(class_=component.class_)
            self.comment(component.selector)

    def _block(self, component):
        """Allow the component to build the closing of a block.
        This does **not** automatically build a **div</div> since that is not flexible enough.
        To be redefined by inheriting builder classed. Default behavior is to do nothing, except 
        showing the **component.selector** as comment."""
        if component.selector:
            self.tabs()
            self._div(comment=component.class_)
            self.comment('%s' % component.selector)

    def linkBlock(self, component, **kwargs):
        self.a(**kwargs)

    def _linkBlock(self, component):
        self._a()

    def text(self, componentOrText, **kwargs):
        u"""
        If in **self._svgMode** output as SVG tags. Otherwise just output if plain text string.
        If it is a components, then get it’s text string.
        """
        if componentOrText is None:
            return
        if isinstance(componentOrText, basestring):
            if self._svgMode:
                self.svgText(componentOrText, **kwargs)
            else:
                self.output(componentOrText)
        else: # Otherwise it must be of type component
            if componentOrText.id:
                self.span(id=id, contentEditable=componentOrText.editable)
            self.output(componentOrText.text)
            if componentOrText.id:
                self._span()

    def image(self, component, class_=None):
        u"""
        """
        if component.style:
            width = component.style.width_html # Take explicit HTML width/height if defined in component.
            height = component.style.height_html
        else:
            width = None
            height = None
        if height is None and width is None:
            width = '100%'
        elif height is not None:
            width = None
        alt = component.alt or TX.path2Name(component.url)
        self.img(src=component.url, width_html=width, height_html=height, alt=alt,
            class_=TX.flatten2Class(class_, component.getPrefixClass()))

    def element(self, **kwargs):
        u"""Elements are used for local CSS definitions. Ignored by HTML output."""
        pass
    
    # D R A W I N G
