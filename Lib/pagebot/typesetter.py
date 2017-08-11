# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
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
    print 'Typesetter: Install Python markdown from https://pypi.python.org/pypi/Markdown'
    markdown = None

from pagebot import newFS, getMarker
from pagebot.elements import Galley, Image, Ruler, TextBox
from pagebot.document import Document

class Typesetter(object):

    IMAGE_CLASS = Image
    TEXTBOX_CLASS = TextBox
    RULER_CLASS = Ruler
    GALLEY_CLASS = Galley

    DEFAULT_BULLET = u'•' # Used if no valid bullet string can be found in styles.

    TAG_MATCHING = {
        'document': [],
        'h1' : ('document',),
        'h2' : ('document', 'h1', 'li'),
        'h3' : ('document', 'h1', 'h2', 'li'),
        'h4' : ('document', 'h1', 'h2', 'h3', 'li'),
        'h5' : ('document', 'h1', 'h2', 'h3', 'h4', 'li'),
        'h6' : ('document', 'h1', 'h2', 'h3', 'h4', 'h5', 'li'),
        'p': ('document', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'),
        'strong': ('document', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'em'),
        'em': ('document', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'strong'),
        'img': ('document', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'strong'),
        'li': ('ul', 'ol'),
        'ul': ('document', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'em'),
    }
    def __init__(self, doc=None, galley=None):
        self._doc = doc # Doc context of the typesetter. Can be None.
        # Galley can also be a TextBox, if typsetting must go directly into a page element. In that case image elements
        # are added as child, loosing contact with their position in the text. A Galley element keeps that relation,
        # by adding multiple TextBox elements between the images.
        # If galley is None, then create an empty Galley instance, without parent.
        if galley is None:
            galley = self.GALLEY_CLASS()
        self.galley = galley 
        # Stack of graphic state as cascading styles. Last is template for the next.
        self.gState = [] 
        self.tagHistory = []
        self.codeBlocks = {} # No results for now. Find codeblock result by codeId after typesetting.

    def _get_doc(self):
        u"""Answer the typesetter self._doc. If it is (still) None, then check if there is a
        doc instance defined in one of the codeblocks. Raise an error if there is 
        more than one doc defined."""
        if self._doc is None: # Not defined, try to find one in the codeblocks result.
            for codeId, result in sorted(self.codeBlocks.items()):
                for resultId, value in sorted(result.items()):
                    if isinstance(value, Document):
                        self.doc = value # Raise an error if mulitple docs are defined.
                        return self._doc
        return self._doc
    def _set_doc(self, doc):
        assert self._doc is None # Don't allow accidental creation or setting of multiple docs.
        self._doc = doc
    doc = property(_get_doc, _set_doc)

    def getTextBox(self, e=None):
        u"""Answer the current text box, if the width fits the current style.
        If style is omitted, then always answer the current latest text box."""
        return self.galley.getTextBox(e)

    def node_h1(self, node, e):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before.
        # Add invisible h1-marker in the string, to be retrieved by the composer.
        #headerId = self.document.addTocNode(node) # Store the node in the self.document.toc for later TOC composition.
        #self.galley.appendString(getMarker(node.tag, headerId)) # Link the node tag with the TOC headerId.
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node, e)

    def node_h2(self, node, e):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before.
        # Add invisible h2-marker in the string, to be retrieved by the composer.
        #headerId = self.document.addTocNode(node) # Store the node in the self.document.toc for later TOC composition.
        #self.galley.appendString(getMarker(node.tag, headerId)) # Link the node tag with the TOC headerId.
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node, e)

    def node_h3(self, node, e):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before.
        # Add invisible h3-marker in the string, to be retrieved by the composer.
        #headerId = self.document.addTocNode(node) # Store the node in the self.document.toc for later TOC composition.
        #self.galley.append(getMarker(node.tag, headerId)) # Link the node tag with the TOC headerId.
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node, e)

    def node_h4(self, node, e):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before.
        # Add invisible h4-marker in the string, to be retrieved by the composer.
        #headerId = self.document.addTocNode(node) # Store the node in the self.document.toc for later TOC composition.
        #self.galley.append(getMarker(node.tag, headerId)) # Link the node tag with the TOC headerId.
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
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
        fs = newFS(s, e, style=brStyle)
        self.galley.appendString(fs) # Add newline in the current setting of FormattedString
        """
    def node_a(self, node, e):
        u"""Ignore links, but process the block"""
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
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
                self.galley.appendString(getMarker('footnote', index))

        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node, e)

    def node_literatureref(self, node, e):
        u"""Collect literature references."""
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
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
                self.galley.appendString(getMarker('literature', index))

        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
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
                        print '### Warning: ', index+1, 'footnote reference not found.', footnotes.keys()
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
                        print '### Warning: ', index+1, 'literature reference not found.', literatureRefs.keys()
            result = None # Nothing to return, we handled the references

        else:
            result = self.typesetNode(node, e)

        return result

    def node_li(self, node, e):
        u"""Generate bullet/Numbered list item."""
        if self.doc is not None:
            bullet = self.doc.css('listBullet')
        else:
            bullet = self.DEFAULT_BULLET # Default, in case doc or css does not exist.
        bulletString = newFS(bullet) # Get styled string with bullet.
        self.galley.appendString(bulletString) # Append the bullet as defined in the style.
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node, e)

    def node_img(self, node, e):
        u"""Process the image. Find nearby empty space on the page to place it,
        possibly intended to fit the w/h ratio of the image and the optional caption.
        A new Image element is created with a PixelMap element and TextBox caption
        element inside. The Image will use style based conditions to define the layout
        interaction between pixelMap and caption."""
        src = node.attrib.get('src')
        #self.pushStyleTag(node.tag)
        imageContainer = self.IMAGE_CLASS(src) # Set path, image w/h and image caontainer scale from style.
        self.galley.appendElement(imageContainer)
        captionString = node.get('title')
        if captionString: # If there is no caption, we can add the Image element directly to the main galley.
            caption = self.TEXTBOX_CLASS(captionString)
            imageContainer.appendElement(caption)
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
        assert len(self.gState)
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

    def runCodeBlocks(self, node, execute=True):
        u"""Answer a set of compiled methods, as found in the <code class="Python">...</code>,
        made by Markdown with 
        ~~~Python
        cid = 'NameOfBlock'
        doc = Document(w=300, h=500)
        ~~~
        block code. In this case the MacDown and MarkDown extension libraries 
        convert this codeblock into 
        <pre><code class="Python">
        cid = 'NameOfBlock'
        doc = Document(w=300, h=500)
        </code></pre>
        This way editors can run PageBot generators controlled by content.
        Content result dictionary (per codeblock) is stored in self.codeBlocks[codeId].

        """
        for index, codeNode in enumerate(node.findall('*//code')):
            if not codeNode.attrib.get('class') == 'Python':
                # "~~~"" code blocks are skipped.
                # "~~~Python" code blocks are processed by self.
                continue
            codeId = 'codeBlock_%d' % index
            result = {} # Will contain all "global" defined objects in one code block.
            try:
                exec(codeNode.text) in result # Exectute code block, where result goes dict.
                codeId = result.get('cid', codeId) # Overwrite base codeId, if defined in the block.
                del result['__builtins__'] # We don't need this set of globals in the results.
            except NameError:
                result = dict(__error__='### NameError', ) # TODO: More error message here.
            except SyntaxError:
                result = dict(__error__='### SyntaxError') # TODO: More error message here.
            # TODO: insert more possible exec() errors here.
            
            # For convenience, store the source code of the block in the result dict.
            if not '__code__' in result:
                result['__code__'] = codeNode.text

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
        #parents = self.TAG_MATCHING.get(tag)
        revHistory = self.tagHistory[:]
        revHistory.reverse()
        matches = []
        for n in range(len(revHistory)):
            styleName = revHistory[:n+1]
            styleName.reverse()
            styleName = ' '.join(styleName)
            if self.doc is not None and styleName in self.doc.styles:
                matches.append(styleName)
        #print tag, parents, revHistory, matches
        #print tag, matches
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

    def typesetString(self, s, e=None, style=None):
        u"""If s is a formatted string, them it is placed untouched. If it is a plain string, then
        use the optional *style* or element *e* (using *e.css(name)*) for searching style parameters. 
        Answer the new formatted string for convenience of the caller. e.g. to measure its size."""
        fs = newFS(s, e, style)
        self.galley.appendString(fs)
        return fs

    def typesetNode(self, node, e=None):
        u"""Recursively typeset the etree *node*, using a reference to element *e* or the cascading *style*.
        If *e* is None, then the tag style is merged on top of the doc.rootStyle. If *e* is defined, then 
        rootstyle of the stack starts with an empty dictionary, leaving root searching for the e.parent path."""

        # Fills self.codeBlocks dictionary from node codeblocks.
        self.runCodeBlocks(node) 

        # Add this tag to the tag-hitstory line
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
            fs = newFS(nodeText, e, nodeStyle)
            self.galley.appendString(fs) # Add the new formatted string to the current flow textBox
        
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
                fs = newFS(childTail, e, nodeStyle)
                self.galley.appendString(fs)  # Add the tail formatted string to the galley.
        
        # Now restore the graphic state at the end of the element content processing to the
        # style of the parent in order to process the tail text. Back to the style of the parent, 
        # which was in nodeStyle.
        self.popStyle()  

        """
        # If there is a postfix for the current state, then add that to the output.
        postfix = style.get('postfix')
        if not postfix and e is not None: # Do we have a style tree?
            postfix = self._strip('', postfix= or e.css('postfix'))

        # XML-nodes are organized as: node - node.text - node.children - node.tail
        # If there is no text or if the node does not have tail text, these are None.
        # Still we want to be able to add the postfix to the tail, so then the tail is changed to empty string.
        nodeTail = self._strip(node.tail, postfix=postfix)
        if nodeTail: # Something of a tail left after stripping?
            fs = newFS(nodeTail, e, nodeStyle)
            self.galley.appendString(fs) # Add to the current flow textBox
        """

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
            mdText = f.read()
            f.close()
            mdExtensions = [FencedCodeExtension(), FootnoteExtension(), LiteratureExtension(), Nl2BrExtension()]
            xml = u'<?xml version="1.0" encoding="utf-8"?>\n<document>%s</document>' % markdown.markdown(mdText, extensions=mdExtensions)
            xml = xml.replace('&nbsp;', ' ')
            fileName = fileName + '.xml' # New file name to XML export
            f = codecs.open(fileName, mode="w", encoding="utf-8")
            f.write(xml)
            f.close()

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
        return root


    def DEPRECATED_makeXMLFile(self, fileName):
        u"""If fileName is pointing to a non-XML file, then try to convert. This needs to be
        extended in the future e.g. to support Word documents or other text resources.
        If the document is already an XML document, then ignore."""
        xml = None # Check is something changed.
        fileExtension = fileName.split('.')[-1].lower()
        if fileExtension == 'xml':
            pass # Ignore, it's already XML
        elif fileExtension == 'md':
            # If we have MarkDown content, convert to XML (XHTML)
            f = codecs.open(fileName, mode="r", encoding="utf-8")
            mdText = f.read()
            f.close()
            mdExtensions = [FootnoteExtension(), LiteratureExtension(), Nl2BrExtension()]
            xml = u'<?xml version="1.0" encoding="UTF-8"?>\n<document>%s</document>' % markdown.markdown(mdText, extensions=mdExtensions)
            xml = xml.replace('&nbsp;', ' ')
        if xml is not None:
            fileName = fileName + '.xml'
            f = codecs.open(fileName, mode="w", encoding="utf-8")
            f.write(xml)
            f.close()
        return fileName # Return altered fileName if converted. Otherwise return original fileName

    def DEPRECATED_typesetFilibuster(self, e, blurbNames=None):
        u"""The typesetFilibuster answers the parsed typeset nodes from a Filibuster blurb. If the blurb
        instances is not given, then create a default Filibuster article."""
        if blurbNames is None: # Nothing supplied: at least create some standard content as article to parse.
            blurbNames = (('h3', 'article_ankeiler'), ('h1', 'article_summary'), ('p', 'article'))
        blurbArticle = []
        from pagebot.contributions.filibuster.blurb import Blurb
        blurb = Blurb()
        for tag, blurbName in blurbNames:
            blurbArticle.append('<%s>%s</%s>\n' % (tag, blurb.getBlurb(blurbName), tag))
        xml = u'<document>%s</document>' % '\n'.join(blurbArticle)
        root = ET.parseString(xml) # Get the root element of the parsed XML tree.
        self.typesetNode(root, e)


