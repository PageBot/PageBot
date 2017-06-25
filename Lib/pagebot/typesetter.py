# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
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
    from pagebot.contributions.markdown.literature import LiteratureExtension
    from pagebot.contributions.markdown.footnotes import FootnoteExtension
except ImportError:
    print 'Typesetter: Install Python markdown from https://pypi.python.org/pypi/Markdown'
    markdown = None

from pagebot import newFS, getMarker
from pagebot.elements import Galley, Image, Ruler, TextBox

class Typesetter(object):

    IMAGE_CLASS = Image
    TEXTBOX_CLASS = TextBox

    def __init__(self, doc, galley):
        self.doc = doc # Doc context of the typesetter.
        self.galley = galley
        self.gState = [] # Stack of graphic state as cascading styles.
     
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
        self.typesetNode(node, e)

    # Solve <br/> best by simple style with: doc.newStyle(name='br', postfix='\n')

    def node_hr(self, node, e):
        u"""Add Ruler instance to the Galley.
        TODO: Need to find a way to address multiple styles here."""
        self.galley.append(Ruler(e)) # Make a new Ruler instance in the Galley

    def node_a(self, node, e):
        u"""Ignore links, but process the block"""
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node)
       
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
        self.typesetNode(node)
 
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
        self.typesetNode(node)
         
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
        bulletString = newFS(self.doc.css('listBullet')) # Get styled string with bullet.
        self.galley.appendString(bulletString) # Append the bullet as defined in the style.
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node, e)

    def node_img(self, node, e):
        u"""Process the image. Find nearby empty space on the page to place it,
        that best fit the w/h ratio of the image and the optional caption.
        A new child Galley is created to hold the combination if there is a caption."""
        src = node.attrib.get('src')
        self.pushStyleTag(node.tag)
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
        self.popStyleTag()
       
    def pushStyleTag(self, tag):
        u"""Push the cascaded style on the gState stack. Make sure that the style is not None and that it 
        is a cascaded style, otherwise it cannot be used as source for child styles. Answer the cascaded 
        style as convenience for the caller. """
        self.gState.append(tag)
        
    def popStyleTag(self):
        u"""Pop the cascaded style from the gState stack and answer the next style that is on top.
        Make sure that there still is a style to pop, otherwise raise an error. """
        assert len(self.gState)
        self.gState.pop()

    def peekStyleTag(self):
        u"""Answer the top cascaded style, without changing the stack."""
        return self.gState[-1]

    def getFootnotes(self, e):
        u"""Answer the footnotes dictionary from the e.lib (derived from the root document)"""
        lib = self.doc.lib
        if lib is not None:
            if not 'footnotes' in lib:
                lib['footnotes'] = {}
            return lib['footnotes']
        return None

    def getLiteratureRefs(self, e):
        u"""Answer the literature reference dictionary from the e.lib (derived from the root document)"""
        lib = self.doc.lib
        if lib is not None:
            if not 'literatureRefs' in lib:
                lib['literatureRefs'] = {}
            return lib['literatureRefs']
        return None

    def getImageRefs(self, e):
        u"""Answer the literature reference dictionary from the e.lib (derived from the root document)"""
        lib = self.doc.lib
        if lib is not None:
            if not 'imageRefs' in lib:
                lib['imageRefs'] = {}
            return lib['imageRefs']
        return None

    def _strip(self, s, prefix=None, postfix=None, forceRightStrip=False):
        u"""Strip the white space from string “s” if prefix and/or postfix are not None.
        Otherwise answer the untouched s."""
        if prefix is not None: # Strip if prefix is not None. Otherwise don't touch.
            s = prefix + (s or '').lstrip() # Force s to empty string in case it is None, to add prefix.
        elif forceRightStrip:
            s = (s or '').rstrip() # Force s to empty string in case it is None.
        elif postfix is not None: # Strip if postfix is not None. Otherwise don't touch.
            s = (s or '').rstrip() + postfix # Force s to empty string in case it is None, to add postfix.
        return s

    def typesetString(self, s, e=None):
        u"""Make sure that s is a formatted string, using element (or doc)e for the style parameters."""
        self.galley.appendString(newFS(s, e))

    def typesetNode(self, node, e=None):
        u"""Recursively typeset the node, using e a reference to the cascading style, doc.styles an the rootStyle."""

        # XML-nodes are organized as: node - node.text - node.children - node.tail
        # If there is no text or if the node does not have tail text, these are None.
        # Still we want to be able to add the prefix to the node.text, so then the text is changed to empty string.
        nodeText = self._strip(node.text)
        if nodeText: # Not None and still has content after stripping?
            fs = newFS(nodeText, e)
            self.galley.appendString(fs) # Add the new formatted string to the current flow textBox

        self.pushStyleTag(node.tag)
        # Type set all child node in the current node, by recursive call.
        for child in node:
            hook = 'node_'+child.tag
            # Method will handle the styled body of the element, but not the tail.
            if hasattr(self, hook):
                # There is a child hook, let this method do the work. 
                getattr(self, hook)(child, e) # Hook must be able to derive styles from e.
                # We are in tail mode now, but we don't know what happened in the child block.
            else:
                # If no method hook defined, then just solve recursively. Child node will get the style.
                self.typesetNode(child, e)

            # XML-nodes are organized as: node - node.text - node.children - node.tail
            # If there is no text or if the node does not have tail text, these are None.
            # Still we want to be able to add the postfix to the tail, so then the tail is changed 
            # to empty string?
            childTail = child.tail #self._strip(child.tail, postfix=style['postfix'])
            if childTail: # Any tail left after stripping, then append to the galley.
                fs = newFS(childTail, e)
                self.galley.appendString(fs)  # Add the tail formatted string to the galley.

        # Now restore the graphic state at the end of the element content processing to the
        # style of the parent in order to process the tail text. Back to the style of the parent.
        self.popStyleTag()

        """
        # If there is a postfix for the current state, then add that to the output.
        postfix = self._strip('', postfix=style['postfix'])
        if postfix:
            fs = newFS(postfix, e, style)
            tb.append(fs) # Add to the current flow textBox

        """
        """
        # XML-nodes are organized as: node - node.text - node.children - node.tail
        # If there is no text or if the node does not have tail text, these are None.
        # Still we want to be able to add the postfix to the tail, so then the tail is changed to empty string.
        nodeTail = self._strip(node.tail, postfix=style['postfix'])
        if nodeTail: # Something of a tail left after stripping?
            fs = newFS(nodeTail, e, style)
            tb.append(fs) # Add to the current flow textBox
        """

    def typesetFile(self, fileName, e=None, xPath=None):
        u"""Read the XML document and parse it into a tree of document-chapter nodes. Make the typesetter
        start at page pageNumber and find the name of the flow in the page template.
        The optional filter can be a list of tag names that need to be included in the 
        composition, ignoring the rest.
        The optional rootStyle can be defined as style for the root tag, cascading force all
        child elements."""
        fileName = self.makeXMLFile(fileName) # Convert to XML if it is not, and use new file name.

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

    def makeXMLFile(self, fileName):
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

    def typesetFilibuster(self, e, blurbNames=None):
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


