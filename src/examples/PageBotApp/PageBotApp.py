from vanilla import Window, Button
from drawBot.ui.drawView import DrawView
from drawBot.scriptTools import ScriptRunner
from drawBot.ui.codeEditor import OutPutEditor
from drawBot.context import getContextForFileExt
from drawBot.drawBotDrawingTools import _drawBotDrawingTool, DrawBotDrawingTool
from drawBot.scriptTools import ScriptRunner, DrawBotNamespace, StdOutput

# Runs a DrawBot script in a separate window.

def hitCallback(sender):

    script = 'fill(random(), random(), random())\nrect(10+random()*100, 10+random()*100, 200, 300)'
    _drawBotDrawingTool.newDrawing()
    namespace = DrawBotNamespace(_drawBotDrawingTool, _drawBotDrawingTool._magicVariables)
    _drawBotDrawingTool._addToNamespace(namespace)

    # Creates a new standard output, catching all print statements and tracebacks.
    output = []
    stdout = StdOutput(output, outputView=outputWindow.outputView)
    stderr = StdOutput(output, isError=True, outputView=outputWindow.outputView)

    # Calls DrawBot's ScriptRunner with above parameters.
    ScriptRunner(script, None, namespace=namespace, stdout=stdout, stderr=stderr)
    context = getContextForFileExt('pdf')
    _drawBotDrawingTool._drawInContext(context)
    pdfDocument = _drawBotDrawingTool.pdfImage()
    w.drawView.setPDFDocument(pdfDocument)
    
w = Window((10, 10, 400, 480), 'Window')
w.button = Button((20,20, 100, 30), 'Hit', callback=hitCallback)
w.drawView = DrawView((0, 64, -0, -0))

w.open()
outputWindow = Window((500, 10, 400, 300), minSize=(1, 1), closable=True)
outputWindow.outputView = OutPutEditor((0, 0, -0, -0), readOnly=True)
outputWindow.open()
#hitCallback(None)