# fonttoolbox.objects.family

### class Family
### class Font
Storage of font information while composing the pages.

    >>> import pagebot
    >>> from pagebot.toolbox.transformer import getFontPath
    >>> p = getFontPath('AmstelvarAlpha-VF')
    >>> from pagebot.fonttoolbox.objects.font import Font
    >>> f = Font(p, install=False)
    >>> f.name
    u'BitcountGrid'

    >>> len(f)
    101

    >>> f.keys()[-1]
    'y'

    >>> f.axes
    {'rndi': (0.0, 1000.0, 1000.0), 'rndo': (0.0, 1000.0, 1000.0), 'sqri': (0.0, 1000.0, 1000.0), 'sqro': (0.0, 1000.0, 1000.0), 'line': (0.0, 1000.0, 1000.0), 'open': (0.0, 0.0, 1000.0), 'wght': (0.0, 500.0, 1000.0)}

    >>> variables = f.variables
    >>> features = f.features
    >>> f.groups
    >>> f.designSpace
    {}

    >>> f.install()
    u'BitcountGrid-SingleCircleSquare-wght500rndi1000rndo1000line1000sqri1000sqro1000open0'

    >>> f.save()
### dict __builtins__
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
(key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
d = {}
for k, v in iterable:
d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
in the keyword argument list.  For example:  dict(one=1, two=2)
### __doc__
### str __file__
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### str __name__
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### str __package__
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### def getFamilies
Construct a dictionary of Family instances from dictionary familyPaths. It is assumed that all paths
are valied to font files. Force key in family from dictionary familyPaths, instead of font.info.styleName.
What is best practice? Keep as option?

Example format of familyPaths dictionary:
LIB_PATH = '/Library/Fonts/'
SOME_SYSTEM_FONTS = {
# Let's try some plain OSX system fonts, while they are still there (not variable yet).
'Georgia': dict(regular=LIB_PATH+'Georgia.ttf', bold=LIB_PATH+'Georgia Bold.ttf', 
italic=LIB_PATH+'Georgia Italic.ttf', boldItalic=LIB_PATH+'Georgia Bold Italic.ttf'),
'Verdana': dict(regular=LIB_PATH+'Verdana.ttf', bold=LIB_PATH+'Verdana Bold.ttf', 
italic=LIB_PATH+'Verdana Italic.ttf', boldItalic=LIB_PATH+'Verdana Bold Italic.ttf'),
}
### def getFamilyFontPaths
### def getFamilyFonts
### def getFontPathOfFont
### def getSystemFontPaths
Answer the cleaned list of installed font names.
### def guessFamilies
Find the family relation of all fonts in the list. Note that this cannot be a 100% safe guess.
Answer a dictionary with Family instances. Key is family name.
### def path2Name
<doc>Answers the file name part of the path.</doc>
