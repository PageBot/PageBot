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
#     xmlbuilder.py
#

from pagebot.contexts.builders.basebuilder import BaseBuilder

class XmlBuilder(BaseBuilder):

    GLOBAL_ATTRIBUTES = set(['cssId', 'cssClass', 'title', 'onclick', 'style'])

    @classmethod
    def class2SpaceString(cls, cssClass):
        # Format the class to comma separated output. Takes any construction of
        # strings and lists.
        # cssClass can be ['name', 'name'] or 'name name' or 'name, name' or
        # ['name', ('name', 'name')]
        if not isinstance(cssClass, (list, tuple)):
            cssClass = [cssClass]
        s = []
        for classNames in cssClass:
            if isinstance(classNames, (list, tuple)):
                s.append(cls.class2SpaceString(classNames))
                continue
            classNames = classNames.replace(',', ' ')
            for className in classNames.split(' '):
                if not className:
                    continue
                s.append(className)
        return ' '.join(s)

    def _initialize(self):
        self.compact = False
        self._newLine = '\n' # Add in case self.compact is False
        self._doIndent = True
        self._tabLevel = 0
        self._tabIndent = '\t'
        self._tagStack = [] # Stack with running tags for closing and XML validation
        self._verbose = True
        self._svgMode = False
        self._useOnline = True

    def tabs(self):
        """"Output tabs to the current level and add newlines, depending on the
        setting of self._newLine (string with newlines) and self._tabLevel
        (number of indents)."""
        if not self.compact and self._verbose:
            self.write(self._newLine + (self._tabIndent * self._tabLevel))

    def tabIn(self):
        if not self.compact and self._doIndent:
            self._tabLevel += 1

    def tabOut(self):
        if not self.compact and self._doIndent:
            self._tabLevel = max(0, self._tabLevel - 1)

    def newLine(self, count=1):
        if not self.compact:
            self.write(self._newLine * count)

    def getandwrite_attributes(self, tagname, args):
        attributes = self.GLOBAL_ATTRIBUTES.union(getattr(self, tagname.upper() + '_ATTRIBUTES', set([])))
        default_attributes = getattr(self, tagname.upper() + '_ATTRIBUTES_DEFAULTS', {})
        self.write_attributes(attributes, default_attributes, args, tagname)

    def get_clean_attribute_key(self, key):
        if key.endswith('_html'): # Change width_html to width and height_html to height
            key = key[:-5]
        elif key.endswith('_css'): # Change class_css, etc. to class_
            key = key[:-4]
        return key

    def write_attributes(self, attributes, default_attributes, args, tagname):
        """Generic function to write HTML attributes. The new HTML5 feature to
        store custom data inside the attribute @data-xxx@ is defined as
        attribute name *data_xxx*. See "HTML-5 Attributes":

        http://ejohn.org/blog/html-5-data-attributes/

        If the key has an attached builder type as @xxx-html@ or @xxx-css@,
        then show the attribute only with the builder type matches the type of
        @self@."""
        for key, value in args.items():
            if key == 'php':
                self.write_php_attribute(value)
            elif key in attributes or key.startswith(u'data_'): # or key.startswith(self.PHP_OPEN):
                # Write the regular attribute
                if not value is None:
                    key = self.get_clean_attribute_key(key)
                    self.get_attribute_exceptions(key, value)

            # TODO: Make attribute writing directly by builder if valid extension
            #else:
            #    key, builderType = attrName2attrBuilderType(key)
            #    if builderType is not None:
            #        # If the key is not in the standard HTML list, is can be a CSS attribute. Just ignore it.

        for key, value in default_attributes.items():
            if key not in args.keys():
                self.get_attribute_exceptions(key, value)

    def write_attribute(self, key, value):
        """Auxiliary function to write each attribute to @self.result@. If the
        *key* is defined in @self.SINGLE_ATTRIBUTES@ then only output the
        single key name (even if this breaks XML validation). By default the
        @self.SINGLE_ATTRIBUTES@ is empty, but it can be redefined by the
        inheriting application class.

        If the *key* is in @self.CASCADING_ATTRIBUTES@ and the *value* is tuple
        or a list, then join the *value*, separated by spaces. This feature is
        especially used to build flexible cascading *cssClass* attributes.  If
        the attribute has no value, then the output is skipped.
        """
        line = None
        if key == 'cssClass':
            key = 'class'
            value = self.class2SpaceString(value)
        if key in self.SINGLE_ATTRIBUTES:
            line = u' ' + key
        elif isinstance(value, (list, tuple)):
            if key in self.CASCADING_ATTRIBUTES:
                value = self.flatten2Class(value)
                if isinstance(value, str):
                    value = value.replace('"', '&quot;');
                if value:
                    line = u' %s="%s"' % (key, value)
            else:
                raise ValueError('[XmlTagBuilder.write_attribute] No list attribute value allowed for %s="%s"' % (key, value))
        elif value:
            if isinstance(value, str):
                value = value.replace('"', '&quot;');
            line = u' %s="%s"' % (key, value)
        if line:
            self.write(line)

    def write_php_attribute(self, value):
        self.write(' ')
        self.write(value)

    def write_tag(self, tagname, open, args):
        """Writes a normally formatted HTML tag, exceptions have a custom
        implementation, see respective functions.
        """
        self.tabs()
        self.write(u'<' + tagname)
        self.getandwrite_attributes(tagname, args)

        if open:
            self.write(u'>')
            # Push as last, so we can see the current tag on the stack
            self._pushTag(tagname)
            self.tabIn()
        else:
            self.write(u'/>')
        self.newLine() # Optional write newline if not self.compat

    def write_tag_noWhitespace(self, tagname, open, args):
        """Writes a normally formatted HTML tag, exceptions have a custom
        implementation, see respective functions. Don’t write any white space
        inside the block. E.g. used by <textarea>"""
        self.write(u'<' + tagname)
        self.getandwrite_attributes(tagname, args)

        if open:
            self.write(u'>')
            # Push as last, so we can see the current tag on the stack
            self._pushTag(tagname)
        else:
            self.write(u'/>')
        self.newLine() # Optional write newline if not self.compat

    #     B L O C K

    def buildTag(self, tag, **kwargs):
        if tag is not None and hasattr(self, tag):
            getattr(self, tag)(**kwargs)

    def _buildTag(self, tag, **kwargs):
        if tag is not None:
            tag = '_' + tag
            if hasattr(self, tag):
                getattr(self, tag)(**kwargs)

    #     N O D E S T A C K

    def _pushTag(self, tag):
        """Push the tag name to the stack of open stags."""
        self._tagStack.append(tag)

    def _closeTag(self, tag):
        self.tabOut()
        self.tabs()
        self.write(u'</%s>' % tag)
        self.newLine() # Optional write newline if not self.compat
        self._popTag(tag)

    def _closeTag_noWhitespace(self, tag):
        """Close the tag. Don’t write any white space inside the block. E.g.
        used by <textarea>."""
        self.write(u'</%s>' % tag)
        self.newLine() # Optional write newline if not self.compat
        self._popTag(tag)

    def _popTag(self, tag):
        """Pop tag from the tag stack."""
        runningTag = self._tagStack.pop()
        if runningTag is None or not runningTag == tag:
            self.write('<div color="#FF0000">Mismatch in closing tag "%s", expected "%s" in tree "%s".</div>' % (tag, runningTag, self._tagStack))
            self.newLine() # Optional write newline if not self.compat

    def _peekTag(self):
        """Answers the name of the current tag."""
        return self._tagStack[-1]

    def getTagStack(self):
        """Answers the stack of current tag names."""
        return self._tagStack
