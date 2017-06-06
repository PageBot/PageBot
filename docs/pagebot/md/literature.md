# md.literature


## Functions

### OrderedDict
A dictionary that keeps its keys in the order in which they're inserted.

Copied from Django's SortedDict with some modifications.
### unicode_literals
### Pattern
Base class that inline patterns subclass.
### LIT_BACKLINK_TEXT
unicode(object='') -> unicode object
unicode(string[, encoding[, errors]]) -> unicode object

Create a new Unicode object from the given encoded string.
encoding defaults to the current default string encoding.
errors can be 'strict', 'replace' or 'ignore' and defaults to 'strict'.
### Postprocessor
Postprocessors are run after the ElementTree it converted back into text.

Each Postprocessor implements a "run" method that takes a pointer to a
text string, modifies it as necessary and returns a text string.

Postprocessors must extend markdown.Postprocessor.
### NBSP_PLACEHOLDER
unicode(object='') -> unicode object
unicode(string[, encoding[, errors]]) -> unicode object

Create a new Unicode object from the given encoded string.
encoding defaults to the current default string encoding.
errors can be 'strict', 'replace' or 'ignore' and defaults to 'strict'.
### Treeprocessor
Treeprocessors are run on the ElementTree object before serialization.

Each Treeprocessor implements a "run" method that takes a pointer to an
ElementTree, modifies it as necessary and returns an ElementTree
object.

Treeprocessors must extend markdown.Treeprocessor.
### function makeExtension
Return an instance of the LiteraturesExtension
### LiteraturePreprocessor
Find all literature references and store for later use.
### LiteraturePostprocessor
Replace placeholders with html entities.
### Preprocessor
Preprocessors are run after the text is broken into lines.

Each preprocessor implements a "run" method that takes a pointer to a
list of lines of the document, modifies it as necessary and returns
either the same pointer or a pointer to a new list.

Preprocessors must extend markdown.Preprocessor.
### etree
### Extension
Base class for extensions to subclass.
### text_type
unicode(object='') -> unicode object
unicode(string[, encoding[, errors]]) -> unicode object

Create a new Unicode object from the given encoded string.
encoding defaults to the current default string encoding.
errors can be 'strict', 'replace' or 'ignore' and defaults to 'strict'.
### LiteratureTreeprocessor
Build and append literature div to end of document.
### TABBED_RE
Compiled regular expression objects
### DEF_RE
Compiled regular expression objects
### LiteraturePattern
InlinePattern for literature markers in a document's body text.
### LiteratureExtension
Literature Extension.
