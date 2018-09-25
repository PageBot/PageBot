print('\nChecking installation paths... \n')

import sys, os
print('System: %s, %s' % (os.name, sys.platform))
print('Python version is:')
print(sys.version)
print('Which Python?')
print(sys.executable)

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

libs = ['pagebot', 'fontTools', 'objc', 'AppKit', 'vanilla', 'drawBot', 'sass']
missing = []

for l in libs:
    try:
        __import__(l)
        print('%s installed at %s' % (l, __import__(l).__file__))
    except:
        print('x %s not installed' % l)
        missing.append(l)
        CLEAN = False

if not CLEAN:
    print('Not all dependencies are installed, please install missing ones:')
    print(', '.join(missing))
else:
    print('Found all dependencies, running some test...')
    # Testing PageBot.
    from pagebot.contexts.platform import getContext
    context = getContext()
    print(context)
    print(context.b)
    import sass

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
