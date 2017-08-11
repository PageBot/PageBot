# Test Content
This file contains Markdown content, including various functions for the **HowTo** scripts.

## Embedded Python
The connection between Markdown content and Python can be made from 2 different directions. 

* PageBot application scripts that creates a **Document** instance, with templates, element and typesetters that parse Markdown text.
* MarkDown text files that include all Python code to create documents.

And example of executing Python code is this:

~~~Python
cid = 'Document'
from pagebot.document import Document
doc = Document(w=400, h=600, title='TestContent')
~~~	

The **Typesetter**, reading this Markdown file, will generate this dictionary as result:

~~~
{'Document': {'doc': <pagebot.document.Document object at 0x119037c10>, 'Document': <class 'pagebot.document.Document'>, 'id': 'Document'}, 'Views': {'aa': 123, 'cc': ['List', 'of', 'things'], 'id': 'Views', 'bb': 234}}
~~~

As can be seen, the resulting dictionary contains of all Python code blocks, indicated by a triple “~” tilde. 
(Since the code block doesn’t contain “Python” after the triple tilde, it is ignored by the **Typesetter**.
If the code block contains a **cid = 'NameOfCodeBlock'** (“cid” is short for “codeId”), then this value is taken as name for the result dictionary.

A code block can contain any kind of Python code. Any “global” created object will become an entry in the resulting dictionary.

~~~Python
cid = 'Views' # Defines id for this code block result.
aa = 123
bb = 234
cc = ['List', 'of', 'things']
~~~	

~~~Python
cid = 'Views'
dd = 567
~~~
