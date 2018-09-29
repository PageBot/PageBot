#!/usr/bin/env python
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
import os
import copy
import codecs
import xml.etree.ElementTree as ET

try:
    import markdown
    from markdown.extensions.nl2br import Nl2BrExtension
    from markdown.extensions.fenced_code import FencedCodeExtension
    from pagebot.contributions.markdown.literature import LiteratureExtension
    from pagebot.contributions.markdown.footnotes import FootnoteExtension
except ImportError:
    print('[Typesetter] ImportError: Install Python markdown from https://pypi.python.org/pypi/Markdown')
    import sys
    sys.exit()

#from pagebot import getMarker
from pagebot.elements import Galley, Image, Ruler, TextBox, CodeBlock
from pagebot.toolbox.units import pt, em
from pagebot.toolbox.color import color, blackColor


class Typesetter:
    u"""Mostly used by the Composer, fhe Typesetter takes one or more markdown files or a sequence
    of markdown strings and builds a galley, using a dictionary of styles for the formatted string
    attributes. The result of the typesetting is a self.galley, that contains a sequence of Element
    instances, such as formatted images, textboxes (with BabelStrings), ruler elements and other
    nested galleys.
    """
    IMAGE_CLASS = Image
    TEXTBOX_CLASS = TextBox
    RULER_CLASS = Ruler
    GALLEY_CLASS = Galley
    CODEBLOCK_CLASS = CodeBlock

    DEFAULT_BULLET = u'•' # Used if no valid bullet string can be found in styles.
    SKIP_TAGS = ('document', 'pre')

    # Default styles for Typesetter, based on the standard markdown HTML-tags
    # Some ugly colors to show that we're in default mode here, for the user to
    # supply a better set.
    DEFAULT_STYLES = dict(
        body=dict(font='Georgia', fontSize=pt(10), leading=em(1.2), textFill=blackColor),
        h1=dict(font='Verdana', fontSize=pt(18), leading=em(1.2), textFill=color(1, 0, 0)),
        h2=dict(font='Verdana', fontSize=pt(16), leading=em(1.2), textFill=color(1, 0, 0.5)),
        h3=dict(font='Georgia', fontSize=pt(14), leading=em(1.2), textFill=color(1, 0.5, 0.5)),
        h4=dict(font='Georgia', fontSize=pt(12), leading=em(1.2), textFill=color(0, 1, 1)),
        h5=dict(font='Georgia-Bold', fontSize=pt(10), leading=em(1.2), textFill=(1, 0, 1)),
        p=dict(font='Georgia', fontSize=pt(10), leading=em(1.2), textFill=(0.5, 1, 0.5)),
        li=dict(font='Verdana', fontSize=pt(10), leading=em(1.2), textFill=color(0.5)),
        em=dict(font='Georgia-Bold'),
    )
    MARKDOWN_EXTENSIONS = [FencedCodeExtension(), FootnoteExtension(), LiteratureExtension(), Nl2BrExtension()]

    def __init__(self, context, styles=None, galley=None, skipTags=None,
            imageAsElement=False, tryExcept=True):
        u"""
        The Typesetter instance interprets an XML or Markdown file (.md) and converts it into
        a Galley instance, with formatted string depending on the current context.

        >>> from pagebot import getResourcesPath
        >>> from pagebot.toolbox.units import em, pt
        >>> from pagebot.toolbox.color import color, blackColor
        >>> from pagebot import getContext
        >>> context = getContext()
        >>> path = getResourcesPath() + '/texts/TEST.md' # Get the path to the text markdown.
        >>> h1Style = dict(font='Verdana', fontSize=pt(24), textFill=color(1, 0, 0))
        >>> h2Style = dict(font='Georgia', fontSize=pt(18), textFill=color(1, 0, 0.5))
        >>> pStyle = dict(font='Verdana', fontSize=pt(10), leading=em(1.4), textFill=blackColor)
        >>> styles = dict(h1=h1Style, h2=h2Style, p=pStyle)
        >>> t = Typesetter(context, styles=styles) # Create a new typesetter for this context
        >>> galley = t.typesetFile(path) # Context indicates hiding of the tags in the output
        >>> len(galley.elements)
        7
        >>> # First element of test-markdown is a code block or text box
        >>> galley.elements[0].__class__.__name__
        'TextBox'
        >>> galley.elements[1].__class__.__name__ # Second element is code block
        'CodeBlock'
        >>> from pagebot.contexts.htmlcontext import HtmlContext
        >>> context = HtmlContext()
        >>> t = Typesetter(context, styles=styles) # Create a new typesetter with a HTML context
        >>> galley = t.typesetFile(path) # Context indicates is to include the HTML tags in output.
        >>> len(galley.elements)
        7
        >>> 'What is PageBot' in galley.elements[2].bs # Skip first code block in test-markdown
        True
        """
        self.context = context
        # Find the context, in case no doc has be defined yet.
        if galley is None:
            galley = self.GALLEY_CLASS(context=context)
        self.galley = galley

        if styles is None:
            styles = self.DEFAULT_STYLES
        self.styles = styles # Style used, in case the current text box does not have them.

        self.imageAsElement = imageAsElement # If True, add the image as element. Otherwise embed as tag.

        # Stack of graphic state as cascading styles. Last is template for the next.
        self.gState = []
        self.tagHistory = []
        # Save some flags in case the typesetter is running in Python try-except mode.
        self.tryExcept = tryExcept
        # If True add tags to the output, otherwise ignore. Can be overwritten by caller for debugging.
        self.writeTags = context.useTags
        self.root = None # Will contain the root node after executing typesetFile.

        # Some MarkDown generated tags need to be skipped on output, while their content still is processed.
        if skipTags is None:
            skipTags = self.SKIP_TAGS
        self.skipTags = skipTags

    def node_h1(self, node, e):
        u"""Handle the <h1> tag."""
        # Add line break to whatever style/content there was before.
        # Add invisible h1-marker in the string, to be retrieved by the composer.
        #headerId = self.document.addTocNode(node) # Store the node in the self.document.toc for later TOC composition.
        #self.append(getMarker(node.tag, headerId)) # Link the node tag with the TOC headerId.
        # Typeset the block of the tag.
        self.typesetNode(node, e)

    def node_h2(self, node, e):
        u"""Handle the <h2> tag."""
        # Add line break to whatever style/content there was before.
        # Add invisible h2-marker in the string, to be retrieved by the composer.
        #headerId = self.document.addTocNode(node) # Store the node in the self.document.toc for later TOC composition.
        #self.append(getMarker(node.tag, headerId)) # Link the node tag with the TOC headerId.
        # Typeset the block of the tag.
        self.typesetNode(node, e)

    def node_h3(self, node, e):
        u"""Handle the <h3> tag."""
        # Add line break to whatever style/content there was before.
        # Add invisible h3-marker in the string, to be retrieved by the composer.
        #headerId = self.document.addTocNode(node) # Store the node in the self.document.toc for later TOC composition.
        #self.append(getMarker(node.tag, headerId)) # Link the node tag with the TOC headerId.
        # Typeset the block of the tag.
        self.typesetNode(node, e)

    def node_h4(self, node, e):
        u"""Handle the <h4> tag."""
        # Add line break to whatever style/content there was before.
        # Add invisible h4-marker in the string, to be retrieved by the composer.
        #headerId = self.document.addTocNode(node) # Store the node in the self.document.toc for later TOC composition.
        #self.append(getMarker(node.tag, headerId)) # Link the node tag with the TOC headerId.
        # Typeset the block of the tag.
        self.typesetNode(node, e)

    def node_h5(self, node, e):
        u"""Handle the <h5> tag."""
        # Add line break to whatever style/content there was before.
        # Add invisible h4-marker in the string, to be retrieved by the composer.
        #headerId = self.document.addTocNode(node) # Store the node in the self.document.toc for later TOC composition.
        #self.append(getMarker(node.tag, headerId)) # Link the node tag with the TOC headerId.
        # Typeset the block of the tag.
        self.typesetNode(node, e)

    def node_em(self, node, e):
        u"""Handle the <em> tag"""
        self.typesetNode(node, e)

    def node_p(self, node, e):
        u"""Handle the <p> tag."""
        self.typesetNode(node, e)

    def node_hr(self, node, e):
        u"""Add Ruler instance to the Galley."""
        if self.peekStyle() is None and e is not None:
            # Root of stack is empty style, to force searching on the e.parent line.
            self.pushStyle({}) # Define top level for styles.
        hrStyle = self.getNodeStyle(node.tag) # Merge found tag style with current top of stack
        self.RULER_CLASS(e, style=hrStyle, parent=self.galley) # Make a new Ruler instance in the Galley

    def getStyleValue(self, name, e=None, style=None, default=None):
        u"""Answer the best style value match for *name*, depending on the status of *style*, *e* and *default*,
        on that order. Answer None if everything failes."""
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
        u"""Add newline instance to the Galley."""
        # For now, just ignore, as <br/> already get a break in MarkDown, as part of the exclosing tag.
        # TODO: now <br/> makes the same vertical spacing as <p>
        """
        if self.peekStyle() is None and e is not None:
            # Root of stack is empty style, to force searching on the e.parent line.
            self.pushStyle({}) # Define top level for styles.
        brStyle = self.getNodeStyle(node.tag) # Merge found tag style with current top of stack
        s = self.getStyleValue('prefix', e, brStyle, default='') + '\n' + self.getStyleValue('postfix', e, brStyle, default='')
        bs = self.context.newString(s, e=e, style=brStyle)
        self.append(bs) # Add newline in the current setting of FormattedString
        """
    def node_a(self, node, e):
        u"""Ignore links, but process the block"""
        # Typeset the block of the tag.
        self.typesetNode(node, e)

    def node_sup(self, node, e):
        u"""Collect footnote references on their page number.
        And typeset the superior footnote index reference."""
        nodeId = node.attrib.get('id')
        # Check if this is a footnote reference
        if nodeId.startswith('fnref'): # This is a footnote reference.
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
        u"""Collect literature references."""
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
        u"""MarkDown generates <div class="footnote">...</div> and <div class="literature">...</div>
        as output at the end of the HTML export. We will handle them separately by looking them up
        in the XML-tree. So we'll skip them in the regular flow process."""

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


    def node_li(self, node, e):
        u"""Generate bullet/Numbered list item."""
        context = self.galley.context
        bullet = self.DEFAULT_BULLET # Default, in case doc or css does not exist.
        style = self.styles.get('bullet') or self.styles.get('li') or self.styles.get('p')
        bulletString = context.newBulletString(bullet, e=e, style=style) # Get styled string with bullet.
        if bulletString is not None: # HtmlContext does not want a bullet character.
            self.append(bulletString) # Append the bullet as defined in the style.
        # Typeset the block of the tag.
        self.typesetNode(node, e)

    def node_img(self, node, e):
        u"""Process the image. adding the img tag or a new image element to the galley."""
        # Typeset the empty block of the img, which creates the HTML tag.
        if self.imageAsElement:
            self.galley.appendElement(self.IMAGE_CLASS(path=node.attrib.get('src'), index=0))
        else:
            self.htmlNode_(node)

    def node_code(self, node, e):
        self.CODEBLOCK_CLASS(node.text, parent=self.galley)

    def pushStyle(self, tag):
        u"""Push the cascaded style on the gState stack. Make sure that the style is not None and that it
        is a cascaded style, otherwise it cannot be used as source for child styles. Answer the cascaded
        style as convenience for the caller. """
        self.gState.append(tag)

    def popStyle(self):
        u"""Pop the cascaded style from the gState stack and answer the next style that is on top.
        Make sure that there still is a style to pop, otherwise raise an error. """
        assert self.gState
        self.gState.pop()
        return self.peekStyle()

    def peekStyle(self):
        u"""Answer the top cascaded style, without changing the stack."""
        if not self.gState: # It's empty, answer None
            return None
        return self.gState[-1]

    def addHistory(self, tag):
        u"""Add the *tag* to the history."""
        if not self.tagHistory or tag != self.tagHistory[-1]:
            self.tagHistory.append(tag)

    def getHistory(self):
        return self.tagHistory

    def getFootnotes(self, e):
        u"""Answer the footnotes dictionary from the e.lib (derived from the root document)"""
        if self.doc is not None:
            lib = self.doc.lib
            if lib is not None:
                if not 'footnotes' in lib:
                    lib['footnotes'] = {}
                return lib['footnotes']
        return None

    def getLiteratureRefs(self, e):
        u"""Answer the literature reference dictionary from the e.lib (derived from the root document)"""
        if self.doc is not None:
            lib = self.doc.lib
            if lib is not None:
                if not 'literatureRefs' in lib:
                    lib['literatureRefs'] = {}
                return lib['literatureRefs']
        return None

    def getImageRefs(self, e):
        u"""Answer the image reference dictionary from the e.lib (derived from the root document)
        if it exists. Otherwise create an empty e.lib['imageRefs'] and answer it as empty dictionary.
        Answer None if e.lib does not exist."""
        lib = e.lib
        if lib is not None:
            if not 'imageRefs' in lib:
                lib['imageRefs'] = {}
            return lib['imageRefs']
        return None

    def _strip(self, s, prefix=None, postfix=None, forceRightStrip=False):
        u"""Strip the white space from string *s* if *prefix* and/or *postfix* are not None.
        Otherwise answer the untouched *s*."""
        if prefix is not None: # Strip if prefix is not None. Otherwise don't touch.
            s = prefix + (s or '').lstrip() # Force s to empty string in case it is None, to add prefix.
        elif forceRightStrip:
            s = (s or '').rstrip() # Force s to empty string in case it is None.
        elif postfix is not None: # Strip if postfix is not None. Otherwise don't touch.
            s = (s or '').rstrip() + postfix # Force s to empty string in case it is None, to add postfix.
        return s

    def getMatchingStyleNames(self, tag):
        u"""Answer the list of matching style, with decreasing relevance."""
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
        u"""Answer the named style and otherwise an empty style dict if the named style
        does not exist."""
        return self.styles.get(styleName, {})

    def getNodeStyle(self, tag):
        u"""Make a copy of the top of the style graphics state and mew *style* into it. Answer the new style."""
        if self.peekStyle() is None: # Not an initialized stack, use doc.rootStyle as default.
            self.pushStyle(self.getNamedStyle('root')) # Happens if calling directly, without check on e
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
        u"""Append the string (or BabelString instance) to the last textbox in galley,
        if it exists. Otherwise create a new TextBox and add it to self.galley."""
        if self.galley.elements and self.galley.elements[-1].isTextBox:
            self.galley.elements[-1].bs += bs
        else:
            self.TEXTBOX_CLASS(bs, parent=self.galley)

    def htmlNode(self, node, end=False):
        u"""Open the tag in HTML output and copy the node attributes if there are any."""
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
        u"""Close the html tag of node."""
        self.append('</%s>' % node.tag)

    def htmlNode_(self, node):
        u"""Opem+close the html tag of node."""
        self.htmlNode(node, end=True)

    def typesetString(self, sOrBs, e=None, style=None):
        u"""If s is a formatted string, then it is placed untouched. If it is a plain string, then
        use the optional *style* or element *e* (using *e.css(name)*) for searching style parameters.
        Answer the new formatted string for convenience of the caller. e.g. to measure its size."""
        # Only convert if not yet BabelString instance.
        bs = self.context.newString(sOrBs, e=e, style=style)
        self.append(bs)
        return bs

    def typesetNode(self, node, e=None):
        u"""Recursively typeset the etree *node*, using a reference to element *e* or the cascading *style*.
        If *e* is None, then the tag style is merged on top of the doc.rootStyle. If *e* is defined, then
        rootstyle of the stack starts with an empty dictionary, leaving root searching for the e.parent path."""

        # Ignore <pre> tag output, as it is part of a ~~~Pyhton code block
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
            bs = self.context.newString(nodeText, e=e, style=nodeStyle)
            self.append(bs)

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
            childTail = child.tail #self._strip(child.tail, postfix=self.getStyleValue('postfix', e, nodeStyle, ''))
            if childTail: # Any tail left after stripping, then append to the galley.
                # Don't cache the context from self.galley as variable, as it may become dynamically updated by code blocks.
                bs = self.context.newString(childTail, e=e, style=nodeStyle)
                self.append(bs)

        # Ignore </pre> tag output, as it is part of a ~~~Pyhton code block
        if self.writeTags and not node.tag in self.skipTags:
            # Close the HTML tag of this node.
            self._htmlNode(node)

        # Now restore the graphic state at the end of the element content processing to the
        # style of the parent in order to process the tail text. Back to the style of the parent,
        # which was in nodeStyle.
        self.popStyle()

    def markDown2XmlFile(self, fileName, mdText, mdExtensions=None):
        u"""Take the markdown source, convert to HTML/XML and save in the file called fileName.
        If the fileName does not end with ".xml" extension, then add it. Answer the (new) fileName.

        >>> from pagebot.contexts.htmlcontext import HtmlContext
        >>> md = '''## Subtitle at start\\n\\n~~~\\npage = page.next\\n~~~\\n\\n# Title\\n\\n##Subtitle\\n\\nPlain text'''
        >>> context = HtmlContext()
        >>> t = Typesetter(context)
        >>> fileName = t.markDown2XmlFile('/tmp/PageBot_Typesetter_test.xml', md)
        >>> os.remove(fileName)
        """
        if mdExtensions is None:
            mdExtensions = self.MARKDOWN_EXTENSIONS
        xmlBody = markdown.markdown(mdText, extensions=mdExtensions)
        xml = u'<?xml version="1.0" encoding="utf-8"?>\n<document>%s</document>' % xmlBody
        xml = xml.replace('&nbsp;', ' ')
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
        os.remove(tmpPath)
        return self.galley

    def typesetFile(self, fileName, e=None, xPath=None):
        u"""Read the XML document and parse it into a tree of document-chapter nodes. Make the typesetter
        start at page pageNumber and find the name of the flow in the page template.
        The optional filter can be a list of tag names that need to be included in the
        composition, ignoring the rest.
        The optional rootStyle can be defined as style for the root tag, cascading force all
        child elements. Answer the root node for convenience of the caller."""
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
            # Collect all flowing text in one formatted string, while simulating the page/flow, because
            # we need to keep track on which page/flow nodes results get positioned (e.g. for toc-head
            # reference, image index and footnote placement.
            self.typesetNode(self.root, e)

        # Answer the self.galley as convenience for the caller.
        return self.galley

if __name__ == '__main__':
    import doctest
    doctest.testmod()
