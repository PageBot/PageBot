import os
import pagebot
from pagebot.typesetter import Typesetter
from pagebot.elements import *
from pagebot.document import Document

doc = Document()
g = Galley()
ts = Typesetter(doc, g)

ROOT_PATH = pagebot.getRootPath()
MD_PATH = ROOT_PATH + "/Examples/Howto/TOC.md"

ts.typesetFile(MD_PATH)
for e in g.elements:
    print e.fs
    print e

