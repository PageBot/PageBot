import os


d = dict(x=10, y=20, width=300, height=200) 

script = '''
#target InDesign 

app.activeDocument.pages.item(0).rectangles.add({              geometricBounds: [%(y)f, %(x)f, %(width)f, %(height)f],              //fillColor: myColorA,            // fillTint: myTint,            });

//fillRect(%(x)f, %(y)f, %(width)f, %(height)f);

    
''' % d




USERPATH = os.path.expanduser("~")

INDESIGNPATH = u"/Library/Preferences/Adobe InDesign/Version 8.0/en_US/Scripts/Scripts Panel/typographics2017/"

f=open(USERPATH+INDESIGNPATH+'test2.jsx', 'w')
f.write(script)
f.close()
