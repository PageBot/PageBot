# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#    dating.py
#
import datetime
from time import localtime
from random import randint
import re

def uniqueLong():
    """The uniqueLong method answers a unique number (as string) of 18 digits.

    >>> len(uniqueLong())
    18
    """
    return Dating.timeStampRandomLong()

def timeStampLong():
    """The timeStampLong method answers the timestamp. This may not be unique.

    >>> len(timeStampLong()) # '152081005707'
    12
    """
    return Dating.timeStampLong()

def uniqueId(size=0):
    """The uniqueId method answers a unique number (as string) of size length
    concatenated timestamps. Minimum length of the number is 18 digits, or else
    string will not be unique.

    >>> len(uniqueId())
    18
    """
    n = ''
    size = max(size,18)
    while len(n) < size:
        n += str(uniqueLong())
    return n[:size]

def leapYear(year):
    """Most common first

    >>> leapYear(1956)
    True
    >>> leapYear(1957)
    False
    >>> leapYear(1900) # No leapday on century crossings.
    False
    >>> leapYear(2000) # But there is a leapday on millennium crossings.
    True
    """
    if year % 4 != 0:
        return False

    if year % 400 == 0:
        return True

    if year % 100 == 0:
        return False

    return True

def monthDays(year, month):
    # Separate method, so it also can be used on initialization
    if month == 2:
        if leapYear(year):
            return 29
        else:
            return 28
    elif month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    else:
        return 30

def checkDateTime(date):
    """The checkDateTime answers the date if it is a date. If date is None,
    then answer None. If date is a string, then convert to datetime. Check on
    the month and day boundaries. Answer the same type that date was. Note that
    we do not check if date was already a datetime. This method is especially
    made to set database fields with dates, where that None will result in a
    NULL value for that field."""
    if not date: # Check on None or empty string
        return None
    if not isinstance(date, datetime):
        return datetime(date=date).date
    return date

def now():
    """Answers the current DateTime instance.

    >>> Dating(year=1900) < now()
    True
    >>> now() < Dating(year=2500)
    True
    """
    return Dating(date='now')

def milliSeconds(milliSeconds):
    """Answers the Duration instance for this amount of milliSeconds

    >>> milliSeconds(5) # Shown as the amount of weeks, days, seconds and ms
    Duration(0d, 0s, 5000us)
    """
    return Duration(milliSeconds=milliSeconds)

def microSeconds(microSeconds):
    """Answers the Duration instance for this amount of microSeconds

    >>> microSeconds(5) # Shown as the amount of days and seconds
    Duration(0d, 0s, 5us)
    """
    return Duration(microSeconds=microSeconds)

def seconds(seconds):
    """Answers the Duration instance for this amount of seconds

    >>> seconds(5) # Shown as the amount of weeks, days, seconds and ms
    Duration(0d, 5s, 0us)
    """
    return Duration(seconds=seconds)

def minutes(minutes):
    """Answers the Duration instance for this amount of minutes

    >>> minutes(5) # Shown as the amount of weeks, days, seconds and ms
    Duration(0d, 300s, 0us)
    >>> minutes(100)
    Duration(0d, 6000s, 0us)
    >>> minutes(1000)
    Duration(0d, 60000s, 0us)
    >>> minutes(10000)
    Duration(6d, 81600s, 0us)
    """
    return Duration(minutes=minutes)

def hours(hours):
    """Answers the Duration instance for this amount of hours

    >>> hours(5) # Shown as the amount of weeks, days, seconds and ms
    Duration(0d, 18000s, 0us)
    >>> hours(100)
    Duration(4d, 14400s, 0us)
    """
    return Duration(hours=hours)

def days(days):
    """Answers the Duration instance for this amount of days

    >>> days(5) # Shown as the amount of weeks
    Duration(5d, 0s, 0us)
    """
    return Duration(days=days)

def weeks(weeks):
    """Answers the Duration instance for this amount of weeks.
    Beyond weeks, the duration depends on the starting date.

    >>> weeks(5) # Shown as the amount of weeks
    Duration(35d, 0s, 0us)
    """
    return Duration(weeks=weeks)

# weeks is the maximum number of a Duration that we know without
# using a start date. As months (and beyond) lengths depend on
# which month it is.

def year(year):
    """Answers the datetime instance of that year

    >>> year(2019)
    Dating(date='2019-01-01')
    """
    return Dating(year=year, month=1, day=1)

def newdatetime(date):
    """The newdatetime method answers a new datetime instance. If the date is
    None, then answer None. If date is a string, then convert to datetime.
    Check on the month and day boundaries."""
    if date is None:
        return None
    if not isinstance(date, datetime):
        date = datetime(date=date)
    return date

