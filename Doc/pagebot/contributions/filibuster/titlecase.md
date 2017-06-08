# contributions.filibuster.titlecase

### CAPFIRST
Compiled regular expression objects
### INLINE_PERIOD
Compiled regular expression objects
### str PUNCT
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### str SMALL
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### SMALL_FIRST
Compiled regular expression objects
### SMALL_LAST
Compiled regular expression objects
### SMALL_WORDS
Compiled regular expression objects
### SUBPHRASE
Compiled regular expression objects
### class TitlecaseTests
Tests to ensure titlecase follows all of the rules
### UC_ELSEWHERE
Compiled regular expression objects
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
### str __doc__
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
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
### def titlecase
Titlecases input text

This filter changes all words to Title Caps, and attempts to be clever
about *un*capitalizing SMALL words like a/an/the in the input.

The list of "SMALL words" which are not capped comes from
the New York Times Manual of Style, plus 'vs' and 'v'.
