
# Embedded Python
The connection between Markdown content and Python can be made from 2 different directions. 

* PageBot application scripts that create a **Document** instance with templates, elements and typesetters that parse Markdown text.
* MarkDown text files that include Python code to create documents.

If possible, the interpreting Composer already made set of globals that include the overall Document instance as “doc”.

For example, you can execute Python code from MarkDown like this:

## The Typesetter

The **Typesetter**, reading this Markdown file, will generate a galley (where galley.elements is a list of all elements found in the MarkDown, including codeblocks) including the code blocks. They are just collected by the Typesetter, not interpreted or executed.

During the process **errors** and **warnings** are collected as part of the global result dictionary.

The resulting dictionary contains Python code blocks, indicated by a triple "~" tilde.

A code block can contain any kind of Python code. Any “globally” created object will become an entry in the resulting dictionary.

## The Composer

The composer inteprets the code blocks, directing the selection of styles and the target page/box for the sequential text elements.

## Code blocks

Using the standard triple-tilde markers in MarkDown blocks of (Python) can be defined, that later get executed by the **Composer**. 
Codeblocks are chunks of Python code that can use globals supplied by the composer. Standard globals are **doc**, **page**, **box**, etc. If they get altered by the codeblock (e.g. by selecting another page or box), then this object is answered back to the composer.

~~~

# It is possible to print from within a code block, 
# to facilitate debugging single lines.
print('This is the current document:', doc)
print('This is the current page:', page)
print('This is the current box:', box)

# Create a new page, from within the code block execution.
page = page.next 
# All MarkDown text and images flow into the current “box”.
box = page.select('Box') # Select named text box from page.
print('New selected box target', box)

# It is also possible to define globals during the 
# processing of code blocks that then answer back 
# into the targets dicionary. 
# The calling application can then use the collected 
# data for further processing. 
# This way a bi-direcitonal communication is possible 
# between the applicaiton an the MarkDown document.

aa = 123
bb = 234
# The answered data can have any format of Python object.
cc = ['List', 'of', 'things']

# Since the "box" of the second page was selected,
# all text after this code block flows into there.
~~~

Blocks of text [p] are glued together here if possible. 

**This is another block in a different [strong] style.**

*And yet another [em] block*

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ipsum quam, scelerisque a varius nec, feugiat vel leo. Ut porta euismod finibus. Etiam auctor lacus nec tellus accumsan gravida. Etiam tempus quam ultrices tortor pharetra lobortis. Donec rutrum rutrum rhoncus. Pellentesque eu dui ipsum. Quisque malesuada eu leo porttitor tristique.

Quisque elementum erat non erat commodo semper. In orci leo, pharetra in finibus ut, aliquet vel elit. Curabitur non nulla rutrum, consectetur nisi tempor, viverra magna. Fusce sed porta augue, eget eleifend nibh. Aliquam eget blandit leo. Integer et massa facilisis, posuere lectus a, laoreet ipsum. Sed tincidunt erat nunc, sed ultrices risus ultrices vel. Pellentesque odio purus, tristique quis odio dapibus, lobortis commodo justo. Integer vitae dui sagittis, sollicitudin neque vitae, ornare augue. Phasellus gravida purus id odio dictum varius. Donec elit nisl, molestie sit amet dignissim quis, vehicula ut lectus. Vestibulum accumsan rutrum dui at blandit. Duis ac lacus ex. Praesent eget elit varius, rutrum massa quis, dapibus diam. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Aliquam accumsan dui in venenatis aliquet.

Nunc congue rhoncus nunc ac tincidunt. Donec sed risus ac felis congue sagittis. Fusce porta molestie facilisis. Proin varius magna ante, sit amet pellentesque diam blandit id. Phasellus non felis aliquet, tincidunt urna sit amet, dapibus lectus. Duis eget semper elit. Nam euismod purus id dui tincidunt finibus. Donec blandit nibh nec viverra pretium. Curabitur tellus lorem, dapibus eget varius sed, mattis nec nibh. Aliquam sit amet leo feugiat eros eleifend ultricies sed et elit. Nullam cursus, lacus sit amet pretium faucibus, arcu mi gravida mauris, et pretium elit felis in justo. Mauris eu sem ornare, laoreet magna condimentum, luctus metus.

Aenean gravida enim sed malesuada sagittis. Phasellus sed elit tortor. Vestibulum ornare lectus ligula, quis commodo lectus porta ut. Nunc semper porta eros quis ullamcorper. Duis porttitor feugiat eros quis pellentesque. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis et rutrum risus, in mollis orci. Vivamus volutpat commodo nulla, pharetra aliquam ipsum imperdiet eget.