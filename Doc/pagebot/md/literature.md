# md.literature

### DEF_RE
Compiled regular expression objects
### class Extension
Base class for extensions to subclass.
### unicode LIT_BACKLINK_TEXT
unicode(object='') -> unicode object
unicode(string[, encoding[, errors]]) -> unicode object

Create a new Unicode object from the given encoded string.
encoding defaults to the current default string encoding.
errors can be 'strict', 'replace' or 'ignore' and defaults to 'strict'.
### class LiteratureExtension
Literature Extension.
### class LiteraturePattern
InlinePattern for literature markers in a document's body text.
### class LiteraturePostprocessor
Replace placeholders with html entities.
### class LiteraturePreprocessor
Find all literature references and store for later use.
### class LiteratureTreeprocessor
Build and append literature div to end of document.
### unicode NBSP_PLACEHOLDER
unicode(object='') -> unicode object
unicode(string[, encoding[, errors]]) -> unicode object

Create a new Unicode object from the given encoded string.
encoding defaults to the current default string encoding.
errors can be 'strict', 'replace' or 'ignore' and defaults to 'strict'.
### class OrderedDict
A dictionary that keeps its keys in the order in which they're inserted.

Copied from Django's SortedDict with some modifications.
### class Pattern
Base class that inline patterns subclass.
### class Postprocessor
Postprocessors are run after the ElementTree it converted back into text.

Each Postprocessor implements a "run" method that takes a pointer to a
text string, modifies it as necessary and returns a text string.

Postprocessors must extend markdown.Postprocessor.
### class Preprocessor
Preprocessors are run after the text is broken into lines.

Each preprocessor implements a "run" method that takes a pointer to a
list of lines of the document, modifies it as necessary and returns
either the same pointer or a pointer to a new list.

Preprocessors must extend markdown.Preprocessor.
### TABBED_RE
Compiled regular expression objects
### class Treeprocessor
Treeprocessors are run on the ElementTree object before serialization.

Each Treeprocessor implements a "run" method that takes a pointer to an
ElementTree, modifies it as necessary and returns an ElementTree
object.

Treeprocessors must extend markdown.Treeprocessor.
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
### unicode __doc__
unicode(object='') -> unicode object
unicode(string[, encoding[, errors]]) -> unicode object

Create a new Unicode object from the given encoded string.
encoding defaults to the current default string encoding.
errors can be 'strict', 'replace' or 'ignore' and defaults to 'strict'.
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
### module etree
### def makeExtension
Return an instance of the LiteraturesExtension
### class text_type
unicode(object='') -> unicode object
unicode(string[, encoding[, errors]]) -> unicode object

Create a new Unicode object from the given encoded string.
encoding defaults to the current default string encoding.
errors can be 'strict', 'replace' or 'ignore' and defaults to 'strict'.
### instance unicode_literals
