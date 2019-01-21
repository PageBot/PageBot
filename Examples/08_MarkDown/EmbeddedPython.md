
# Embedded Python
The connection between Markdown content and Python can be made from 2 different directions. 

* PageBot application scripts that create a **Document** instance with templates, elements and typesetters that parse Markdown text.
* MarkDown text files that include Python code to create documents.

If possible, the interpreting Composer already made set of globals that include the overall Document instance as “doc”.

For example, you can execute Python code from MarkDown like this:

## The Typesetter

The **Typesetter**, reading this Markdown file, will generate a galley (list of elements) including the code blocks. They are just collected by the Typesetter, not interpreted or executed.

During the process **errors** and **warnings** are collected as part of the global result dictionary.

The resulting dictionary contains Python code blocks, indicated by a triple "~" tilde.

A code block can contain any kind of Python code. Any “globally” created object will become an entry in the resulting dictionary.

## The Composer

The composer inteprets the code blocks, directing the selection of styles and the target page/box for the sequential text elements.

~~~

# It is possible to print from within a code block, to facilitate debugging single lines.
print('This is the current document:', doc)
print('This is the current page:', page)
print('This is the current box:', box)

page = page.next # Creates a new page, from within the code block execution.

# It is also possible to define globals during the processing of code blocks
# that then answer back into the targets dicionary. The calling applicaiton can
# then use the collected data for further processing. 
# This way a bi-direcitonal communication is possible between the applicaiton and
# the MarkDown document.

aa = 123
bb = 234
# The answered data can have any format of Python object.
cc = ['List', 'of', 'things']

~~~
