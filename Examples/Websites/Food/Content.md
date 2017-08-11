~~~Python
cid = 'Document'
from pagebot.document import Document
from pagebot.elements import *
doc = Document(title='Bitcount Minisite', autoPages=2)
page = doc[0]
newTextBox('AAA', parent=page, w=200, h=200, fill=(1, 1, 0))

~~~

# Food Examples
This website shows the building of **HTML/CSS** pages, directly from a mixture of markdown content and embedded **PageBot** Python code. 
