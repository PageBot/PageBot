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

print os.path.exists(MD_PATH)