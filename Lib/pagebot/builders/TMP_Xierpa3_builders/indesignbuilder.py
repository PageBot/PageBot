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
#   indesignbuilder.py
#
#    https://www.adobe.com/content/dam/Adobe/en/devnet/indesign/sdk/cs6/scripting/InDesign_ScriptingTutorial.pdf
#    http://wwwimages.adobe.com/www.adobe.com/content/dam/Adobe/en/devnet/indesign/sdk/cs6/scripting/InDesign_ScriptingGuide_JS.pdf
#
from xierpa3.builders.javascriptbuilder import JavaScriptBuilder
from xierpa3.builders.builderparts.xmltransformerpart import XmlTransformerPart
from xierpa3.toolbox.transformer import TX

class InDesignBuilder(XmlTransformerPart, JavaScriptBuilder):
    u"""The InDesignBuilder allows to create InDesign JavaScript, that build the document
    of the calling site instance.
    """
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = JavaScriptBuilder.C 

    ID = 'indesign' # Dispatcher id of this builder

    EXTENSION = 'jsx'
    INDESIGN_USER = 'petr'
    INDESIGN_VERSION = '9.0'
    INDESIGN_LANGUAGE = 'en_US'
    # Export path, needs user name to complete the path to InDesign script folder.
    PATH_EXPORT = '/Users/%s/Library/Preferences/Adobe InDesign/Version %s/%s/Scripts/Scripts Panel/Xierpa3' % (INDESIGN_USER, INDESIGN_VERSION, INDESIGN_LANGUAGE) 
    
    def theme(self, component):
        self.comment('Document %s' % component.name)
        self.output("var myDocument = app.documents.add();\n") # Change for multiple pages inside one document
        self.output("var myPage;\n")
        self.output("var myTextFrame;\n")
        
    def _theme(self, component):
        pass
    
    def page(self, component):
        self.output("myPage = myDocument.pages.add();\n")

    def _page(self, component):
        pass
    
    def text(self, s):
        if s is not None:   
            self.output("""myTextFrame.contents = myTextFrame.contents.concat("%s");\n""" % s.replace('"', '\"').replace('\n', u'¶'))

    # M E A S U R E
    
    @classmethod
    def M(cls, attribute):
        u"""Measurement conversions dispatcher for CSS-like attributes to InDesign units."""
        try:            
            v = attribute.raw
            hook = 'm_' + v[0]
            v = v[1:]
            if hasattr(cls, hook):
                v = getattr(cls, hook)(v)
        except AttributeError:
            v = attribute or 0
        # @@@ For now
        if isinstance(v, basestring) and v.endswith('%'):
            v = 250
        return '%spt' % v
    
    @classmethod
    def m_Em(cls, value):
        return value[0] * 12 # Hard translation from Em to pts for now.
                
    # T A G S
    
    def div(self, **kwargs):
        x = kwargs.get('x', kwargs.get('marginleft', 20))
        y = kwargs.get('y', kwargs.get('margintop', 20))
        w = kwargs.get('width') or 400
        h = kwargs.get('height') or 200
        self.output("myTextFrame = myPage.textFrames.add();\n")
        self.output("""myTextFrame.geometricBounds = ["%s", "%s", "%s", "%s"];\n""" % (self.M(x), self.M(y), self.M(w), self.M(h)))
        self.output("""myTextFrame.contents = "";\n""") 

    def _div(self, comment=None):
        if comment is not None:
            self.comment(comment)
    
    def h2(self, **kwargs):
        self.text('[h2] ')
        
    def _h2(self):
        self.text('[/h2] ')

    def h4(self, **kwargs):
        self.text('[h4] ')
        
    def _h4(self):
        self.text('[/h4] ')

    def h5(self, **kwargs):
        self.text('[h5] ')
        
    def _h5(self):
        self.text('[/h5] ')

    def p(self, **kwargs):
        self.text('[p] ')
        
    def _p(self):
        self.text('[/p] ')
        
    def sup(self, **kwargs):
        self.text('[sup] ')
        
    def _sup(self):
        self.text('[/sup] ')
        
    def pre(self, **kwargs):
        self.text('[pre] ')
        
    def _pre(self):
        self.text('[/pre] ')
        
    def em(self, **kwargs):
        self.text('[em] ')
        
    def _em(self):
        self.text('[/em] ')
        
    def blockquote(self, **kwargs):
        self.text('[blockquote] ')
        
    def _blockquote(self):
        self.text('[/blockquote] ')
        
    def span(self, **kwargs):
        self.text('[span] ')
        
    def _span(self):
        self.text('[/span] ')
        
    def nav(self, **kwargs):
        self.text('[nav] ')
        
    def _nav(self):
        self.text('[/nav] ')
        
    def img(self, **kwargs):
        self.text('[img] ')
        
    def _img(self):
        self.text('[/img] ')
        
    def ul(self, **kwargs):
        self.text('[ul] ')
                   
    def _ul(self):
        self.text('[\ul] ')
         
    def ol(self, **kwargs):
        self.text('[ol] ')
                   
    def _ol(self):
        self.text('[\ol] ')
         
    def li(self, **kwargs):
        self.text('[li] ')
                   
    def _li(self):
        self.text('[\li] ')
         
    def a(self, **kwargs):
        self.text('[a] ')
                   
    def _a(self):
        self.text('[\a] ')
         
                   
    # I / O
       
    def save(self, filePath): 
        if not filePath.endswith(self.EXTENSION):
            filePath += '.' + self.EXTENSION
        if not filePath.startswith('/'):
            filePath = '/' + filePath
        JavaScriptBuilder.save(self, self.PATH_EXPORT + filePath)      
        
