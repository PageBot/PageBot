#!/usr/bin/env python
from pagebot.typesetter import Typesetter

# Path to markdown file, including Python code blocks.
MARKDOWN_PATH = u"TEST_CONTENT.md"

# Export PDF, showing what is found inside the markdown file.
EXPORT_PATH = '_export/EmbeddedPythonCodeBlocks.pdf'
# Create an unbound Typesetter instance (trying to find a Document
# instance in the codeblock result. If no Galley instance is supplied
# to the Typesetter, it will create one.
t = Typesetter()
# Parse the markdown content and execute the embedded Python code blocks.
t.typesetFile(MARKDOWN_PATH)
# Typesetter found document definition inside content.
print('Document title:', t.doc.title)
# Multiple code blocks found with identical identifier.
# Added counter 'Views_0' to 'Views' to make it unique.
print('Found code blocks:', t.codeBlocks.keys())

t.doc.export(EXPORT_PATH)

