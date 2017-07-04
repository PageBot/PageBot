from vanilla import Window, Button
from drawBot.ui.drawView import DrawView
from drawBot.scriptTools import ScriptRunner
from drawBot.ui.codeEditor import OutPutEditor
from drawBot.context import getContextForFileExt
from drawBot.context.drawBotContext import DrawBotContext
from drawBot.drawBotDrawingTools import _drawBotDrawingTool
from drawBot.scriptTools import ScriptRunner, DrawBotNamespace, StdOutput
import AppKit

# Runs a DrawBot script in a separate window.

context = getContextForFileExt('pdf')
output = []

def hitCallback(sender):
    script = 'fill(random(), random(), random())\nrect(10+random()*100, 10+random()*100, 200, 300)'
    newDrawing()
    namespace = DrawBotNamespace(_drawBotDrawingTool, _drawBotDrawingTool._magicVariables)
    _drawBotDrawingTool._addToNamespace(namespace)

    # Creates a new standard output, catching all print statements and tracebacks.
    stdout = StdOutput(output, outputView=outputWindow.outputView)
    stderr = StdOutput(output, isError=True, outputView=outputWindow.outputView)

    # Calls DrawBot's ScriptRunner with above parameters.
    ScriptRunner(script, None, namespace=namespace, stdout=stdout, stderr=stderr)
    _drawBotDrawingTool._drawInContext(context)
    pdfDocument = _drawBotDrawingTool.pdfImage()
  
if __name__ == '__main__':

    w = Window((10, 10, 400, 200), 'Window')
    w.button = Button((20,20, 100, 30), 'Hit', callback=hitCallback)
    w.open()

    outputWindow = Window((500, 10, 400, 300), minSize=(1, 1), closable=True)
    outputWindow.outputView = OutPutEditor((0, 0, -0, -0), readOnly=True)
    outputWindow.open()