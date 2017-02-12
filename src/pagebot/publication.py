# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
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
    def __init__(self, documents=None, exportPath=None):
        self.exportPath = exportPath or '_export/'
        if documents is None:
            documents = {}
        self.documents = documents 
        
    def build(self):
        pass
        
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

