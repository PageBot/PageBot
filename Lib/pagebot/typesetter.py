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
#     typesetter.py
#
import re, copy, codecs, traceback
import xml.etree.ElementTree as ET

try:
    import markdown
    from markdown.extensions.nl2br import Nl2BrExtension
    from markdown.extensions.fenced_code import FencedCodeExtension
except ImportError:
    print('[Typesetter] ImportError: Install Python markdown from https://pypi.python.org/pypi/Markdown')
    print(traceback.format_exc())
    import sys
    sys.exit()

from pagebot.contributions.markdown.literature import LiteratureExtension
from pagebot.contributions.markdown.footnotes import FootnoteExtension
from pagebot.contributions.markdown.inline import InlineExtension

#from pagebot import getMarker
from pagebot.elements import Galley, Image, Ruler, TextBox, CodeBlock
from pagebot.toolbox.units import pt, em
from pagebot.toolbox.color import color, blackColor
from pagebot.constants import *
from pagebot.toolbox.transformer import asIntOrNone


class Typesetter:
    """Mostly used by the Composer, fhe Typesetter takes one or more markdown
    files or a sequence of markdown strings and builds a galley, using a
    dictionary of styles for the formatted string attributes. The result of the
    typesetting is a self.galley, that contains a sequence of Element
    instances, such as formatted images, textboxes (with BabelStrings), ruler
    elements and other nested galleys."""
    IMAGE_CLASS = Image
    TEXTBOX_CLASS = TextBox
    RULER_CLASS = Ruler
    GALLEY_CLASS = Galley
    CODEBLOCK_CLASS = CodeBlock

    DEFAULT_BULLET = '•\t' # Used if no valid bullet string can be found in styles.
    SKIP_TAGS = ('document',
        'pre', # Ignore as part of a code block
        'figure', 'figcaption', # Not implemented by all browsers. Use ![]()*Caption* instead.
    )

    # Default styles for Typesetter, based on the standard markdown HTML-tags
    # Some ugly colors to show that we're in default mode here, for the user to
    # supply a better set.
    DEFAULT_STYLES = dict(
        document=dict(font='Georgia', fontSize=pt(10), leading=em(1.2), textFill=blackColor),
        dropcap=dict(font='Verdana', fontSize=pt(64), leading=em(1.2), textFill=color(1, 0, 0)),
        h1=dict(font='Verdana', fontSize=pt(18), leading=em(1.2), textFill=color(1, 0, 0)),
        h2=dict(font='Verdana', fontSize=pt(16), leading=em(1.2), textFill=color(1, 0, 0.5)),
        h3=dict(font='Georgia', fontSize=pt(14), leading=em(1.2), textFill=color(1, 0.5, 0.5)),
        h4=dict(font='Georgia', fontSize=pt(12), leading=em(1.2), textFill=color(0, 1, 1)),
        h5=dict(font='Georgia-Bold', fontSize=pt(10), leading=em(1.2), textFill=(1, 0, 1)),
        p=dict(font='Georgia', fontSize=pt(10), leading=em(1.2), textFill=(0.5, 1, 0.5)),
        bullet=dict(font='Georgia', fontSize=pt(10), leading=em(1.2), textFill=(0.5, 1, 0.5)),
        li=dict(font='Verdana', fontSize=pt(10), leading=em(1.2), textFill=color(0.5)),
        em=dict(font='Georgia-Bold'),
    )
    MARKDOWN_EXTENSIONS = [
        # These extension are needed to make PageBot markdown compatible with
        # default MacDown behavior.
        InlineExtension(),
        FencedCodeExtension(),
        FootnoteExtension(),
        LiteratureExtension(),
        Nl2BrExtension(),
    ]

    def __init__(self, context, styles=None, galley=None, skipTags=None, tryExcept=True,
            return2Space=False, tabs2Space=False, br2Return=True, stripHead=False,
            stripTail=False):
        """The Typesetter instance interprets an XML or Markdown file (.md) and
        converts it into a Galley instance with formatted string depending on
        the current context.

        >>> from pagebot import getResourcesPath
        >>> from pagebot.toolbox.units import em, pt
        >>> from pagebot.toolbox.color import color, blackColor
        >>> from pagebot.contexts.htmlcontext import HtmlContext
        >>> context = HtmlContext()
        >>> h1Style = dict(font='Verdana', fontSize=pt(24), textFill=color(1, 0, 0))
        >>> h2Style = dict(font='Georgia', fontSize=pt(18), textFill=color(1, 0, 0.5))
        >>> h3Style = dict(font='Georgia', fontSize=pt(14), textFill=color(0, 1, 0))
        >>> pStyle = dict(font='Verdana', fontSize=pt(10), leading=em(1.4), textFill=blackColor)
        >>> styles = dict(h1=h1Style, h2=h2Style, p=pStyle)
        >>> t = Typesetter(context, styles=styles) # Create a new typesetter for this context
        >>> mdText = '''
        ... ~~~Python
        ... box = page.select['content']
        ... ~~~
        ... # H1 header
        ... ## H2 header
        ... ### H3 header
        ... ~~Delete~~
        ... _Underline_
        ... ==Mark==
        ... *Em*
        ... "Quote"
        ... **Strong**
        ... //Emphasis//
        ... ^Sup
        ... !!Sub
        ... '''
        >>> galley = t.typesetMarkdown(mdText)
        >>> len(galley.elements)
        3
        """
        self.context = context
        # Find the context, in case no doc has be defined yet.
        if galley is None:
            galley = self.GALLEY_CLASS(context=context)
        self.galley = galley

        if styles is None:
            styles = self.DEFAULT_STYLES
        self.styles = styles # Style used, in case the current text box does not have them.

        # Stack of graphic state as cascading styles. Last is template for the next.
        self.gState = []
        self.tagHistory = [] # Sequential list of all tags that passed parsing
        self.tagStack = [] # Stack of currently active tag names.
        # Save some flags in case the typesetter is running in Python try-except mode.
        self.tryExcept = tryExcept
        # If True add tags to the output, otherwise ignore. Can be overwritten by caller for debugging.
        self.writeTags = context.useTags
        self.root = None # Will contain the root node after executing typesetFile.

        # Some MarkDown generated tags need to be skipped on output, while
        # their content still is processed.
        if skipTags is None:
            skipTags = self.SKIP_TAGS
        self.skipTags = skipTags

        # Flags how to filter white space
        self.return2Space = return2Space # If True (default), then all \r will be replaced by ' '
        self.tabs2Space = tabs2Space # If False, then \t is preserved into <tab/> and later converted back into '\t
        self.br2Return = br2Return # If True, the <br/> will be replaced by '\r'
        self.stripHead = stripHead # If there is trailing white space a string, then strip it.
        self.stripTail = stripTail # If there is tail white space in a string, then strip it

        self.currentImage = None # Keep the last processed image, in case there are captions to add.

    def node_tab(self, node, e):
        """Non-HTML tag, substituted from \t, now convert back into \t."""
        self.append('\t')

    def dropcap(self, node, e):
        context = self.context
        style = self.styles.get('dropcap')

    def getStyleValue(self, name, e=None, style=None, default=None):
        """Answers the best style value match for *name*, depending on the
        status of *style*, *e* and *default*, in that order. Answer None if
        everything fails."""
        value = None

        if style is not None:
            value = style.get(name)
        if value is None and e is not None:
            value = e.css(name)
        if value is None:
            value = default
        return value

    # Solve <br/> best by simple style with: doc.newStyle(name='br', postfix='\n')

    def node_br(self, node, e):
        """Add newline instance to the Galley."""
        if self.br2Return:
            context = self.context
            style = self.styles.get('br') or self.styles.get('p')
            bs = context.newString('\r', style=style)
            self.append(bs)
        else:
            self.typesetNode(node, e)

    def node_a(self, node, e):
        """Ignore links, but process the block"""
        # Typeset the block of the tag.
        self.typesetNode(node, e)

    def node_sup(self, node, e):
        """Collect footnote references on their page number.
        And typeset the superior footnote index reference."""
        nodeId = node.attrib.get('id')
        # Check if this is a footnote reference
        if nodeId is not None and nodeId.startswith('fnref'): # This is a footnote reference.
            footnotes = self.getFootnotes(e)
            if footnotes is not None:
                nodeId = nodeId.split(':')[1]
                index = len(footnotes)+1
                # Footnode['p'] content node will be added if <div class="footnote">...</div> is detected.
                footnotes[index] = dict(nodeId=nodeId, index=index, node=node, e=e, p=None)
                # Add invisible mark, so we can scan the text after page composition to find
                # on which page it ended up.
                #self.append(getMarker('footnote', index))

        # Typeset the block of the tag.
        self.typesetNode(node, e)

    def node_literatureref(self, node, e):
        """Collect literature references."""
        # Typeset the block of the tag.
        # Check if this is a literature reference
        nodeId = node.attrib.get('id')
        if nodeId.startswith('litref:'): # It is a literature reference.
            literatureRefs = self.getLiteratureRefs(e)
            if literatureRefs:
                nodeId = nodeId.split(':')[1]
                index = len(literatureRefs)+1
                # Warning if the reference id is already used.
                assert not nodeId in literatureRefs
                # Make literature reference entry. Content <p> and split fields will be added later.
                literatureRefs[index] = dict(nodeId=nodeId, node=node, e=e, p=None, pageIds=[])
                #self.append(getMarker('literature', index))

        # Typeset the block of the tag.
        self.typesetNode(node, e)

    def node_div(self, node, e):
        """MarkDown generates <div class="footnote">...</div> and <div
        class="literature">...</div> as output at the end of the HTML export.
        We will handle them separately by looking them up in the XML-tree. So
        we'll skip them in the regular flow process."""

        if node.attrib.get('class') == 'footnote':
            # Find the content of the footnotes. Store the content and add marker.
            footnotes = self.getFootnotes(e)
            if footnotes is not None:
                for index, p in enumerate(node.findall('./ol/li/p')):
                    if index+1 in footnotes:
                        # Store the content as node, so we can process it with a Typesetter in case of child nodes.
                        footnotes[index+1]['p'] = p
                    else:
                        print('### Warning: %d footnote reference not found. %s' % (index+1, footnotes.keys()))
            result = None # Nothing to return, we handled the references

        elif node.attrib.get('class') == 'literature':
            literatureRefs = self.getLiteratureRefs(e)
            if literatureRefs:
                for index, p in enumerate(node.findall('./ol/li/p')):
                    if index+1 in literatureRefs:
                        # Store the content as node, so we can process it with a Typesetter in case of child nodes.
                        # Spltting fields inside the p content will be done by the calling application or Composer.
                       literatureRefs[index+1]['p'] = p
                    else:
                        print('### Warning: %d literature reference not found. %s' % (index+1, literatureRefs.keys()))

        else:
            self.typesetNode(node, e)

    def node_ul(self, node, e):
        context = self.galley.context
        style = self.styles.get('ul')
        if style is not None:
            s = context.newString('\n', style=style)
            self.append(s)
        self.typesetNode(node, e)
        if style is not None:
            self.append(s)

    def node_li(self, node, e):
        """Generate bullet/Numbered list item."""
        context = self.galley.context
        bulletStyle = self.styles.get('bullet') or self.styles.get('li') or self.styles.get('p')
        bullet = bulletStyle.get('listBullet', self.DEFAULT_BULLET)
        # Only defined for non-HTML.
        bulletString = context.newBulletString(bullet+'\t', e=e, style=bulletStyle) # Get styled string with bullet.
        if bulletString is not None:
            self.append(bulletString) # Append the bullet as defined in the style.
        # Typeset the block of the tag.
        self.typesetNode(node, e)

    # For now, using the full figure tag as HTML in Markdown does not work, as
    # <figure> and <figcaption> are not supported by all browsers.
    # <figure class="inlineImage">
    #   <img src="images/myImage.png" alt="Alt text here"/>
    #   <figcaption>Caption here</figcaption>
    # </figure>
    #
    IMAGE_CACHE_WIDTH = re.compile('w=([012345679]*)')
    IMAGE_CACHE_HEIGHT = re.compile('h=([012345679]*)')
    IMAGE_CACHE_XALIGN = re.compile('x=([a-z]*)')
    IMAGE_CACHE_YALIGN = re.compile('y=([a-z]*)')
    # TODO: Add parameter ro prevent scaling

    def node_img(self, node, e):
        """Process the image. adding the img tag or a new image element to the
        galley.  The alt attribute can contain additional information for the
        Image element.  Keep the Image element in self.currentImage, in case we
        need to add captions.

        If there is a "w=<number>" pattern in the alt-attribute, then use it as
        width measurement for creating a cached image. This way an author can
        control the required size from within the content.

        Markdown could use code such as ![MyImage w=450](images/myImage.jpg)

        If one or both if (w, h) are defined, then set the imageScale flag accordingly.
        """
        w = ww = h = hh = xAlign = yAlign = None # Values are optional set by alt content.
        proportional = not (w is not None and h is not None) # Not proportional if both are defined.
        path = node.attrib.get('src')
        alt = node.attrib.get('alt')
        if alt:
            xAlign = (self.IMAGE_CACHE_XALIGN.findall(alt) or [None])[0] # x=center
            yAlign = (self.IMAGE_CACHE_YALIGN.findall(alt) or [None])[0] # y=top
            w = asIntOrNone((self.IMAGE_CACHE_WIDTH.findall(alt)  or [None])[0]) # w=800
            h = asIntOrNone((self.IMAGE_CACHE_HEIGHT.findall(alt)  or [None])[0]) # h=800
        doScale = not path.endswith('.'+FILETYPE_SVG) and not path.endswith('.'+FILETYPE_GIF)
        # doScale = doScale or w is not None or h is not None
        self.currentImage = self.IMAGE_CLASS(path=path, parent=self.galley,
            scaleImage=doScale, # Scale the image if one or both (w, h) is defined.
            xAlign=xAlign, yAlign=yAlign, w=w, h=h, alt=alt, proportional=proportional,
            index=node.attrib.get('index', 0))

    def node_caption(self, node, e):
        """If there is a self.currentImage set, then redirect output of the
        caption nodes into the image, instead of the self.galley. Otherwise
        just output as plain text, ignoring the caption tag. Multiple captions
        are added to the the current image until it is changed. The caption
        tag is triggered by *[[...]]* in MarkDown.
        """
        if self.currentImage is not None: # In case there is a current image, attach caption to it.
            savedGalley = self.galley # Temporary redirect node parent
            self.galley = self.currentImage
            self.typesetNode(node, e)
            self.galley = savedGalley
        else:
            self.typesetNode(node, e)

    def node_code(self, node, e):
        """Creates a NodeBlock element that contains the code source, to be
        executed by the Composer in sequence of composition."""
        self.CODEBLOCK_CLASS(node.text, parent=self.galley)

    def pushStyle(self, style):
        """Pushes the cascaded style on the gState stack. Makes sure that the
        style is not None and that it is a cascaded style, otherwise it cannot
        be used as source for child styles. Answers the cascaded style."""
        self.gState.append(style)

    def popStyle(self):
        """Pop the cascaded style from the gState stack and answer the next
        style that is on top. Make sure that there still is a style to pop,
        otherwise raise an error. """
        assert self.gState
        self.gState.pop()
        return self.peekStyle()

    def peekStyle(self):
        """Answers the top cascaded style, without changing the stack."""
        if not self.gState: # It's empty, answer None
            return None
        return self.gState[-1]

    def addHistory(self, tag):
        """Add the *tag* to the history."""
        if not self.tagHistory or tag != self.tagHistory[-1]:
            self.tagHistory.append(tag)

    def getHistory(self):
        return self.tagHistory

    def getFootnotes(self, e):
        """Answers the footnotes dictionary from the e.lib (derived from the root document)"""
        if self.doc is not None:
            lib = self.doc.lib
            if lib is not None:
                if not 'footnotes' in lib:
                    lib['footnotes'] = {}
                return lib['footnotes']
        return None

    def getLiteratureRefs(self, e):
        """Answers the literature reference dictionary from the e.lib (derived
        from the root document)"""
        if self.doc is not None:
            lib = self.doc.lib
            if lib is not None:
                if not 'literatureRefs' in lib:
                    lib['literatureRefs'] = {}
                return lib['literatureRefs']
        return None

    def getImageRefs(self, e):
        """Answers the image reference dictionary from the e.lib (derived from
        the root document) if it exists. Otherwise create an empty
        e.lib['imageRefs'] and answer it as empty dictionary. Answer None if
        e.lib does not exist."""
        lib = e.lib
        if lib is not None:
            if not 'imageRefs' in lib:
                lib['imageRefs'] = {}
            return lib['imageRefs']
        return None

    def _strip(self, s, prefix=None, postfix=None):
        """Strip the white space from string *s* if *prefix* and/or *postfix* are not None.
        Otherwise answer the untouched *s*."""
        s = s or ''
        if self.stripHead:
            s = s.lstrip()
        if self.stripTail:
            s = s.rstrip()
        if prefix is not None: # Strip if prefix is not None. Otherwise don't touch.
            s = str(prefix or '') + s
        if postfix is not None:
            s += str(postfix or '')
        return s

    def getMatchingStyleNames(self, tag):
        """Answers the list of matching style, with decreasing relevance."""
        revHistory = self.tagHistory[:]
        revHistory.reverse()
        matches = []
        for n in range(len(revHistory)):
            styleName = revHistory[:n+1]
            styleName.reverse()
            styleName = ' '.join(styleName)
            style = self.getNamedStyle(styleName)
            if style:
                matches.append(styleName)
        matches.reverse()
        return matches

    def getNamedStyle(self, styleName):
        """Answers the named style and otherwise an empty style dict if the
        named style does not exist."""
        return self.styles.get(styleName, {})

    def getRootStyle(self):
        for name in ('root', 'document', 'body', 'p'):
            if name in self.styles:
                return self.getNamedStyle(name)
        return {}

    def getNodeStyle(self, tag):
        """Makes a copy of the top of the style graphics state and mew *style*
        into it. Answer the new style. This can be used to match custom tag
        names (such as <dropcap>...</dropcap> to a style with the same name.
        """
        if self.peekStyle() is None: # Not an initialized stack, use doc.rootStyle as default.
            # Happens if calling directly, without check on e or non-existing style for a node.
            self.pushStyle(self.getRootStyle())
        mergedStyle = copy.copy(self.peekStyle())
        # Find the best matching style for tag on order of relevance,
        # considering the possible HTML tag parents and the history.
        for styleName in self.getMatchingStyleNames(tag):
            nodeStyle = self.getNamedStyle(styleName)
            if nodeStyle: # Not None and not empty
                for name, value in nodeStyle.items():
                    mergedStyle[name] = value
                break
        return mergedStyle

    def append(self, bs):
        """Append the string (or BabelString instance) to the last textbox in
        galley, if it exists. Otherwise create a new TextBox and add it to
        self.galley."""
        if self.galley.elements and self.galley.elements[-1].isTextBox:
            box = self.galley.elements[-1]
            if box.bs is None:
                box.bs = bs
            else:
                box.bs += bs
        elif hasattr(bs, 's'):
            while bs.s and bs.s[0] in ' \t\n\r':
                bs.s = bs.s[1:]
            self.TEXTBOX_CLASS(bs, parent=self.galley)
        else:
            self.TEXTBOX_CLASS(bs, parent=self.galley)

    def htmlNode(self, node, end=False):
        """Open the tag in HTML output and copy the node attributes if there are any."""
        htmlTag = u'<%s' % node.tag
        attrs = []
        for name, value in node.items():
            if name == 'src' and value.startswith('docs/'): # Exception hack to bridge the .md --> img url.
                value = value[5:]
            attrs.append('%s="%s"' % (name, value))
        if attrs:
            htmlTag += u' '+u' '.join(attrs)
        if end:
            htmlTag += '/'
        htmlTag += '>'
        self.append(htmlTag)

    def _htmlNode(self, node):
        """Close the html tag of node."""
        self.append('</%s>' % node.tag)

    def htmlNode_(self, node):
        """Opem+close the html tag of node."""
        self.htmlNode(node, end=True)

    def typesetString(self, sOrBs, e=None, style=None):
        """If s is a formatted string, then it is placed untouched. If it is a
        plain string, then use the optional *style* or element *e* (using
        *e.css(name)*) for searching style parameters.  Answer the new
        formatted string for convenience of the caller. e.g. to measure its
        size."""
        # Only convert if not yet BabelString instance.
        bs = self.context.newString(sOrBs, e=e, style=style)
        self.append(bs)
        return bs

    def typesetNode(self, node, e=None):
        """Recursively typeset the etree *node*, using a reference to element
        *e* or the cascading *style*. If *e* is None, then the tag style is
        merged on top of the doc.rootStyle. If *e* is defined, then rootstyle
        of the stack starts with an empty dictionary, leaving root searching
        for the e.parent path."""

        # Ignore <pre> tag output, as it is part of a ~~~Pyhton ... ~~~ code block
        if self.writeTags and not node.tag in self.skipTags:
            # Open the node in HTML export for this node
            self.htmlNode(node)

        # Add this tag to the tag-history line. It is used to connect to the right style in case
        # we are rendering towards a FormattedString or another context-equivalent.
        self.addHistory(node.tag)

        # If e is undefined, then we make sure that the stack contains the doc.rootStyle on top.
        # If e is defined then root queries for style should follow the e.parent path.
        if self.peekStyle() is None and e is not None:
            # Root of stack is empty style, to force searching on the e.parent line.
            self.pushStyle({}) # Define top level for styles.
        nodeStyle = self.getNodeStyle(node.tag) # Merge found tag style with current top of stack
        self.pushStyle(nodeStyle) # Push this merged style on the stack

        # XML-nodes are organized as: node - node.text - node.children - node.tail
        # If there is no text or if the node does not have tail text, these are None.
        # Still we want to be able to add the prefix to the node.text, so then the text is changed to an empty string.

        nodeText = self._strip(node.text)
        if nodeText: # Not None and still has content after stripping?
            # Don't cache the context from self.galley as variable, as it may become dynamically updated by code blocks.
            # The galley context will define the type of BabelStrings generated by the Typesetter.
            firstTagIndent = nodeStyle.get('firstTagIndent')
            if firstTagIndent is not None and len(self.tagHistory) > 2 and self.tagHistory[-2] != '_'+node.tag:
                nodeStyle['firstLineIndent'] = firstTagIndent
            bs = self.context.newString(nodeText, e=e, style=nodeStyle)
            self.append(bs)

        self.tagStack.append(node.tag) # Add current node to the stack

        # Type set all child node in the current node, by recursive call.
        for child in node:
            hook = 'node_'+child.tag
            # Method will handle the styled body of the element, but not the tail.
            if hasattr(self, hook):
                # There is a hook for this node, let this method do the work.
                getattr(self, hook)(child, e) # Hook must be able to derive styles from e.
                # We are in tail mode now, but we don't know what happened in the child block.
            else:
                # If no method hook defined, then just solve recursively. Child node will get the style.
                self.typesetNode(child, e)
            # XML-nodes are organized as: node - node.text - node.children - node.tail
            # If there is no text or if the node does not have tail text, these are None.
            # Still we want to be able to add the postfix to the tail, so then the tail is changed
            # to empty string?
            childTail = self._strip(child.tail)
            #childTail = child.tail #self._strip(child.tail, postfix=self.getStyleValue('postfix', e, nodeStyle, ''))
            if childTail: # Any tail left after stripping, then append to the galley.
                # Don't cache the context from self.galley as variable, as it may become dynamically updated by code blocks.
                bs = self.context.newString(childTail, e=e, style=nodeStyle)
                self.append(bs)

        self.tagStack.pop() # Pop current node from the list.

        # Add this closing tag to the tag-history line. It is used to test on difference between the
        # last closed tag and the current tag, e.g. to control the firstTagIndent --> firtLineIndent.
        self.addHistory('_'+node.tag)

        # Ignore </pre> tag output, as it is part of a ~~~Pyhton code block
        if self.writeTags and not node.tag in self.skipTags:
            # Close the HTML tag of this node.
            self._htmlNode(node)

        # Now restore the graphic state at the end of the element content processing to the
        # style of the parent in order to process the tail text. Back to the style of the parent,
        # which was in nodeStyle.
        self.popStyle()

    def markDown2XmlFile(self, fileName, mdText, mdExtensions=None):
        """Take the markdown source, convert to HTML/XML and save in the file
        called fileName. If the fileName does not end with ".xml" extension,
        then add it. Answer the (new) fileName.

        >>> import os
        >>> from pagebot.contexts.htmlcontext import HtmlContext
        >>> md = '''## Subtitle at start\\n\\n~~~\\npage = page.next\\n~~~\\n\\n# Title\\n\\n##Subtitle\\n\\nPlain text'''
        >>> context = HtmlContext()
        >>> t = Typesetter(context)
        >>> fileName = t.markDown2XmlFile('/tmp/PageBot_Typesetter_test.xml', md)
        >>> os.remove(fileName)
        """
        if mdExtensions is None:
            mdExtensions = self.MARKDOWN_EXTENSIONS

        if not self.tabs2Space: # Otherwise MarkDown will auto-convert
            mdText = mdText.replace('\t', '<tab/>') # Keep the tabs, as they get replaced into spaced by MarkDown

        xmlBody = markdown.markdown(mdText, extensions=mdExtensions)
        xml = u'<?xml version="1.0" encoding="utf-8"?>\n<document>%s</document>' % xmlBody

        if self.return2Space:
            for c1, c2 in (('\r', ' '), ('\n', ' '), ('&nbsp;', ' ')):
                xml = xml.replace(c1, c2) # Replace all returns by tabs. Paragraphs should be made with <p> and <br/>
            xml += '\r'

        if not fileName.endswith('.xml'):
            fileName = fileName + '.xml' # Make sure file name has xml extension.
        f = codecs.open(fileName, mode="w", encoding="utf-8") # Save the XML as unicode.
        f.write(xml)
        f.close()
        return fileName

    def typesetMarkdown(self, mdText, mdExtensions=None, e=None, xPath=None):
        tmpPath = '/tmp/PageBot_Typesetter.xml'
        fileName = self.markDown2XmlFile(tmpPath, mdText, mdExtensions)
        self.typesetFile(fileName, e=e, xPath=xPath)
        #os.remove(tmpPath)
        return self.galley

    def typesetFile(self, fileName, e=None, xPath=None):
        """Read the XML document and parse it into a tree of document-chapter
        nodes. Make the typesetter start at page pageNumber and find the name
        of the flow in the page template.  The optional filter can be a list of
        tag names that need to be included in the composition, ignoring the
        rest.

        The optional rootStyle can be defined as style for the root tag,
        cascading force all child elements. Answer the root node for
        convenience of the caller."""
        fileExtension = fileName.split('.')[-1]
        if fileExtension == 'md':
            # If we have MarkDown content, convert to XML (XHTML)
            f = codecs.open(fileName, mode="r", encoding="utf-8")
            mdText = f.read() # Read the raw MarkDown source
            f.close()
            fileName = self.markDown2XmlFile(fileName, mdText) # Translate MarkDown to HTML and save in file.
        tree = ET.parse(fileName)
        self.root = tree.getroot() # Get the root element of the tree and store for later retrieval.

        # If there is XSL filtering defined, they get the filtered nodes.
        if xPath is not None:
            filteredNodes = self.root.findall(xPath)
            if filteredNodes:
                # How to handle if we got multiple result nodes?
                self.typesetNode(filteredNodes[0], e)
        else:
            # Collect all flowing text in one formatted string, while
            # simulating the page/flow, because we need to keep track on which
            # page/flow nodes results get positioned (e.g. for toc-head
            # reference, image index and footnote placement.
            self.typesetNode(self.root, e)

        # Answer the self.galley as convenience for the caller.
        return self.galley

if __name__ == '__main__':
    import doctest
    doctest.testmod()
