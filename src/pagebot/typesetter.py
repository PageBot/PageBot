# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in Drawbot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     typesetter.py
#
import copy
import codecs
import xml.etree.ElementTree as ET

import markdown
from markdown.extensions.nl2br import Nl2BrExtension
from markdown.extensions.footnotes import FootnoteExtension

import pagebot
reload(pagebot)
from pagebot import getFormattedString, getMarker

import pagebot.literature
reload(pagebot.literature)
from pagebot.literature import LiteratureExtension

import pagebot.elements
reload(pagebot.elements)
from pagebot.elements import Galley, Image

class Typesetter(object):
    
    def __init__(self, document, galley):
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
        tb.append(getMarker(node.tag, cStyle))
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node, cStyle)

    def node_h2(self, node):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before. 
        # Add invisible h2-marker in the string, to be retrieved by the composer.
        cStyle = self.getCascadedNodeStyle(node.tag)
        tb = self.getTextBox(cStyle) # Get the latest galley text box. Answer new if width changed.
        tb.append(getMarker(node.tag, cStyle))
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node, cStyle)

    def node_h3(self, node):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before. 
        # Add invisible h3-marker in the string, to be retrieved by the composer.
        cStyle = self.getCascadedNodeStyle(node.tag)
        tb = self.getTextBox(cStyle) # Get the latest galley text box. Answer new if width changed.
        tb.append(getMarker(node.tag, cStyle))
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node, cStyle)
        
    def node_h4(self, node):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before. 
        # Add invisible h3-marker in the string, to be retrieved by the composer.
        cStyle = self.getCascadedNodeStyle(node.tag)
        tb = self.getTextBox(cStyle) # Get the latest galley text box. Answer new if width changed.
        tb.append(getMarker(node.tag, cStyle))
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node, cStyle)

    def node_br(self, node):
        u"""Add line break to the formatted string."""
        cStyle = self.getCascadedNodeStyle(node.tag)
        tb = self.getTextBox(cStyle) # Get the latest galley text box. Answer new if width changed.
        tb.append('\n', cStyle)# + getMarker(node.tag)

    def node_hr(self, node):
        u"""Add Ruler instance to the Galley.
        TODO: Need to find a way to address multiple styles here."""
        cStyle = self.getCascadedNodeStyle(node.tag)
        self.galley.newRuler(cStyle) # Make a new Ruler instance in the Galley

    def node_a(self, node):
        u"""Ignore links, but process the block"""
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node)
        
    def node_sup(self, node):
        u"""Collect footnote references on their page number.
        And typeset the superior footnote index reference."""
        cStyle = self.getCascadedNodeStyle(node.tag)
        nodeId = node.attrib.get('id')
        if nodeId.startswith('fnref'): # This is a footnote reference.
            footnotes = self.document.footnotes
            footnotes[len(footnotes)+1] = [node, cStyle]
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node, cStyle)
 
    def node_literatureref(self, node):
        u"""Collect literature references."""
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node)
         
    def node_div(self, node):
        u"""MarkDown generates <div class="footnote">...</div> and <div class="literature">...</div>
        as output, but we will handle them separately by looking them up in the XML-tree.
        So we'll skip them in the regular flow process."""
        # TODO: Check specific on the class name. Process otherwise.
        if node.attrib.get('class') == 'literature':
            cStyle = self.getCascadedNodeStyle(node.tag)
            tb = self.getTextBox(cStyle)  # Get the latest galley text box. Answer new if width changed.
            return

        if node.attrib.get('class') == 'footnote':
            # Find the content of the footnotes.
            #node.findall('./ol/li/p')
            #for index, p in enumerate(node.findall('./ol/li/p')):
            #    self.document.footnotes[index+1].append(p)
            cStyle = self.getCascadedNodeStyle(node.tag)
            tb = self.getTextBox(cStyle)  # Get the latest galley text box. Answer new if width changed.
            return

        return self.typesetNode(node)

    def node_li(self, node):
        u"""Generate bullet/Numbered list item."""
        # Make sure this is a cascaded style, expanded from current values in top style in gState.
        cStyle = self.getCascadedNodeStyle(node.tag)
        tb = self.getTextBox(cStyle) # Get the latest galley text box. Answer new if width changed.
        tb.append(cStyle['listBullet'], cStyle) # Append the bullet as defined in the style.
        # Typeset the block of the tag. Pass on the cascaded style, as we already calculated it.
        self.typesetNode(node, cStyle)

    def node_img(self, node):
        u"""Process the image. Find empty space on the page to place it,
        closest related to the w/h ration of the image."""
        src = node.attrib.get('src')
        g = Galley()
        cStyle = self.getCascadedNodeStyle(node.tag)
        imageElement = Image(src, cStyle) # Set path, image w/h and image scale from style.
        g.append(imageElement)
        caption = node.attrib.get('title')
        if caption is not None:
            captionStyle = self.getCascadedNodeStyle('caption')
            tb = g.getTextBox(captionStyle)
            caption = node.attrib.get('title')
            # Add invisible marker to the FormattedString, to indicate where the image
            # reference went in a textBox after slicing the string.
            tb.append(caption+'\n', captionStyle)
            tb.append(getMarker(node.tag, src))
        self.galley.append(g)
        if cStyle is not None:
            self.popStyle()

    def getCascadedStyle(self, style):
        u"""As we want cascading font and fontSize in the page elements, we need to keep track
        of the stacking of XML-hierarchy of the previous tag styles.
        The styles can omit the font or fontSize, and still we need to be able to set the element
        attributes. Copy the current style and add overwrite the values from the new style.
        This way the current style always contains all attributes of the root style."""
        cascadedStyle = copy.copy(self.gState[-1]) # Take the top of the stack as source.
        if style is not None: # Style may be None. In that case answer just copied of current gState top.
            for name, value in style.items():
                cascadedStyle[name] = value # Overwrite the style value.
            style['cascaded'] = True # Mark that this is a cascaded style, to distinguish from plain styles.
        return cascadedStyle

    def getCascadedNodeStyle(self, name):
        style = self.document.getStyle(name)
        return self.getCascadedStyle(style)

    def pushStyle(self, style):
        self.gState.append(style)
        return style
        
    def popStyle(self):
        self.gState.pop()
        return self.gState[-1]

    def _strip(self, s, style):
        u"""Strip the white space from s if style.preFix and/or style.postFix are not None."""
        if not None in (s, style):
            preFix = style.get('preFix')
            if preFix is not None: # Strip if prefix is not None. Otherwise don't touch.
                s = preFix + s.lstrip()
                postFix = style.get('postFix')
            if postFix is not None:
                s = s.rstrip() + postFix
        return s

    def typesetNode(self, node, style=None):
        u"""Recursively typeset the node, using style. Style can be None, in which case it should be not
        pushed and popped. If there is a valid style, push it on the graphics state and answer a merged
        style with the one that was on top before. This way automatic cascading values are in the style
        answered by the push."""
        if style is None:
            style = self.getCascadedNodeStyle(node.tag)
        elif not style.cascaded: # For some reason this is a plain style. Make it cascaded.
            style = self.getCascadedStyle(style)
        if style is not None: # Do we have a real style?
            style = self.pushStyle(style)

        # Get current flow text box from Galley to fill. Style can be None. If the width of the
        # latest textBox is not equal to style.w, then create a new textBox in the galley.
        tb = self.getTextBox(style)

        nodeText = self._strip(node.text, style)
        if nodeText: # Not None and still with content after stripping?
            tb.append(nodeText, style)
            # If style is None, just add plain string to current FormattedString.
            
        # Type set all child node in the current node, by recursive call.
        for child in node:
            hook = 'node_'+child.tag
            # Method will handle the styled body of the element, but not the tail.
            if hasattr(self, hook):
                getattr(self, hook)(child) # Hook must be able to derive style from node.
                # We are on tail mode now, but we don't know what happened in the child block.
                # So, to be sure, we'll push the current style again.
                if style is not None:
                    self.pushStyle(style)
                childTail = self._strip(child.tail, style)
                if childTail: # Any tailf left after stripping, then append to the current textBox.
                    # Get current flow text box from Galley to fill. Style can be None. If the width of the
                    # latest textBox is not equal to style.w, then create a new textBox in the galley.
                    tb = self.getTextBox(style)
                    tb.append(childTail, style)  # In case style is None, just add plain string.
                if style is not None: # And we pop the style again if it exists, as it was needed for the tail.
                    self.popStyle()

            else:
                # If no method hook defined, then just solve recursively. Child node will get the style.
                self.typesetNode(child)

        # Restore the graphic state at the end of the element content processing to the
        # style of the parent in order to process the tail text.
        if style is not None: # Only pop if there was a pushed style.
            style = self.popStyle()

        # XML-nodes are organized as: node - node.text - node.children - node.tail
        # If there is no text or if the node does not have tail text, these are None.
        nodeTail = self._strip(node.tail, style)
        if nodeTail: # Something of a tail left after stripping?
            tb.append(nodeTail, style) # If style is None, just add plain string.

    def typesetFile(self, fileName):
        u"""Read the XML document and parse it into a tree of document-chapter nodes. Make the typesetter
        start at page pageNumber and find the name of the flow in the page template."""

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
        # Collect all flowing text in one formatted string, while simulating the page/flow, because
        # we need to keep track on which page/flow nodes results get positioned (e.g. for toc-head
        # reference, image index and footnote placement.   
        self.typesetNode(root)
        
    def typesetFootnotes(self):
        footnotes = self.document.footnotes
        for index, (page, e, p) in footnotes.items():
            style = page.getStyle('footnote')
            fs = getFormattedString('%d ' % index, style)
            tb = page.findElement('footnote')
            if tb is not None:
                self.typesetNode(p, page, style)

