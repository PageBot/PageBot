# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     publication.py
#
import os
           
class Publication(object):
    u"""The abstract Publication class, implements everything needed for a specific kind of publication.
    It can hold multiple related Document instances and serves various output formats."""
    def __init__(self, documents=None, name=None, exportPath=None):
        self.exportPath = exportPath or '_export/'
        self.name = name or self.__class__.__name__
        if documents is None:
            documents = {}
        self.documents = documents 
    
    def __repr__(self):
        return self.name

    def build(self):
        pass
    
    def draw(self):
        for document in self.documents.values():
            document.draw()
                
    def export(self, fileName=None):
        if not self.exportPath.endswith('/'):
            self.exportPath += '/'
        if not os.path.exists(self.exportPath):
            os.makedirs(self.exportPath)
        for document in self.documents.values():
            #print document
            #print self.exportPath
            #print fileName, document.fileName
            document.export(self.exportPath + (fileName or document.fileName or 'Document.pdf'))

