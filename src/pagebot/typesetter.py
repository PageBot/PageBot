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
from lxml.etree import XPath

import markdown
from markdown.extensions.nl2br import Nl2BrExtension
from markdown.extensions.footnotes import FootnoteExtension

import pagebot
reload(pagebot)
from pagebot import getFormattedString, getMarker

import pagebot.md.literature
reload(pagebot.md.literature)
from pagebot.md.literature import LiteratureExtension

import pagebot.md.footnotes
reload(pagebot.md.footnotes)
from pagebot.md.footnotes import FootnoteExtension

import pagebot.elements
reload(pagebot.elements)
from pagebot.elements import Galley, Image

class Typesetter(object):

    GALLEY_CLASS = Galley
    IMAGE_CLASS = Image

    def __init__(self, document, galley):
        # TODO: Maybe Typesetter does not need a document.
        self.document = document
        self.galley = galley
        self.gState = [document.getRootStyle()] # Stack of graphic state as cascading styles.
     
    def getTextBox(self, style=None):
        u"""Answer the current text box, if the width fits the current style.
        If style is omitted, then always answer the current latest text box."""
        return self.galley.getTextBox(style)

    def node_h1(self, node):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before. 
        # Add invisible h2-marker in the string, to be retrieved by the composer.
        cStyle = self.getCascadedNodeStyle(node.tag)
        tb = self.getTextBox(cStyle) # Get the latest galley text box. Answer new if width changed.
        headerId = self.document.addTocNode(node) # Store the node in the self.document.toc for later TOC composition.
        tb.append(getMarker(node.tag, headerId)) # Link the node tag with the TOC headerId.
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node, cStyle)

    def node_h2(self, node):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before. 
        # Add invisible h2-marker in the string, to be retrieved by the composer.
        cStyle = self.getCascadedNodeStyle(node.tag)
        tb = self.getTextBox(cStyle) # Get the latest galley text box. Answer new if width changed.
        headerId = self.document.addTocNode(node) # Store the node in the self.document.toc for later TOC composition.
        tb.append(getMarker(node.tag, headerId)) # Link the node tag with the TOC headerId.
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node, cStyle)

    def node_h3(self, node):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before. 
        # Add invisible h3-marker in the string, to be retrieved by the composer.
        cStyle = self.getCascadedNodeStyle(node.tag)
        tb = self.getTextBox(cStyle) # Get the latest galley text box. Answer new if width changed.
        headerId = self.document.addTocNode(node) # Store the node in the self.document.toc for later TOC composition.
        tb.append(getMarker(node.tag, headerId)) # Link the node tag with the TOC headerId.
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node, cStyle)
        
    def node_h4(self, node):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before. 
        # Add invisible h3-marker in the string, to be retrieved by the composer.
        cStyle = self.getCascadedNodeStyle(node.tag)
        tb = self.getTextBox(cStyle) # Get the latest galley text box. Answer new if width changed.
        headerId = self.document.addTocNode(node) # Store the node in the self.document.toc for later TOC composition.
        tb.append(getMarker(node.tag, headerId)) # Link the node tag with the TOC headerId.
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node, cStyle)

    def node_em(self, node):
        cStyle = self.getCascadedNodeStyle(node.tag)
        self.typesetNode(node, cStyle)

    # Solve <br/> best by simple style with: doc.newStyle(name='br', postfix='\n')

    def node_hr(self, node):
        u"""Add Ruler instance to the Galley.
        TODO: Need to find a way to address multiple styles here."""
        cStyle = self.getCascadedNodeStyle(node.tag)
        self.galley.newRuler(cStyle) # Make a new Ruler instance in the Galley

    def node_a(self, node):
        u"""Ignore links, but process the block"""
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node)
       
    def XXXnode_sup(self, node):
        u"""Collect footnote references on their page number.
        And typeset the superior footnote index reference."""
        cStyle = self.getCascadedNodeStyle(node.tag)
        nodeId = node.attrib.get('id')
        # Check if this is a footnote reference
        if nodeId.startswith('fnref'): # This is a footnote reference.
            footnotes = self.document.footnotes
            nodeId = nodeId.split(':')[1]
            index = len(footnotes)+1
            # Footnode['p'] content node will be added if <div class="footnote">...</div> is detected.
            footnotes[index] = dict(nodeId=nodeId, index=index, node=node, style=cStyle, p=None)
            tb = self.getTextBox(cStyle)
            # Add invisible mark, so we can scan the text after page composition to find
            # on which page it ended up.
            tb.fs += getMarker('footnote', index) 

        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node)
 
    def node_literatureref(self, node):
        u"""Collect literature references."""
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        # Check if this is a literature reference
        cStyle = self.getCascadedNodeStyle(node.tag)
        nodeId = node.attrib.get('id')
        
        if nodeId.startswith('litref:'): # It is a literature reference.
            literatureRefs = self.document.literatureRefs
            nodeId = nodeId.split(':')[1]
            index = len(literatureRefs)+1
            # Warning if the reference id is already used.
            assert not nodeId in literatureRefs
            # Make literature reference entry. Content <p> and split fields will be added later.
            literatureRefs[index] = dict(nodeId=nodeId, node=node, style=cStyle, p=None)
            tb = self.getTextBox(cStyle)
            tb.fs += getMarker('literature', index)

        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node)
         
    def node_div(self, node):
        u"""MarkDown generates <div class="footnote">...</div> and <div class="literature">...</div>
        as output at the end of the HTML export. We will handle them separately by looking them up 
        in the XML-tree. So we'll skip them in the regular flow process."""

        if node.attrib.get('class') == 'footnote':
            # Find the content of the footnotes. Store the content and add marker.
            footnotes = self.document.footnotes
            for index, p in enumerate(node.findall('./ol/li/p')):
                if index+1 in footnotes:
                    # Store the content as node, so we can process it with a Typesetter in case of child nodes.
                    footnotes[index+1]['p'] = p
                else:
                    print '### Warning: ', index+1, 'footnote reference not found.', footnotes.keys()
            result = None # Nothing to return, we handled the references

        elif node.attrib.get('class') == 'literature':
            literatureRefs = self.document.literatureRefs
            for index, p in enumerate(node.findall('./ol/li/p')):
                if index+1 in literatureRefs:
                    # Store the content as node, so we can process it with a Typesetter in case of child nodes.
                    # Spltting fields inside the p content will be done by the calling application or Composer.
                   literatureRefs[index+1]['p'] = p
                else: 
                    print '### Warning: ', index+1, 'literature reference not found.', literatureRefs.keys()
            result = None # Nothing to return, we handled the references

        else:
            result = self.typesetNode(node)

        return result

    def node_li(self, node):
        u"""Generate bullet/Numbered list item."""
        # Make sure this is a cascaded style, expanded from current values in top style in gState.
        cStyle = self.getCascadedNodeStyle(node.tag)
        tb = self.getTextBox(cStyle) # Get the latest galley text box. Answer new if width changed.
        bulletString = getFormattedString(cStyle['listBullet'], cStyle) # Make styled string with bullet.
        tb.append(bulletString) # Append the bullet as defined in the style.
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node, cStyle)

    def node_img(self, node):
        u"""Process the image. Find nearby empty space on the page to place it,
        that best fit the w/h ratio of the image and the optional caption.
        A new child Galley is created to hold the combination if there is a caption."""
        src = node.attrib.get('src')
        imageStyle = self.getCascadedNodeStyle(node.tag)
        if imageStyle is not None:
            self.pushStyle(imageStyle)
        imageElement = self.IMAGE_CLASS(src, imageStyle) # Set path, image w/h and image scale from style.
        caption = node.attrib.get('title')
        if 1 or caption is None:
            # If there is no caption, we can add the Image element directly to the main galley.
            self.galley.append(imageElement)
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
        if imageStyle is not None:
            self.popStyle()

    def getCascadedStyle(self, style):
        u"""As we want cascading font and fontSize in the page elements, we need to keep track
        of the stacking of XML-hierarchy of the previous tag styles.
        The styles can omit the font or fontSize, and still we need to be able to set the element
        attributes. Copy the current style and add overwrite the values from the new style.
        This way the current style always contains all attributes of the root style."""
        cascadedStyle = copy.copy(self.gState[-1]) # Take a copy of the top of the gState stack as source.
        if style is not None: # Style may be None. In that case answer just the copy, which is already cascaded.
            for name, value in style.items():
                cascadedStyle[name] = value # Overwrite the value from altering tag style.
            # Mark that this is a cascaded style now, to distinguish from individual plain tag styles.
            # Since the style copy is cascaded by definition, we still set the flag just in case
            # the tag style had it set to False.
            # The flag is also used to verify that only cascaded styles get added to the gState stack.
            cascadedStyle['cascaded'] = True
        return cascadedStyle

    def getCascadedNodeStyle(self, name):
        u"""Answer the cascaded named style, if it exists. Otherwise answer the root style
        (which is already cascaded by definition)."""
        style = self.document.getStyle(name)
        if style is None : # If there is not style defined for this node,
            style = {} # just use an empty dictionary, so it gets the whole of the gstate top.
            # There is style with that name. Answer it, if already cascaded.
        # Make a copy and cascade the style (filling in the missing values) from the top of the gState stack.
        return self.getCascadedStyle(style)
        
    def pushStyle(self, cascadedStyle):
        u"""Push the cascaded style on the gState stack. Make sure that the style is not None and that it 
        is a cascaded style, otherwise it cannot be used as source for child styles. Answer the cascaded 
        style as convenience for the caller. """
        assert cascadedStyle is not None and cascadedStyle.get('cascaded')
        self.gState.append(cascadedStyle)
        return cascadedStyle
        
    def popStyle(self):
        u"""Pop the cascaded style from the gState stack and answer the next style that is on top.
        Make sure that there still is a style to pop, otherwise raise an error. """
        assert len(self.gState)
        self.gState.pop()
        return self.peekStyle() # Answer the current style as convenience for the caller.

    def peekStyle(self):
        u"""Answer the top cascaded style, without changing the stack."""
        return self.gState[-1]

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

    def typesetNode(self, node, style=None):
        u"""Recursively typeset the node, using style. Style can be None, in which case we'll try to
        find if there is a style related to node.tag.
        If there is a valid style, make sure it is cascaded and push it on the graphics state.
        This way automatic cascading values are in the style answered by the push."""
        if style is None:
            style = self.getCascadedNodeStyle(node.tag)
        else: # If for some reason this is an un-cascaded plain style. Make it cascaded. Otherwise don't touch.
            style = self.getCascadedStyle(style)
        self.pushStyle(style)

        # Get current flow text box from Galley to fill. Style can be None. If the width of the
        # latest textBox.w is not equal to style['w'], then create a new textBox in the galley.
        tb = self.getTextBox(style)

        # XML-nodes are organized as: node - node.text - node.children - node.tail
        # If there is no text or if the node does not have tail text, these are None.
        # Still we want to be able to add the prefix to the node.text, so then the text is changed to empty string.
        nodeText = self._strip(node.text, prefix=style['prefix'])
        if nodeText: # Not None and still has content after stripping?
            fs = getFormattedString(nodeText, style)
            tb.append(fs) # Add the new formatted string to the current flow textBox

        # Type set all child node in the current node, by recursive call.
        for child in node:
            hook = 'node_'+child.tag
            # Method will handle the styled body of the element, but not the tail.
            if hasattr(self, hook):
                getattr(self, hook)(child) # Hook must be able to derive style from node.
                # We are on tail mode now, but we don't know what happened in the child block.
                # So, to be sure, we'll push the current style again.
                childTail = self._strip(child.tail, postfix=style['postfix'])
                if childTail: # Any tail left after stripping, then append to the current textBox.
                    # Get current flow text box from Galley to fill. If may have changed, if another
                    # element was created by the tree of nodes, e.g an image or table. If the latest
                    # galley element is still a flow, and if the current width of the textBox is
                    # equal to style['w'] then continue using the same. Otherwise a new textBox
                    # is created by the galley.
                    fs = getFormattedString(childTail, style)
                    tb = self.getTextBox(style)
                    tb.append(fs)  # Add the tail formatted string to the current flow textBox
            else:
                # If no method hook defined, then just solve recursively. Child node will get the style.
                self.typesetNode(child)

        # If the current style has postfix, then add this to output string.
        XXX = self._strip(node.tail, postfix=style['postfix'])
        # Restore the graphic state at the end of the element content processing to the
        # style of the parent in order to process the tail text.
        # Back to the style for the tail of this tag, which is the style of the parent.
        style = self.popStyle()

        # XML-nodes are organized as: node - node.text - node.children - node.tail
        # If there is no text or if the node does not have tail text, these are None.
        # Still we want to be able to add the postfix to the tail, so then the tail is changed to empty string.
        nodeTail = self._strip(node.tail, postfix=style['postfix'])
        if nodeTail: # Something of a tail left after stripping?
            fs = getFormattedString(nodeTail, style)
            tb.append(fs) # Add to the current flow textBox


    def typesetFile(self, fileName, rootStyle=None, xPath=None):
        u"""Read the XML document and parse it into a tree of document-chapter nodes. Make the typesetter
        start at page pageNumber and find the name of the flow in the page template.
        The optional filter can be a list of tag names that need to be included in the 
        composition, ignoring the rest.
        The optional rootStyle can be defined as style for the root tag, cascading force all
        child elements."""
        fileExtension = fileName.split('.')[-1]
        if fileExtension == 'md':
            # If we have MarkDown content, conver to HTNK/XML
            f = codecs.open(fileName, mode="r", encoding="utf-8")
            mdText = f.read()
            f.close()
            mdExtensions = [FootnoteExtension(), LiteratureExtension(), Nl2BrExtension()]
            xml = '<document>%s</document>' % markdown.markdown(mdText, extensions=mdExtensions)
            xmlName = fileName + '.xml'
            f = codecs.open(xmlName, mode="w", encoding="utf-8")
            f.write(xml)
            f.close()
            fileName = xmlName

        tree = ET.parse(fileName)
        root = tree.getroot() # Get the root element of the tree.
        # If there is XSL filtering defined, they get the filtered nodes.
        if xPath is not None:
            filteredNodes = root.findall(xPath)
            if filteredNodes:
                # How to handle if there is multiple result nodes?
                self.typesetNode(filteredNodes[0], style=rootStyle)
        else:
            # Collect all flowing text in one formatted string, while simulating the page/flow, because
            # we need to keep track on which page/flow nodes results get positioned (e.g. for toc-head
            # reference, image index and footnote placement.   
            self.typesetNode(root, style=rootStyle)

    def typesetFootnotes(self):
        footnotes = self.document.footnotes
        for index, (page, e, p) in footnotes.items():
            style = page.getStyle('footnote')
            fs = getFormattedString('%d ' % index, style)
            tb = page.findElement('footnote')
            if tb is not None:
                self.typesetNode(p, page, style)

