from pagebot.typesetter import Typesetter

# Path to markdown file, including Python code blocks.
MARKDOWN_PATH = u"Content.md"

# Create an unbound Typesetter instance (trying to find a Document 
# instance in the codeblock result. If no Galley instance is supplied
# to the Typesetter, it will create one.
t = Typesetter()
# Parse the markdown content and execute the embedded Python code blocks.
t.typesetFile(MARKDOWN_PATH)
# Get the document as created by one of the code blocks in the content file.
print t.codeBlocks.keys()
# View settings and export format must be defined.
doc = t.doc 
print t.doc
# Export HTML, showing what is found inside the markdown file.
# Use the created document as exporter, to create the website files.
EXPORT_PATH = '_export/%s/index.html' % doc.title
doc.export(EXPORT_PATH)
# Export HTML, showing what is found inside the markdown file.
# Use the created document as exporter, to create the website files.
EXPORT_PATH = '_export/%s/index.css' % doc.title
doc.export(EXPORT_PATH)