class Duration:
    """The Duration class contains a duration in time. It can e.g. be used to
    add to a datetime instance with a new date as result.

    All common arithmetic applies to a Duration instance.

    >>> Duration(3)
    Duration(3d, 0s, 0us)
    >>> Duration(seconds=10)
    Duration(0d, 10s, 0us)
    >>> d = Duration(3)
    >>> d * 3 # is a duration of 9 days.
    Duration(9d, 0s, 0us)
    >>> d + 2 # is a duration of 6 days
    Duration(8d, 0s, 0us)

    """
    def __init__(self, days=0, seconds=0, microSeconds=0, milliSeconds=0,
            minutes=0, hours=0, weeks=0, td=None):
        """An extension of the builtin datetime.timedelta class, extending to
        millennia to match SQL's INTERVAL type Note that by itself, a duration
        of months is meaningless due to diffing month lengths. But when doing
        date arithmetic, we can figure it out."""
        if td:
            self.timedelta = td
        else:
            self.timedelta = datetime.timedelta(days, seconds, microSeconds, milliSeconds, minutes, hours, weeks)


    def _get_weeks(self):
        return self.timedelta.days // 7

    weeks = property(_get_weeks)

    def _get_days(self):
        return self.timedelta.days

    days = property(_get_days)

    def _get_hours(self):
        return self.timedelta.second // (60 * 60)

    hours = property(_get_hours)

    def _get_minutes(self):
        return self.timedelta.seconds // 60

    minutes = property(_get_minutes)

    def _get_seconds(self):
        return self.timedelta.seconds

    seconds = property(_get_seconds)

    def _get_microSeconds(self):
        return self.timedelta.microseconds

    microSeconds = property(_get_microSeconds)

    def __len__(self):
        return self.days

    def __str__(self):
        return '%s(%dd, %ds, %dus)' % (self.__class__.__name__, self.days, self.seconds, self.microSeconds)

    __repr__ = __str__

    # To be added __iter__

    def __coerce__(self, p):
        return None

    def __nonzero__(self):
        return self.weeks or self.days or self.seconds or self.microSeconds

    def __eq__(self, other):
        if not isinstance(other, Duration):
            return False
        return self.timedelta == other.timedelta

    def __ne__(self,other):
        if not isinstance(other, Duration):
            return False
        return self.timedelta != other.timedelta

    def __mul__(self, n):
        assert isinstance(n, (int, float))
        return Duration(td=self.timedelta*n)

    def __div__(self, n):
        assert isinstance(n, (int, float))
        return Duration(td=self.timedelta/n)

    __truediv__ = __div__
    __itruediv__ = __rtruediv__ = __rdiv__ = __div__

    # FIXME: gives a pylint error:
    # E:287,27: bad operand type for unary -: NoneType (invalid-unary-operand-type)
    def __neg__(self):
        return Duration(td=-self.timedelta)

    def __add__(self, value):
        # Duration + Date = Date
        # Duration + Duration = Duration
        # Duration + 3 = Duration
        if isinstance(value, (int, float)): # Count as days
            return self + Duration(td=self.timedelta + datetime.timedelta(value))

        if isinstance(value, Duration):
            return Duration(td=self.timedelta + value.timedelta)

        if isinstance(value, Dating):
            return Dating(year=value.year, day=value.day+self.days, hour=value.hour,
                minute=value.minute, second=value.second+self.seconds,
                microSecond=value.microSecond+self.microSeconds)

        raise ValueError('[Duration.__add__] Illegal type to add to a Duration instance "%s"' % value)

    def __sub__(self, dating):
        # Duration - Date = Date
        # Duration - Duration = Duration
        # Duration - 3 = Duration
        if isinstance(dating, (int, float, Duration)):
            return self + -dating

        if isinstance(dating, Dating):
            return dating + -self

        raise ValueError('[Duration.__sub__] Illegal type to subtract from a Duration instance "%s"' % dating)

    def __iadd__(self, item):
        return self + item

    def __isub__(self, item):
        return self - item

    def __imul__(self, item):
        return self * item

    def __idiv__(self, item):
        return self / item

    def min(self):
        """Most negative timedelta object that can be represented.

        """
        return datetime.timedelta.min

    def max(self):
        """Most positivie timedelta object that can be represented.

        """
        return datetime.timedelta.max

    def resolution(self):
        """Smallest resolvable difference that a timedelta object can represent.

        """
        return datetime.timedelta.resolution

