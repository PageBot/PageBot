# toolbox.dating

### DateTime
The ``newdate`` method answers a new ``DateTime`` instance. If the ``date`` is
``None``, then answer ``None``. If ``date`` is a string, then convert to
``DateTime``. Check on the month and day boundaries.<br/>
<list>
<li>Initialize the current date if the ``date`` is equal to ``now``</li>
<li>Initialize on first day of the week if year and week are defined</li>
<li>Initialize from existing datetime if "dt" is defined</li>
<li>Initialize from ``date_time`` string, date and time separated by white space.</li>
<li>Initialize from ``date`` string (identical to the result of self.date) if defined</li>
<li>Initialize from ``time`` string (identical to the result of self.time) if defined</li>
<li>Initialize from (year, month, day) if all of them are defined.</li>
<li>Otherwise raise an error</li>
</list>
If the ``trimvalues`` attribute is set to ``False`` (default is ``True``) then the
input values of the date are <em>not</em> trimmed to their minimum and maximum values. This checking is done in
context for days in months and years.<br/>
<python>
DateTime(date='now')
DateTime(date='2008-11-23')
DateTime(date='2008-11-23', time='23:11')
DateTime(date='2008-11-23', time='23:11:22')
DateTime(2008, 11, 23)
DateTime(2008, 11, 23, 23, 11, 22, 0)
DateTime(2008, week=23)
</python>
### Duration
The ``Duration`` class contains a duration in time. It can e.g. be used to add to a ``DateTime``
instance with a new date as result.<br/>
<python>
Duration(3)<br/>
Duration(seconds=10)<br/>
Duration(td=timedelta)<br/>
</python>
All common arithmetic applies to a ``Duration`` instance. 
<python>
d = Duration(3)<br/>
d * 3 is a duration of 6 days.<br/>
</python>
### Period
The ``Duration`` class contains a duration in time. It can e.g. be used to add to a ``DateTime``
instance with a new date as result.<br/>
<python>
Duration(3)<br/>
Duration(seconds=10)<br/>
Duration(td=timedelta)<br/>
</python>
All common arithmetic applies to a ``Duration`` instance. 
<python>
d = Duration(3)<br/>
d * 3 is a duration of 6 days.<br/>
</python>
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
### def checkdatetime
The ``checkdatetime`` answers the ``date`` if it is a date. If date is None, then answer None. If
date is a string, then convert to DateTime. Check on the month and day boundaries. Answer the same type that date
was. Note that we do not check if date was already a DateTime. This method is especially made to set database fields
with dates, where that None will result in a NULL value for that field.
### def leapyear
### localtime
localtime([seconds]) -> (tm_year,tm_mon,tm_mday,tm_hour,tm_min,
  tm_sec,tm_wday,tm_yday,tm_isdst)

Convert seconds since the Epoch to a time tuple expressing local time.
When 'seconds' is not passed in, convert the current time instead.
### def monthdays
### def newdatetime
The ``newdate`` method answers a new ``DateTime`` instance. If the ``date`` is
``None``, then answer ``None``. If ``date`` is a string, then convert to
``DateTime``. Check on the month and day boundaries.<br/>
### def timestampLong
The ``timestampLong`` method answers the timestamp. This may not be unique.
### def uniqueId
The ``uniqueId`` method answers a unique number (as string) of ``size`` length concatenated
timestamps. Minimum length of the number is 18 digits, or else string will not be unique.
### def uniqueLong
The ``uniqueLong`` method answers a unique number (as string) of 18 digits.
