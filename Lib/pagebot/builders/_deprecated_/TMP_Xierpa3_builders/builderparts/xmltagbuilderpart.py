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
#    xmltagbuilderpart.py
#
from xierpa3.toolbox.transformer import TX

class XmlTagBuilderPart:
        
    GLOBAL_ATTRIBUTES = set(['id', 'class_', 'title', 'onclick', 'style'])

    @classmethod
    def class2SpaceString(cls, class_):
        # Format the class to comma separated output. Takes any construction of strings and lists.
        # class_ can be ['name', 'name'] or 'name name' or 'name, name' or ['name', ('name', 'name')]
        if not isinstance(class_, (list, tuple)):
            class_ = [class_]
        s = []
        for classNames in class_:
            if isinstance(classNames, (list, tuple)):
                s.append(cls.class2SpaceString(classNames))
                continue
            classNames = classNames.replace(',', ' ')
            for className in classNames.split(' '):
                if not className:
                    continue
                s.append(className)
        return ' '.join(s)

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
        u"""Generic function to write HTML attributes. The new HTML5 feature to store custom data inside the attribute
        @data-xxx@ is defined as attribute name *data_xxx*. See "HTML-5 Attributes":http://ejohn.org/blog/html-5-data-attributes/
        If the key has an attached builder type as @xxx-html@ or @xxx-css@, 
        then show the attribute only with the builder type matches the type of @self@.
        """
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
            #    key, builderType = TX.attrName2attrBuilderType(key)
            #    if builderType is not None:
            #        # If the key is not in the standard HTML list, is can be a CSS attribute. Just ignore it.

        for key, value in default_attributes.items():
            if key not in args.keys():
                self.get_attribute_exceptions(key, value)

    def write_attribute(self, key, value):
        u"""
        Auxiliary function to write each attribute to @self.result@. If the *key* is defined in
        @self.SINGLE_ATTRIBUTES@ then only output the single key name (even if this breaks XML
        validation). By default the @self.SINGLE_ATTRIBUTES@ is empty, but it can be redefined by the
        inheriting application class.
        If the *key* is in @self.CASCADING_ATTRIBUTES@ and the *value* is tuple or
        a list, then join the *value*, separated by spaces. This feature is especially used to build flexible
        cascading *class_* attributes.
        If the attribute has no value, then the output is skipped.
        """
        line = None
        if key == 'class_':
            key = 'class'
            value = self.class2SpaceString(value)
        if key in self.SINGLE_ATTRIBUTES:
            line = u' ' + key
        elif isinstance(value, (list, tuple)):
            if key in self.CASCADING_ATTRIBUTES:
                value = TX.flatten2Class(value)
                if isinstance(value, basestring):
                    value = value.replace('"', '&quot;');
                if value:
                    line = u' %s="%s"' % (key, value)
            else:
                raise ValueError('[XmlTagBuilder.write_attribute] No list attribute value allowed for %s="%s"' % (key, `value`))
        elif value:
            if isinstance(value, basestring):
                value = value.replace('"', '&quot;');
            line = u' %s="%s"' % (key, value)
        if line:
            self.output(line)

    def write_php_attribute(self, value):
        self.output(' ')
        self.output(value)

    def write_tag(self, tagname, open, args):
        u"""
        Writes a normally formatted HTML tag, exceptions have a custom implementation, see respective functions.
        """
        self.tabs()
        self.output(u'<' + tagname)
        self.getandwrite_attributes(tagname, args)

        if open:
            self.output(u'>')
            # Push as last, so we can see the current tag on the stack
            self._pushTag(tagname)
            self.tabIn()
        else:
            self.output(u'/>')

    def write_tag_noWhitespace(self, tagname, open, args):
        u"""
        Writes a normally formatted HTML tag, exceptions have a custom implementation, see respective functions.
        Don’t write any white space inside the block. E.g. used by <textarea>
        """
        self.output(u'<' + tagname)
        self.getandwrite_attributes(tagname, args)

        if open:
            self.output(u'>')
            # Push as last, so we can see the current tag on the stack
            self._pushTag(tagname)
        else:
            self.output(u'/>')

    # ---------------------------------------------------------------------------------------------------------
    #     B L O C K

    def buildTag(self, tag, **kwargs):
        if tag is not None and hasattr(self, tag):
            getattr(self, tag)(**kwargs)

    def _buildTag(self, tag, **kwargs):
        if tag is not None:
            tag = '_' + tag
            if hasattr(self, tag):
                getattr(self, tag)(**kwargs)

    # ---------------------------------------------------------------------------------------------------------
    #     N O D E S T A C K

    def _pushTag(self, tag):
        self._tagStack.push(tag)

    def _closeTag(self, tag):
        self.tabOut()
        self.tabs()
        self.output(u'</%s>' % tag)
        self._popTag(tag)

    def _closeTag_noWhitespace(self, tag):
        u"""Close the tag. Don’t write any white space inside the block. E.g. used by <textarea>."""
        self.output(u'</%s>' % tag)
        self._popTag(tag)

    def _popTag(self, tag):
        u"""
        Pop tag from the tag stack.
        """
        runningTag = self._tagStack.pop()
        if runningTag is None or not runningTag == tag:
            self.output('<div color=%s>Mismatch in closing tag "%s", expected "%s" in tree "%s".</div>' %
                    (self.C.CLASS_ERROR, tag, runningTag, `self._tagStack`))

    def _peekTag(self):
        return self._tagStack.top()

    def getTagStack(self):
        return self._tagStack