class Dating:
    """The newdate method answers a new datetime instance. If the date is None,
    then answer None. If date is a string, then convert to datetime. Check on
    the month and day boundaries.

    - Initialize the current date if the date is equal to now
    - Initialize on first day of the week if year and week are defined
    - Initialize from existing datetime if "dt" is defined
    - Initialize from datetime string, date and time separated by white space.
    - Initialize from date string (identical to the result of self.date) if defined
    - Initialize from time string (identical to the result of self.time) if defined
    - Initialize from (year, month, day) if all of them are defined.
    - Otherwise raise an error

    If the trimvalues attribute is set to False (default is True) then the
    input values of the date are _not_ trimmed to their minimum and
    maximum values. This checking is done in context for days in months and
    years.

    >>> #Dating(date='now') # 2018-03-15 13:50:55
    >>> Dating(date='2018-11-23')
    Dating(date='2018-11-23')
    >>> Dating(date='2018-11-23', time='23:11')
    Dating(date='2018-11-23' time='23:11:00')
    >>> Dating(date='2018-11-23', time='23:11:22')
    Dating(date='2018-11-23' time='23:11:22')
    >>> Dating(2018, 11, 23)
    Dating(date='2018-11-23')
    >>> Dating(2018, 11, 23, 23, 11, 22, 0)
    Dating(date='2018-11-23' time='23:11:22')
    >>> Dating(2018, week=23)
    Dating(date='2018-06-04')
    >>> d1 = Dating(year=2018, month=2, day=10)
    >>> d2 = Dating(year=2018, month=3, day=14)
    """
    """
    >>> d1 + Duration(123)
    Dating(date='2018-06-13' time='00:00:00')
    >>> #d1 - Duration(days=2)
    2018-06-11 00:00:00
    >>> p = Duration(seconds=10) * 6 / 2 # Calculate with durations, 30 seconds
    >>> p
    Duration(0d, 30s, 0us)
    >>> #d1 + Duration(days=10)
    2018-06-23 00:00:00
    >>> d1.weekDay, d1.dayName, d1.month, d1.monthName
    (5, 'Sat', 2, 'Feb')
    >>> d1.nextWorkDay, d1.nextWorkDay.dayName
    (Dating(date='2018-02-12' time='00:00:00'), 'Mon')
    >>> d1 + 6 # 6 days later
    Dating(date='2018-02-16' time='00:00:00')
    >>> d1.month, d1.monthName
    (2, 'Feb')
    >>> d1.week, d2.week
    (6, 11)
    >>> d1.nextWorkDay # Next working day of dating d1
    Dating(date='2018-02-12' time='00:00:00')
    >>> d1
    Dating(date='2018-02-10' time='00:00:00')
    >>> d1 + p # Date + 30 seconds
    Dating(date='2018-02-10' time='00:00:30')
    >>> d1 + p + minutes(20) # Add 30 seconds and 20 minutes
    Dating(date='2018-02-10' time='00:20:30')
    >>> d1 + 6 # Answer a Dating for six days later
    Dating(date='2018-02-16' time='00:00:00')
    >>> d1 + 60 # Answer a Dating for sixty days later
    Dating(date='2018-04-11' time='00:00:00')
    >>> d1 + 600 # Answer a Dating for sixhundred days later --> 2019
    Dating(date='2019-10-03' time='00:00:00')
    >>> (d1 + 60).nextWorkDay # First work day after 600 days
    Dating(date='2018-04-11' time='00:00:00')
    >>> #d1 - 20 # 20 days earlier
    2018-01-21 00:00:00
    >>> d1 - p # 30 seconds earlier
    Dating(date='2018-02-09' time='23:59:30')
    >>> d1.date
    '2018-02-10'
    >>> d1.dateNumber
    20180210
    >>> d1.time # Single date
    '00:00:00'
    >>> d1.dateTuple
    (2018, 2, 10)
    >>> d1.nextDayNamed(5).dayName
    'Sat'
    >>> d1.nextDayNamed(5).nextWorkDay.dayName
    'Mon'
    >>> d1.nextDayNamed(6).nextWorkDay.dayName
    'Mon'
    >>> d1.leapYear
    False
    >>> Dating(date='2000-2-29').leapYear
    True
    >>> d3 = Dating(2007, 12, 20)
    >>> d3
    Dating(date='2007-12-20' time='00:00:00')
    >>> d3.nextMonth
    Dating(date='2008-01-01' time='00:00:00')
    >>> #d3.prevMonth # Goes back to previous year
    2007-11-01 00:00:00
    >>> #d3 - d1

    >>> d3 = Dating(d1.year, d1.month, 1)
    >>> d3
    Dating(date='2018-02-01' time='00:00:00')
    >>> d1.monthStart, d1.monthEnd
    (Dating(date='2018-02-01' time='00:00:00'), Duration(0m, 38d, 0s, 0us))
    >>> d1 - Duration(days=1)
    Dating(date='2018-02-09' time='00:00:00')
    >>> Dating(date='2007-12-10').monthStart.week # First week of this month
    48
    >>> #Dating(date='2007-12-10').monthStart.weekStart # Date of start of first week of this month

    """
    """

    print('Date of start of first week of this month', datetime(date='2007-12-10').monthStart.weekStart)
    print('Previous month of 2007-12-10 is', datetime(date='2007-12-10').prevMonth.date)
    print('Previous month of 2008-1-10 is', datetime(date='2008-1-10').prevMonth.date)
    print('Next month of 2007-12-10 is', datetime(date='2007-12-10').nextMonth.date)
    print('Next month of 2008-1-10 is', datetime(date='2008-1-10').nextMonth.date)
    print('First day of third week', datetime(year=2008, week=2).date)
    print('Trim day value', datetime(year=2008, month=2, day=35).date)
    print('Trim month and day value', datetime(year=2008, month=22, day=35).date)
    print('Year start and end', d1.yearStart.date, d1.yearEnd.date)
    print('Month start and end', d1.monthStart.date, d1.monthEnd.date)
    print(d1.calendarMonth)
    print(datetime(date='2008-2-29').calendarMonth)
    print(datetime(date='2007-12-31').calendarYear)

    >>> dt1 = datetime(2007, 12, 20)
    >>> dt1.nextMonth.monthName
    'Jan'
    >>> dt2 = datetime(2008, 1, 15)
    >>> dt2.prevMonth.monthName
    'Dec'
    >>> (dt2 - dt1).days
    26
    >>> dt3 = datetime(dt1.year, dt1.month, 1)
    >>> dt3 + Duration(days=dt3.monthDays - 1)
    2007-12-31 00:00:00
    >>> dt1.monthStart, dt1.monthEnd
    (2007-12-01 00:00:00, 2007-12-31 00:00:00)
    >>> dt1 - Duration(days=1)
    2007-12-19 00:00:00
    >>> 'First week of this month', datetime(date='2007-12-10').monthStart.week
    ('First week of this month', 48)
    >>> 'Date of start of first week of this month', datetime(date='2007-12-10').monthStart.weekStart
    ('Date of start of first week of this month', 2007-11-26 00:00:00)
    >>> 'Previous month of 2007-12-10 is', datetime(date='2007-12-10').prevMonth.date
    ('Previous month of 2007-12-10 is', '2007-11-01')

    print('Previous month of 2008-1-10 is', datetime(date='2008-1-10').prevMonth.date)
    print('Next month of 2007-12-10 is', datetime(date='2007-12-10').nextMonth.date)
    print('Next month of 2008-1-10 is', datetime(date='2008-1-10').nextMonth.date)
    print('First day of third week', datetime(year=2008, week=2).date)
    print('Trim day value', datetime(year=2008, month=2, day=35).date)
    print('Trim month and day value', datetime(year=2008, month=22, day=35).date)
    print('Year start and end', d1.yearStart.date, d1.yearEnd.date)
    print('Month start and end', d1.monthStart.date, d1.monthEnd.date)
    print(d1.calendarMonth)
    print(datetime(date='2008-2-29').calendarMonth)
    print(datetime(date='2007-12-31').calendarYear)

    """
    # TODO: Add localized names here, supporting the language codes in constants
    keys = {'year': 0, 'month': 1, 'day': 2, 'hour': 3, 'minute': 4, 'second': 5, 'weekDay': 6, 'yearday': 7, 'tz': 8}
    dayNames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    fullDayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    monthNames = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    fullMonthNames = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    def __init__(self, year=0, month=0, day=0, hour=0, minute=0, second=0, microSecond=0, tz=None,
        dt=None, date=None, time=None, week=None, trimvalues=True, mtime=None):

        if dt is not None: # If datetime object, just store it.
            # Assume that dt is of type date string. Direct init from existing datetime
            self.datetime = dt
        else:
            if date == 'now':
                self.datetime = datetime.datetime.now()
                return

            if date is not None:
                if isinstance(date, str):
                    # Could be one of the follovwing formats
                    # YYYY-MM-DD HH:MM:SS
                    stamp = re.compile("(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)([\-\+]\d+)?")
                    m = stamp.match(date)
                    if m:
                        year = int(m.group(1))
                        month = int(m.group(2))
                        day = int(m.group(3))
                        hour = int(m.group(4))
                        minute = int(m.group(5))
                        second = int(m.group(6))
                        #@# tz must be a tzinfo object, not an integer, leave it as None for now.
                        #tz = int(m.group(7) or tz)
                    else:
                        try:
                            if '.' in date or '/' in date:
                                date = date.replace('.', '-').replace('/', '-')
                            date = date.split(' ')[0]    # Skip possible time part of date input
                            year, month, day = date.split('-')
                            if int(day) > int(year):    # If notation 25-03-2007, then swap day and year
                                year, day = day, year
                        except:
                            raise ValueError('[datetime] Wrong date format "%s"' % date)
                else:
                    # If date is an integer .... format: YYYYMMDD
                    d = str(date)
                    year, month, day = d[:4], d[4:6], d[6:]

            if mtime is not None:
                # Evaluate the number of seconds since the beginning of time
                tt = localtime(mtime)
                year = tt.tm_year
                month = tt.tm_mon
                day = tt.tm_mday
                hour = tt.tm_hour
                minute = tt.tm_min
                second = tt.tm_sec

            if time is not None:
                time = time.split(' ')[-1]    # Skip possible date part of the time input
                timeParts = time.split(':')
                if len(timeParts) == 2:
                    hour, minute = timeParts
                    second = 0
                elif len(timeParts) == 3:
                    hour, minute, second = timeParts
                    if '.' in second:
                        second, microSecond = second.split('.',1)
                        if len(microSecond) < 6:
                            microSecond += '0' * (6-len(microSecond))

            if year is not None and week is not None:
                week = int(week)
                # Set date of first day in the requested week
                dt = datetime.datetime(int(year), 1, 1) + datetime.timedelta(weeks=week)
                self.datetime = dt - datetime.timedelta(days=dt.timetuple()[self.keys['weekDay']])
                # This algorithm may be one week off, so test and adjust if it does not match.
                if self.week > week:
                    self.datetime -= datetime.timedelta(days=7)

            elif year is None or month is None or day is None:
                if time is not None:
                    # Just a time was specified,
                    year = month = day = 0
                else:
                    raise ValueError('[datetime] Did not supply all values of y,m,d (%s,%s,%s)' % (year, month, day))

            elif trimvalues:
                year = int(year)
                month = min(12, max(1, int(month)))
                day = min(monthDays(year, month), max(1, int(day)))
                hour = min(23, max(0, int(hour)))
                minute = min(60, max(0, int(minute)))
                second = min(60, max(0, int(second)))
                microSecond = min(99, max(0, int(microSecond)))
                self.datetime = datetime.datetime(year, month, day, hour, minute, second, microSecond, tz)
            else: # Nothing specified, assume it is now.
                self.datetime = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second),
                                                int(microSecond), tz)

    def __str__(self):
        """The function repr(dt) answers the string representation of the date,
        typically identical to dt.date + ' ' + dt.time.

        >>> dating = Dating(date='2018-11-23')
        >>> str(dating)
        "Dating(date='2018-11-23')"
        >>> dating += hours(4)
        """
        if self.timeTuple == (0, 0, 0):
            return "%s(date='%s')" % (self.__class__.__name__, self.date)
        return "%s(date='%s' time='%s')" % (self.__class__.__name__, self.date, self.time)

    __repr__ = __str__

    def __nonzero__(self):
        """Always answer True indicating that a dating instance can never be zero.

        """
        return True

    def __lt__(self, dating):
        """Answers True if self is in the past of date dt as in self < dt.
        Note that in evaluating the condition the difference in time is taken
        into account as well.  Use self.dateNumber < dt.dateNumber to test on
        date comparison only instead of dy < self.

        >>> dating1 = Dating(date='2019-11-23')
        >>> dating2 = Dating(date='2018-11-23') # Same date, later in time
        >>> dating2 < dating1
        True
        """
        if isinstance(dating, Dating):
            return self.datetime < dating.datetime
        return False

    def __le__(self, dating):
        """Answers True if self is in the past of or equal to date dt as in
        self <= dt.  Note that in evaluating the condition the difference in
        time is taken into account as well.  Use self.dateNumber <
        dt.dateNumber to test on date comparison only instead of dy <=
        self.

        >>> dt1 = Dating(date='2018-11-25')
        >>> dt2 = Dating(date='2018-11-23')
        >>> dt2 <= dt1
        True
        """
        if isinstance(dating, Dating):
            return self.datetime <= dating.datetime
        return False

    def __gt__(self, dating):
        """Answers True if self is in the future of or equal to date dt as in
        self > dt.  Note that in evaluating the condition the difference in
        time is taken into account as well.  Use self.dateNumber <
        dt.dateNumber to test on date comparison only instead of dy <=
        self.

        >>> dt1 = Dating(date='2019-11-25')
        >>> dt2 = Dating(date='2018-11-23')
        >>> dt2 > dt1
        False
        >>> dt2 + 500, dt2 + 500 > dt1
        (Dating(date='2020-04-06'), True)
        """
        if isinstance(dating, Dating):
            return self.datetime > dating.datetime
        return False

    def __ge__(self, dating):
        """Answers True if self is in the future of or equal to date dt as in
        self >= dt.  Note that in evaluating the condition the difference in
        time is taken into account as well.  Use self.dateNumber <
        dt.dateNumber to test on date comparison only instead of dy <=
        self.

        >>> dt1 = Dating(date='2019-11-25')
        >>> dt2 = Dating(date='2018-11-23')
        >>> dt2 >= dt1
        False
        """
        if isinstance(dating, Dating):
            return self.datetime >= dating.datetime
        return False

    def __ne__(self, dating):
        """Answers True if self is in the past of or equal to date dt as in
        self != dt.  Note that in evaluating the condition the difference in
        time is taken into account as well.  Use self.dateNumber <
        dt.dateNumber to test on date comparison only instead of dy <=
        self.

        >>> dating1 = Dating(date='2019-11-25')
        >>> dating2 = Dating(date='2018-11-23')
        >>> dating2 != dating1
        True
        """
        if isinstance(dating, Dating):
            return self.datetime != dating.dateTime
        return False

    def __eq__(self, dating):
        """Answers True if self is equal to date dt as in self == dt.  Note
        that in evaluating the condition the difference in time is taken into
        account as well. Use self.dateNumber < dt.dateNumber to test on date
        comparison only instead of dy < self.

        >>> dt1 = Dating(date='2019-11-25')
        >>> dt2 = Dating(date='2018-11-23')
        >>> dt2 == dt1
        False
        >>> dt3 = Dating(date='2018-11-23')
        >>> dt2 == dt3
        True
        """
        if isinstance(dating, Dating):
            return self.datetime == dating.datetime
        return False

    def __coerce__(self, duration):
        return None

    def __iadd__(self, item):
        return self + item

    def __isub__(self, item):
        return self - item

    def __add__(self, duration):
        """Add the duration to self.

        Date + Duration = Date
        Date + 3 = Date

        >>> d1 = Dating(year=1950)
        >>> d1 + 3
        Dating(date='1950-01-04')
        >>> d1 + 2250 # Integer defaults to adding days, creating leap day
        Dating(date='1956-02-29')
        >>> d1 + Duration(hours=8)
        Dating(date='1950-01-01' time='08:00:00')
        """
        if isinstance(duration, (int, float)):
            duration = Duration(days=duration)
        assert isinstance(duration, Duration)
        return Dating(dt=self.datetime + duration.timedelta)

    def __sub__(self, durationOrDate):
        """Subtract duration or dat from self

        Date - Duration = Date
        Date - Date = Duration
        Date - 3 = Date

        >>> d1 = Dating(year=1950)
        >>> d1 - 10
        Dating(date='1949-12-22')
        >>> d1 - Duration(days=356) # Duration(years=1) not allowed, because of leapyear context
        Dating(date='1949-01-10')
        >>> d1 - Dating(year=1949)
        Duration(365d, 0s, 0us)

        """
        if isinstance(durationOrDate, (int, float)): # Interpret as days, create a new date
            return Dating(dt=self.datetime - Duration(days=durationOrDate).timedelta)
        if isinstance(durationOrDate, Duration):
            # Date - Duration = Date
            return Dating(dt=self.datetime - durationOrDate.timedelta)
        if isinstance(durationOrDate, Dating):
            # Date - Date = Duration
            return Duration(td=self.datetime - durationOrDate.datetime)
        raise ValueError('Cannot subtract %s - %s' % (self, durationOrDate))

    def _get_year(self):
        """Answers the year of self.

        >>> Dating(year=2017).year
        2017
        """
        return self.datetime.year
    year = property(_get_year)

    @classmethod
    def timeStampRandomLong(cls):
        """The uniqueNumber property answers a unique number of format
        '20090621200511993066', derived from date, time and a six digit random
        number. This can be used e.g. in a URL as parameters to make sure that
        browser will not cache the content of the page. The number is also used
        to create a unique file name for background shell scripts.

        >>> timeStamp = Dating(year=1980).timeStampRandomLong()
        >>> len(timeStamp) # Cannot test on random number
        18
        >>> d = Dating(year=2100, month=2, day=15, hour=3).timeStampRandomLong()
        >>> len(d) # Cannot test on random number
        18
        """
        return cls.timeStampLong() + ('%06d' % randint(0, 999999))

    @classmethod
    def timeStampLong(cls):
        import time
        return '%012d' % int(time.time()*100)

    def getTimeStamp(self, usetz=False):
        """The self.getTypeStamp answers a formatted string 2010-10-05
        16:47:29+04 of the date. This is exactly what SQL needs as timestamp
        with time zone definition. Use of tz does not yet work, and is
        ignored.

        >>> Dating(year=1980).getTimeStamp()
        '1980-01-01 00:00:00'
        >>> Dating(year=2100, month=2, day=15, hour=3).getTimeStamp()
        '2100-02-15 03:00:00'
        """
        if self.datetime.tzinfo is None or not usetz:
            tz = ""
        else:
            tz = "+%02d" % self.datetime.tzinfo

        # FIXME: gives a pylint error:
        # E:287,27: bad operand type for unary -: NoneType (invalid-unary-operand-type)
        #elif self.tz < 0:
        #    tz = "-%02d" % -self.datetime.tzinfo

        return  "%s %s%s" % (self.date, self.time, tz)

    def _get_date(self):
        """The self.date property answers a formatted string 2008-10-23 of the
        date. This is exactly what SQL needs as date-string definition.

        >>> Dating(date='2017-05-01').date
        '2017-05-01'
        """
        return '%04d-%02d-%02d' % (self.year, self.month, self.day)
    date = property(_get_date)

    def _get_year(self):
        """Answers the year value of self.

        >>> Dating(year=2010).year
        2010
        """
        return self.datetime.year
    year = property(_get_year)

    def _get_month(self):
        """Answers the month value of self.

        >>> Dating(year=2010, month=5).month
        5
        """
        return self.datetime.month
    month = property(_get_month)

    def _get_day(self):
        """Answers the day value of self.

        >>> Dating(year=2010, month=5, day=15).day
        15
        """
        return self.datetime.day
    day = property(_get_day)

    def _get_hour(self):
        """Answers the hour value of self.

        >>> Dating(year=2010, month=5, day=15, hour=3).hour
        3
        """
        return self.datetime.hour
    hour = property(_get_hour)

    def _get_minute(self):
        """Answers the minute value of self.

        >>> Dating(year=2010, month=5, day=15, hour=3, minute=4).minute
        4
        """
        return self.datetime.minute
    minute = property(_get_minute)

    def _get_second(self):
        """Answers the second value of self.

        >>> Dating(year=2010, month=5, day=15, hour=3, minute=4, second=7).second
        7
        """
        return self.datetime.second
    second = property(_get_second)

    def _get_microSecond(self):
        """Answers the second value of self.

        >>> Dating(year=2010, month=5, day=15, hour=3, microSecond=11).microSecond
        11
        """
        return self.datetime.microsecond
    microSecond = property(_get_microSecond)

    def _get_euroDate(self):
        """The self.euroDate property answers a formatted string 23-10-2008 of
        the date.

        >>> Dating(date='2015-6-7').euroDate
        '07-06-2015'
        """
        return '%02d-%02d-%02d' % (self.day, self.month, self.year)
    euroDate = property(_get_euroDate)

    def _get_studyYear(self):
        """The self.studyYear property answers a string 0708 with leading zero
        for the study year from 2007-08-01 until 2008-07-31
        >>> Dating(date='2015-6-7').studyYear
        '1415'
        >>> Dating(date='2005-6-7').studyYear
        '0405'
        """
        studyYear = (self.year - 2000) * 100 + self.year - 2000 + 1
        if self.month <= 8: # Switch study year on end of summer break
            studyYear -= 101
        return '%04d' % studyYear
    studyYear = property(_get_studyYear)

    def _get_dateNumber(self):
        """The self.dateNumber property answers a long integer number 20080502
        of the date. This can by used to compare dates on day only and not on
        time. Or it can be used as ordering key.

        >>> Dating(date='2015-6-7').dateNumber
        20150607
        >>> Dating(date='2005-6-7').dateNumber
        20050607
        """
        return self.year * 10000 + self.month * 100 + self.day
    dateNumber = property(_get_dateNumber)

    def _get_dateTuple(self):
        """The self.dateTuple property answers a tuple (y,m,d) of the date.

        >>> Dating(date='2015-6-7', hour=12, minute=5).dateTuple
        (2015, 6, 7)
        """
        return self.year, self.month, self.day
    dateTuple = property(_get_dateTuple)

    def _get_time(self):
        """The self.dateNumber property answers a formatted '12:23:45' time string.

        >>> Dating(date='2015-6-7', hour=12, minute=5).time
        '12:05:00'
        """
        return '%02d:%02d:%02d' % (self.hour, self.minute, self.second)
    time = property(_get_time)

    def _get_dateTime(self):
        """The self.datetime property answers a formatted '2010-12-06 12:23:34'
        date/time string.

        >>> Dating(date='2015-6-7', hour=12, minute=5).dateTime
        '2015-06-07 12:05:00'
        """
        return '%s %s' % (self.date, self.time)
    dateTime = property(_get_dateTime)

    def _get_timeTuple(self):
        """The self.timeTuple property answers a tuple (h, m, s) of the time.

        >>> Dating(date='2015-6-7', hour=12, minute=5).timeTuple
        (12, 5, 0)
        """
        return self.hour, self.minute, self.second
    timeTuple = property(_get_timeTuple)

    def _get_timeZone(self):
        """The self.timeZone property answers the timezone dt.tz.

        """
        return self.datetime.tzinfo
    timeZone = property(_get_timeZone)

    def _get_week(self):
        """The self.week property answers the weeknummer according to ISO 8601
        where the first week of the year that contains a thursday.

        >>> Dating(date='2015-6-7', hour=12, minute=5).week
        23
        """
        return self.datetime.isocalendar()[1]
    week = property(_get_week)

    def _get_dayName(self):
        """The self.dayName property answers a 3 letter abbreviation of current
        day name.

        >>> Dating(date='2015-6-7', hour=12, minute=5).dayName
        'Sun'
        """
        return self.dayNames[self.weekDay]
    dayName = property(_get_dayName)

    def _get_fullDayName(self):
        """The self.fullDayName property answers the full name of the current
        day.

        >>> Dating(date='2015-6-7', hour=12, minute=5).fullDayName
        'Sunday'
        """
        return self.fullDayNames[self.weekDay]
    fullDayName = property(_get_fullDayName)

    def _get_monthName(self):
        """The self.monthName property answers a 3 letter abbreviation of
        current month name.

        >>> Dating(date='2015-6-7', hour=12, minute=5).monthName
        'Jun'
        """
        return self.monthNames[self.month]
    monthName = property(_get_monthName)

    def _get_fullMonthName(self):
        """The self.fullMonthName property answers the full name of the current
        month.

        >>> Dating(date='2015-6-7', hour=12, minute=5).fullMonthName
        'June'
        """
        return self.fullMonthNames[self.month]
    fullMonthName = property(_get_fullMonthName)

    def _get_monthStart(self):
        """The self.monthStart property answers the first day of the current
        month.

        >>> Dating(date='2015-6-7', hour=12, minute=5).monthStart
        Dating(date='2015-06-01' time='12:05:00')
        """
        return self + (1 - self.day) # Keep integer calculation combined by brackets
    monthStart = property(_get_monthStart)

    def _get_monthEnd(self):
        """The self.monthEnd property answers the last day of the current
        month.

        >>> Dating(date='2015-6-7', hour=12, minute=5).monthEnd
        Dating(date='2015-06-30' time='12:05:00')
        """
        return self - self.day + self.monthDays
    monthEnd = property(_get_monthEnd)

    def _get_weekStart(self):
        """The self.weekStart property answers the “Monday” date of the current
        week.

        >>> Dating(date='2015-6-7', hour=12, minute=5).weekStart
        Dating(date='2015-06-01' time='12:05:00')
        """
        return self - self.weekDay
    weekStart = property(_get_weekStart)

    def _get_weekEnd(self):
        """The self.weekEnd property answers the Friday date of the current
        week.

        >>> Dating(date='2015-6-7', hour=12, minute=5).weekEnd
        Dating(date='2015-06-08' time='12:05:00')
        """
        return self + (7 - self.weekDay)
    weekEnd = property(_get_weekEnd)

    def _get_yearStart(self):
        """The self.yearStart property answers the first day of the current
        year.

        >>> Dating(date='2015-6-7', hour=12, minute=5).yearStart
        Dating(date='2015-01-01')
        """
        return Dating(self.year, 1, 1)
    yearStart = property(_get_yearStart)

    def _get_yearEnd(self):
        """The self.yearEnd property answers the last day of the current year.

        >>> Dating(date='2015-6-7', hour=12, minute=5).yearEnd
        Dating(date='2015-12-31')
        """
        return Dating(self.year, 12, 31)
    yearEnd = property(_get_yearEnd)

    def _get_workDay(self):
        """The self.workDay property answers True if this day is one of Monday
        till Friday.

        >>> Dating(date='2015-6-7').workDay
        False
        >>> (Dating(date='2015-6-7') + 3).workDay
        True
        """
        return 0 <= self.weekDay <= 4
    workDay = property(_get_workDay)

    def _get_weekDay(self):
        """Answers the number of day in the week.

        >>> d = Dating(date='2015-6-1')
        >>> d.dayName, d.weekDay
        ('Mon', 0)
        >>> Dating(date='2015-6-7').weekDay
        6
        >>> (Dating(date='2015-6-7') + 12).weekDay
        4
        """
        return self.datetime.weekday()
    weekDay = property(_get_weekDay)

    def _get_nextWorkDay(self):
        """The self.nextWorkDay property answers the first next date (including
        itself) that is a workday

        >>> d = Dating(date='2015-6-1') - 2
        >>> d.dayName, d.nextWorkDay.dayName
        ('Sat', 'Mon')
        """
        if self.workDay:
            return self
        return self + (7 - self.weekDay) # Keep integer calculation combined by brackets
    nextWorkDay = property(_get_nextWorkDay)

    def _get_leapYear(self):
        """The self.leapYear property answers a boolean if the dt is a leap
        year.

        >>> Dating(date='2015-6-1').leapYear
        False
        >>> Dating(date='2020-6-1').leapYear
        True
        """
        return leapYear(self.year)
    leapYear = property(_get_leapYear)

    def _get_yearDays(self):
        """The self.yearDays property answers the number of days in the current
        year.

        >>> Dating(date='2015-6-1').yearDays
        365
        >>> Dating(date='2020-6-1').yearDays
        366
        """
        if leapYear(self.year):
            return 366
        return 365
    yearDays = property(_get_yearDays)

    def _get_monthDays(self):
        """The self.monthDays property answers the number of days in the
        current month.

        >>> Dating(date='2015-2-1').monthDays
        28
        >>> Dating(date='2020-2-1').monthDays
        29
        >>> Dating(date='2020-8-1').monthDays
        31
        >>> Dating(date='2020-9-1').monthDays
        30
        """
        return monthDays(self.year, self.month)
    monthDays = property(_get_monthDays)

    def _get_nextMonth(self):
        """The nextMonth property answers the first day of the month after the
        current month. Due to length differences between the months, it is not
        consistent to answer the current day number in the next month, so it is
        set to 1.

        >>> Dating(date='2015-2-1').nextMonth
        Dating(date='2015-03-01')
        >>> Dating(date='2015-12-1').nextMonth
        Dating(date='2016-01-01')
        """
        return self + (self.monthDays - self.day + 1)
    nextMonth = property(_get_nextMonth)

    def _get_prevMonth(self):
        """The prevMonth property answers the first day of the month previous
        to the current month. Due to length differences between the months, it
        is not consistent to answer the current day number in the previous
        month

        >>> Dating(date='2015-2-1').prevMonth
        Dating(date='2015-01-01')
        >>> Dating(date='2015-12-1').prevMonth
        Dating(date='2015-11-01')
        """
        return (self.monthStart - 1).monthStart
    prevMonth = property(_get_prevMonth)

    def _get_calendarMonth(self):
        """The calendarMonth property answers a list of lists containing the
        weeks with dates of the current month. Note that the first and lost
        week are filled with the days of end of the previous month and the
        start of the next month.

            [
                [p01, p02, p03, d01, d02, d03, d04],
                [d05, d06, d07, d08, d09, d10, d11],
                [d12, d13, d14, d15, d16, d17, d18],
                [d19, d20, d21, d22, d23, d24, d25],
                [d26, d27, d28, d29, d30, n01, n02]
            ]

        >>> len(Dating(date='2015-2-1').calendarMonth) # Number of weeks
        5
        >>> Dating(date='2015-2-1').calendarMonth[3][2] # Second day of 3rd week
        Dating(date='2015-02-18')
        >>> Dating(date='2015-2-1').calendarMonth[0][0] # First day of first week in previous month
        Dating(date='2015-01-26')
        >>> Dating(date='2015-2-1').calendarMonth[-1][-1] # Last day of last week
        Dating(date='2015-03-01')
        """
        monthWeekDates = []
        weekStart = self.monthStart.weekStart
        running = False
        while not running or weekStart.month == self.month:
            weekDates = []
            monthWeekDates.append(weekDates)
            for day in range(7):
                weekDates.append(weekStart + day)
            weekStart += 7
            running = True
        return monthWeekDates
    calendarMonth = property(_get_calendarMonth)

    def _get_calendarYear(self):
        """The calendarYear property answers a list of lists of lists
        containing all calendarMonths of the year.

            [
            [
                [p01, p02, p03, d01, d02, d03, d04],
                [d05, d06, d07, d08, d09, d10, d11],
                [d12, d13, d14, d15, d16, d17, d18],
                [d19, d20, d21, d22, d23, d24, d25],
                [d26, d27, d28, d29, d30, n01, n02]
            ]
            [
            ...
            ]
            ...
            ]

        >>> len(Dating(date='2015-2-1').calendarYear) # Number of months
        12
        >>> Dating(date='2015-2-1').calendarYear[3][1][2] # Second day of first week of 3rd month
        Dating(date='2015-04-08')
        """
        yearWeekDates = []
        for month in range(1, 13):
            yearWeekDates.append(Dating(year=self.year, month=month, day=1).calendarMonth)
        return yearWeekDates
    calendarYear = property(_get_calendarYear)

    def nextDayNamed(self, weekDay):
        if not (0 <= weekDay <= 7):
            raise ValueError('[%s.nextDayNamed] weekDay "%s" must be in range (0, 8)' % (self.__class__.__name__, weekDay))
        nextDay = self + Duration(days=1)
        for n in range(1, 8):
            if nextDay.weekDay == weekDay:
                return nextDay
            nextDay = nextDay + n
        return None

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
