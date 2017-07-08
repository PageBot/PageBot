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

def markDown2XMLFile(self, path):
    u"""If fileName is pointing to a non-XML file, then try to convert. This needs to be
    extended in the future e.g. to support Word documents or other text resources.
    If the document is already an XML document, then ignore."""
    fileExtension = path.split('.')[-1].lower()
    assert fileExtension.lower() == 'md'
    # If we have MarkDown content, convert to XML (XHTML)
    f = codecs.open(path, mode="r", encoding="utf-8")
    mdText = f.read()
    f.close()
    mdExtensions = [FootnoteExtension(), LiteratureExtension(), Nl2BrExtension()]
    xml = u'<?xml version="1.0" encoding="UTF-8"?>\n<document>%s</document>' % markdown.markdown(mdText, extensions=mdExtensions)
    xml = xml.replace('&nbsp;', ' ')

    xmlPath = path + '.xml'
    f = codecs.open(xmlPath, mode="w", encoding="utf-8")
    f.write(xml)
    f.close()
    return fileName # Return altered fileName if converted. Otherwise return original fileName

def readXMLFile(path, xPath=None):
    u"""Read the XML from path and answer the compiled etree."""
    fileExtension = path.split('.')[-1].lower()
    print fileExtension
    assert fileExtension.lower() in ('xml', 'xsl', 'html')
    try:
        tree = ET.parse(path)
        root = tree.getroot() # Get the root element of the tree.
        # If there is XSL filtering defined, they get the filtered nodes.
        if xPath is not None:
            return root.findall(xPath)
        return root
    except ParseError:
        
def readHTMLFile(path, xPath=None):
    u"""Read the HTML body tag from path and answer the compiled etree."""
    return readXMLFile(path, xPath='body')
def readMarkDown(path):
    u"""Read the markdown from path and answer the compiled etree."""
    xmlPath = markDown2XMLFile(path)
    return readXMLFile(xmlPath)


path = u"/Users/petr/git/Opentype-1.8-Axis-Proposal/index.html"
path = u"/Users/petr/git/Opentype-1.8-Axis-Proposal/index.html"
aa = readXMLFile(path)
print aa