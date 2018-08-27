print('\nChecking installation paths... \n')

import sys, os  
print('System: %s, %s' % (os.name, sys.platform))
print('Python version is:')
print(sys.version)

CLEAN = True

try:
    import site
    print('Found site at %s' % site.__file__)
    packages = site.getsitepackages()
    for p in packages:
        print(' - %s' % p)
except:
    print('x Could not read site packages :S')

# TODO: add svgwrite, flat, markdown etc?
# TODO automate, eval()?
# TODO: make OS dependent.

try:
    import objc
    print('PyObjc found at %s' % objc.__path__)
except:
    print('x No PyObjc installed')
    CLEAN = False

try:
    import AppKit
    print('AppKit found at %s' % AppKit.__path__[0])
except:
    print('x No AppKit')
    CLEAN = False
    
try:
    import pagebot
    print('Pagebot found at %s' % pagebot.__path__[0])
except:
    print('\nx Pagebot not found')
    CLEAN = False

try:
    import drawBot
    print('DrawBot found at %s' % drawBot.__path__[0])
except:
    print('\nx DrawBot not found')
    CLEAN = False

try:
    import sass
    print('Sass found at %s' % sass.__file__)
except Exception as e:
    print(e)
    print('x No sass dependency found.')
    CLEAN = False

if not CLEAN:
    print('Not all dependencies are installed, please install missing ones.')
else:
    # Testing PageBot.
    from pagebot.contexts.platform import getContext
    context = getContext()
    print(context)
    print(context.b)

    # Testing Sass.
    css = sass.compile(string='a { b { color: blue; } }')
    print(css)
    css = sass.compile(filename='sass/test.scss')
    print(css)
    
    test_scss = open('test.scss', 'w')
    import os, os.path
    if not os.path.exists('css'):
        os.mkdir('css')
    sass.compile(dirname=('sass', 'css'), output_style='compressed')
    with open('css/test.css') as example_css:
        print(example_css.read())

    # Export with HtmlBuilder.
    from pagebot.contexts.builders.htmlbuilder import HtmlBuilder 
    hb = HtmlBuilder()
    print(hb)
    hb.compileScss('sass/test.scss')