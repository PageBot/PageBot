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
#     htmlbuilderpart.py
#
from xierpa3.toolbox.transformer import TX

class HtmlBuilderPart:
    """
    The ``HtmlBuilderPart`` class implements the standard XHTML tag set with all attributes. No additional
    whitespace is added.
    """
    # Names of attributes that are written without their value.
    # Since this breaks XML validation, this list is empty by default,
    # but it can be redefined by the inheriting application class.
    SINGLE_ATTRIBUTES = []
    # Attributes that allow attributes to be tuple or list and joined
    # on tag output with separating spaces.
    CASCADING_ATTRIBUTES = ('class_', 'class')

    HTML_ATTRIBUTES = set(['dir', 'lang', 'xmllang', 'manifest'])

    HEAD_ATTRIBUTES = set(['profile'])

    LINK_ATTRIBUTES = set([ 'charset', 'href', 'hreflang', 'media', 'rel',
        'rev', 'target', 'dir', 'lang', 'type', 'sizes', ])

    BODY_ATTRIBUTES = set(['dir', 'lang',
        'onload', 'onunload', 'ondblclick', 'onmousedown',
        'onmouseup', 'onmouseover', 'onmousemove', 'onmouseout', 'onkeypress',
        'onkeydown', 'onkeyup', ])

    H_ATTRIBUTES = set([ 'dir', 'lang', ])

    LABEL_ATTRIBUTES = set(['for'])

    BUTTON_ATTRIBUTES = INPUT_ATTRIBUTES = set([
        'type', 'name', 'size', 'value', 'accept',
        'autocorrect', 'autocapitalize', 'placeholder', 'inputmode',
        'relation', 'checked', 'src', 'alt', 'readonly',
        'tabindex', 'accesskey', 'onfocus', 'onblur', 'onselect',
        'onchange', 'ondblclick', 'onmousedown',
        'onmouseup', 'onmouseover', 'onmousemove', 'onmouseout',
        'onkeypress', 'onkeydown', 'onkeyup', 'maxlength', 'disabled',
        'autocorrect', 'autocapitalize', 'placeholder', 'results',
    ])

    BLOCKQUOTE_ATTRIBUTES = set([])

    INPUT_ATTRIBUTES_DEFAULTS = {'alt': '+', 'disabled': False}

    CANVAS_ATTRIBUTES = set(['width_html', 'height_html'])

    SELECT_ATTRIBUTES = set(['name', 'onchange', 'multiple',
        'size', 'disabled', ])

    OPTION_ATTRIBUTES = set(['value', 'selected', 'onmouseup'])

    OPTGROUP_ATTRIBUTES = set(['label', ])

    TEXTAREA_ATTRIBUTES = set(['onblur', 'onchange',
        'ondblclick', 'onfocus', 'onselect', 'onmousedown', 'onmouseout', 'onmousemove',
        'onmouseover', 'onmouseup', 'onkeydown', 'onkeypress', 'onkeyup',
        'name', 'cols', 'rows', ])

    PARAM_ATTRIBUTES = set(['name', 'type', 'value', 'valuetype', ])

    OBJECT_ATTRIBUTES = set(['dir', 'lang', 'xmllang',
        'align', 'archive', 'border', 'classid', 'codebase', 'codetype', 'data',
        'declare', 'height_html', 'hspace', 'name', 'standby', 'type', 'usemap', 'vspace',
        'width_html', 'accesskey', 'tabindex', 'ondblclick', 'onmousedown',
        'onmouseup', 'onmouseover', 'onmousemove', 'onmouseout', 'onkeypress',
        'onkeydown', 'onkeyup', ])

    META_ATTRIBUTES = set(['charset', 'content', 'httpequiv', 'name', ])

    P_ATTRIBUTES = STRONG_ATTRIBUTES = EM_ATTRIBUTES = B_ATTRIBUTES = U_ATTRIBUTES = S_ATTRIBUTES = Q_ATTRIBUTES = set([
        'type', 'itemid', 'itemprop', 'itemref', 'itemscope', 'itemtype'])

    H1_ATTRIBUTES = H2_ATTRIBUTES = H3_ATTRIBUTES = H4_ATTRIBUTES = H5_ATTRIBUTES = H6_ATTRIBUTES = set([
        'itemid', 'itemprop', 'itemref', 'itemscope', 'itemtype'])

    FIGURE_ATTRIBUTES = set(['accesskey', 'contenteditable', 'contextmenu', 'dir',
        'draggable', 'hidden', 'lang', 'spellcheck', 'tabindex'])

    SUB_ATTRIBUTES = SUP_ATTRIBUTES = set([])

    BR_ATTRIBUTES = set(['class_', 'id', 'title', 'style', 'clear' ])

    TABLE_ATTRIBUTES = set([
        'align', 'bgcolor', 'border', 'cellpadding', 'cellspacing',
        'width_html', 'height_html'])

    THEAD_ATTRIBUTES = set([
        'dir', 'lang', 'xmllang',
        'align', 'char', 'charoff', 'valign', 'ondblclick', 'onmousedown',
        'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onkeydown', 'onkeypress',
        'onkeyup'])

    TFOOT_ATTRIBUTES = set([
        'dir', 'lang', 'xmllang',
        'align', 'char', 'charoff', 'valign', 'ondblclick', 'onmousedown',
        'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onkeydown', 'onkeypress',
        'onkeyup'])

    TBODY_ATTRIBUTES = set([
        'dir', 'lang',
        'xmllang', 'align', 'char', 'charoff',
        'valign', 'ondblclick', 'onmousedown',
        'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onmousedown',
        'onkeydown', 'onkeypress', 'onkeyup'])

    TR_ATTRIBUTES = set([
        'relation', 'onmousemove', 'onmouseout', 'onmouseover',
        'onmouseup', 'onmousedown', 'onkeydown', 'onkeypress', 'onkeyup'])

    TD_ATTRIBUTES = set([ 'width_html', 'height_html', 'rowspan',
        'colspan', 'valign', 'align', 'nowrap', 'relation',
        'ondblclick', 'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onmousedown',
        'onkeydown', 'onkeypress', 'onkeyup'])

    TH_ATTRIBUTES = set([ 'width_html', 'height_html', 'rowspan', 'colspan',
        'valign', 'align', 'nowrap'])

    UL_ATTRIBUTES = DL_ATTRIBUTES = set([ 'type' ])

    OL_ATTRIBUTES = set([
    'compact', 'start', 'type'
    ])

    I_ATTRIBUTES = TT_ATTRIBUTES = SMALL_ATTRIBUTES = BIG_ATTRIBUTES = LI_ATTRIBUTES = DT_ATTRIBUTES = DD_ATTRIBUTES = set([
    'dir', 'lang', 'xmllang'
    ])

    DIV_ATTRIBUTES = set([
        'onmouseout', 'relation', 'name', 'disabled',
        'onmouseover', 'onmousedown', 'onmouseup', 'ondblclick', 'onfocus', 'onblur',
        'itemid', 'itemprop', 'itemref', 'itemscope', 'itemtype', 'role', 'default',
        'width_html', 'contenteditable'])

    IMG_ATTRIBUTES = set([
        'src', 'name', 'width_html', 'height_html', 'onmouseover', 'onmousedown', 'onmouseup', 'onmouseout',
        'alt', 'border', 'hspace',
        'vspace', 'align', 'relation', 'usemap',
        'itemid', 'itemprop', 'itemref', 'itemscope', 'itemtype'])

    # IMG_ATTRIBUTES_DEFAULTS = {'alt': '_'}

    AREA_ATTRIBUTES = set([
        'shape', 'coords', 'href', 'target', 'border',
        'onmouseover', 'onmouseout', 'onmousedown', "onmouseup"])

    SPAN_ATTRIBUTES = set([ 'relation', 'itemprop',
        'onmouseover', 'onmouseout', 'onmousedown', 'onmouseup', 'contenteditable'])

    FRAMESET_ATTRIBUTES = set([
        'cols', 'rows',
        'onload', 'onunload'])

    FRAME_ATTRIBUTES = set([
        'frameborder', 'longdesc', 'marginheight', 'marginwidth',
        'name', 'noresize', 'scrolling', 'src'
        ])

    NOFRAMES_ATTRIBUTES = set([
        'dir', 'lang'
        ])

    IFRAME_ATTRIBUTES = set([
        'src', 'align', 'frameborder', 'longdesc', 'type', 'border',
        'marginheight', 'marginwidth', 'name', 'scrolling',
        'width_html', 'height_html'])

    AREA_ATTRIBUTES_DEFAULTS = {'width_html': 600, 'height_html': 400}

    HR_ATTRIBUTES = set([ 'align', 'color', 'noshade',
            'size', 'width_html' ])

    HGROUP_ATTRIBUTES = set(['itemscope'])

    ARTICLE_ATTRIBUTES = set([
        'itemid', 'itemprop', 'itemref', 'itemscope', 'itemtype'])

    SECTION_ATTRIBUTES = set([
        'itemid', 'itemprop', 'itemref', 'itemscope', 'itemtype'])

    HEADER_ATTRIBUTES = set(['cite'])

    EMBED_ATTRIBUTES = set([
        'src', 'href', 'quality', 'name', 'menu',
        'type', 'width_html', 'wmode', 'align', 'allowscriptaccess',
        'height_html', 'autoplay', 'loop', 'controller',
        'playeveryframe', 'bgcolor', 'movieid', 'kioskmode',
        'targetcache', 'hidden', 'volume', 'pluginspace',
        'scale', 'allowfullscreen', 'flashvars'])

    A_ATTRIBUTES = set(['href', 'target', 'alt', 'name', 'itemprop',
        'onmouseout', 'onmouseover', 'onmousedown', 'onmouseup',
        'ondblclick', 'onfocus', 'accesskey', 'rel', 'rev', 'relation',
        'type'])

    # A_ATTRIBUTES_DEFAULTS = {'alt': '='}
    NAV_ATTRIBUTES = set(['accesskey'])

    BOOLEAN_ATTRIBUTES = {'checked': 'checked', 'selected': 'selected', 'disabled': 'disabled'}

    def get_attribute_exceptions(self, key, value):
        u"""
        The ``get_attribute_exceptions`` method writes the attribute, and checks on naming differences between
        the Xierpa attributes and HTML attributes.
        """
        # Boolean attributes.
        key = TX.dataAttribute2Html5Attribute(key)

        if key in self.BOOLEAN_ATTRIBUTES:
            if TX.value2Bool(value): # Can be boolean or text boolean
                self.write_attribute(key, self.BOOLEAN_ATTRIBUTES[key])
        else:
            # Some exceptions.
            if key.startswith('html'):
                key = key[3:]
            if key == 'class_':
                key = 'class'
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
                    value = u'#' + value

            # Handle Angular.org attributes that contain underscores, translate them to hyphens
            elif key.startswith('ng_'):
                key = key.replace('_', '-')

            self.write_attribute(key, value)

    def docType(self, s):
        self.output('<!DOCTYPE %s>\n' % s)

    def html(self, xmlns=None, **args):
        """
        <seealso><www href="http://www.w3schools.com/tags/tag_html.asp" target="external"/></seealso>
        <python>
        self.html(xmlns="http://www.w3.org/1999/xhtml", dir=ltr, lang=no, xmllang=no)<br/>
        ...<br/>
        self._html()
        </python>
        Default value for xmlns is "http://www.w3.org/1999/xhtml".
        """
        self.output(u'<html xmlns="%s"' % (xmlns or 'http://www.w3.org/1999/xhtml'))
        self.getandwrite_attributes(u'html', args)
        self.output(u'>')
        self.tabIn()
        # Push as last, so we can see the current tag on the stack
        self._pushTag(u'html')

    def _html(self):
        self._closeTag(u'html')

    def head(self, **args):
        u"""
        The head element can contain information about the document.¬†The browser does not display the
        "head information" to the user. The following tags can be in the head section: ``base``,
        ``link``, ``meta``, ``script``, ``style`` and ``title``.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_head.asp" target="external"/></seealso>
        <python>
        self.head()<br/>
        ...<br/>
        self._head()
        </python>
        """
        self.tabs()
        self.tabIn()
        self.output(u'<head')
        self.getandwrite_attributes(u'head', args)
        self.output(u'>')
        # Automatic meta charset tag, so we don't forget we only want to work in UTF-8
        self.meta(httpequiv='Content-Type', content='text/html;charset=UTF-8')
        # Push as last, so we can see the current tag on the stack
        self._pushTag(u'head')

    def _head(self):
        self._closeTag(u'head')

    def title(self):
        """
        This tag defines the title of the document.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_title.asp" target="external"/></seealso>
        <python>
        self.title()<br/>
        ...<br/>
        self._title()
        </python>
        """
        self.tabs()
        self.tabIn()
        self.output(u'<title>')
        # Push as last, so we can see the current tag on the stack
        self._pushTag(u'title')

    def _title(self):
        self._closeTag(u'title')

    def title_(self, s):
        self.title()
        self.output(s)
        self._title()

    def link(self, **args):
        """
        The ``link`` tag defines the relationship between two linked documents.<br/>
        Note that this tag is defined by ``XierpaBuilder``. When using an inheriting class
        from ``XierpaBuilder`` then use the ``rellink`` tag name instead.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_link.asp" target="external"/></seealso>
        <python>
        self.head()<br/>
        ...<br/>
        self.link(href='/_images/favicon.ico', rel='shortcut icon')<br/>
        ...<br/>
        self._head()
        </python>
        """
        self.write_tag(u'link', False, args)


    def body(self, **args):
        """
        The body element defines the documents' body. It contains all the contents
        of the document (like text, images, colors, graphics, etc.).<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_body.asp" target="external"/></seealso>
        <python>
        self.body(onload='javascript:loadpage()')<br/>
        ...<br/>
        self._body()
        </python>
        """
        self.write_tag(u'body', True, args)


    def _body(self):
        self._closeTag(u'body')


    def h1(self, **args):
        u"""
        The ``h1`` to ``h6`` tags define headers.
        ``h1`` defines the largest header. ``h6`` defines the smallest header.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_hn.asp" target="external"/></seealso>
        <python>
        self.h1(class_='chapter')<br/>
        ...<br/>
        self._h1()
        </python>
        """
        self.write_tag_noWhitespace(u'h1', True, args)

    def _h1(self):
        self._closeTag_noWhitespace(u'h1')
        self.newline()

    def h1_(self, s, **args):
        u"""
        The ``h1_`` to ``h6_`` tags define headers, combining the opening and closing tag
        where the ``s`` attribute is the block content.
        """
        self.h1(**args)
        self.text(s)
        self._h1()

    def h2(self, **args):
        u"""
        The ``h1`` to ``h6`` tags define headers.
        ``h1`` defines the largest header. ``h6`` defines the smallest header.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_hn.asp" target="external"/></seealso>
        <python>
        self.h2(class_='head')<br/>
        ...<br/>
        self._h2()
        </python>
        """
        self.write_tag_noWhitespace(u'h2', True, args)

    def _h2(self):
        self._closeTag_noWhitespace(u'h2')
        self.newline()

    def h2_(self, s, **args):
        u"""
        The ``h1_`` to ``h6_`` tags define headers, combining the opening and closing tag
        where the ``s`` attribute is the block content.
        """
        self.h2(**args)
        self.text(s)
        self._h2()

    def h3(self, **args):
        u"""
        The ``h1`` to ``h6`` tags define headers.
        ``h1`` defines the largest header. ``h6`` defines the smallest header.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_hn.asp" target="external"/></seealso>
        <python>
        self.h3(class_='subhead')<br/>
        ...<br/>
        self._h3()
        </python>
        """
        self.write_tag_noWhitespace(u'h3', True, args)

    def _h3(self):
        self._closeTag_noWhitespace(u'h3')
        self.newline()

    def h3_(self, s, **args):
        u"""
        The ``h1_`` to ``h6_`` tags define headers, combining the opening and closing tag
        where the ``s`` attribute is the block content.
        """
        self.h3(**args)
        self.text(s)
        self._h3()

    def h4(self, **args):
        u"""
        The ``h1`` to ``h6`` tags define headers.
        ``h1`` defines the largest header. ``h6`` defines the smallest header.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_hn.asp" target="external"/></seealso>
        <python>
        self.h4(class_='subsubhead')<br/>
        ...<br/>
        self._h4()
        </python>
        """
        self.write_tag_noWhitespace(u'h4', True, args)

    def _h4(self):
        self._closeTag_noWhitespace(u'h4')
        self.newline()

    def h4_(self, s, **args):
        u"""
        The ``h1_`` to ``h6_`` tags define headers, combining the opening and closing tag
        where the ``s`` attribute is the block content.
        """
        self.h4(**args)
        self.text(s)
        self._h4()

    def h5(self, **args):
        u"""
        The ``h1`` to ``h6`` tags define headers.
        ``h1`` defines the largest header. ``h6`` defines the smallest header.<br/>
         <seealso><www href="http://www.w3schools.com/tags/tag_hn.asp" target="external"/></seealso>
        <python>
        self.h5(class_='caption')<br/>
        ...<br/>
        self._h5()
        </python>
        """
        self.write_tag_noWhitespace(u'h5', True, args)

    def _h5(self):
        self._closeTag_noWhitespace(u'h5')

    def h5_(self, s, **args):
        u"""
        The ``h1_`` to ``h6_`` tags define headers, combining the opening and closing tag
        where the ``s`` attribute is the block content.
        """
        self.h5(**args)
        self.text(s)
        self._h5()

    def h6(self, **args):
        u"""
        The ``h1`` to ``h6`` tags define headers.
        ``h1`` defines the largest header. ``h6`` defines the smallest header.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_hn.asp" target="external"/></seealso>
        <python>
        self.h6(class_='footnote')<br/>
        ...<br/>
        self._h6()
        </python>
        """
        self.write_tag_noWhitespace(u'h6', True, args)

    def _h6(self):
        self._closeTag_noWhitespace(u'h6')

    def h6_(self, s, **args):
        u"""
        The ``h1_`` to ``h6_`` tags define headers, combining the opening and closing tag
        where the ``s`` attribute is the block content.
        """
        self.h6(**args)
        self.text(s)
        self._h6()

    def figure(self, **args):
        u"""
        The ``figure`` method (HTML5) is used for annotating illustrations, diagrams, photos, code listings, etc.
        You can use the tag to associate a caption together with some embedded content, such as a graphic or video.
        You can use the tag in conjunction with the <tag>figcaption</tag> element to provide a caption for the contents
        of your <tag>figure</tag> element.
        """
        self.write_tag(u'figure', True, args)

    def _figure(self):
        self._closeTag(u'figure')

    def figcaption(self, **args):
        u"""
        The ``figure`` method (HTML5) is used for annotating illustrations, diagrams, photos, code listings, etc.
        You can use the tag to associate a caption together with some embedded content, such as a graphic or video.
        You can use the tag in conjunction with the <tag>figcaption</tag> element to provide a caption for the contents
        of your <tag>figure</tag> element.
        """
        self.write_tag(u'figcaption', True, args)

    def _figcaption(self):
        self._closeTag(u'figcaption')

    def hgroup(self, **args):
        u"""
        The ``hgroup`` method (HTML5) defines the heading of a section or a document.
        The hgroup element is used to group headers, <tag>h1</tag> to <tag>h6</tag>, where the largest
        is the main heading of the section, and the others are sub-headings.
        """
        self.write_tag(u'hgroup', True, args)

    def _hgroup(self):
        self._closeTag(u'hgroup')

    def article(self, **args):
        u"""
        The ``article`` method (HTML5) defines external content.
        The external content could be a news-article from an external provider, or a text from a web log
        (blog), or a text from a forum, or any other content from an external source.
        """
        self.write_tag(u'article', True, args)

    def _article(self):
        self._closeTag(u'article')

    def header(self, **args):
        u"""
        The ``article`` method (HTML5) defines an introduction to the document.
        """
        self.write_tag(u'header', True, args)

    def _header(self):
        self._closeTag(u'header')

    def section(self, **args):
        u"""
        The ``section`` method (HTML5) defines defines sections in a document. Such as chapters, headers, footers, or any other sections of the document.
        """
        self.write_tag(u'section', True, args)

    def _section(self):
        self._closeTag(u'section')

    def pre(self, **args):
        """
        The pre element defines preformatted text. The text enclosed in the pre element usually preserves spaces and line
        breaks. The text renders in a fixed-pitch font.
        """
        self.write_tag_noWhitespace(u'pre', True, args)

    def _pre(self):
        self._closeTag_noWhitespace(u'pre')

    def blockquote(self, **args):
        u"""
        The ``blockquote`` tag is the standard XHTML tag.
        """
        self.write_tag(u'blockquote', True, args)

    def _blockquote(self):
        self._closeTag(u'blockquote')

    def cite(self, **args):
        u"""
        The ``cite`` tag is the standard XHTML tag.
        """
        self.write_tag(u'cite', True, args)

    def _cite(self):
        self._closeTag(u'cite')

    def p(self, **args):
        """
        The ``p`` tag is the standard XHTML paragraph.
        <todo>Add the other attributes to the ``p`` tag such as: id, class, title, style, dir, lang,
        onclick, ondblclick, onmousedown, onmouseup, onmouseover, onmousemove, onmouseout, onkeypress, onkeydown,
        onkeyup</todo>
        <seealso><www href="http://www.w3schools.com/tags/tag_p.asp" target="external"/></seealso>
        """
        self.write_tag_noWhitespace(u'p', True, args)

    def _p(self):
        self._closeTag_noWhitespace(u'p')

    def tt(self, **args):
        u"""
        The ``tt`` method is showing the old teletype font.
        """
        self.write_tag_noWhitespace(u'tt', True, args)

    def _tt(self):
        self._closeTag_noWhitespace(u'tt')

    def code(self, **args):
        u"""
        The ``code`` method is the standard XHTML tag, for showing computer code in fixed width font.
        """
        self.write_tag_noWhitespace(u'code', True, args)

    def _code(self):
        self._closeTag_noWhitespace(u'code')

    def strong(self, **args):
        """
        The ``strong`` tag is the standard XHTML strong.  Note that nowadays it is better to implement this
        typographic behavior through ``span`` and CSS.<para/>
        <todo>Add the other attributes to the ``b`` tag such as: id, class, title, style, dir, lang,
        onclick, ondblclick, onmousedown, onmouseup, onmouseover, onmousemove, onmouseout, onkeypress, onkeydown,
        onkeyup</todo>
        <seealso><www href="http://www.w3schools.com/tags/tag_font_style.asp" target="external"/></seealso>
        """
        self.write_tag_noWhitespace(u'strong', True, args)

    def _strong(self):
        self._closeTag_noWhitespace(u'strong')

    def em(self, **args):
        """
        The ``em`` tag is the standard XHTML emphasis.
        """
        self.write_tag_noWhitespace(u'em', True, args)

    def _em(self):
        self._closeTag_noWhitespace(u'em')

    def b(self, **args):
        """
        The ``b`` tag is the standard XHTML bold.  Note that nowadays it is better to implement this
        typographic behavior through ``span`` and CSS.<para/>
        <todo>Add the other attributes to the ``b`` tag such as: id, class, title, style, dir, lang,
        onclick, ondblclick, onmousedown, onmouseup, onmouseover, onmousemove, onmouseout, onkeypress, onkeydown,
        onkeyup</todo>
        <seealso><www href="http://www.w3schools.com/tags/tag_font_style.asp" target="external"/></seealso>
        """
        self.write_tag_noWhitespace(u'b', True, args)

    def _b(self):
        self._closeTag_noWhitespace(u'b')

    def u(self, **args):
        """
        The ``u`` tag is the standard XHTML underline.  Note that nowadays it is better to implement
        this typographic behavior through ``span`` and CSS.<para/>
        <todo>Add the other attributes to the ``u`` tag such as: id, class, title, style, dir, lang,
        onclick, ondblclick, onmousedown, onmouseup, onmouseover, onmousemove, onmouseout, onkeypress, onkeydown,
        onkeyup</todo>
        <seealso><www href="http://www.w3schools.com/tags/tag_font_style.asp" target="external"/></seealso>
        """
        self.write_tag_noWhitespace(u'u', True, args)

    def _u(self):
        self._closeTag_noWhitespace(u'u')

    def i(self, **args):
        """
        The ``i`` tag is the standard XHTML italic. Note that nowadays it is better to implement
        this typographic behavior through ``span`` and CSS.<para/>
        <todo>Add the other attributes to the ``p`` tag such as: id, class, title, style, dir, lang,
        onclick, ondblclick, onmousedown, onmouseup, onmouseover, onmousemove, onmouseout, onkeypress, onkeydown,
        onkeyup</todo>
        <seealso><www href="http://www.w3schools.com/tags/tag_font_style.asp" target="external"/></seealso>
        """
        self.write_tag_noWhitespace(u'i', True, args)

    def _i(self):
        self._closeTag_noWhitespace(u'i')

    def s(self, **args):
        """
        The ``s`` tag is the standard XHTML strike. Note that nowadays it is better to implement
        this typographic behavior through ``span`` and CSS.<para/>
        <todo>Add the other attributes to the ``p`` tag such as: id, class, title, style, dir, lang,
        onclick, ondblclick, onmousedown, onmouseup, onmouseover, onmousemove, onmouseout, onkeypress, onkeydown,
        onkeyup</todo>
        <seealso><www href="http://www.w3schools.com/tags/tag_strike.asp" target="external"/></seealso>
        """
        self.write_tag_noWhitespace(u's', True, args)

    def _s(self):
        self._closeTag_noWhitespace(u's')

    # D E P R E C A T E D ?
    # strike = s
    # _strike = _s

    def q(self, **args):
        """

        The ``q`` tag defines the start of a short quotation. Note that nowadays it is better to implement
        this typographic behavior through ``span`` and CSS.<para/>
        <todo>Add the other attributes to the ``p`` tag such as: id, class, title, style, dir, lang,
        onclick, ondblclick, onmousedown, onmouseup, onmouseover, onmousemove, onmouseout, onkeypress, onkeydown,
        onkeyup</todo>
        <seealso><www href="http://www.w3schools.com/tags/tag_q.asp" target="external"/></seealso>

        """
        self.write_tag_noWhitespace(u'q', True, args)

    def _q(self):
        self._closeTag_noWhitespace(u'q')

    def sup(self, **args):
        """
        The ``sup`` tag implements the standard XTHML tag for superior (superscript) text.
        <python>
        self.text(u'Normal text')<br/>
        self.sup()<br/>
        self.text(u'and superior')<br/>
        self._sup()<br/>
        </python>
        Normal text <sup>and suporior</sup>
        """
        self.write_tag_noWhitespace(u'sup', True, args)

    def _sup(self):
        self._closeTag_noWhitespace(u'sup')

    def sub(self, **args):
        """
        The ``sub`` tag implements the standard XTHML tag for inferior (subscript) text.
        <python>
        self.text(u'Normal text')<br/>
        self.sub()<br/>
        self.text(u'and inferior')<br/>
        self._sub()<br/>
        </python>
        Normal text <sub>and inferior</sub>
        """
        self.write_tag_noWhitespace(u'sub', True, args)
    def _sub(self):
        self._closeTag_noWhitespace(u'sub')


    def br(self, count=1, **args):
        """
        The ``br`` tag inserts a single line break.<br/>
        The count attribute is not standard XHTML. It indicates the number of ``br`` to repeat.<br/>
        The ``class_`` can define the amount of leading in ``px`` of the break.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_br.asp" target="external"/></seealso>
        <python>
        self.br()<br/>
        </python>
        """
        for _ in range(count):
            self.write_tag_noWhitespace(u'br', False, args)

    def nbsp(self, count=1):
        """
        The ``nbsp`` generates the ``count`` (default is 1) amound of non-breaking-spaces.
        """
        self.output('&nbsp;'*count)

    def table(self, **args):
        u"""
        The ``table`` tag defines a table.¬†Inside a ``table`` tag you can put table headers,
        table rows, table cells, and other tables.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_table.asp" target="external"/></seealso>
        <python>
        self.table()<br/>
        ...<br/>
        self._table()
        </python>
        """
        self.write_tag_noWhitespace(u'table', True, args)
        #self._debugclass(u'table', self.getClassName(args, self.TABLE_ATTRIBUTES))

    def getClassName(self, args, attributes):
        if 'class_' in args:
            return self.class_2SpaceString(args['class_'])
        else:
            return None

    def _table(self):
        self._closeTag(u'table')


    def thead(self, **args):
        u"""
        Defines the text header of a table.
        """
        self.write_tag_noWhitespace(u'thead', True, args)


    def _thead(self):
        self._closeTag_noWhitespace(u'thead')


    def tfoot(self, **args):
        u"""
        Defines the text footer of a table.
        """
        self.write_tag(u'tfoot', True, args)


    def _tfoot(self):
        self._closeTag(u'tfoot')


    def tbody(self, **args):
        u"""
        Defines the text body of a table.
        """
        self.write_tag(u'tbody', True, args)


    def _tbody(self):
        self._closeTag(u'tbody')

    def tr(self, **args):
        u"""
        Defines a row in a table.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_tr.asp" target="external"/></seealso>
        <python>
        self.tr()<br/>
        ...<br/>
        self._tr()
        </python>
        """
        self.write_tag(u'tr', True, args)

    def _tr(self):
        self._closeTag(u'tr')

    def td(self, **args):
        """
        Defines a cell in a table. If the ``rolspan`` or ``colspan`` are not defined or if their value is ``1``
        then the output is ignored.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_td.asp" target="external"/></seealso>
        <python>
        self.td()<br/>
        ...<br/>
        self._td()
        </python>
        """
        self.write_tag_noWhitespace(u'td', True, args)
        #self._debugclass(u'td', self.getClassName(args, self.TD_ATTRIBUTES))

    def _td(self):
        self._closeTag_noWhitespace(u'td')

    def th(self, **args):
        """
        Defines a table header cell in a table. The text within the th element usually renders in bold. If the ``rolspan
        `` or ``colspan`` are not defined or if their value is ``1`` then the output is ignored.
        <br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_th.asp" target="external"/></seealso>
        <python>
        self.th()<br/>
        ...<br/>
        self._th()
        </python>
        """
        self.write_tag_noWhitespace(u'th', True, args)

    def _th(self):
        self._closeTag_noWhitespace(u'th')

    def style(self, type='text/css', **args):
        """
        Defines a style in a document. The style element goes in the head section. If you want to include a style sheet in
        your page, you should define the style sheet externally, and link to it using XHTML ``link`` (note that
        this tag is redefined in XierpaBuilder.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_style.asp" target="external"/></seealso>
        <python>
        self.style()<br/>
        ...<br/>
        self._style()
        </python>
        """
        self.write_tag('style', True, args)

    def _style(self):
        self._closeTag('style')

    def span(self, **args):
        self.write_tag_noWhitespace(u'span', True, args)

    def _span(self):
        self._closeTag_noWhitespace(u'span')

    def div(self, **args):
        """
        The ``div`` tag defines a division/section in a document.<br/>
        <note>Browsers usually place a line break before and after the div element.</note>
        <seealso><www href="http://www.w3schools.com/tags/tag_div.asp" target="external"/></seealso>
        <python>
        self.div()<br/>
        ...<br/>
        self._div()
        </python>
        """
        self.write_tag_noWhitespace(u'div', True, args)

    def _div(self, comment=None):
        self._closeTag_noWhitespace(u'div')
        if comment is not None:
            self.comment(comment)

    def canvas(self, **args):
        """
        The ``canvas`` tag defines a canvas in a document.
        """
        self.write_tag(u'canvas', True, args)
        self._debugclass(u'canvas', self.getClassName(args, self.CANVAS_ATTRIBUTES))

    def _canvas(self):
        self._closeTag(u'canvas')

    def img(self, **args):
        """
        The ``img`` tag defines an image. The ``img`` tag has no block.<br/>
        To avoid compatibility problems between browser with the default ``border`` value,
        it is set to ``0`` if not defined.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_img.asp" target="external"/></seealso>
        **self.img(src='./_image/animage.png', width=100)**.
        If not using online, the replace the url by a local place holder image.
        """
        if not args.get('border'):
            args['border'] = self.C.IMG_DEFAULTBORDER
        if not self.C.useOnline(): # If online, then use the real url. Otherwise local image placeholder
            args['src'] = self.C.URL_IMAGEPLACEHOLDER
        self.write_tag(u'img', False, args)

    def map(self, name):
        self.output(u'<map name="%s">' % name)
        self._pushTag(u'map')

    def _map(self):
        self._closeTag(u'map')

    def area(self, **args):
        if not args.get('border'):
            args['border'] = self.AREA_DEFAULTBORDER
        if args['href']:
            args['href'] = self.e.getPath(args['href'])
        self.write_tag(u'area', False, args)


    def hr(self, **args):
        """
        The ``hr`` tag inserts a horizontal rule.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_hr.asp" target="external"/></seealso>
        <python>
        self.hr(size=15, color='green')
        <hr size="15" color="green"/>
        </python>
        """
        self.write_tag_noWhitespace(u'hr', False, args)


    def a(self, **kwargs):
        """
        The ``a`` tag defines an anchor. An anchor can be used in two ways:<br/>
        <list>
            <sep>To create a link to another document by using the href attribute</sep>
            <sep>To create a bookmark inside a document, by using the name or id attribute</sep>
        </list>
        <todo>Add missing attributes</todo>
        <seealso><www href="http://www.w3schools.com/tags/tag_a.asp"/></seealso>
        <python>
        self.a(href='http://www.xierpa.com', class_='navigationlink'<br/>
        ...<br/>
        self._a()
        </python>
        """
        self.write_tag_noWhitespace(u'a', True, kwargs)

    def _a(self):
        self._closeTag_noWhitespace(u'a')

    def nav(self, **kwargs):
        self.write_tag_noWhitespace(u'nav', True, kwargs)

    def _nav(self):
        self._closeTag_noWhitespace(u'nav')

    def frameset(self, **args):
        """
        The ``frameset`` tag creates an frame set that contains frames with other documents.
        <seealso><www href="http://www.w3schools.com/tags/tag_frameset.asp"/></seealso>
        """
        self.write_tag(u'frameset', True, args)


    def _frameset(self):
        self._closeTag(u'frameset')


    def frame(self, **args):
        """
        The ``frame`` tag defines one particular window (frame) within a frameset.
        Each frame in a frameset can have different attributes, such as border, scrolling, the ability to resize, etc.
        <seealso><www href="http://www.w3schools.com/tags/tag_frame.asp"/></seealso>
        """
        self.write_tag(u'frame', True, args)
        self._debugclass(u'frame', self.getClassName(args, self.FRAME_ATTRIBUTES))


    def _frame(self):
        self._closeTag(u'frame')


    def noframes(self, **args):
        """
        The ``noframes`` tag is used for browsers that do not handle frames.<br/>
        The noframes element can contain all the elements that you can find inside the body element of a normal HTML
        page.<br/>
        The noframes element is most used to link to a non-frameset version of the web site or to display a message to
        users that frames are required.<br/>
        The noframes element goes inside the frameset element.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_noframes.asp"/></seealso>
        """
        self.write_tag(u'noframes', False, args)
        self._debugclass(u'noframes', self.getClassName(args, self.NOFRAMES_ATTRIBUTES))

    def _noframes(self):
        self._closeTag(u'noframes')

    def iframe(self, src, **args):
        """
        The ``iframe`` tag creates an inline frame that contains another document.
        <seealso><www href="http://www.w3schools.com/tags/tag_iframe.asp"/></seealso>
        """
        r = self.result
        r.write(u'<iframe src="%s"' % src)
        self.getandwrite_attributes(u'iframe', args)
        self.output(u'></iframe>')

    def embed(self, **args):
        """
        <error>Does not seem to be defined in w3schools??</error>
        <python>
        self.embed(src='./_images/amovie.qt')
        </python>
        """
        self.write_tag(u'embed', False, args)

    def script(self, charset='UTF-8', type='text/javascript', **args):
        """
        The ``br`` tag inserts a single line break.<br/>
        Defines a script, such as a JavaScript. Note that if @src is used, then no ``self._script()`` must be used.
        The count attribute is not standard XHTML. It indicates the number of ``br`` to repeat.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_script.asp" target="external"/></seealso>
        <python>
        self.script()<br/>
        ...<br/>
        self._script()
        </python>
        """
        #
        #     Build script. Note that if @src is used, then no self._script()
        #     must be used.
        #
        r = self.result.peek()
        r.write(u'<script')
        # Make sure to write "UTF-8" instead of "utf-8" since FireFox 2.0.0.4 will
        # ignore the script otherwise.
        r.write(u' charset="%s"' % charset.upper())
        r.write(u' type="%s"' % type)
        language = args.get(u'language')
        if language is not None:
            r.write(u' language="%s"' % language)
        for key, value in args.items():
            r.write(u' %s="%s"' % (TX.dataAttribute2Html5Attribute(key), value))
        src = args.get(u'src')
        if src is not None:
            r.write(u'></script>\n')
        else:
            self._pushTag(u'script')
            r.write(u'>\n')

    def _script(self):
        self.output(u'\n')
        self._closeTag(u'script')
        self.newline()

    #
    #     L I S T things
    #

    def ul(self, **args):
        """
        The ``ul`` tag defines an unordered list.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_ul.asp" target="external"/></seealso>
        <python>
        self.ul()<br/>
        ...<br/>
        self._ul()
        </python>
        """
        self.write_tag(u'ul', True, args)

    def _ul(self):
        self._closeTag(u'ul')

    def ol(self, **args):
        """
        The ``ol`` tag defines the start of a definition list.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_ol.asp" target="external"/></seealso>
        <python>
        self.ol()<br/>
        ...<br/>
        self._ol()
        </python>
        """
        self.write_tag(u'ol', True, args)


    def _ol(self):
        self._closeTag(u'ol')


    def li(self, **args):
        """
        The ``li`` tag defines the start of a list item. The ``li`` tag is used in both ordered
        (``ol``) and unordered lists (``ul``).
        <seealso><www href="http://www.w3schools.com/tags/tag_li.asp" target="external"/></seealso>
        <python>
        self.li()<br/>
        ...<br/>
        self._li()
        </python>
        """
        self.write_tag_noWhitespace(u'li', True, args)

    def _li(self):
        self._closeTag_noWhitespace(u'li')

    def dl(self, **args):
        """
        The ``dl`` tag defines an unordered list.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_dl.asp" target="external"/></seealso>
        <python>
        self.dl()<br/>
        ...<br/>
        self._dl()
        </python>
        """
        self.write_tag(u'dl', True, args)

    def _dl(self):
        self._closeTag(u'dl')

    def dt(self, **args):
        """
        The ``dt`` tag defines the start of a definition list term.
        The ``dt`` tag is used only in definition lists (``dl``).
        <seealso><www href="http://www.w3schools.com/tags/tag_dt.asp" target="external"/></seealso>
        <python>
        self.dt()<br/>
        ...<br/>
        self._dt()
        </python>
        """
        self.write_tag(u'dt', True, args)

    def _dt(self):
        self._closeTag(u'dt')

    def dd(self, **args):
        """
        The ``dd`` tag defines the start of a definition list term.
        The ``dd`` tag is used only in definition lists (``dl``).
        <seealso><www href="http://www.w3schools.com/tags/tag_dd.asp" target="external"/></seealso>
        <python>
        self.dd()<br/>
        ...<br/>
        self._dd()
        </python>
        """
        self.write_tag(u'dd', True, args)

    def _dd(self):
        self._closeTag(u'dd')


    #
    #     F O R M things
    #

    def form(self, class_=None, name=None, enctype="multipart/form-data", action=None, role=None, method=None,
             onsubmit=None, onreset=None, target=None, style=None, id=None):
        u"""
        The form element creates a form for user input. A form can contain elements such as textfields, checkboxes and
        radio-buttons. Forms are used to pass user data to a specified URL.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_form.asp" target="external"/></seealso>

        If an upload tag is used in the form, then the ``enctype`` attribute should be set to ``
        enctype="multipart/form-data"``
        <python>
        self.form(action=e['path'])<br/>
        ...<br/>
        self._form()
        </python>
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
        self.output(u'<form method="%s" action="%s"' % (method, action))
        if class_ is not None:
            self.output(u' class="%s"' % class_)
        if id is not None:
            self.output(u' id="%s"' % id)
        if role is not None:
            self.output(u' role="%s"' % role)
        if name is not None:
            self.output(u' name="%s"' % name)
        if onsubmit is not None:
            self.output(u' onsubmit="%s"' % onsubmit)
        if enctype is not None:
            self.output(u' enctype="%s"' % enctype)
        if style is not None:
            self.output(u' style="%s"' % style)
        self.output(u' accept-charset="utf-8">')
        # Push as last, so we can see the current tag on the stack
        self._pushTag(u'form')

    def _form(self):
        self._closeTag(u'form')

    def input(self, **args):
        """
        The ``input`` tag defines the start of an input field where the user can enter data.<br/>
        The attribute ``type`` can be one of ``button | checkbox | file | hidden | image | password | radio |
        reset | submit | text``.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_input.asp" target="external"/></seealso>
        <python>
        self.input(type='checkbox', name='mycheckbox')<br/>
        </python>
        """
        self.write_tag(u'input', False, args)

    def label(self, **args):
        """
        The ``label`` tag associates a block of plain text with a form input, usually a check or radio box.
        This way the user can click anywhere in the label text to toggle the input on or off.
        It can be implemented two ways: ``<label><input…> Text</label>``, or ``<label for='id_of_input'>
        Text</label>…<input id='id_of_input' …>``.
        <seealso><www href="http://www.w3schools.com/tags/tag_label.asp" target="external"/></seealso>
        """
        self.write_tag(u'label', True, args)

    def _label(self):
        self._closeTag(u'label')

    def select(self, **args):
        """
        The select element creates a drop-down list.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_select.asp" target="external"/></seealso>
        <python>
        self.select()<br/>
        ...<br/>
        self._select()
        </python>
        """
        self.write_tag(u'select', True, args)

    def _select(self):
        self._closeTag(u'select')

    def option(self, **args):
        """
        The ``option`` tag defines an option in the drop-down list.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_option.asp" target="external"/></seealso>
        <python>
        self.option()<br/>
        ...<br/>
        self._option()
        </python>
        """
        self.write_tag(u'option', True, args)

    def _option(self):
        self._closeTag(u'option')

    def optgroup(self, **args):
        """
        The ``optgroup`` tag defines an option group in the drop-down list.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_optgroup.asp" target="external"/></seealso>
        <python>
        self.optgroup()<br/>
        ...<br/>
        self._optgroup()
        </python>
        """
        self.write_tag(u'optgroup', True, args)

    def _optgroup(self):
        self._closeTag(u'optgroup')

    def button(self, **args):
        """
        ``button`` is the standard XHTML control. It is much like ``input type="button"`` but more
        versatile. It has open and close tags, and can take almost any non-form HTML structure inside.
        <seealso><www href="http://xhtml.com/en/xhtml/reference/button/" target="external"/></seealso>
        """
        self.write_tag(u'button', True, args)

    def _button(self):
        self._closeTag(u'button')

    def textarea(self, **args):
        """
        Defines a text area (a multi-line text input control). A user can write text in the text area. In a text
        area you can write an unlimited number of characters. The default font in the text area is fixed pitch.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_textarea.asp" target="external"/></seealso>
        <python>
        self.textarea()<br/>
        ...<br/>
        self._textarea()
        </python>
        """
        self.write_tag_noWhitespace(u'textarea', True, args) # No tabbing inside the <textarea> tag.

    def _textarea(self):
        self._closeTag_noWhitespace(u'textarea')

    def meta(self, **args):
        """
        The ``meta`` element provides meta-information about your page, such as descriptions and keywords for
        search engines and refresh rates.<br/>
        <seealso><www href="http://www.w3schools.com/tags/tag_meta.asp" target="external"/></seealso>
        <python>
        self.meta()<br/>
        ...<br/>
        self._meta()
        </python>
        """
        self.write_tag(u'meta', False, args)

    def object(self, **args):
        u"""The ``object`` defines an embedded object. Use this element to add
        multimedia to your XHTML page. This element allows you to specify the data and
        parameters for objects inserted into HTML documents, and the code that can be used to
        display/manipulate that data."""
        self.write_tag_noWhitespace(u'object', True, args)

    def _object(self):
        self._closeTag_noWhitespace(u'object')

    def small(self, **args):
        self.write_tag_noWhitespace(u'small', True, args)

    def _small(self):
        self._closeTag_noWhitespace(u'small')

    def big(self, **args):
        self.write_tag_noWhitespace(u'big', True, args)

    def _big(self):
        self._closeTag_noWhitespace(u'big')

    def param(self, **args):
        u"""The param element allows you to specify the run-time settings for an object inserted
        into XHTML documents."""
        self.write_tag(u'param', False, args)

    # N O N - H T M L

    def comment(self, s):
        if s:
            self.output('<!-- %s -->' % TX.object2SpacedString(s))
