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

from pagebot.contexts.platform import getContext
#from pagebot import getMarker
from pagebot.elements import Galley, Image, Ruler, TextBox

class Typesetter(object):

    IMAGE_CLASS = Image
    TEXTBOX_CLASS = TextBox
    RULER_CLASS = Ruler
    GALLEY_CLASS = Galley

    DEFAULT_BULLET = u'•' # Used if no valid bullet string can be found in styles.

    def __init__(self, doc=None, context=None, galley=None, globalDocName=None, globalPageName=None, globalBoxName=None,
            tryExcept=True, verbose=False, writeTags=True):
        u"""
        The Typesetter instance interprets an XML or Markdown file (.md) and converts it into
        a Galley instance, with formatted string depending on the current context.

        >>> from pagebot import getResourcesPath
        >>> from pagebot.document import Document
        >>> from pagebot.elements.element import Element
        >>> path = getResourcesPath() + '/texts/TEST.md'
        >>> doc = Document(autoPages=1, context=getContext())
        >>> t = Typesetter(doc=doc) # Create a new typesetter for this document
        >>> nodeTree = t.typesetFile(path) # Parse the Markdown file into HTML-->nodeTree
        >>> nodeTree.__class__.__name__ # This is an etree root, also called "Element", different class.
        'Element'
        >>> e = Element()
        >>> t.typesetNode(nodeTree, e)

        """
        # Set the doc context of the typesetter. doc be None, in which case it is expected that one of the code blocks
        # will define it in ~~~Python or it is set later by the calling application.
        self.doc = doc
        # Keep track of current page, as may have been defined in code blocks.
        self.page = None
        # The galley can be a Galley or a TextBox instance, if typsetting must go directly into a page element.
        # In that case image elements are added as child, loosing contact with their position in the text.
        # A Galley element keeps that relation, by adding multiple TextBox elements between the images.
        # If galley is None, then create an empty Galley instance, without parent.
        # Note that the single Galley will use the pagebot.contexts.Context as reference.
        # Also note that self.box and self.galley refer to the same object. self.box is used
        # in MarkDown files as reference where text should go.

        # Find the context, in case no doc has be defined yet.
        if context is None and doc is not None:
            context = doc.context
        if context is None:
            context = getContext()
        self.context = context

        if galley is None:
            galley = self.GALLEY_CLASS(context=context)
        self.galley = galley
        # Stack of graphic state as cascading styles. Last is template for the next.
        self.gState = []
        self.tagHistory = []
        # Code block results if any ~~~Python blocks defined in the Markdown file.
        self.globalDocName = globalDocName or 'doc' # Name of global doc to find in code blocks, to be stored in self.doc
        self.globalPageName = globalPageName or 'page'
        self.globalBoxName = globalBoxName = 'box'
        self.codeBlocks = {} # No results for now. Find codeblock result by codeId after typesetting.
        # Save some flags in case the typesetter is running in Python try-except mode.
        self.tryExcept = tryExcept
        self.verbose = verbose
        self.writeTags = writeTags

    def _get_box(self):
        return self.galley
    def _set_box(self, e):
        self.galley = e
    box = property(_get_box, _set_box)

    def getTextBox(self, e=None):
        u"""Answer the current text box, if the width fits the current style.
        If style is omitted, then always answer the current latest text box."""
        return self.galley.getTextBox(e)

    def node_h1(self, node, e):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before.
        # Add invisible h1-marker in the string, to be retrieved by the composer.
        #headerId = self.document.addTocNode(node) # Store the node in the self.document.toc for later TOC composition.
        #self.galley.append(getMarker(node.tag, headerId)) # Link the node tag with the TOC headerId.
        # Typeset the block of the tag.
        self.typesetNode(node, e)

    def node_h2(self, node, e):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before.
        # Add invisible h2-marker in the string, to be retrieved by the composer.
        #headerId = self.document.addTocNode(node) # Store the node in the self.document.toc for later TOC composition.
        #self.galley.append(getMarker(node.tag, headerId)) # Link the node tag with the TOC headerId.
        # Typeset the block of the tag.
        self.typesetNode(node, e)

    def node_h3(self, node, e):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before.
        # Add invisible h3-marker in the string, to be retrieved by the composer.
        #headerId = self.document.addTocNode(node) # Store the node in the self.document.toc for later TOC composition.
        #self.galley.append(getMarker(node.tag, headerId)) # Link the node tag with the TOC headerId.
        # Typeset the block of the tag.
        self.typesetNode(node, e)

    def node_h4(self, node, e):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before.
        # Add invisible h4-marker in the string, to be retrieved by the composer.
        #headerId = self.document.addTocNode(node) # Store the node in the self.document.toc for later TOC composition.
        #self.galley.append(getMarker(node.tag, headerId)) # Link the node tag with the TOC headerId.
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
        self.galley.appendElement(self.RULER_CLASS(e, style=hrStyle)) # Make a new Ruler instance in the Galley

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
        fs = e.newString(s, e=e, style=brStyle)
        self.galley.append(fs) # Add newline in the current setting of FormattedString
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
                #self.galley.append(getMarker('footnote', index))

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
                #self.galley.append(getMarker('literature', index))

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
            result = None # Nothing to return, we handled the references

        else:
            result = self.typesetNode(node, e)

        return result

    def node_li(self, node, e):
        u"""Generate bullet/Numbered list item."""
        context = self.galley.context
        if self.doc is not None:
            bullet = self.doc.css('listBullet')
        else:
            bullet = self.DEFAULT_BULLET # Default, in case doc or css does not exist.
        bulletString = context.newBulletString(bullet) # Get styled string with bullet.
        if bulletString is not None: # HtmlContext does not want a bullet character.
            self.galley.append(bulletString) # Append the bullet as defined in the style.
        # Typeset the block of the tag.
        self.typesetNode(node, e)

    def node_img(self, node, e):
        u"""Process the image. Find nearby empty space on the page to place it,
        possibly intended to fit the w/h ratio of the image and the optional caption.
        A new Image element is created with a PixelMap element and TextBox caption
        element inside. The Image will use style based conditions to define the layout
        interaction between pixelMap and caption."""
        #src = node.attrib.get('src')
        #self.pushStyleTag(node.tag)
        #image = self.IMAGE_CLASS(src) # Set path, image w/h and image caontainer scale from style.
        #self.galley.append(image)
        #captionString = node.get('title')
        #if captionString: # If there is no caption, we can add the Image element directly to the main galley.
        #    caption = self.TEXTBOX_CLASS(captionString)
        #    imageContainer.appendElement(caption)
        # Typeset the empty block of the img, which creates the HTML tag.
        self.htmlNode_(node)

        """
        else:
            # If there is a caption, create a new child Galley to hold image + caption
            g = self.GALLEY_CLASS()
            g.append(imageElement)
            captionStyle = self.getCascadedNodeStyle('caption')
            tb = g.getTextBox(captionStyle)
            caption = node.attrib.get('title')
            # Add invisible marker to the FormattedString, to indicate where the image
            # reference went in a textBox after slicing the string.
            tb.append(caption+'\n', captionStyle)
            tb.append(getMarker(node.tag, src))
            self.galley.append(g)
        """
        #self.popStyleTag()

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

    def runCodeBlock(self, node, execute=True):
        u"""Answer a set of compiled methods, as found in the <code class="Python">...</code>,
        made by Markdown with
        ~~~Python
        cid = 'NameOfBlock'
        doc = Document(w=300, h=500)
        ~~~
        block code. In this case the MacDown and MarkDown extension libraries
        convert this codeblock to
        <pre><code class="Python">
        cid = 'NameOfBlock'
        doc = Document(w=300, h=500)
        </code></pre>
        This way editors can run PageBot generators controlled by content.
        Content result dictionary (per codeblock) is stored in self.codeBlocks[codeId].

        """
        if node.tag != 'code' or not node.attrib.get('class') in ('language-Python', 'Python'):
            # "~~~"" code blocks are skipped.
            # "~~~Python" code blocks are processed by self.
            return None, None

        codeId = 'codeBlock_%d' % (len(self.codeBlocks)+1)
        # Will contain all "global" defined objects in one code block.
        # self.doc contains the Typesetter doc reference, which can be defined in an earlier code block
        result = {self.globalDocName:self.doc, self.globalPageName:self.page, self.globalBoxName:self.box}
        if execute and node.text:
            if not self.tryExcept:
                if self.verbose:
                     print(u'Globals: %s' % result)
                     print(u'Typesetter: %s' % node.text)
                exec(node.text, result) in result # Exectute code block, where result goes dict.
                codeId = result.get('cid', codeId) # Overwrite base codeId, if defined in the block.
                del result['__builtins__'] # We don't need this set of globals in the returned results.
            else:
                error = None
                try:
                    exec(node.text, result) in result # Exectute code block, where result goes dict.
                    codeId = result.get('cid', codeId) # Overwrite base codeId, if defined in the block.
                    del result['__builtins__'] # We don't need this set of globals in the results.
                except TypeError:
                    error = u'TypeError'
                except NameError:
                    error = 'NameError'
                except SyntaxError:
                    error = 'SyntaxError'
                except AttributeError:
                    error = 'AttributeError'
                result['__error__'] = error
                if self.verbose and error is not None:
                    print(u'### %s ### %s' % (error, node.text))

        # doc, page or box may have changed, store them back into the typesetter,
        # so they are available for the execution of a next code block.
        self.doc = result.get(self.globalDocName)
        self.page = result.get(self.globalPageName)
        self.box = result.get(self.globalBoxName)
        # TODO: insert more possible exec() errors here.

        # For convenience, store the source code of the block in the result dict.
        if '__code__' not in result:
            result['__code__'] = node.text

        # Store the result dict as code block. Global values have become dict entries.
        # Make sure that we have a unique codeId (it may have been defined in different
        # markdown files, so sequential index it no guarantee.)
        if codeId in self.codeBlocks:
            n = 0
            codeIdTmp = codeId
            while codeIdTmp in self.codeBlocks:
                codeIdTmp = '%s_%d' % (codeId, n)
                n += 1
            codeId = codeIdTmp # We have a codeId now that does not already exist.
        # Store the result dict in self.codeBlocks under the unique name.
        self.codeBlocks[codeId] = result
        return codeId, result

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
            if self.doc is not None and styleName in self.doc.styles:
                matches.append(styleName)
        matches.reverse()
        return matches

    def getNamedStyle(self, styleName):
        u"""Answer the named style and otherwise an empty style dict if the named style
        does not exist."""
        if self.doc is not None:
            if styleName == 'root':
                return self.doc.getRootStyle()
            return self.doc.getStyle(styleName)
        return {}

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
        u"""Append the string (or BabelString instance) to the current box,
        if it is defined and it has a context. Otherwise add to the existing galley."""
        # Add the tail formatted string to the textBox or galley. Equivalent to self.box.
        if self.galley is not None:
            self.galley.append(bs)
        elif self.verbose:
            print('### Typesetter.append: Cannot append "%s"' % bs)

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
        bs = self.galley.newString(sOrBs, e=e, style=style)
        self.append(bs)
        return bs

    def typesetNode(self, node, e=None):
        u"""Recursively typeset the etree *node*, using a reference to element *e* or the cascading *style*.
        If *e* is None, then the tag style is merged on top of the doc.rootStyle. If *e* is defined, then
        rootstyle of the stack starts with an empty dictionary, leaving root searching for the e.parent path."""

        # Fills self.codeBlocks dictionary from node codeblocks.
        # Side effect is to update self.doc, self.page and self.box
        cid, codeResult = self.runCodeBlock(node)
        if codeResult is not None:
            return

        # Ignore <pre> tag output, as it is part of a ~~~Pyhton code block
        if self.writeTags and node.tag != 'pre':
            # Open the node in HTML export for this node
            self.htmlNode(node)
            # Add this tag to the tag-history line
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
        if self.writeTags and node.tag != 'pre':
            # Close the HTML tag of this node.
            self._htmlNode(node)

        # Now restore the graphic state at the end of the element content processing to the
        # style of the parent in order to process the tail text. Back to the style of the parent,
        # which was in nodeStyle.
        self.popStyle()

    def markDown2XML(self, mdText=None, fileName=None):
        u"""In case the markdown source mdText is defined, use that as content string. Otherwise
        read it from the file indicated by fileName.
        """
        if mdText is None:
            # If we have MarkDown content, convert to XML (XHTML)
            f = codecs.open(fileName, mode="r", encoding="utf-8")
            mdText = f.read()
            f.close()
        else:
            fileName = 'Untitled.md' # Define to make XML saved into XML file.
        mdExtensions = [FencedCodeExtension(), FootnoteExtension(), LiteratureExtension(), Nl2BrExtension()]
        xml = u'<?xml version="1.0" encoding="utf-8"?>\n<document>%s</document>' % markdown.markdown(mdText, extensions=mdExtensions)
        xml = xml.replace('&nbsp;', ' ')
        # If there is an input file name, write the xml into an output file for debugging convenience.
        if fileName is not None:
            fileName = fileName + '.xml' # New file name to XML export
            f = codecs.open(fileName, mode="w", encoding="utf-8")
            f.write(xml)
            f.close()
        return fileName # Answer xml for convenience of the caller.

    def typesetFile(self, fileName, e=None, xPath=None):
        u"""Read the XML document and parse it into a tree of document-chapter nodes. Make the typesetter
        start at page pageNumber and find the name of the flow in the page template.
        The optional filter can be a list of tag names that need to be included in the
        composition, ignoring the rest.
        The optional rootStyle can be defined as style for the root tag, cascading force all
        child elements. Answer the root node for convenience of the caller."""
        fileExtension = fileName.split('.')[-1]
        if fileExtension == 'md':
            fileName = self.markDown2XML(fileName=fileName) # Convert MarkDown file to XML file.

        tree = ET.parse(fileName)
        root = tree.getroot() # Get the root element of the tree.
        # If there is XSL filtering defined, they get the filtered nodes.
        if xPath is not None:
            filteredNodes = root.findall(xPath)
            if filteredNodes:
                # How to handle if there is multiple result nodes?
                self.typesetNode(filteredNodes[0], e)
        else:
            # Collect all flowing text in one formatted string, while simulating the page/flow, because
            # we need to keep track on which page/flow nodes results get positioned (e.g. for toc-head
            # reference, image index and footnote placement.
            self.typesetNode(root, e)
        # Answer the root element of the etree (Note this class also is called "Element", another kind
        # of node than the PageBot Element.
        return root

if __name__ == '__main__':
    import doctest
    doctest.testmod()
