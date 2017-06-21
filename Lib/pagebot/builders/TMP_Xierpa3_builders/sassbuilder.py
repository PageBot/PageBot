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
#   sassbuilder.py
#
#   Validating:
#   http://jigsaw.w3.org/css-validator/
#
import re
from xierpa3.builders.builder import Builder
from xierpa3.builders.builderparts.xmltransformerpart import XmlTransformerPart
from xierpa3.toolbox.transformer import TX 
from xierpa3.toolbox.stack import Stack
from xierpa3.descriptors.style import Media
from xierpa3.attributes import Selection, Em, Shadow, asValue, Frame, Value, Transition, Z, Url, Gradient, LinearGradient

trackAttributes = Stack() # Collect the stack of certain style attribute that are cascading for debugging.

class SassBuilder(XmlTransformerPart, Builder):
    """
    Build the SASS source for a given component.
    For automatic Sass compilation, use inheriting CssBuilder instead.

        >>> from xierpa3.components import Page, Column
        >>> from xierpa3.constants.constants import Constants as C
        >>> column = Column(writingmode=C.WM_HORIZONTALTB)
        >>> p = Page(components=column)
        >>> sb = SassBuilder()
        >>> p.build(sb)
        >>> sb.getResult()
        '\n\n/* Start page "page" */\n\n  /* End page "page" */'

    """
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Builder.C 

    # Used for dispatching component.build_sass, if components want to define builder dependent behavior.
    ID = C.TYPE_SASS
    EXTENSION = 'scss'
    ATTR_POSTFIX = 'css' # Postfix of dispatcher and attribute names above generic names.
    DEFAULT_PATH = 'css/style.css' # Default can be redefined by inheriting classes.
   
    def initialize(self):
        Builder.initialize(self)
        #self.mediaExpressions = set() # Collect the @media output expressions that we need a media run for.
        self.mediaSelectors = Stack() # Collect the hierarchy of runtime media selectors
        self.mediaSelectorResults = {} # Collect #media selector:results to skip doubles
        self.runtimeMedia = [] # Collect the @media that are collected during runtime
        self.variables = {} # Collect all selector-value combinations to output as Sass variables.
        #self.selectors = {} # Collect all value-selector combinations to combine identical values.
        self.firstSelectors = Stack() # Collect the nested selector-result to avoid multiple definitions.
        
    def theme(self, component):
        u"""Build the reset code for the default values of HTML elements.
        Called by block of **theme** component.
        Open the theme block (omitted if the style has no selector) and build the style of **component.style**."""
        self.reset() # Build the reset code for the default values of HTML elements.
        self.pushFirst() # Make level for dictionary if select-content pairs, to check on duplicates on this level.
        # If there is a base style defined for this theme, then export them before the CSS of all
        for style in component.style.styles:
            self.styleBlock(style.selector) # Build the opening of the style block if the selector is defined.
            self.buildStyle(style)
            self._styleBlock(style.selector) # Build the closing of the style block if the selector is defined.
            self.newline()
            # Export specific child components now.
        self.styleBlock(component.selector) # Build the opening of the style block if the selector is defined.

    def _theme(self, component): 
        u"""Close the theme block. Omit of **component.selector** is not defined."""
        self._styleBlock(component.selector) # Build the closing of the style block if the selector is defined.
        self.popFirst() # Reduce level for firstSelectors.
        # Finally, run through the component-styles for each of the collected media style expression.
        self.buildMedia(component)

    def page(self, component):
        u"""Mark the CSS start of the specific page *component* style. 
        Called by block of **Page** component."""
        self.newline()
        self.tabs()
        self.comment('Start page "%s"' % component.name)
        self.div(class_='page_' + component.name or component.class_ or self.C.CLASS_PAGE)
        #self.styleBlock(component.selector) # Build the opening of the style block if the selector is defined.

    def _page(self, component):
        u"""Mark the CSS end of the page *component* style."""
        self._div(comment='.page_'+(component.name or component.class_ or self.C.CLASS_PAGE))
        #self._styleBlock(component.selector) # Build the opening of the style block if the selector is defined.
        self.newline()
        self.tabs()
        self.comment('End page "%s"' % component.name)

    @classmethod
    def value2SassValue(cls, value):
        if isinstance(value, basestring) and value.startswith('http'):
            value = '"%s"' % value
        return value

    @classmethod
    def selector2Class(cls, class_):
        u"""
        Format the class to comma separated output. Takes any construction of strings and lists. class_ can be
        ['name', 'name'] or 'name name' or ['name', ('name', 'name')].
        """
        if isinstance(class_, (list, tuple)):
            class_ = cls.selector2Class(class_[-1])
        parts = class_.split(' ')
        if len(parts) > 1:
            class_ = parts[-1]
        return class_

    def getCurrentArticleId(self):
        u"""Always answer @None@, to trigger the execution of style method, built into components."""
        return None

    def getFilePath(self, component, root=None):
        u"""Answer the CSS file path of @component@."""
        return TX.asDir(root or (self.ROOT_PATH + component.__class__.__name__.lower())) + self.DEFAULT_PATH

    def save(self, component, root=None, path=None):
        u"""Export the current state of the Sass to *path*. First the set of collected variables
        and then the result it self. """
        if path is None: # Allow full overwrite of complete path.
            path = self.getFilePath(component, root)
        # Because we collected the variables during the process, 
        # we must now place them at the start of the output stream.
        content = ['/* %s SASS/CSS generated by Xierpa3 */' % component.name]
        for name, value in sorted(self.variables.items()):
            content.append('$%s: %s;\n' % (name, self.value2SassValue(value)))
        content.append(self.getResult()) 
        self.saveAsFile(path, TX.list2Lines(content), makeDir=True)
        return path

    def block(self, component):
        u"""Ignore additional classes here. They should be defined separately by the user.
        This builds the main component class name CSS.
        Test if component.BUILD_CSS is True, components may be HTML only, not showing up in the CSS.
        Make nesting of output stream, to test if a current block created content, so the headers can be skipped."""
        # print component, component.BUILD_CSS, component.isEmpty()
        if component.selector is not None:
            self.pushFirst() # Make level for dictionary if select-content pairs, to check on duplicates on this level.
            self.styleBlock(component.selector) # Open the block if there is a valid selector
        self.buildStyle(component.style)

    def _block(self, component):
        u"""Close the block if there is a valid selector in the *component*."""
        if component.selector is not None:
            self._styleBlock(component.selector)
            self.popFirst() # Reduce level for firstSelectors.

    def linkBlock(self, component, **kwargs):
        if component.BUILD_CSS:
            self.a(**kwargs)

    def _linkBlock(self, component):
        if component.BUILD_CSS:
            self._a()

    def styleBlock(self, selector):
        u"""Open the CSS with the selector. If the style does not have a selector
        then don't open the block and don't indent. This way the CSS keeps the original
        indented position. The reverse happens when closing the block."""
        if selector:
            self.tag('div', **dict(selectorpath=selector))
            
    def _styleBlock(self, selector):
        if selector:
            self._tag()
            
    def _class2ClassComment(self, class_):
        u"""Convert the class to a comment, if there is more than one class"""
        if class_ is None or not isinstance(class_, (tuple, list)):
            return None
        s = []
        for c in class_:
            s.append('.%s' % c)
        return ', '.join(s)
    
    def element(self, tag=None, **kwargs):
        u"""Element is used to define CSS values for elements that are part of an XML tree, where they
        cannot be reached for specification. Using element as pseudo tag, allows the definintion of
        styles for elements that are otherwise hidden."""
        self.tag(tag or 'div', **kwargs)
        self._tag()
        
    def tag(self, tag, **kwargs):
        u"""Used for non-component blocks. Build the *tag* with the given arguments as 
        selector and SASS source attribute values. If there is a attribute ending with "_css" then ignore
        the output of the attribute with the same name, without "_css" ending. 
        This offers the opportunity to specifically describe css attribute, preferred above the generic attribute value.
        All attributes that have the postfix of another builder are ignored. 
        Make forked nesting of output streams, to test if a current block created content, so the headers can be skipped
        if there already is an identical selector-content match inside the current block."""
        self.pushResult() # Divert the selector output, so we can see at closing if the result was empty.
        self.tabs()
        # Get the selector of the CSS. See working of the self.getSelector(...) for the order of interpretation.
        # self.getSelector(tag, id, selectorPath, selector, class_, class_postfix, pseudo):
        selector = self.getSelector(tag, kwargs.get('id'), kwargs.get('selectorPath'), kwargs.get('selector'), kwargs.get('class_'), kwargs.get('class_'+self.ATTR_POSTFIX), kwargs.get('pseudo'))
        if selector:
            self.mediaSelectors.push(selector) # Save the stack of selectors for runtime @media
            self.output('%s { ' % selector)
            self.comment(self._class2ClassComment(kwargs.get('class_')))
            self.tabIn()
        self.pushResult() # Divert the tag content output, so we can see at closing if the result was empty.
        for key, value in kwargs.items():
            # Check if the key has a companion with the same name+postfix for this builder type.
            # In that case ignore the attribute value. If the postfix is one of the other
            # builder postfixes, then also ignore. So "<key>" is compared with "<key>_css"
            # for a match to execute. Or "<key>" is compared with "<key>_html", 
            # which is the ignored here.
            keyPostfix = key.split('_')[-1]
            if not key or kwargs.has_key(key+'_'+self.ATTR_POSTFIX) or \
                (keyPostfix != self.ATTR_POSTFIX and keyPostfix in self.C.ATTR_POSTFIXES): 
                continue
            if keyPostfix == self.ATTR_POSTFIX:
                # Remove the postfix from the attribute name
                key = '_'.join(key.split('_')[:-1])
            if key == self.C.ATTR_MEDIA: # Collect the runtime Media instances as defined in the 'media' attribute.
                # Copy the current stack of selectors in combination with the @media instances.
                # Value can be a single Media instance or a list of instances.
                # When all SCSS is done, the collected @media gets built from this.
                self.runtimeMedia.append((self.mediaSelectors.getAll()[:], TX.asList(value))) 
                continue # Don't add to the current property set for output.
            # This loop can result in an empty block, e.g. if there is only a media attribute.
            self.buildHookProperties(key, value)
        self.pushFirst() # Make level for dictionary if select-content pairs, to check on duplicates on this level.

    def _tag(self, comment=None):
        u"""Closing the tag, get the selector and context of the block from the stacked result writers.
        If there is a selector and content, then check if the parent block didn't already have an identical
        combination. This e.g. happens when building from a list of data. If there already is a match
        with the selector-content combination, then ignore. If there is already a selector, but with different
        content, then export the code with a warning as comment."""
        self.popFirst() # Reduce level for firstSelectors.
        firstSelectors = self.firstSelectors.peek()
        tagContent = self.popResult()
        tagSelector = self.popResult()
        tc = tagContent.strip()
        ts = tagSelector.strip()
        # Output warning if the selector already exist, but with different content.
        # This doesn't have to be an error, it can be that there are two blocks with the same selector
        # but different content. But for clarity, it would be better to given them a different additional class
        # to make the selector different. In that case the warning will not appear.
        if ts and tc and firstSelectors is not None and firstSelectors.has_key(ts) and firstSelectors[ts] != tc:
            self.tabs()
            self.comment('@@@ Warning: redefine of existing selector')
        if ts and firstSelectors is not None:
            if tc and firstSelectors.get(ts) != tc: # firstSelectors value can be None, for first time
                self.output(tagSelector)
                self.output(tagContent)
                self.tabOut()
                self.tabs()
                self.output('} ')
                if comment is not None:
                    self.comment(comment)
            else:
                self.tabOut()
        # Pop the current stack of selectors, so the runtime @media knows that the block ended.
        self.mediaSelectors.pop()
        # Keep the latest version as first now for comparison in next iteration
        # Mark that we had this selector-content, to avoid duplicates
        if firstSelectors is not None:
            firstSelectors[ts] = tc
    
    def pushFirst(self):
        u"""Push a new empty dictionary of selectors on the firstSelectors stack.""" 
        self.firstSelectors.push({})
    
    def popFirst(self):
        u"""Pop and answer the current dictionary of selectors for this block and answer it."""
        return self.firstSelectors.pop()
            
    #  T A G S
    
    def image(self, component):
        # ???if component.BUILD_CSS:
        self.img(src=component.url, width=component.width, maxwidth=component.width, minwidth=0,
            height=component.height, alt=component.alt, class_=component.getPrefixClass())

    def comment(self, s):
        if self._verbose and s is not None:
            self.output('/* %s */' % TX.object2SpacedString(s))

    def error(self, s):
        if s is not None:
            self.comment('### %s ###' % TX.object2SpacedString(s))

    def buildStyle(self, style):
        u"""If there is *style* defined, run trough its attributes to match withs corresponding CSS methods.
        This way the CSS-related attributes are separated from the others. For this reason some the the standard
        attributes have other names, e.g. there is a **style.url** and **style.cssurl**."""
        if style is not None:
            for key, value in style.items():
                # Call the css_<key> method if it exists. This filters the CSS attributes from the HTML attributes.
                self.buildHookProperties(key, value)
                # Collect any media expression in this style for later examination
                #self.collectMediaExpressions(style)
            # Build the children styles of style
            self.buildStyles(style.styles)

    def buildStyles(self, styles):
        u"""Build each style in *styles*."""
        self.pushFirst() # Make level for dictionary if select-content pairs, to check on duplicates on this level.
        for style in styles:
            selector = style.selector
            self.styleBlock(selector)
            self.buildStyle(style)
            self._styleBlock(selector)
        self.popFirst() # Reduce level for firstSelectors.

    def buildMedia(self, component):
        u"""Here all style have been written. What remains is the to sort and output the collected @media expression
        of *component* as media queries.
        The collected **Media** instances will generate a selector that is related to
        the path of their parent styles and objects."""
        mediaExpressions = {}
        for selectors, mediaList in self.runtimeMedia:
            # Distribute the selectors+media over their own media expressions,
            # this ways collecting all media expression together.
            for media in mediaList:
                if not mediaExpressions.has_key(media.expression):
                    mediaExpressions[media.expression] = []
                mediaExpressions[media.expression].append((selectors, media))
            
        for expression, selectorMedia in sorted(mediaExpressions.items()):
            self.tabs()
            self.output('@media %s {' % expression)
            self.tabIn()
            # Build the media styles that were collected in by components
            # Skip the top levels of site and pages
            self.tabs()
            # Build the collected runtime Media of this expression
            for selectors, media in selectorMedia:
                self.buildSelectorsMedia(selectors, media)
            self.tabOut()
            self.tabs()
            self.output('}')
            self.newline()
    
    def buildSelectorsMedia(self, selectors, media):
        self.pushResult() # Save current output stream
        self.buildMediaItem(media)
        selectors = ' '.join(selectors).strip()
        result = self.popResult() # Get content of the temp output stream
        # See if there was output for this block, besides white space and not doubled:
        if self.mediaSelectorResults.get(selectors) != result and selectors and result.strip(): 
            self.tabs()
            self.output('%s {' % selectors)
            self.output(result) # There is content in the block, output it with the block header and footer.
            self.tabs()
            self.output('}')
            self.mediaSelectorResults[selectors] = result # Keep to check for doubles
            
    def buildMediaItem(self, media):
        self.tabIn()
        # Test if the block is empty, so the style block can be skipped.
        self.pushResult() # Save current output stream
        for key, value in media.items():
            # Call the css_<key> method if it exists. This filters the CSS attributes from the HTML attributes.
            self.tabIn()
            self.buildHookProperties(key, value)
            self.tabOut()
        result = self.popResult() # Get content of the temp output stream.
        if result.strip(): # See if there was output for this block, besides white space
            self.styleBlock(media.selector)
            self.output(result) # There is content in the block, output it with the block header and footer.
            self._styleBlock(media.selector)
        self.tabOut()

    def getSassVariable(self, name, value, cnt=0):
        u"""
        Build the name-value. This is done in some steps, in order to create the Sass variables. If there is already a
        name-value match in self.variables, then use that reference. If the value is a list or dict, then don't create a
        Sass variable, feed directly into the CSS hook call.
        """
        if isinstance(value, (Selection,)):
            # Select the attribute, based on parameters in the url.
            value = value.selectFromParams(self.e.form)
        elif isinstance(value, (Em,)):
            value = value.value
        #elif name == 'style':
        #    pass # Keep value as it is. Hardcoded CSS cannot be a SASS variable.
        elif name.startswith('class_'):
            pass # Keep value as it is
        elif isinstance(value, float):
            value = ('%0.2f' % value).replace('.', '_') # Keep the period visible in the name.
        # Now see if the rendered value can be translated into a Sass variable.
        if isinstance(value, (int, long, basestring)):
            valueName = name + TX.asIdentifier(value).capitalize()
            valuepx = TX.px(value) #  Add px to integer values
            if cnt > 0:
                valueName += str(cnt)
            if self.variables.get(valueName) == valuepx:
                # It exists in identical name-value match. We can reuse it as variable reference.
                value = '$' + valueName
            elif self.variables.has_key(valueName):
                # Does not exist as name-value match, but the name may exist with different value.
                # In that case construct a new name and recursively see if that one fits.
                value = self.getSassVariable(name, value, cnt + 1)
            else: # name-value does not exists yet, add it and answer untouched.
                self.variables[valueName] = valuepx
                value = '$' + valueName
        elif isinstance(value, (Z,)):
            value = value.value # @@@ TODO: put this in SASS variable too, avoid adding px
        return value

    def getSelector(self, tag, id, selectorPath, selector, class_, class_postfix, pseudo):
        u"""Build the selector for this tag, depending on the setting of id and input selector attributes.
        The order of interpretations is:
        * selectorpath
        * selector
        * "#" + id
        * class_postfix
        * class_postfix + ":" + pseudo
        * class_
        * tag
        * tag + ":" + +pseudo
        """
        result = False
        if selectorPath is not None:
            result = selectorPath
        elif selector is not None:
            result = self.selector2Class(selector)
        elif id is not None:
            result = '#' + id
        elif class_postfix is not None:
            result = '%s.%s' % (tag, self.selector2Class(class_postfix))
            if pseudo:
                result += ':'+pseudo
        elif class_ is not None:
            result = '%s.%s' % (tag, self.selector2Class(class_))
            if pseudo:
                result += ':'+pseudo
        else:
            result = tag
            if pseudo:
                result += ':'+pseudo
        return result

    def buildHookProperties(self, name, value):
        u"""Build the CSS properties, depending if the hook **'css3_'+name** method exists.
        If the value is an instance of **Media** then the attributes are generated on another
        output stream."""
        csshook = 'css3_' + name
        if isinstance(value, Media):
            pass # @@@ Fill in here output of Media (needs style parent) for a single tag media
        elif hasattr(self, csshook) and value is not None:
            sassValue = self.getSassVariable(name, value)
            self.tabs()
            getattr(self, csshook)(sassValue)

    def text(self, textComponent):
        u"""Ignore output if *textComponent* is a plain text string."""
        if textComponent is not None and not isinstance(textComponent, basestring):
            self.buildStyle(textComponent.style)
    
    # R E S O U R C E S

    def reset(self):
        u"""Resets fallback values for CSS."""
        self.output("""
/* Reset */
html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
b, u, i, center,
dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td,
article, aside, canvas, details, embed, 
figure, figcaption, footer, header, hgroup, 
menu, nav, output, ruby, section, summary,
time, mark, audio, video {
    margin: 0;
    padding: 0;
    border: 0;
    font-size: 100%;
    font: inherit;
    vertical-align: baseline;
}
article, aside, details, figcaption, figure, 
footer, header, hgroup, menu, nav, logo, section {
    display: block;
}
a { text-decoration: none;
    img {
    border: 0; }
}
table tr th, table tr, td {
    vertical-align: top; text-align: left;
}
figure {
    position: relative; }
    
/* Editable elements */
[contenteditable="true"] {padding: 10px; background: rgba(240, 240, 240, 0.9);}
[contenteditable="true"]:hover{ background: rgba(240, 240, 200, 0.9);}
 
/* Solve the difference between IE, Safari, Mozilla and Opera for 100% and auto image widths.
Make the img of class "autowidth" to get the function working.
See www.webmonkey.com/2010/02/browser-specific_css_hacks/
IE (default, as there is no clear way to determine IE now) */
img.autoWidth { width:100%; }
// Mozilla
@-moz-document url-prefix() {
    img.autoWidth { max-width: 100%; width:100%; }
}
// Webkit
@media screen and (-webkit-min-device-pixel-ratio:0) {
    img.autoWidth { max-width: 100%; width:auto; }
}
// Opera
@media all and (-webkit-min-device-pixel-ratio:10000), not all and (-webkit-min-device-pixel-ratio:0) {
    img.autoWidth { max-width: 100%; width:100%; }
}

/* CSS Enhancements for Better User Experience */
html {
    overflow-y:scroll;
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
    tap-highlight-color: rgba(0, 0, 0, 0);
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
}
/* Brakes Text for Mobile */
.page-break {
    page-break-before:always;
}
input[type=submit], label, select, .pointer {
    cursor:pointer;
}
/* Hack */
@media all and (-webkit-min-device-pixel-ratio: 1){
    selectors {
        properties: values;
    }
}
""")
        # If in documentation mode, add the CSS for the documentation page.
        # TODO: This could be generated from the documentation builder page,
        # but somehow the SASS/CSS builders don't get there.
        if self.e.form[self.C.PARAM_DOCUMENTATION]: # /documentation
            self.output("""
/* /documentation */
div.documentation {
    
    font-size: 1em;
    width:90%; 
    margin: 20px auto 20px auto;
    font-family: Verdana;
    font-size: 0.8em;
    h1 {font-size:2em; font-weight: bold; padding-top:0.5em; padding-bottom:0.5em;}
    h2 {font-size:1.5em; font-weight: bold; padding-top:0.5em; padding-bottom:0.5em;}
    table {width: 100%; font-size: 1em}
    table th {background-color: #EEE; color:#222;}
    table td {border-bottom: 1px solid #DDD;}
    table th, table td {padding-top: 4px; padding-bottom: 4px;}
    th.name, td.name {width: 20%;}
    th.value, td.value {width: 20%;}
    th.description, td.description {width: 60%;}
    strong, b {font-weight: bold;}
    code {font-family: Courier, monospace; font-size: 1.1em;}
}
""")  

    # ---------------------------------------------------------------------------------------------------------
    #    H T M L  T A G S

    def a(self, **kwargs):
        self.tag('a', **kwargs)

    def _a(self):
        self._tag()

    def br(self, **kwargs):
        self.tag('br', **kwargs)
        self._tag()

    def img(self, **kwargs):
        self.tag('img', **kwargs)
        self._tag()

    def hr(self, **kwargs):
        self.tag('hr', **kwargs)
        self._tag()

    def div(self, **kwargs):
        self.tag('div', **kwargs)

    def _div(self, comment=None):
        self._tag(comment)

    def p(self, **kwargs):
        self.tag('p', **kwargs)

    def _p(self):
        self._tag()

    def sup(self, **kwargs):
        self.tag('sup', **kwargs)
        
    def _sup(self):
        self._tag()
        
    def form(self, **kwargs):
        self.tag('form', **kwargs)

    def _form(self):
        self._tag()

    def input(self, **kwargs):
        self.tag('input', **kwargs)

    def _input(self):
        self._tag()

    def h1(self, **kwargs):
        self.tag('h1', **kwargs)

    def _h1(self):
        self._tag()

    def h2(self, **kwargs):
        self.tag('h2', **kwargs)

    def _h2(self):
        self._tag()

    def h3(self, **kwargs):
        self.tag('h3', **kwargs)

    def _h3(self):
        self._tag()

    def h4(self, **kwargs):
        self.tag('h4', **kwargs)

    def _h4(self):
        self._tag()

    def h5(self, **kwargs):
        self.tag('h5', **kwargs)

    def _h5(self):
        self._tag()

    def h6(self, **kwargs):
        self.tag('h6', **kwargs)

    def _h6(self):
        self._tag()

    def span(self, **kwargs):
        self.tag('span', **kwargs)

    def _span(self):
        self._tag()

    def b(self, **kwargs):
        self.tag('b', **kwargs)
        
    def _b(self):
        self._tag()
        
    def em(self, **kwargs):
        self.tag('em', **kwargs)
        
    def _em(self):
        self._tag()
        
    def pre(self, **kwargs):
        self.tag('pre', **kwargs)
        
    def _pre(self):
        self._tag()
        
    def nav(self, **kwargs):
        self.tag('nav', **kwargs)

    def _nav(self):
        self._tag()

    def section(self, **kwargs):
        self.tag('section', **kwargs)

    def _section(self):
        self._tag()

    def figure(self, **kwargs):
        self.tag('figure', **kwargs)

    def _figure(self):
        self._tag()

    def figcaption(self, **kwargs):
        self.tag('figcaption', **kwargs)

    def _figcaption(self):
        self._tag()

    def select(self, **kwargs):
        self.tag('select', **kwargs)

    def _select(self):
        self._tag()

    def option(self, **kwargs):
        self.tag('option', **kwargs)

    def _option(self):
        self._tag()

    def ul(self, **kwargs):
        self.tag('ul', **kwargs)

    def _ul(self):
        self._tag()

    def ol(self, **kwargs):
        self.tag('ol', **kwargs)

    def _ol(self):
        self._tag()

    def li(self, **kwargs):
        self.tag('li', **kwargs)

    def _li(self):
        self._tag()
    
    def lead(self, **kwargs):
        self.tag('lead', **kwargs)
        
    def _lead(self):
        self._tag()
        
    def blockquote(self, **kwargs):
        self.tag('blockquote', **kwargs)
        
    def _blockquote(self):
        self._tag()
        
    def nbsp(self, count):
        pass

    def textarea(self, **kwargs):
        self.tag('textarea', **kwargs)

    def _textarea(self):
        self._tag()

    def script(self, **kwargs):
        u"""Ignore all Javascript."""
        self.pushResult()
        
    def _script(self):
        self.popResult()
    
    def table(self, **kwargs):
        self.tag('table', **kwargs)
        
    def _table(self):
        self._tag('table')
        
    def tr(self, **kwargs):
        self.tag('tr', **kwargs)
        
    def _tr(self):
        self._tag('tr')
        
    def td(self, **kwargs):
        self.tag('td', **kwargs)
        
    def _td(self):
        self._tag('td')
        
    def th(self, **kwargs):
        self.tag('th', **kwargs)
        
    def _th(self):
        self._tag('th')
        
    # Ignore SVG styles
    
    def svg(self, **kwargs):
        self.pushResult()
        
    def _svg(self):
        self.popResult()
    
    def circle(self, **kwargs):
        pass
         
    # ---------------------------------------------------------------------------------------------------------
    #    C S S  M N E M O N I C S

    def XXXcss3_style(self, value):
        # Plain CSS output trough the style goes to CSS instead of directed into the HTML tag.
        assert isinstance(value, basestring)
        if not value.endswith(';'):
            value += ';'
        self.output(value)

    def css3_class_(self, value):
        pass # Class attributes are never CSS arguments

    def css3_csssrc(self, value):
        # Usage with CSS: attribute name is csssrc, to avoid confusion with HTML tag attribute.
        if isinstance(value, Url):
            value.build('src', self)
        else: # We assume here that it is an url.
            self.output("src: url(%s);" % value)

    def css3_content(self, value):
        self.output('content: "%s";' % value)

    def css3_boxshadow(self, value):
        if isinstance(value, Shadow):
            value.build('box-shadow', self)
        elif value is not None: # Otherwise single CSS line. Better use Shadow instance for browser prefix output.
            self.output('box-shadow: %s;' % value)

    def css3_textshadow(self, value):
        if isinstance(value, Shadow):
            value.build('text-shadow', self)
        elif value is not None: # Otherwise single CSS line. Better use Shadow instance for browser prefix output.
            self.output('text-shadow: %s;' % value)

    def css3_background(self, value):
        if isinstance(value, Gradient):
            value.build('background', self)
        elif value is not None:
            self.output('background: %s;' % value)

    def css3_backgroundsize(self, value):
        css = self.getCssBackgroundSizeValue(value, object="background-size")
        if css:
            self.output(css)

    def css3_backgroundattachment(self, value):
        if value:
            self.output('background-attachment: %s;' % value)

    def css3_backgroundcolor(self, value):
        if value:
            self.output('background-color: %s;' % value)

    def css3_backgroundimageurl(self, value):
        self.output("background-image: url(%s);" % value)

    def css3_backgroundimage(self, value):
        if isinstance(value, (Url, LinearGradient)):
            value.build('background-image', self)
        else: # We assume here that it is an url.
            self.css3_backgroundimageurl(value)

    def css3_backgroundposition(self, value):
        if value:
            self.output('background-position: %s;' % value)

    def css3_backgroundrepeat(self, value):
        if value:
            self.output('background-repeat: %s;' % value)

    def css3_overflow(self, value):
        self.output('overflow: %s;' % value)

    def css3_textoverflow(self, value):
        self.output('text-overflow: %s;' % value)

    def css3_opacity(self, value):
        u"""
        The ``opacity`` method answers the CSS syntax for opacity for the browsers that support the feature. 
        For now this feature is not implemented in all browsers.
        """
        css = self.getCssOpacityValue(value)
        self.output(css)

    def css3_columncount(self, value):
        self.output('-moz-column-count: %s;' % value)
        self.output('-webkit-column-count: %s;' % value)
        self.output('column-count: %s;' % value)

    def css3_columngap(self, value):
        self.output('-moz-column-gap: %s;' % value)
        self.output('-webkit-column-gap: %s;' % value)
        self.output('column-gap: %s;' % value)

    def css3_border(self, value):
        if isinstance(value, Frame): # Identical to Border class
            value = value.value
        self.output('border: %s;' % asValue(value))

    def css3_gradient(self, value):
        css = self.getCssGradientValue(value)
        self.output(css)

    def css3_borderwidth(self, value):
        self.output('border-width: %s;' % asValue(value))

    def css3_bordercollapse(self, value):
        self.output('border-collapse: %s;' % value)

    def css3_bordercolor(self, value):
        self.output('border-color: %s;' % value)

    def css3_borderspacing(self, value):
        self.output('border-spacing: %s;' % asValue(value))

    def css3_borderstyle(self, value):
        self.output('border-style: %s;' % value)

    def css3_bordertop(self, value):
        if isinstance(value, Frame): # Identical to Border class
            value = value.value
        self.output('border-top: %s;' % asValue(value))

    def css3_borderbottom(self, value):
        if isinstance(value, Frame): # Identical to Border class
            value = value.value
        self.output('border-bottom: %s;' % asValue(value))

    def css3_borderleft(self, value):
        if isinstance(value, Frame): # Identical to Border class
            value = value.value
        self.output('border-left: %s;' % asValue(value))

    def css3_borderright(self, value):
        if isinstance(value, Frame): # Identical to Border class
            value = value.value
        self.output('border-right: %s;' % asValue(value))

    def css3_borderradius(self, value):
        css = self.getCssRadiusValue(asValue(value))
        self.output(css)

    def css3_borderradiustopleft(self, value):
        css = self.getCssBorderRadiusCornerValue(asValue(value), 'top', 'left')
        self.output(css)

    def css3_borderradiustopright(self, value):
        css = self.getCssBorderRadiusCornerValue(asValue(value), 'top', 'right')
        self.output(css)

    def css3_borderradiusbottomleft(self, value):
        css = self.getCssBorderRadiusCornerValue(asValue(value), 'bottom', 'left')
        self.output(css)

    def css3_borderradiusbottomright(self, value):
        css = self.getCssBorderRadiusCornerValue(asValue(value), 'bottom', 'right')
        self.output(css)

    def css3_bottom(self, value):
        self.output('bottom: %s;' % asValue(value))

    def css3_clip(self, value):
        self.output('clip: %s;' % value)

    def css3_color(self, value):
        self.output('color: %s;' % value)

    def css3_filter(self, value):
        self.output('filter: %s;' % value)

    def css3_transition(self, value):
        if isinstance(value, Transition):
            value.build('transition', self)
        else:
            self.output('transition: %s;' % value)

    def css3_cursor(self, value):
        self.output('cursor: %s;' % value)

    def css3_display(self, value):
        self.output('display: %s;' % value)

    def css3_visibility(self, value):
        self.output('visibility: %s;' % value)

    def css3_font(self, value):
        self.output('font: %s;' % value)

    def css3_fontfamily(self, value):
        self.output('font-family: %s;' % value)

    def css3_fontsize(self, value):
        self.output('font-size: %s;' % asValue(value))

    def css3_fontstyle(self, value):
        self.output('font-style: %s;' % value)

    def css3_fontvariant(self, value):
        self.output('font-variant: %s;' % value)

    def css3_fontweight(self, value):
        self.output('font-weight: %s;' % value)

    def css3_typesmooth(self, value):
        u"""Smoothness attributes: values are one of ['none', 'antialiased', 'subpixel-antialiased']."""
        self.output(self.getCssFontSmoothValue(value))

    def css3_texttransform(self, value):
        self.output('text-transform: %s;' % value)

    def css3_height(self, value):
        self.output('height: %s;' % asValue(value))

    def css3_minheight(self, value):
        self.output('min-height: %s;' % asValue(value))

    def css3_maxheight(self, value):
        self.output('max-height: %s;' % asValue(value))

    def css3_minwidth(self, value):
        self.output('min-width: %s;' % asValue(value))

    def css3_maxwidth(self, value):
        self.output('max-width: %s;' % asValue(value))

    def css3_left(self, value):
        self.output('left: %s;' % asValue(value))

    css3_x = css3_left

    def css3_top(self, value):
        self.output('top: %s;' % asValue(value))

    css3_y = css3_top

    def css3_letterspacing(self, value):
        if isinstance(value, Value):
            value = value.value
        self.output('letter-spacing: %s;' % value)

    css3_tracking = css3_letterspacing

    def css3_lineheight(self, value):
        self.output('line-height: %s;' % asValue(value))

    css3_leading = css3_lineheight

    def css3_baselineshift(self, value):
        # This works?
        self.output('baseline-shift: %s;' % value)

    def css3_liststyle(self, value):
        self.output('list-style: %s;' % value)

    def css3_liststyletype(self, value):
        self.output('list-style-type: %s;' % value)

    def css3_liststyleposition(self, value):
        self.output('list-style-position: %s;' % value)

    def css3_liststyleimage(self, value):
        self.output("list-style-image:url(%s);" % value)

    def css3_margin(self, value):
        if isinstance(value, Frame): # Identical to Margin class
            value = value.value
        elif isinstance(value, (tuple, list)):
            t, r, b, l = value
            value = '%s %s %s %s' % (asValue(t), asValue(r), asValue(b), asValue(l))
        else:
            value = asValue(value)
        self.output('margin: %s;' % value)

    def css3_marginbottom(self, value):
        self.output('margin-bottom: %s;' % asValue(value))

    def css3_marginleft(self, value):
        self.output('margin-left: %s;' % asValue(value))

    def css3_marginright(self, value):
        self.output('margin-right: %s;' % asValue(value))

    def css3_margintop(self, value):
        self.output('margin-top: %s;' % asValue(value))

    def css3_outline(self, value):
        self.output('outline: %s;' % value)

    def css3_padding(self, value):
        if isinstance(value, Frame): # Identical to Padding class
            value = value.value
        elif isinstance(value, (tuple, list)):
            t, r, b, l = value
            value = '%s %s %s %s' % (asValue(t), asValue(r), asValue(b), asValue(l))
        else:
            value = asValue(value)
        self.output('padding: %s;' % value)

    def css3_paddingbottom(self, value):
        self.output('padding-bottom: %s;' % asValue(value))

    def css3_paddingleft(self, value):
        self.output('padding-left: %s;' % asValue(value))

    def css3_paddingright(self, value):
        self.output('padding-right: %s;' % asValue(value))

    def css3_paddingtop(self, value):
        self.output('padding-top: %s;' % asValue(value))

    def css3_position(self, value):
        self.output('position: %s;' % value)

    def css3_right(self, value):
        self.output('right: %s;' % asValue(value))

    def css3_textalign(self, value):
        self.output('text-align: %s;' % value)

    css3_align = css3_textalign

    def css3_verticalalign(self, value):
        self.output('vertical-align: %s;' % value)

    css3_valign = css3_verticalalign

    def css3_zindex(self, value):
        self.output('z-index: %s;' % value)

    css3_z = css3_zindex

    def css3_textdecoration(self, value):
        self.output('text-decoration: %s;' % value)

    def css3_textindent(self, value):
        self.output('text-indent: %s;' % asValue(value))

    def css3_width(self, value):
        self.output('width: %s;' % asValue(value))

    # def css3_id(self, value):
    #    self.output('id: %s;' % value)

    def css3_wordspacing(self, value):
        self.output('word-spacing: %s;' % value)

    def css3_wordbreak(self, value):
        self.output('word-break: %s;' % value)

    def css3_float(self, value):
        self.output('float: %s;' % value)

    def css3_clear(self, value):
        self.output('clear: %s;' % value)

    def css3_whitespace(self, value):
        self.output('white-space: %s;' % value)

    def css3_writingmode(self, value):
        u"""Supported modes for *value*: horizontal-tb, rl-tb, vertical-lr, vertical-rl,
        bt-rl, bt-lr, lr-bt, rl-bt, lr, lr-tb, rl, tb, tb-lr, tb-rl"""
        self.output('writing-mode: %s;' % value)

    # ---------------------------------------------------------------------------------------------------------
    #    B R O W S E R  D E P E N D E N C I E S

    @classmethod
    def getCssOpacityValue(cls, value, browser=None):
        u"""
        The ``cssBorderRadiusValue`` method answers browser dependent css ``border-radius`` value.
        """
        alpha = None
        if not isinstance(value, basestring):
            if value > 1:
                value /= 100.0
            alpha = int(value * 100)
        result = ['opacity: %s;' % value]
        if alpha and browser in (None, cls.BROWSER_IE):
            result.append('filter:alpha(opacity=%s);' % alpha)
        return ''.join(result)

    @classmethod
    def XXXgetCssBoxShadowValues(cls, color, x=None, y=None, blur=None, inout=None):
        outcolor = ''
        if color == 'none':
            return None, 0, 0, 0, 0
        if isinstance(color, (list, tuple)):
            if len(color) == 4:
                outcolor, x, y, blur = color
            elif len(color) == 5:
                outcolor, x, y, blur, inout = color
        else:
            try:
                preformat = re.compile('(\w?) ?(\d+)px (\d+)px (\d+)px #(.+)')
                preformatrgb = re.compile('(.*)rgba\((.+)\)(.*)')
                m = preformatrgb.match(color)
                if m:
                    outcolor = 'rgba(' + m.group(2) + ')'
                    color = color.replace(outcolor, '')
                m = preformat.match(color)
                if m:
                    inout = m.group(1) or None
                    x = int(m.group(2))
                    y = int(m.group(3))
                    blur = int(m.group(4))
                    outcolor = '#' + m.group(5)
                else:
                    vals = color.split(' ')
                    if len(vals) > 1:
                        result = []
                        for s in color.split(' '):
                            s = s.strip()
                            if s.endswith('px'):
                                result.append(int(s[:-2]))
                            elif s.startswith('#'):
                                outcolor = s
                            elif s in ('inset', 'outset'):
                                inout = s
                        x, y, blur = result
            except ValueError:
                print '### [CssCanvas.getCssBoxShadowValues] Cannot process "%s" */' % result
                return 'black', 0, 0, False, inout
        return outcolor, x, y, blur, inout

    @classmethod
    def XXXgetCssBackgroundSizeValue(cls, value, object="background-size", browser=None):
        u"""
        
        The ``getCssBackgroundSizeValue`` method answers browser dependent css ``background-size`` value.<br/>
        
        """
        result = ['%s: %s;' % (object, value)]
        if browser in (None, cls.BROWSER_SAFARI, cls.BROWSER_CHROME):
            result.append('-webkit-%s: %s;' % (object, value))
        if browser in (None, cls.BROWSER_FIREFOX):
            result.append('-moz-%s: %s;' % (object, value))
        if browser in (None, cls.BROWSER_OPERA):
            result.append('-o-%s: %s;' % (object, value))
        return ''.join(result)

    @classmethod
    def XXXgetCssBoxShadowValue(cls, color, x=None, y=None, blur=None, inout=None, browser=None, object="box"):
        u"""
        
        The ``cssBoxShadowValue`` method answers browser dependent css ``box-shadow`` value.<br/>
        Or, if ``object`` is ``text``, answers browser dependent css ``text-shadow`` value.<br/>
        The value can be a list or tuple, as in ``self.css(ids="...", boxshadow=("#888888", 6, 6, 20))``<br/>
        Or it may be separate arguments as can be used in a ``style`` attribute:<br/>
        self.div(style=self.cssBoxShadowValue("#888888", 6, 6, 20))<br/>
        self.div(style=self.cssBoxShadowValue("#888888", 6, 6, 20, "inset"))<br/>
        self.div(style=self.cssBoxShadowValue("inset 6px 6px 20px #888888")<br/>
        Omitting the optional ``browser`` attribute will result in the output for all browsers.
        
        """
        # TODO: getCssBoxShadowValue now also output the text-shadow css. We may then need a better name for the method.
        # @@ color may also be formatted value, such as '4px 4px 3px #888'
        # @@ self.css(ids="...", bowshadow='4px 4px 3px #888')
        # so we need to analyze:
        if ',' in color:
            color, x, y, blur = color.split(',')
            x = TX.asInt(x)
            y = TX.asInt(y)
            blur = TX.asInt(blur)
        color, x, y, blur, inout = cls.getCssBoxShadowValues(color, x, y, blur, inout)

        #    Css box-shadow value
        if y is None:
            y = x
        # standard format: "#888888 6px 6px 20px"
        if color is None:
            format = 'none'
        elif x is None and y is None and blur is None:
            # color is supposed to the be the formatted string already
            format = color
        else:
            format = color + ' ' + asValue(x) + ' ' + asValue(y)
            if blur:
                format = format + ' ' + asValue(blur)
            if inout:
                format = inout + ' ' + format
        result = ['%s-shadow: %s;' % (object, format)]
        if browser in (None, cls.BROWSER_IE):
            filter = "progid:DXImageTransform.Microsoft.dropShadow(color=%s,offX=%d,offY=%d,positive=true)" % (color, x, y)
            result.append("-ms-filter:'" + filter + "';")
            result.append('filter: ' + filter + ';')
        if browser in (None, cls.BROWSER_SAFARI, cls.BROWSER_CHROME):
            result.append('-webkit-%s-shadow: %s;' % (object, format))
        if browser in (None, cls.BROWSER_FIREFOX):
            result.append('-moz-%s-shadow: %s;' % (object, format))
        return ''.join(result)

    @classmethod
    def XXXgetCssGradientValue(cls, startcolor, endcolor=None, x0='left', x1='left', y0='top', y1='bottom', type='linear', browser=None):
        u"""
        
        The ``cssBoxShadowValue`` method answers browser dependent css ``gradient`` value.<br/>
        self.div(style=self.cssGradientValue({'startcolor':'#fff000','endcolor':'#999999'}))<br/>
        self.div(style=self.cssGradientValue('#fff000','#999999'))<br/>
        <br/>
        <em>Browser dependent formatting:</em><br/>
        background: -webkit-gradient(linear, left top, left bottom, from(#fff000), to(#999999));<br/>
        background: -moz-linear-gradient(top,  #fff000,  #999999);<br/>
        filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#fff000', endColorstr='#999999');<br/>
        Omitting the optional ``browser`` attribute will result in the output for all browsers.
        
        """
        args = (('x0', x0), ('x1', x1), ('y0', y0), ('y1', y1), ('type', type))
        if not startcolor:
            return ''
        elif isinstance(startcolor, dict):
            value = startcolor
            for arg, val in args:
                value[arg] = value.get(arg) or val
        else:
            value = {}
            value['endcolor'] = endcolor
            value['startcolor'] = startcolor
            for arg, val in args:
                value[arg] = val

        result = []
        if browser in (None, cls.BROWSER_IE):
            filter = "progid:DXImageTransform.Microsoft.gradient(startColorstr='%(startcolor)s', endColorstr='%(endcolor)s')" % value
            result.append('-ms-filter: "' + filter + '";')
            result.append('filter: ' + filter + ';')
        if browser in (None, cls.BROWSER_SAFARI, cls.BROWSER_CHROME):
            result.append('background: -webkit-gradient(%(type)s, %(x0)s %(y0)s, %(x1)s %(y1)s, from(%(startcolor)s), to(%(endcolor)s));' % value)
        if browser in (None, cls.BROWSER_FIREFOX):
            result.append("background: -moz-%(type)s-gradient(%(y0)s,  %(startcolor)s, %(endcolor)s);" % value)
        if browser in (None, cls.BROWSER_OPERA):
            result.append("background: -o-%(type)s-gradient(%(y0)s,  %(startcolor)s, %(endcolor)s);" % value)
        return ''.join(result)

    @classmethod
    def getCssTransformValue(cls, scale=None, skew=None, rotate=None, browser=None):
        u"""
        The ``buildCssTransformValue`` method answers browser dependent css ``border-radius`` value.
        <br/> Omitting the optional ``browser`` attribute will result in the output for all browsers.
        """
        value = []
        result = []
        if scale is not None:
            value.append('scale(%s)' % scale)
        if skew is not None:
            value.append('skew(%s)' % skew)
        if rotate is not None:
            value.append('rotate(%s)' % rotate)
        value = ' '.join(value)
        if value:
            result = cls.getCssBrowserValue(value, attribute='transform', browser=browser)
        return ''.join(result)

    @classmethod
    def getCssBrowserValue(cls, value, attribute, browser=None):
        result = ['%s: %s;' % (attribute, value)]
        if browser is None:
            for p in cls.BROWSER_CSSPREFIXES:
                result.append('%s%s: %s;' % (p, attribute, value))
        else:
            p = cls.BROWSER_CSSPREFIX.get(browser)
            result.append('%s%s: %s;' % (p, attribute, value))
        return result

    @classmethod
    def getCssBorderRadiusCornerValue(cls, value, topbottom, leftright, browser=None):
        u"""
        The ``cssBorderRadiusCornerValue`` method answers browser dependent CSS ``border-radius``
        value of a specific corner.<br/>
        Omitting the optional ``browser`` attribute will result in the output for all browsers.
        
        """
        result = ['border-%s-%s-radius: %s;' % (topbottom, leftright, value)]
        if browser in (None, cls.BROWSER_SAFARI, cls.BROWSER_CHROME):
            result.append('-webkit-border-%s-%s-radius: %s;' % (topbottom, leftright, value))
        if browser in (None, cls.BROWSER_FIREFOX):
            result.append('-moz-border-radius-%s%s: %s;' % (topbottom, leftright, value))
        return ''.join(result)

    @classmethod
    def getCssBorderRadiusValue(cls, value, browser=None):
        u"""
        The ``cssBorderRadiusValue`` method answers browser dependent CSS ``border-radius`` value.<br/>
        Omitting the optional ``browser`` attribute will result in the output for all browsers.
        
        """
        result = ['border-radius: %s;' % (value)]
        if browser in (None, cls.BROWSER_SAFARI, cls.BROWSER_CHROME):
            result.append('-webkit-border-radius: %s;' % (value))
        if browser in (None, cls.BROWSER_FIREFOX):
            result.append('-moz-border-radius: %s;' % (value))
        return ''.join(result)

    @classmethod
    def getCssFontSmoothValue(cls, value, browser=None):
        u"""
        
        The ``get`` method answers the browser dependent css for font smoothing.
        Values are one of ``['none', 'antialiased', 'subpixel-antialiased']``.
        
        """
        result = ''
        if browser in (None, cls.BROWSER_SAFARI, cls.BROWSER_CHROME):
            result = '-webkit-font-smoothing: %s;' % value
        return result


def _runDocTests():
    import xierpa3
    import doctest
    import fbits.floqmodel4.floqmodel
    return doctest.testmod(xierpa3.builders.sassbuilder)

if __name__ == '__main__':
    _runDocTests()
