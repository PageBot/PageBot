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
#     htmlbuilder.py
#
import os
import codecs
try:
    import sass
except:
    pass

from pagebot.contexts.builders.xmlbuilder import XmlBuilder
from pagebot.toolbox.dating import now
from pagebot.toolbox.color import noColor
from pagebot.toolbox.transformer import (dataAttribute2Html5Attribute,
        object2SpacedString, value2Bool)
from pagebot.toolbox.units import upt
from pagebot.fonttoolbox.objects.font import Font

class HtmlBuilder(XmlBuilder):
    """The HtmlBuilder class implements the standard XHTML tag set with all
    attributes. No additional whitespace is added.

    >>> from pagebot.toolbox.color import color
    >>> b = HtmlBuilder()
    >>> b.compact = True
    >>> b.html()
    >>> b.body()
    >>> b.addHtml('Hello world')
    >>> b.addCss('body {background-color: %s;}' % color('yellow').css)
    >>> b._body()
    >>> b._html()
    >>> b.getHtml()
    '<html xmlns="http://www.w3.org/1999/xhtml"><body>Hello world</body></html>'
    >>> ''.join(b._cssOut)
    'body {background-color: #FFFF00;}'
    """
    PB_ID = 'html' # Id to make build_html hook name. Views will be calling e.build_html()

    # Names of attributes that are written without their value.
    # Since this breaks XML validation, this list is empty by default,
    # but it can be redefined by the inheriting application class.
    SINGLE_ATTRIBUTES = []
    # Attributes that allow attributes to be tuple or list and joined
    # on tag output with separating spaces.
    CASCADING_ATTRIBUTES = ('cssClass', 'class')

    HTML_ATTRIBUTES = {'dir', 'lang', 'xmllang', 'manifest'}

    HEAD_ATTRIBUTES = {'profile'}

    LINK_ATTRIBUTES = {'charset', 'href', 'hreflang', 'media', 'rel',
        'rev', 'target', 'dir', 'lang', 'type', 'sizes' }

    BODY_ATTRIBUTES = {'dir', 'lang',
        'onload', 'onunload', 'ondblclick', 'onmousedown', 'onmouseup',
        'onmouseover', 'onmousemove', 'onmouseout', 'onkeypress', 'onkeydown',
        'onkeyup'}

    H_ATTRIBUTES = {'dir', 'lang'}

    LABEL_ATTRIBUTES = {'for'}

    BUTTON_ATTRIBUTES = INPUT_ATTRIBUTES = {
        'type', 'name', 'size', 'value', 'accept', 'autocorrect',
        'autocapitalize', 'placeholder', 'inputmode', 'relation', 'checked',
        'src', 'alt', 'readonly', 'tabindex', 'accesskey', 'onfocus', 'onblur',
        'onselect', 'onchange', 'ondblclick', 'onmousedown', 'onmouseup',
        'onmouseover', 'onmousemove', 'onmouseout', 'onkeypress', 'onkeydown',
        'onkeyup', 'maxlength', 'disabled', 'autocorrect', 'autocapitalize',
        'placeholder', 'results',
    }

    BLOCKQUOTE_ATTRIBUTES = {}

    INPUT_ATTRIBUTES_DEFAULTS = {'alt': '+', 'disabled': False}

    CANVAS_ATTRIBUTES = {'width_html', 'height_html'}

    SELECT_ATTRIBUTES = {'name', 'onchange', 'multiple',
        'size', 'disabled'}

    OPTION_ATTRIBUTES = {'value', 'selected', 'onmouseup'}

    OPTGROUP_ATTRIBUTES = {'label'}

    TEXTAREA_ATTRIBUTES = {'onblur', 'onchange',
        'ondblclick', 'onfocus', 'onselect', 'onmousedown', 'onmouseout',
        'onmousemove', 'onmouseover', 'onmouseup', 'onkeydown', 'onkeypress',
        'onkeyup', 'name', 'cols', 'rows'}

    PARAM_ATTRIBUTES = {'name', 'type', 'value', 'valuetype'}

    OBJECT_ATTRIBUTES = {'dir', 'lang', 'xmllang',
        'align', 'archive', 'border', 'classid', 'codebase', 'codetype',
        'data', 'declare', 'height_html', 'hspace', 'name', 'standby', 'type',
        'usemap', 'vspace', 'width_html', 'accesskey', 'tabindex',
        'ondblclick', 'onmousedown', 'onmouseup', 'onmouseover', 'onmousemove',
        'onmouseout', 'onkeypress', 'onkeydown', 'onkeyup'}

    META_ATTRIBUTES = {'charset', 'content', 'httpequiv', 'name'}

    P_ATTRIBUTES = STRONG_ATTRIBUTES = EM_ATTRIBUTES = B_ATTRIBUTES = U_ATTRIBUTES = S_ATTRIBUTES = Q_ATTRIBUTES = {
        'type', 'itemid', 'itemprop', 'itemref', 'itemscope', 'itemtype'}

    H1_ATTRIBUTES = H2_ATTRIBUTES = H3_ATTRIBUTES = H4_ATTRIBUTES = H5_ATTRIBUTES = H6_ATTRIBUTES = {
        'itemid', 'itemprop', 'itemref', 'itemscope', 'itemtype', 'onclick'}

    FIGURE_ATTRIBUTES = {'accesskey', 'contenteditable', 'contextmenu', 'dir',
        'draggable', 'hidden', 'lang', 'spellcheck', 'tabindex'}

    SUB_ATTRIBUTES = SUP_ATTRIBUTES = {}

    BR_ATTRIBUTES = {'cssClass', 'cssId', 'title', 'style', 'clear' }

    TABLE_ATTRIBUTES = {
        'align', 'bgcolor', 'border', 'cellpadding', 'cellspacing',
        'width_html', 'height_html'}

    THEAD_ATTRIBUTES = TFOOT_ATTRIBUTES = {
        'dir', 'lang', 'xmllang', 'align', 'char', 'charoff', 'valign',
        'ondblclick', 'onmousedown', 'onmousemove', 'onmouseout',
        'onmouseover', 'onmouseup', 'onkeydown', 'onkeypress', 'onkeyup'}

    TBODY_ATTRIBUTES = {
        'dir', 'lang',
        'xmllang', 'align', 'char', 'charoff', 'valign', 'ondblclick', 'onmousedown',
        'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onmousedown',
        'onkeydown', 'onkeypress', 'onkeyup'}

    TR_ATTRIBUTES = {
        'relation', 'onmousemove', 'onmouseout', 'onmouseover',
        'onmouseup', 'onmousedown', 'onkeydown', 'onkeypress', 'onkeyup'}

    TD_ATTRIBUTES = {'width_html', 'height_html', 'rowspan',
        'colspan', 'valign', 'align', 'nowrap', 'relation', 'ondblclick',
        'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onmousedown',
        'onkeydown', 'onkeypress', 'onkeyup'}

    TH_ATTRIBUTES = {'width_html', 'height_html', 'rowspan', 'colspan',
        'valign', 'align', 'nowrap'}

    UL_ATTRIBUTES = DL_ATTRIBUTES = {'type'}

    OL_ATTRIBUTES = {'compact', 'start', 'type'}

    I_ATTRIBUTES = TT_ATTRIBUTES = SMALL_ATTRIBUTES = BIG_ATTRIBUTES = LI_ATTRIBUTES = DT_ATTRIBUTES = DD_ATTRIBUTES = {
        'dir', 'lang', 'xmllang', 'script', 'ondblclick',
        'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onmousedown',
        'onkeydown', 'onkeypress', 'onkeyup'}

    DIV_ATTRIBUTES = {
        'onmouseout', 'relation', 'name', 'disabled', 'onmouseover', 'onclick',
        'onmousedown', 'onmouseup', 'ondblclick', 'onfocus', 'onblur',
        'itemid', 'itemprop', 'itemref', 'itemscope', 'itemtype', 'role',
        'default', 'width_html', 'contenteditable'}

    IMG_ATTRIBUTES = {
        'src', 'name', 'width_html', 'height_html', 'onmouseover',
        'onmousedown', 'onmouseup', 'onmouseout', 'alt', 'border', 'hspace',
        'vspace', 'align', 'relation', 'usemap', 'itemid', 'itemprop',
        'itemref', 'itemscope', 'itemtype'}

    # IMG_ATTRIBUTES_DEFAULTS = {'alt': '_'}

    AREA_ATTRIBUTES = {
        'shape', 'coords', 'href', 'target', 'border', 'onmouseover',
        'onmouseout', 'onmousedown', "onmouseup"}

    SPAN_ATTRIBUTES = {'relation', 'itemprop', 'onmouseover', 'onmouseout',
            'onmousedown', 'onmouseup', 'contenteditable'}

    FRAMESET_ATTRIBUTES = {'cols', 'rows', 'onload', 'onunload'}

    FRAME_ATTRIBUTES = {
        'frameborder', 'longdesc', 'marginheight', 'marginwidth',
        'name', 'noresize', 'scrolling', 'src'
        }

    NOFRAMES_ATTRIBUTES = {'dir', 'lang'}

    IFRAME_ATTRIBUTES = {
        'src', 'align', 'frameborder', 'longdesc', 'type', 'border',
        'marginheight', 'marginwidth', 'name', 'scrolling',
        'width_html', 'height_html'}

    AREA_ATTRIBUTES_DEFAULTS = {'width_html': 600, 'height_html': 400}

    HR_ATTRIBUTES = {'align', 'color', 'noshade',
            'size', 'width_html' }

    HGROUP_ATTRIBUTES = {'itemscope'}

    ARTICLE_ATTRIBUTES = {
        'itemid', 'itemprop', 'itemref', 'itemscope', 'itemtype'}

    SECTION_ATTRIBUTES = {
        'itemid', 'itemprop', 'itemref', 'itemscope', 'itemtype'}

    HEADER_ATTRIBUTES = {'cite'}

    EMBED_ATTRIBUTES = {
        'src', 'href', 'quality', 'name', 'menu', 'type', 'width_html',
        'wmode', 'align', 'allowscriptaccess', 'height_html', 'autoplay',
        'loop', 'controller', 'playeveryframe', 'bgcolor', 'movieid',
        'kioskmode', 'targetcache', 'hidden', 'volume', 'pluginspace', 'scale',
        'allowfullscreen', 'flashvars'}

    A_ATTRIBUTES = {'href', 'target', 'alt', 'name', 'itemprop', 'onmouseout',
            'onmouseover', 'onmousedown', 'onmouseup', 'ondblclick', 'onfocus',
            'accesskey', 'rel', 'rev', 'relation', 'type'}

    # A_ATTRIBUTES_DEFAULTS = {'alt': '='}
    NAV_ATTRIBUTES = {'accesskey', 'role'}

    SVG_ATTRIBUTES = {'width', 'height'}

    BOOLEAN_ATTRIBUTES = {'checked': 'checked', 'selected': 'selected', 'disabled': 'disabled'}

    USE_JQUERY = True
    #USE_VANILLAJS = True

    SECTION_CSS_W = 50
    SECTION_CSS = '/*\n' + '-'*SECTION_CSS_W + '\n\t%s\n'+ '.'*SECTION_CSS_W + '\n*/\n'

    # Standard CSS code to reset browser specific presets.
    # http://meyerweb.com/eric/tools/css/reset/
    RESET_CSS = (SECTION_CSS % """http://meyerweb.com/eric/tools/css/reset/
    v2.0 | 20110126
    License: none (public domain)""") + """html, body, div, span, applet, object, iframe,
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
/* HTML5 display-role reset for older browsers */
article, aside, details, figcaption, figure, footer, header, hgroup, menu, nav, section {
    display: block;
}
body {
    line-height: 1;
}
ol, ul {
    list-style: none;
}
blockquote, q {
    quotes: none;
}
blockquote:before, blockquote:after, q:before, q:after {
    content: '';
    content: none;
}
table {
    border-collapse: collapse;
    border-spacing: 0;
}
"""

    def __init__(self):
        self.clearHtml() # Initialize the HTML output stream.
        self._cssOut = [] # Keep the collected CSS and JS from elements here.
        self._scssVariables = {}
        self.clearJs() # Keep optional js chunck names, so avoid double output.
        self._copyPaths = []
        self._initialize()

    def get_attribute_exceptions(self, key, value):
        """
        The get_attribute_exceptions method writes the attribute and checks on naming differences between
        the element attributes and HTML attributes.
        """
        # Boolean attributes.
        key = dataAttribute2Html5Attribute(key)

        if key in self.BOOLEAN_ATTRIBUTES:
            if value2Bool(value): # Can be boolean or text boolean
                self.write_attribute(key, self.BOOLEAN_ATTRIBUTES[key])
        else:
            # Some exceptions.
            if key.startswith('html'):
                key = key[3:]
            if key == 'cssClass':
                key = 'class'
            if key == 'cssId':
                key = 'id'
            # elif key == 'src':
            #    value = self.e.getPath(value)
            elif key == 'rowspan':
                if int(value) <= 1:
                    return
            elif key == 'colspan':
                if int(value) <= 1:
                    return
            elif key == 'xmllang':
                key = 'xml:lang'
            elif key == 'httpequiv':
                key = 'http-equiv'
            elif key == 'usemap':
                if not value.startswith(u'#'):
                    value = '#' + value
            elif key == 'style': # In case CSS-style attribute, try to translate.
                if isinstance(value, dict):
                    value = str(value) # @@@@ TODO: needs more translations
                elif not isinstance(value, str):
                    value = str(value)

            # Handle Angular.org attributes that contain underscores, translate them to hyphens
            elif key.startswith('ng_'):
                key = key.replace('_', '-')

            self.write_attribute(key, value)

    #   Compatible component support

    def textBox(self, bs, box, align=None):
        """Just add the text, ignore position for now."""
        self.div()
        self.addHtml(str(bs))
        self._div()

    text = textBox

    #   J S

    def clearJs(self):
        """Clearing the JS-output storage in the page. Should be called for every page
        when exporting a site, or else the JS will cumulate from precious pages.
        """
        self._jsOut = []
        self._jsNames = set() # Keep optional js chunck names, so avoid double output.

    def addJs(self, js, name=None):
        """Add js to output, if name is None or optional name is not already in self._jsNames.
        Otherwise skip export, to avoid JS chunks to double in the output. This is used
        to avoid doubling JS chunks if multiple elements of the same type are in one page."""
        assert isinstance(js, str), ('Added Javascript should be of type str "%s"' % js)
        if name is None or not name in self._jsNames:
            self._jsOut.append(js)
        if name is not None:
            self._jsNames.add(name)

    def hasJs(self):
        return len(self._jsOut)

    def importJs(self, path):
        """Import a chunk of UTF-8 CSS code from the path."""
        if os.path.exists(path):
            f = codecs.open(path, 'r', 'utf-8')
            self.addJs(f.read())
            f.close()
        else:
            self.comment('Cannot find JS file "%s"' % path)

    def copyPath(self, path):
        """Collect path of files to copy to the output website."""
        self._copyPaths.append(path)

    def getJs(self):
        """Answers the flat string of JS."""
        return ''.join(self._jsOut)

    def writeJs(self, path):
        """Write the collected set of css JS to path."""
        try:
            f = codecs.open(path, 'w', 'utf-8')
            f.write(self.getJs())
            f.close()
        except IOError:
            print('[%s.writeJs] Cannot write JS file "%s"' % (self.__class__.__name__, path))

    #   C S S

    def addCss(self, css):
        """Add the css chunk to self.css, the ordered list of css for output.
        Don't write if empty or None."""
        if css:
            assert isinstance(css, str), ('Added CSS should be of type str "%s"' % css)
            self._cssOut.append(css)

    def getCss(self):
        """Answers the joined content of sel._cssOut."""
        return ''.join(self._cssOut)

    def hasCss(self):
        """Answers if there is any accumulated CSS in self._cssOut."""
        return len(self._cssOut)

    def importCss(self, path):
        """Import a chunk of UTF-8 CSS code from the path."""
        if os.path.exists(path):
            f = codecs.open(path, 'r', 'utf-8')
            self.addCss(f.read())
            f.close()
        else:
            self.comment('Cannot find CSS file "%s"' % path)

    def writeCss(self, path, css=None):
        """Write the collected set of CSS chunks to path."""
        try:
            if css is None:
                css = self.getCss()
            f = codecs.open(path, 'w', 'utf-8')
            f.write(css)
            f.close()
        except IOError:
            print('[HtmlBuilder.writeCss] Cannot write CSS file "%s"' % path)

    def headerCss(self, name):
        """Add the CSS code to the header of the output page.

        >>> b = HtmlBuilder()
        >>> b.headerCss('NameOfCss')
        >>> 'Generated by PageBot' in ''.join(b._cssOut)
        True
        """
        self.addCss(self.SECTION_CSS % ('CSS of "%s"\n\n\tGenerated by PageBot\n\tCreated %s' % (name, now())))

    def resetCss(self):
        """Export the CSS to reset specific default behavior of browsers."""
        self.addCss(self.RESET_CSS)

    def sectionCss(self, title):
        """Add named section marker in CSS output.
        TODO: Make optional if compact CSS is needed."""
        self.addCss(self.SECTION_CSS % title)

    #   S A S S

    def writeScss(self, path):
        """Write the collect set of SCSS variables to path."""
        try:
            #print('Writing "%s"' % path)
            f = codecs.open(path, 'w', 'utf-8')
            for scssId, value in sorted(self._scssVariables.items()):
                f.write('$%s: %s;\n' % (scssId, value))
            f.close()
        except IOError:
            print('[HtmlBuilder.writeSass] Cannot write SCSS file "%s"' % path)

    def compileScss(self, scssPath, cssPath=None, compressed=True):
        u"""For now using sass to support SCSS. SASS support could be added later."""
        if cssPath is None:
            cssPath = scssPath.replace('.scss', '.css')
        css = sass.compile(filename=scssPath)#, output_style={True:sass.SASS_STYLE_COMPRESSED}.get(compressed))
        f = codecs.open(cssPath, 'w', 'utf-8')
        f.write(css)
        f.close()

    def build_scss(self, e, view):
        scss = self._scssVariables
        if e.cssId: # If the #id is defined, then use that as CSS reference.
            scssId = e.cssId
        elif e.cssClass: # Otherwise for now, we only can generate CSS if the element has a class name defined.
            scssId = e.__class__.__name__ + '-' + e.cssClass.replace(' ','_')
        else:
            scssId = e.__class__.__name__
        if upt(e.ml):
            scss[scssId+'-margin-left'] = e.ml
        if upt(e.mt):
            scss[scssId+'-margin-top'] = e.mt
        if upt(e.mb):
            scss[scssId+'-margin-bottom'] = e.mb
        if upt(e.mr):
            scss[scssId+'-margin-right'] = e.mr
        if upt(e.pl):
            scss[scssId+'-padding-left'] = e.ml
        if upt(e.pt):
            scss[scssId+'-padding-top'] = e.pt
        if upt(e.pb):
            scss[scssId+'-padding-bottom'] = e.pb
        if upt(e.pr):
            scss[scssId+'-padding-right'] = e.pr
        if e.css('font') is not None:
            if os.path.exists(e.css('font')):
                font = Font(e.css('font'))
                scss[scssId+'-font-family'] = '"%s"' % font.info.fullName
            else:
                font = e.css('font')
        if e.css('fontSize') is not None:
            scss[scssId+'-font-size'] = e.css('fontSize')
        if e.css('fontStyle') is not None:
            scss[scssId+'-font-style'] = e.css('fontStyle')
        if e.css('fontWeight') is not None:
            scss[scssId+'-font-weight'] = e.css('fontWeight')
        if e.css('tracking') is not None:
            scss[scssId+'-letter-spacing'] = e.css('tracking')
        if e.css('fill') not in (noColor, None): # Must Color instance
            scss[scssId+'-background-color'] = e.css('fill').css
        if e.css('textFill') not in (noColor, None): # Must be Color instance
            scss[scssId+'-color'] = e.css('textFill').css

    def build_css(self, scss, selector=None, e=None, message=None):
        """Build the CSS output for the defined selector and style."""
        css = ''
        attributes = []
        if e:
            style = e.style
            if upt(e.ml):
                attributes.append('margin-left: %s;' % e.ml)
            if upt(e.mt):
                attributes.append('margin-top: %s;' % e.mt)
            if upt(e.mb):
                attributes.append('margin-bottom: %s;' % e.mb)
            if upt(e.mr):
                attributes.append('margin-right: %s;' % e.mr)
            if upt(e.pl):
                attributes.append('padding-left: %s;' % e.pl)
            if upt(e.pt):
                attributes.append('padding-top: %s;' % e.pt)
            if upt(e.pb):
                attributes.append('padding-bottom: %s;' % e.pb)
            if upt(e.pr):
                attributes.append('padding-right: %s;' % e.pr)
            if style.get('font') is not None:
                attributes.append('font-family: "%s";' % style['font'])
            if style.get('fontSize') is not None:
                attributes.append('font-size: %s;' % style['fontSize'])
            if style.get('fontStyle') is not None:
                attributes.append('font-style: %s;' % style['fontStyle'])
            if style.get('fontWeight') is not None:
                attributes.append('font-weight: %s;' % style['fontWeight'])
            if style.get('tracking') is not None:
                attributes.append('letter-spacing: %s;' % style['tracking'])
            if style.get('fill') not in (noColor, None): # Must Color instance
                attributes.append('background-color: %s;' % style['fill'].css)
            if style.get('textFill') not in (noColor, None): # Must be Color instance
                attributes.append('color: %s;' % style['textFill'].css)
            value = style.get('transition')
            if value is not None:
                attributes.append('transition=%s;' % value)
                attributes.append('-webkit-transition=%s;' % value)
                attributes.append('-moz-transition=%s;' % value)
                attributes.append('-o-transition=%s;' % value)

        if selector is not None and attributes:
            css += '%s {\n\t%s} ' % (selector, '\n\t'.join(attributes))
        if message is not None:
            css += '/* %s */' % message
        css += '\n'
        self.addCss(css)

        b = HtmlBuilder()
        # Write all collected cSS vatiables into one file
        b.writeScss(self.DEFAULT_CSS_PATH)


    #   H T M L

    def addHtml(self, html):
        """Add the HTML chunk to self.html, the ordered list of HTML for
        output. Test if the html is a plain string or of type
        HtmlString(BabelString). Otherwise raise an error, because we don't
        want to support BabelString conversion. They should have been created
        of the right type in the context from the start."""

        #if not isinstance(html, str): # It's something else, test on the kind of BabelString.
        #    assert isinstance(html, HtmlString)
        try:
            assert isinstance(html.s, str)
            html = html.s # Get the collected html from the BabelString.
        except AttributeError:

            html = str(html) # Make sure it is a string
        self._htmlOut.append(html)

    write = addHtml

    def importHtml(self, path):
        """Import a chunk of UTF-8 HTML code from the path."""
        if os.path.exists(path):
            f = codecs.open(path, 'r', 'utf-8')
            self.addHtml(f.read())
            f.close()
        else:
            self.comment('Cannot find HTML file "%s"' % path)

    def writeHtml(self, path):
        """Write the collected set of html chunks to path."""
        try:
            f = codecs.open(path, 'w', 'utf-8')
            f.write(self.getHtml())
            f.close()
        except IOError:
            print('### Cannot write HTML file "%s"' % path)

    def getHtml(self):
        """Answers the accumulated HTML as single string."""
        return ''.join(self._htmlOut)

    def clearHtml(self):
        """Clear the output stream, as should be done after each page export.
        This is likely to be done by Page elements, starting to render a new page.
        The content of previous pages then should be cleared."""
        self._htmlOut = []

    def clearCss(self):
        """
        We can safely clear the CSS, because the local CSS is not intended to
        collect all for the entire site. THis is just for local additions in the
        page. This is likely to be done by Page elements, starting to render a new page.
        The content of previous pages then should be cleared."""
        self._cssOut = []

    def docType(self, s=None):
        self.write('<!DOCTYPE %s>\n' % (s or 'html'))

    def html(self, xmlns=None, **args):
        """
        <www href="http://www.w3schools.com/tags/tag_html.asp" target="external"/>
        self.html(xmlns="http://www.w3.org/1999/xhtml", dir=ltr, lang=no, xmllang=no)
            ...
        self._html()
        Default value for xmlns is "http://www.w3.org/1999/xhtml".

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.html()
        >>> b._html()
        >>> b.getHtml()
        '<html xmlns="http://www.w3.org/1999/xhtml"></html>'
        """
        self.write('<html xmlns="%s"' % (xmlns or 'http://www.w3.org/1999/xhtml'))
        self.getandwrite_attributes('html', args)
        self.write('>')
        self.tabIn()
        # Push as last, so we can see the current tag on the stack
        self._pushTag('html')

    def _html(self):
        self._closeTag('html')

    def head(self, **args):
        """The head element can contain information about the document. The
        browser does not display the "head information" to the user. The
        following tags can be in the head section: base, link, meta, script,
        style and title.
        <www href="http://www.w3schools.com/tags/tag_head.asp" target="external"/>
        self.head()
            ...
        self._head()
        """
        self.tabs()
        self.write('<head')
        self.getandwrite_attributes('head', args)
        self.write('>')
        # Push as last, so we can see the current tag on the stack
        self._pushTag('head')

    def _head(self):
        self._closeTag('head')

    def title(self):
        """This tag defines the title of the document.

        <www href="http://www.w3schools.com/tags/tag_title.asp" target="external"/>
        self.title()
            ...
        self._title()

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.html()
        >>> b.head()
        >>> b.title()
        >>> b.addHtml('Title of the page')
        >>> b._title()
        >>> b._head()
        >>> b._html()
        >>> b.getHtml().startswith('<html')
        True
        """
        self.tabs()
        self.tabIn()
        self.write_tag('link', True, {})

    def _title(self):
        self._closeTag('title')

    def title_(self, s):
        """Write the stripped string s as <title>...</title> tag.

        >>> b = HtmlBuilder()
        >>> b.title_('This is a title')
        >>> b.getHtml().strip()
        '<title>This is a title</title>'
        """
        self.tabs()
        self.tabIn()
        self.write('<title>%s</title>' % s.strip())

    def link(self, **args):
        """The link tag defines the relationship between two linked documents.

        <www href="http://www.w3schools.com/tags/tag_link.asp" target="external"/>
        self.head()
            ...
            self.link(href='/_images/favicon.ico', rel='shortcut icon')
            ...
        self._head()
        """
        self.write_tag('link', False, args)
        self.newLine() # Optional newline is self.compact is False.


    def body(self, **args):
        """The body element defines the documents' body. It contains all the
        contents of the document (like text, images, colors, graphics, etc.).

        <www href="http://www.w3schools.com/tags/tag_body.asp" target="external"/>
        self.body(onload='javascript:loadpage()')
            ...
        self._body()
        """
        self.write_tag('body', True, args)

    def _body(self):
        self._closeTag('body')


    def h1(self, **args):
        """
        The h1 to h6 tags define headers. h1 defines the largest header. h6
        defines the smallest header.
        <www href="http://www.w3schools.com/tags/tag_hn.asp" target="external"/>
        self.h1(cssClass='chapter')
            ...
        self._h1()

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.h1()
        >>> b.addHtml('Hello world')
        >>> b._h1()
        >>> b.getHtml()
        '<h1>Hello world</h1>'
        """
        self.write_tag_noWhitespace('h1', True, args)

    def _h1(self):
        self._closeTag_noWhitespace('h1')
        self.newLine() # Optional newline is self.compact is False.

    def h1_(self, s, **args):
        """The h1_ to h6_ tags define headers, combining the opening and
        closing tag where the s attribute is the block content.

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.h1_('Hello world')
        >>> b.getHtml()
        '<h1>Hello world</h1>'
        """
        self.h1(**args)
        self.addHtml(s)
        self._h1()

    def h2(self, **args):
        """The h1 to h6 tags define headers.
        h1 defines the largest header. h6 defines the smallest header.
        <www href="http://www.w3schools.com/tags/tag_hn.asp" target="external"/>
        self.h2(cssClass='head')
            ...
        self._h2()

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.h2()
        >>> b.addHtml('Hello world')
        >>> b._h2()
        >>> b.getHtml()
        '<h2>Hello world</h2>'
        """
        self.write_tag_noWhitespace('h2', True, args)

    def _h2(self):
        self._closeTag_noWhitespace('h2')
        self.newLine() # Optional newline is self.compact is False.

    def h2_(self, s, **args):
        """
        The h1_ to h6_ tags define headers, combining the opening and closing tag
        where the s attribute is the block content.

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.h2_('Hello world')
        >>> b.getHtml()
        '<h2>Hello world</h2>'
        """
        self.h2(**args)
        self.addHtml(s)
        self._h2()

    def h3(self, **args):
        """
        The h1 to h6 tags define headers.
        h1 defines the largest header. h6 defines the smallest header.
        <www href="http://www.w3schools.com/tags/tag_hn.asp" target="external"/>
        self.h3(cssClass='subhead')
            ...
        self._h3()

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.h3()
        >>> b.addHtml('Hello world')
        >>> b._h3()
        >>> b.getHtml()
        '<h3>Hello world</h3>'
        """
        self.write_tag_noWhitespace('h3', True, args)

    def _h3(self):
        self._closeTag_noWhitespace('h3')
        self.newLine() # Optional newline is self.compact is False.

    def h3_(self, s, **args):
        """
        The h1_ to h6_ tags define headers, combining the opening and closing tag
        where the s attribute is the block content.

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.h3_('Hello world')
        >>> b.getHtml()
        '<h3>Hello world</h3>'
        """
        self.h3(**args)
        self.addHtml(s)
        self._h3()

    def h4(self, **args):
        """
        The h1 to h6 tags define headers.
        h1 defines the largest header. h6 defines the smallest header.
        <www href="http://www.w3schools.com/tags/tag_hn.asp" target="external"/>
        self.h4(cssClass='subsubhead')
            ...
        self._h4()

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.h4()
        >>> b.addHtml('Hello world')
        >>> b._h4()
        >>> b.getHtml()
        '<h4>Hello world</h4>'
        """
        self.write_tag_noWhitespace('h4', True, args)

    def _h4(self):
        """Closing tag of h4."""
        self._closeTag_noWhitespace('h4')
        self.newLine() # Optional newline is self.compact is False.

    def h4_(self, s, **args):
        """
        The h1_ to h6_ tags define headers, combining the opening and closing tag
        where the s attribute is the block content.

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.h4_('Hello world')
        >>> b.getHtml()
        '<h4>Hello world</h4>'
        """
        self.h4(**args)
        self.addHtml(s)
        self._h4()

    def h5(self, **args):
        """
        The h1 to h6 tags define headers.
        h1 defines the largest header. h6 defines the smallest header.
         <www href="http://www.w3schools.com/tags/tag_hn.asp" target="external"/>
        self.h5(cssClass='caption')
            ...
        self._h5()

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.h5()
        >>> b.addHtml('Hello world')
        >>> b._h5()
        >>> b.getHtml()
        '<h5>Hello world</h5>'
        """
        self.write_tag_noWhitespace('h5', True, args)

    def _h5(self):
        self._closeTag_noWhitespace('h5')

    def h5_(self, s, **args):
        """
        The h1_ to h6_ tags define headers, combining the opening and closing tag
        where the s attribute is the block content.

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.h5_('Hello world')
        >>> b.getHtml()
        '<h5>Hello world</h5>'
        """
        self.h5(**args)
        self.addHtml(s)
        self._h5()

    def h6(self, **args):
        """
        The h1 to h6 tags define headers.
        h1 defines the largest header. h6 defines the smallest header.
        <www href="http://www.w3schools.com/tags/tag_hn.asp" target="external"/>
        self.h6(cssClass='footnote')
            ...
        self._h6()

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.h6()
        >>> b.addHtml('Hello world')
        >>> b._h6()
        >>> b.getHtml()
        '<h6>Hello world</h6>'
        """
        self.write_tag_noWhitespace('h6', True, args)

    def _h6(self):
        self._closeTag_noWhitespace('h6')

    def h6_(self, s, **args):
        """
        The h1_ to h6_ tags define headers, combining the opening and closing tag
        where the s attribute is the block content.

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.h6_('Hello world')
        >>> b.getHtml()
        '<h6>Hello world</h6>'
        """
        self.h6(**args)
        self.addHtml(s)
        self._h6()

    def figure(self, **args):
        """The figure method (HTML5) is used for annotating illustrations,
        diagrams, photos, code listings, etc. You can use the tag to associate
        a caption together with some embedded content, such as a graphic or
        video.  You can use the tag in conjunction with the
        <tag>figcaption</tag> element to provide a caption for the contents of
        your <tag>figure</tag> element.

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.figure()
        >>> b.addHtml('Hello world')
        >>> b._figure()
        >>> b.getHtml()
        '<figure>Hello world</figure>'
        """
        self.write_tag('figure', True, args)

    def _figure(self):
        self._closeTag('figure')

    def figcaption(self, **args):
        """The figure method (HTML5) is used for annotating illustrations,
        diagrams, photos, code listings, etc. You can use the tag to associate
        a caption together with some embedded content, such as a graphic or
        video.  You can use the tag in conjunction with the
        <tag>figcaption</tag> element to provide a caption for the contents of
        your <tag>figure</tag> element.

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.figure()
        >>> b.figcaption()
        >>> b.addHtml('Hello world')
        >>> b._figcaption()
        >>> b._figure()
        >>> b.getHtml()
        '<figure><figcaption>Hello world</figcaption></figure>'
        """
        self.write_tag('figcaption', True, args)

    def _figcaption(self):
        self._closeTag('figcaption')

    def hgroup(self, **args):
        """
        The hgroup method (HTML5) defines the heading of a section or a document.
        The hgroup element is used to group headers, <tag>h1</tag> to <tag>h6</tag>, where the largest
        is the main heading of the section, and the others are sub-headings.

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.hgroup()
        >>> b.addHtml('Hello world')
        >>> b._hgroup()
        >>> b.getHtml()
        '<hgroup>Hello world</hgroup>'
        """
        self.write_tag('hgroup', True, args)

    def _hgroup(self):
        self._closeTag('hgroup')

    def article(self, **args):
        """The article method (HTML5) defines external content. The external
        content could be a news-article from an external provider, or a text
        from a web log (blog), or a text from a forum, or any other content
        from an external source."""
        self.write_tag('article', True, args)

    def _article(self):
        self._closeTag('article')

    def header(self, **args):
        """The header method (HTML5) defines an introduction to the document.
        """
        self.write_tag('header', True, args)

    def _header(self):
        self._closeTag('header')

    def footer(self, **args):
        """The footer method (HTML5) defines a footer to the document.
        """
        self.write_tag('footer', True, args)

    def _footer(self):
        self._closeTag('footer')

    def section(self, **args):
        """The section method (HTML5) defines defines sections in a document.
        Such as chapters, headers, footers, or any other sections of the
        document."""
        self.write_tag('section', True, args)

    def _section(self):
        self._closeTag('section')

    def pre(self, **args):
        """The pre element defines preformatted text. The text enclosed in the
        pre element usually preserves spaces and line breaks. The text renders
        in a fixed-pitch font."""
        self.write_tag_noWhitespace('pre', True, args)

    def _pre(self):
        self._closeTag_noWhitespace('pre')

    def blockquote(self, **args):
        """The blockquote tag is the standard XHTML tag."""
        self.write_tag('blockquote', True, args)

    def _blockquote(self):
        self._closeTag('blockquote')

    def cite(self, **args):
        """The cite tag is the standard XHTML tag."""
        self.write_tag('cite', True, args)

    def _cite(self):
        self._closeTag('cite')

    def p(self, **args):
        """The p tag is the standard XHTML paragraph.
        http://www.w3schools.com/tags/tag_p.asp

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.p()
        >>> b.addHtml('Hello world')
        >>> b._p()
        >>> b.getHtml()
        '<p>Hello world</p>'
        """
        self.write_tag_noWhitespace('p', True, args)

    def _p(self):
        self._closeTag_noWhitespace('p')

    def tt(self, **args):
        """The tt method is showing the old teletype font."""
        self.write_tag_noWhitespace('tt', True, args)

    def _tt(self):
        self._closeTag_noWhitespace('tt')

    def code(self, **args):
        """The code method is the standard XHTML tag, for showing computer code
        in fixed width font."""
        self.write_tag_noWhitespace('code', True, args)

    def _code(self):
        self._closeTag_noWhitespace('code')

    def strong(self, **args):
        """The strong tag is the standard XHTML strong.  Note that nowadays it
        is better to implement this typographic behavior through span and
        CSS.

        TODO: Add the other attributes to the b tag such as: id, class, title,
        style, dir, lang, onclick, ondblclick, onmousedown, onmouseup,
        onmouseover, onmousemove, onmouseout, onkeypress, onkeydown,
        onkeyup.

        <www href="http://www.w3schools.com/tags/tag_font_style.asp" target="external"/>

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.strong()
        >>> b.addHtml('Hello world')
        >>> b._strong()
        >>> b.getHtml()
        '<strong>Hello world</strong>'
        """
        self.write_tag_noWhitespace('strong', True, args)

    def _strong(self):
        self._closeTag_noWhitespace('strong')

    def em(self, **args):
        """
        The em tag is the standard XHTML emphasis.
        """
        self.write_tag_noWhitespace('em', True, args)

    def _em(self):
        self._closeTag_noWhitespace('em')

    def b(self, **args):
        """
        The b tag is the standard XHTML bold.  Note that nowadays it is better to implement this
        typographic behavior through span and CSS.<para/>
        <www href="http://www.w3schools.com/tags/tag_font_style.asp" target="external"/>

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.b()
        >>> b.addHtml('Hello world')
        >>> b._b()
        >>> b.getHtml()
        '<b>Hello world</b>'
        """
        self.write_tag_noWhitespace('b', True, args)

    def _b(self):
        self._closeTag_noWhitespace('b')

    def u(self, **args):
        """
        The u tag is the standard XHTML underline.  Note that nowadays it is better to implement
        this typographic behavior through span and CSS.<para/>
        <todo>Add the other attributes to the u tag such as: id, class, title, style, dir, lang,
        onclick, ondblclick, onmousedown, onmouseup, onmouseover, onmousemove, onmouseout, onkeypress, onkeydown,
        onkeyup</todo>
        <www href="http://www.w3schools.com/tags/tag_font_style.asp" target="external"/>
        """
        self.write_tag_noWhitespace('u', True, args)

    def _u(self):
        self._closeTag_noWhitespace('u')

    def i(self, **args):
        """
        The i tag is the standard XHTML italic. Note that nowadays it is better to implement
        this typographic behavior through span and CSS.<para/>
        <todo>Add the other attributes to the p tag such as: id, class, title, style, dir, lang,
        onclick, ondblclick, onmousedown, onmouseup, onmouseover, onmousemove, onmouseout, onkeypress, onkeydown,
        onkeyup</todo>
        <www href="http://www.w3schools.com/tags/tag_font_style.asp" target="external"/>
        """
        self.write_tag_noWhitespace('i', True, args)

    def _i(self):
        self._closeTag_noWhitespace('i')

    def s(self, **args):
        """
        The s tag is the standard XHTML strike. Note that nowadays it is better to implement
        this typographic behavior through span and CSS.<para/>
        <todo>Add the other attributes to the p tag such as: id, class, title, style, dir, lang,
        onclick, ondblclick, onmousedown, onmouseup, onmouseover, onmousemove, onmouseout, onkeypress, onkeydown,
        onkeyup</todo>
        <www href="http://www.w3schools.com/tags/tag_strike.asp" target="external"/>
        """
        self.write_tag_noWhitespace('s', True, args)

    def _s(self):
        self._closeTag_noWhitespace('s')

    # D E P R E C A T E D ?
    # strike = s
    # _strike = _s

    def q(self, **args):
        """

        The q tag defines the start of a short quotation. Note that nowadays it is better to implement
        this typographic behavior through span and CSS.<para/>
        <todo>Add the other attributes to the p tag such as: id, class, title, style, dir, lang,
        onclick, ondblclick, onmousedown, onmouseup, onmouseover, onmousemove, onmouseout, onkeypress, onkeydown,
        onkeyup</todo>
        <www href="http://www.w3schools.com/tags/tag_q.asp" target="external"/>

        """
        self.write_tag_noWhitespace('q', True, args)

    def _q(self):
        self._closeTag_noWhitespace('q')

    def sup(self, **args):
        """
        The sup tag implements the standard XTHML tag for superior (superscript) text.
        self.text('Normal text')
        self.sup()
        self.text('and superior')
        self._sup()
        Normal text <sup>and suporior</sup>
        """
        self.write_tag_noWhitespace('sup', True, args)

    def _sup(self):
        self._closeTag_noWhitespace('sup')

    def sub(self, **args):
        """
        The sub tag implements the standard XTHML tag for inferior (subscript) text.
        self.text('Normal text')
        self.sub()
        self.text('and inferior')
        self._sub()
        Normal text <sub>and inferior</sub>
        """
        self.write_tag_noWhitespace('sub', True, args)
    def _sub(self):
        self._closeTag_noWhitespace('sub')


    def br(self, count=1, **args):
        """
        The br tag inserts a single line break.
        The count attribute is not standard XHTML. It indicates the number of br to repeat.
        The cssClass can define the amount of leading in px of the break.
        <www href="http://www.w3schools.com/tags/tag_br.asp" target="external"/>
        self.br()
        """
        for _ in range(count):
            self.write_tag_noWhitespace('br', False, args)

    def nbsp(self, count=1):
        """
        The nbsp generates the count (default is 1) amound of non-breaking-spaces.
        """
        self.write('&nbsp;'*count)

    def table(self, **args):
        """
        The table tag defines a table.¬†Inside a table tag you can put table headers,
        table rows, table cells, and other tables.
        <www href="http://www.w3schools.com/tags/tag_table.asp" target="external"/>
        self.table()
            ...
        self._table()
        """
        self.write_tag_noWhitespace('table', True, args)
        #self._debugclass('table', self.getClassName(args, self.TABLE_ATTRIBUTES))

    def getClassName(self, args, attributes):
        if 'cssClass' in args:
            return self.cssClass2SpaceString(args['cssClass'])
        else:
            return None

    def _table(self):
        self._closeTag('table')


    def thead(self, **args):
        """
        Defines the text header of a table.
        """
        self.write_tag_noWhitespace('thead', True, args)


    def _thead(self):
        self._closeTag_noWhitespace('thead')


    def tfoot(self, **args):
        """
        Defines the text footer of a table.
        """
        self.write_tag('tfoot', True, args)


    def _tfoot(self):
        self._closeTag('tfoot')


    def tbody(self, **args):
        """
        Defines the text body of a table.
        """
        self.write_tag('tbody', True, args)


    def _tbody(self):
        self._closeTag('tbody')

    def tr(self, **args):
        """
        Defines a row in a table.
        <www href="http://www.w3schools.com/tags/tag_tr.asp" target="external"/>
        self.tr()
            ...
        self._tr()
        """
        self.write_tag('tr', True, args)

    def _tr(self):
        self._closeTag('tr')

    def td(self, **args):
        """
        Defines a cell in a table. If the rolspan or colspan are not defined or if their value is 1
        then the output is ignored.
        <www href="http://www.w3schools.com/tags/tag_td.asp" target="external"/>
        self.td()
            ...
        self._td()
        """
        self.write_tag_noWhitespace('td', True, args)
        #self._debugclass('td', self.getClassName(args, self.TD_ATTRIBUTES))

    def _td(self):
        self._closeTag_noWhitespace('td')

    def th(self, **args):
        """
        Defines a table header cell in a table. The text within the th element usually renders in bold. If the rolspan
         or colspan are not defined or if their value is 1 then the output is ignored.

        <www href="http://www.w3schools.com/tags/tag_th.asp" target="external"/>
        self.th()
            ...
        self._th()
        """
        self.write_tag_noWhitespace('th', True, args)

    def _th(self):
        self._closeTag_noWhitespace('th')

    def style(self, type='text/css', **args):
        """Defines a style in a document. The style element goes in the head
        section. If you want to include a style sheet in your page, you should
        define the style sheet externally, and link to it using XHTML link.

        <www href="http://www.w3schools.com/tags/tag_style.asp" target="external"/>
        self.style()
            ...
        self._style()
        """
        self.write_tag('style', True, args)

    def _style(self):
        self._closeTag('style')

    def span(self, **args):
        self.write_tag_noWhitespace('span', True, args)

    def _span(self):
        self._closeTag_noWhitespace('span')

    def div(self, **args):
        """
        The div tag defines a division/section in a document.
        <note>Browsers usually place a line break before and after the div element.</note>
        <www href="http://www.w3schools.com/tags/tag_div.asp" target="external"/>
        self.div()
            ...
        self._div()
        """
        self.write_tag_noWhitespace('div', True, args)

    def _div(self, comment=None):
        self._closeTag_noWhitespace('div')
        if comment is not None:
            self.comment(comment)

    def svg(self, **args):
        self.write_tag('svg', True, args)

    def _svg(self):
        self._closeTag('svg')

    def canvas(self, **args):
        """The canvas tag defines a canvas in a document.
        """
        self.write_tag('canvas', True, args)
        self._debugclass('canvas', self.getClassName(args, self.CANVAS_ATTRIBUTES))

    def _canvas(self):
        self._closeTag('canvas')

    def img(self, **args):
        """The img tag defines an image. The img tag has no block.
        To avoid compatibility problems between browser with the default border value,
        it is set to 0 if not defined.
        http://www.w3schools.com/tags/tag_img.asp

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.img(src="myImage.png", cssClass="myClass", width="100%")
        >>> b.getHtml()
        '<img src="myImage.png" class="myClass"/>'
        """
        if not args.get('border'):
            args['border'] = 0
        self.write_tag('img', False, args)

    def map(self, name):
        self.write('<map name="%s">' % name)
        self._pushTag('map')

    def _map(self):
        self._closeTag('map')

    def area(self, **args):
        if not args.get('border'):
            args['border'] = self.AREA_DEFAULTBORDER
        if args['href']:
            args['href'] = self.e.getPath(args['href'])
        self.write_tag('area', False, args)


    def hr(self, **args):
        """The hr tag inserts a horizontal rule.
        www href="http://www.w3schools.com/tags/tag_hr.asp

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.hr()
        >>> b.getHtml()
        '<hr/>'
        >>> b.clearHtml()
        >>> b.hr(cssClass='wide')
        >>> b.getHtml()
        '<hr class="wide"/>'
        """
        self.write_tag_noWhitespace('hr', False, args)


    def a(self, **kwargs):
        """The a tag defines an anchor. An anchor can be used in two ways:
        To create a link to another document by using the href attribute
        To create a bookmark inside a document, by using the name or id attribute
        href="http://www.w3schools.com/tags/tag_a.asp

        >>> b = HtmlBuilder()
        >>> b.compact = True
        >>> b.a(href="mypage.html", target="external", cssClass='myClass')
        >>> b.write('Hello')
        >>> b._a()
        >>> b.getHtml()
        '<a href="mypage.html" target="external" class="myClass">Hello</a>'
        >>> b.clearHtml()
        >>> b.a(name="marker")
        >>> b.getHtml()
        '<a name="marker">'
        """
        self.write_tag_noWhitespace('a', True, kwargs)

    def _a(self):
        self._closeTag_noWhitespace('a')


    def nav(self, **kwargs):
        self.write_tag_noWhitespace('nav', True, kwargs)

    def _nav(self):
        self._closeTag_noWhitespace('nav')


    def frameset(self, **args):
        """The frameset tag creates an frame set that contains frames with
        other documents.
        <www href="http://www.w3schools.com/tags/tag_frameset.asp"/>
        """
        self.write_tag('frameset', True, args)

    def _frameset(self):
        self._closeTag('frameset')


    def frame(self, **args):
        """The frame tag defines one particular window (frame) within a
        frameset. Each frame in a frameset can have different attributes, such
        as border, scrolling, the ability to resize, etc.

        <www href="http://www.w3schools.com/tags/tag_frame.asp"/>
        """
        self.write_tag('frame', True, args)
        self._debugclass('frame', self.getClassName(args, self.FRAME_ATTRIBUTES))


    def _frame(self):
        self._closeTag('frame')


    def noframes(self, **args):
        """The noframes tag is used for browsers that do not handle frames.
        The noframes element can contain all the elements that you can find
        inside the body element of a normal HTML page.

        The noframes element is most used to link to a non-frameset version of
        the web site or to display a message to users that frames are required.
        The noframes element goes inside the frameset element.
        <www href="http://www.w3schools.com/tags/tag_noframes.asp"/>
        """
        self.write_tag('noframes', False, args)
        self._debugclass('noframes', self.getClassName(args, self.NOFRAMES_ATTRIBUTES))

    def _noframes(self):
        self._closeTag('noframes')

    def iframe(self, src, **args):
        """The iframe tag creates an inline frame that contains another document.
        <www href="http://www.w3schools.com/tags/tag_iframe.asp"/>
        """
        self.write('<iframe src="%s"' % src)
        self.getandwrite_attributes('iframe', args)
        self.write('>')

    def _iframe(self):
        self.write('</iframe>')

    def iframe_(self, src, **args):
        self.iframe(src, **args)
        self._iframe()


    def embed(self, **args):
        """FIXME: Does not seem to be defined in w3schools??
        self.embed(src='./_images/amovie.qt')
        """
        self.write_tag('embed', False, args)

    def script(self, charset='UTF-8', type='text/javascript', **args):
        """The br tag inserts a single line break.  Defines a script, such as a
        JavaScript. Note that if @src is used, then no self._script() must be
        used.

        The count attribute is not standard XHTML. It indicates the number of
        br to repeat.

        <www href="http://www.w3schools.com/tags/tag_script.asp" target="external"/>
        self.script()
            ...
        self._script()
        """
        #
        #     Build script. Note that if @src is used, then no self._script()
        #     must be used.
        #
        self.write('<script')
        # Make sure to write "UTF-8" instead of "utf-8" since FireFox 2.0.0.4 will
        # ignore the script otherwise.
        self.write(' charset="%s"' % charset.upper())
        self.write(' type="%s"' % type)
        language = args.get('language')
        if language is not None:
            self.write(' language="%s"' % language)
        for key, value in args.items():
            self.write(' %s="%s"' % (dataAttribute2Html5Attribute(key), value))
        src = args.get('src')
        if src is not None:
            self.write('></script>\n')
        else:
            self._pushTag('script')
            self.write('>\n')

    def _script(self):
        self.write('\n')
        self._closeTag('script')
        self.newLine() # Optional newline is self.compact is False.

    def script_(self, js, charset='UTF-8', type='text/javascript', **args):
        self.script(charset='UTF-8', type='text/javascript', **args)
        self.addHtml(js)
        self._script()

    #
    #     L I S T things
    #

    def ul(self, **args):
        """The ul tag defines an unordered list.

        <www href="http://www.w3schools.com/tags/tag_ul.asp" target="external"/>
        self.ul()
            ...
        self._ul()
        """
        self.write_tag('ul', True, args)

    def _ul(self):
        self._closeTag('ul')

    def ol(self, **args):
        """The ol tag defines the start of a definition list.

        <www href="http://www.w3schools.com/tags/tag_ol.asp" target="external"/>
        self.ol()
            ...
        self._ol()
        """
        self.write_tag('ol', True, args)


    def _ol(self):
        self._closeTag('ol')


    def li(self, **args):
        """The li tag defines the start of a list item. The li tag is used in
        both ordered (ol) and unordered lists (ul).

        <www href="http://www.w3schools.com/tags/tag_li.asp" target="external"/>
        self.li()
            ...
        self._li()
        """
        self.write_tag_noWhitespace('li', True, args)

    def _li(self):
        self._closeTag_noWhitespace('li')

    def dl(self, **args):
        """The dl tag defines an unordered list.

        <www href="http://www.w3schools.com/tags/tag_dl.asp" target="external"/>
        self.dl()
            ...
        self._dl()
        """
        self.write_tag('dl', True, args)

    def _dl(self):
        self._closeTag('dl')

    def dt(self, **args):
        """The dt tag defines the start of a definition list term.  The dt tag
        is used only in definition lists (dl).

        <www href="http://www.w3schools.com/tags/tag_dt.asp" target="external"/>
        self.dt()
            ...
        self._dt()
        """
        self.write_tag('dt', True, args)

    def _dt(self):
        self._closeTag('dt')

    def dd(self, **args):
        """The dd tag defines the start of a definition list term.  The dd tag
        is used only in definition lists (dl).

        <www href="http://www.w3schools.com/tags/tag_dd.asp" target="external"/>
        self.dd()
            ...
        self._dd()
        """
        self.write_tag('dd', True, args)

    def _dd(self):
        self._closeTag('dd')


    #
    #     F O R M things
    #

    def form(self, cssClass=None, name=None, enctype="multipart/form-data", action=None, role=None, method=None,
             onsubmit=None, onreset=None, target=None, style=None, cssId=None):
        """The form element creates a form for user input. A form can contain
        elements such as textfields, checkboxes and radio-buttons. Forms are
        used to pass user data to a specified URL.

        <www href="http://www.w3schools.com/tags/tag_form.asp" target="external"/>

        If an upload tag is used in the form, then the enctype attribute should be set to
        enctype="multipart/form-data"
        self.form(action=e['path'])
            ...
        self._form()
        """
        #
        #     @class_
        #     @method        GET | POST (default: POST)
        #     @action        (default: e['path'])
        #     @onsubmit
        #     @onreset
        #     @enctype
        #     @target
        #
        if method is None:
            method = 'POST'
        if action is None:
            action = self.e['path']
        self.write('<form method="%s" action="%s"' % (method, action))
        if cssClass is not None:
            self.write(' class="%s"' % cssClass)
        if cssId is not None:
            self.write(' id="%s"' % cssId)
        if role is not None:
            self.write(' role="%s"' % role)
        if name is not None:
            self.write(' name="%s"' % name)
        if onsubmit is not None:
            self.write(' onsubmit="%s"' % onsubmit)
        if enctype is not None:
            self.write(' enctype="%s"' % enctype)
        if style is not None:
            self.write(' style="%s"' % style)
        self.write(' accept-charset="utf-8">')
        # Push as last, so we can see the current tag on the stack
        self._pushTag('form')

    def _form(self):
        self._closeTag('form')

    def input(self, **args):
        """The input tag defines the start of an input field where the user can
        enter data.  The attribute type can be one of button | checkbox | file
        | hidden | image | password | radio | reset | submit | text.

        <www href="http://www.w3schools.com/tags/tag_input.asp" target="external"/>
        self.input(type='checkbox', name='mycheckbox')
        """
        self.write_tag('input', False, args)

    def label(self, **args):
        """The label tag associates a block of plain text with a form input,
        usually a check or radio box.  This way the user can click anywhere in
        the label text to toggle the input on or off.  It can be implemented
        two ways: <label><input…> Text</label>, or <label for='id_of_input'>
        Text</label>…<input id='id_of_input' …>.

        <www href="http://www.w3schools.com/tags/tag_label.asp" target="external"/>
        """
        self.write_tag('label', True, args)

    def _label(self):
        self._closeTag('label')

    def select(self, **args):
        """The select element creates a drop-down list.
        <www href="http://www.w3schools.com/tags/tag_select.asp" target="external"/>
        self.select()
            ...
        self._select()
        """
        self.write_tag('select', True, args)

    def _select(self):
        self._closeTag('select')

    def option(self, **args):
        """The option tag defines an option in the drop-down list.
        <www href="http://www.w3schools.com/tags/tag_option.asp" target="external"/>
        self.option()
            ...
        self._option()
        """
        self.write_tag('option', True, args)

    def _option(self):
        self._closeTag('option')

    def optgroup(self, **args):
        """The optgroup tag defines an option group in the drop-down list.
        <www href="http://www.w3schools.com/tags/tag_optgroup.asp" target="external"/>
        self.optgroup()
            ...
        self._optgroup()
        """
        self.write_tag('optgroup', True, args)

    def _optgroup(self):
        self._closeTag('optgroup')

    def button(self, **args):
        """button is the standard XHTML control. It is much like input
        type="button" but more versatile. It has open and close tags, and can
        take almost any non-form HTML structure inside.
        <www href="http://xhtml.com/en/xhtml/reference/button/" target="external"/>
        """
        self.write_tag('button', True, args)

    def _button(self):
        self._closeTag('button')

    def button_(self, label, **args):
        self.button(**args)
        self.addHtml(label)
        self._button()

    def textarea(self, **args):
        """Defines a text area (a multi-line text input control). A user can
        write text in the text area. In a text area you can write an unlimited
        number of characters. The default font in the text area is fixed pitch.

        <www href="http://www.w3schools.com/tags/tag_textarea.asp" target="external"/>
        self.textarea()
            ...
        self._textarea()
        """
        self.write_tag_noWhitespace('textarea', True, args) # No tabbing inside the <textarea> tag.

    def _textarea(self):
        self._closeTag_noWhitespace('textarea')

    def meta(self, **args):
        """The meta element provides meta-information about your page, such as
        descriptions and keywords for search engines and refresh rates.

        <www href="http://www.w3schools.com/tags/tag_meta.asp" target="external"/>
        self.meta()
            ...
        self._meta()
        """
        self.write_tag('meta', False, args)

    def object(self, **args):
        """The object defines an embedded object. Use this element to add
        multimedia to your XHTML page. This element allows you to specify the
        data and parameters for objects inserted into HTML documents, and the
        code that can be used to display/manipulate that data."""
        self.write_tag_noWhitespace('object', True, args)

    def _object(self):
        self._closeTag_noWhitespace('object')

    def small(self, **args):
        self.write_tag_noWhitespace('small', True, args)

    def _small(self):
        self._closeTag_noWhitespace('small')

    def big(self, **args):
        self.write_tag_noWhitespace('big', True, args)

    def _big(self):
        self._closeTag_noWhitespace('big')

    def param(self, **args):
        """The param element allows you to specify the run-time settings for an
        object inserted into XHTML documents."""
        self.write_tag('param', False, args)

    # N O N - H T M L

    def comment(self, s):
        if s:
            self.write('<!-- %s -->' % object2SpacedString(s))


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
