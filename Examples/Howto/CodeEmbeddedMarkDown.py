from pagebot.document import Document
from pagebot.typesetter import Typesetter
from pagebot.elements import Galley

path = u"/Users/petr/Desktop/git/PageBot/Examples/README.md"

g = Galley()
t = Typesetter(None, g)
t.typesetFile(path)
for codeName, values in t.codeBlocks.items():
    print codeName, values.keys()