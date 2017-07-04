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
#    xmltransformerpart.py
#
class XmlTransformerPart:

    def addDocBaseClass(self, class_, attrs):
        if not attrs.has_key('class_'):
            attrs['class_'] = [class_]
        elif not isinstance(attrs['class_'], (list, tuple)):
            attrs['class_'] = [class_] + [attrs['class_']]
        else:
            attrs['class_'] = [class_, attrs['class_']]
        return attrs

    def docTagElement(self, element):
        u"""Copy the attributes to a new dictionart, are we may need to alter them,
        and we don't want to touch the original etree element attributes."""
        attrs = {}
        for key, item in element.attrib.items():
            # Class attribute is special
            if key == 'class':
                key = 'class_'
                if not isinstance(item, (tuple, list)):
                    item = [item]
            attrs[key] = item

        hook = 'doc_%s' % element.tag
        if hasattr(self, hook):
            getattr(self, hook)(element, attrs)
        else:
            self.span(style='color:red;')
            self.text('[%s]' % element.tag)
            self._span()
            
    def _docTagElement(self, element):
        hook = '_doc_%s' % element.tag
        if hasattr(self, hook):
            getattr(self, hook)()
        else:
            self.span(style='color:red;')
            self.text('[/%s]' % element.tag)
            self._span()
    
    # E L E M E N T  D I S P A T C H 
    
    def doc_topic(self, element, attrs):
        attrs = self.addDocBaseClass('topic', attrs)
        self.div(**attrs)

    def _doc_topic(self):
        self._div(comment='topic')

    def doc_summary(self, element, attrs):
        attrs = self.addDocBaseClass('summary', attrs)
        self.div(**attrs)

    def _doc_summary(self):
        self._div(comment='summary')

    def doc_chapters(self, element, attrs):
        attrs = self.addDocBaseClass('chapters', attrs)
        self.div(**attrs)
        
    def _doc_chapters(self):
        self._div(comment='chapters')
        
    def doc_chapter(self, element, attrs):
        attrs = self.addDocBaseClass('chapter', attrs)
        self.div(**attrs)
        
    def _doc_chapter(self):
        self._div(comment='chapter')
        
    def doc_meta(self, element, attrs):
        u"""Ignore the meta tag, just process titel and subtitle and summary by 
        direct XPath query."""
        self.pushResult()
    
    def _doc_meta(self):
        u"""Ignore the content by popping the current result stream."""
        self.popResult()
    
    def doc_title(self, element, attrs):
        u"""Transform chapter/title into h2."""
        self.h2()
        
    def _doc_title(self):
        self._h2()
     
    def doc_lead(self, element, attrs):
        attrs = self.addDocBaseClass('lead', attrs)
        self.p(**attrs)
        
    def _doc_lead(self):
        self._p()
       
    def doc_h1(self, element, attrs):
        self.h1(**attrs)
        
    def _doc_h1(self): 
        self._h1()
        
    def doc_h2(self, element, attrs):
        self.h2(**attrs)
        
    def _doc_h2(self): 
        self._h2()
        
    def doc_h3(self, element, attrs):
        self.h3(**attrs)
        
    def _doc_h3(self): 
        self._h3()
        
    def doc_h4(self, element, attrs):
        self.h4(**attrs)
        
    def _doc_h4(self): 
        self._h4()
        
    def doc_h5(self, element, attrs):
        self.h5(attrs)
        
    def _doc_h5(self): 
        self._h5()
        
    def doc_h6(self, element, attrs):
        self.h6(**attrs)
        
    def _doc_h6(self): 
        self._h6()
        
    def doc_p(self, element, attrs):
        # Mark in the class if the element is first of its kind in list of siblings.
        previous = element.getprevious()
        if previous is None or previous.tag != element.tag:
            item = attrs.get('class_') or []
            item.append(self.C.CLASS_FIRST)
            attrs['class_'] = item
        # Mark in the class if the element is last of its kind in list of siblings.            
        next = element.getnext()
        if next is None or next.tag != element.tag:
            item = attrs.get('class_') or []
            item.append(self.C.CLASS_LAST)
            attrs['class_'] = item
        
        self.p(**attrs)
        
    def _doc_p(self):
        self._p()
    
    def doc_b(self, element, attrs):
        self.b()
        
    def _doc_b(self):
        self._b()
           
    def doc_blockquote(self, element, attrs):
        self.blockquote(**attrs)
        
    def _doc_blockquote(self):
        self._blockquote()
    
    def doc_code(self, element, attrs):
        self.pre(**attrs)
        
    def _doc_code(self):
        self._pre()
      
    def doc_em(self, element, attrs):
        self.em(**attrs)
        
    def _doc_em(self):
        self._em()
              
    def doc_list(self, element, attrs):
        self.ul(**attrs)
    
    def _doc_list(self):
        self._ul()

    doc_ul = doc_list # For compatibility convenience
    _doc_ul = _doc_list
    
    def doc_nlist(self, element, attrs):
        self.ol(**attrs)
        
    def _doc_nlist(self):
        self._ol()

    doc_ol = doc_nlist # For compatibility convenience
    _doc_ol = _doc_nlist
            
    def doc_item(self, element, attrs):
        self.li(**attrs)
        
    def _doc_item(self):
        self._li()

    doc_li = doc_item # For compatibility convenience
    _doc_li = _doc_item
    
    def doc_amp(self, element, attrs):
        self.text('&amp;')
        
    def _doc_amp(self):
        pass
    
    def doc_footnote(self, element, attrs):
        u"""The optional attribute *label* is a Python string template that defines the content of the reference.
        Default is "[%s]" where the tag is replaced by the index number of the footnote."""
        if not attrs.has_key('class_'):
            attrs['class_'] = 'footnote'
        self._footnoteCount += 1
        self.sup(**attrs)
        self.a(href='#fnref:footnote%d' % self._footnoteCount, name='fnref:footnoteRef%d' % self._footnoteCount)
        self.text(attrs.get('label', '[%s]') % self._footnoteCount)
        self.pushResult()
        
    def _doc_footnote(self):
        tail = self.popResult() 
        self._a()
        self._sup()
  
    # I M A G I N G
               
    def doc_image(self, element, attrs):
        self.div(class_=self.C.CLASS_IMAGEBLOCK)
        if not attrs.has_key('src'): # No src url defined, then use default image.
            attrs['src'] = "http://data.petr.com.s3.amazonaws.com/_images/xierpa/kruis6.jpg"
        if not attrs.has_key('class_'):
            attrs['class_'] = self.C.CLASS_AUTOWIDTH
        self.img(**attrs)
        self.pushResult() # Push output stream, to catch any caption output
        
    def _doc_image(self):
        u"""Pop the result output streams."""
        caption = self.popResult().strip()
        if caption:
            self.div(class_=self.C.CLASS_CAPTION)
            self.text(caption)
            self._div() 
        self._div() # .imageBlock
        
    # L I N K S
    
    def doc_www(self, element, attrs):
        u"""Make full http url, if the href does not start with a "/". This way we can make internal
        links appear to be external (opening a new window)."""
        href = attrs.get('href')
        if href and not href.startswith('http://') and not href.startswith('/'):
            href = 'http://' + href
        self.a(href=href, target=attrs.get('target', self.C.TARGET_EXTERN))
    
    def _doc_www(self):
        self._a()
  
    #def doc_next(self, element, attrs):
    #def doc_prev(self, element, attrs):
     
    # S V G
    
    def doc_svgexample(self, element, attrs):
        from xierpa3.components.examples.svg import SvgExample
        svgComponent = SvgExample()
        svgComponent.draw(self, drawingId=attrs.get('id' or 0))
        
    def _doc_svgexample(self):
        pass
    
