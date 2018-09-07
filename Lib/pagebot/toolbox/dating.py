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
    """The uniqueId method answers a unique number (as string) of size length concatenated
    timestamps. Minimum length of the number is 18 digits, or else string will not be unique.

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
    >>> leapYear(2000) # But there is a leapday on millemium crossings.
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

def checkdatetime(date):
    """

    The checkdatetime answers the date if it is a date. If date is None, then answer None. If
    date is a string, then convert to datetime. Check on the month and day boundaries. Answer the same type that date
    was. Note that we do not check if date was already a datetime. This method is especially made to set database fields
    with dates, where that None will result in a NULL value for that field.

    """
    if not date: # Check on None or empty string
        return None
    if not isinstance(date, datetime):
        return datetime(date=date).date
    return date

def now():
    return datetime(date='now')

def milliseconds(milliseconds):
    """Answer the Duration instance for this amount of milliseconds

    >>> milliseconds(5) # Shown as the amount of days and seconds
    Duration(0m, 0d, 0s, 5000us)
    """
    return Duration(milliseconds=milliseconds)

def microseconds(microseconds):
    """Answer the Duration instance for this amount of microseconds

    >>> microseconds(5) # Shown as the amount of days and seconds
    Duration(0m, 0d, 0s, 5us)
    """
    return Duration(microseconds=microseconds)

def seconds(seconds):
    """Answer the Duration instance for this amount of seconds

    >>> seconds(5) # Shown as the amount of days and seconds
    Duration(0m, 0d, 5s, 0us)
    """
    return Duration(seconds=seconds)

def minutes(minutes):
    """Answer the Duration instance for this amount of minutes

    >>> minutes(5) # Shown as the amount of days and seconds
    Duration(0m, 0d, 300s, 0us)
    >>> minutes(100) # Shown as the amount of days and seconds
    Duration(0m, 0d, 6000s, 0us)
    >>> minutes(1000) # Shown as the amount of days and seconds
    Duration(0m, 0d, 60000s, 0us)
    >>> minutes(10000) # Shown as the amount of days and seconds
    Duration(0m, 6d, 81600s, 0us)
    """
    return Duration(minutes=minutes)

def hours(hours):
    """Answer the Duration instance for this amount of hours

    >>> hours(5) # Shown as the amount of seconds
    Duration(0m, 0d, 18000s, 0us)
    >>> hours(100) # Shown as the amount of seconds
    Duration(0m, 4d, 14400s, 0us)
    """
    return Duration(hours=hours)

def days(days):
    """Answer the Duration instance for this amount of days

    >>> days(5) # Shown as the amount of months
    Duration(0m, 5d, 0s, 0us)
    """
    return Duration(days=days)

def months(months):
    """Answer the Duration instance for this amount of months

    >>> months(5) # Shown as the amount of months
    Duration(5m, 0d, 0s, 0us)
    """
    return Duration(months=months)

def years(years):
    """Answer the Duration instance for this amount of years

    >>> years(1) # Shown as the amount of months
    Duration(12m, 0d, 0s, 0us)
    >>> years(5) # Shown as the amount of months
    Duration(60m, 0d, 0s, 0us)
    """
    return Duration(years=years)

def decades(decades):
    """Answer the Duration instance for this amount of decades

    >>> decades(1) # Shown as the amount of months
    Duration(120m, 0d, 0s, 0us)
    >>> decades(5) # Shown as the amount of months
    Duration(600m, 0d, 0s, 0us)
    """
    return Duration(decades=decades)

def centuries(centuries):
    """Answer the Duration instance for this amount of centuries

    >>> centuries(1) # Shown as the amount of months
    Duration(1200m, 0d, 0s, 0us)
    >>> centuries(5) # Shown as the amount of months
    Duration(6000m, 0d, 0s, 0us)
    """
    return Duration(centuries=centuries)

def millennia(millennia):
    """Answer the Duration instance for this amount of millennia

    >>> millennia(1) # Shown as the amount of months
    Duration(12000m, 0d, 0s, 0us)
    >>> millennia(5) # Shown as the amount of months
    Duration(60000m, 0d, 0s, 0us)
    """
    return Duration(millennia=millennia)


def year(year):
    """Answer the datetime instance of that year

    >>> year(2019)
    Dating(date='2019-01-01' time='00:00:00')
    """
    return Dating(year=year, month=1, day=1)

def newdatetime(date):
    """
    The newdatetime method answers a new datetime instance. If the date is
    None, then answer None. If date is a string, then convert to
    datetime. Check on the month and day boundaries.

    """
    if date is None:
        return None
    if not isinstance(date, datetime):
        date = datetime(date=date)
    return date

class Duration:
    """The Duration class contains a duration in time. It can e.g. be used to add to a datetime
    instance with a new date as result.
    All common arithmetic applies to a Duration instance.

    >>> Duration(3)
    Duration(0m, 3d, 0s, 0us)
    >>> Duration(seconds=10)
    Duration(0m, 0d, 10s, 0us)
    >>> d = Duration(3)
    >>> d * 3 # is a duration of 9 days.
    Duration(0m, 9d, 0s, 0us)
    >>> d + 2 # is a duration of 6 days
    Duration(0m, 5d, 0s, 0us)

    """

    #hack months and larger onto datetime.timedleta, which only goes up to weeks
    months = None
    timeDelta = None

    def __init__(self, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, 
            weeks=0, months=0, years=0, decades=0, centuries=0, millennia=0, td=None):
        """

        An extension of the builtin datetime.timeDelta class, extending to millennia to match SQL's INTERVAL type
        Note that by itself, a duration of months is meaningless due to diffing month lengths.
        But when doing date arithmetic, we can figure it out.

        """
        # Convert everything larger than months into months
        self.months = float(months + years*12 + decades*120 + centuries*1200 + millennia*12000)

        if td is not None:
            self.timeDelta = td
        else:
            self.timeDelta = datetime.timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)

    def _get_days(self):
        return self.timeDelta.days
    days = property(_get_days) 
    
    def _get_seconds(self):
        return self.timeDelta.seconds
    seconds = property(_get_seconds) 
    
    def _get_microseconds(self):
        return self.timeDelta.microseconds
    microseconds = property(_get_microseconds) 
    
    def __len__(self):
        return self.days

    def __str__(self):
        return '%s(%dm, %dd, %ds, %dus)' % (self.__class__.__name__, self.months, self.days, self.seconds, self.microseconds)

    __repr__ = __str__

    # To be added __iter__

    def __coerce__(self, p):
        return None

    def __nonzero__(self):
        return self.months or self.days or self.seconds or self.microseconds

    def __eq__(self, other):
        if not isinstance(other, Duration):
            return False
        return self.months==other.months and self.days==other.days and self.seconds==other.seconds and self.microseconds==other.microseconds

    def __ne__(self,other):
        return not self.__eq__(other)

    def __mul__(self, n):
        return Duration(months=self.months * n, days=self.days * n, seconds=self.seconds * n, microseconds=self.microseconds * n)

    def __div__(self, n):
        return Duration(months=self.months / n, days=self.days / n, seconds=self.seconds / n, microseconds=self.microseconds / n)

    __truediv__ = __div__
    __itruediv__ = __rtruediv__ = __rdiv__ = __div__

    def __neg__(self):
        return self * -1;

    def __add__(self, value):
        # Duration + Date = Date
        # Duration + Duration = Duration
        # Duration + 3 = Duration
        if isinstance(value, int):
            return self + Duration(days=value)

        if isinstance(value, Duration):
            return Duration(months=self.months + value.months, days=self.days + value.days, seconds=self.seconds + value.seconds, microseconds=self.microseconds + value.microseconds)

        if isinstance(value, Dating):
            #need to do some magic to take into account leap years etc
            extraDays = 0
            import math

            if self.months > 0:
                otherMonth = value.month
                otherYear = value.year
                monthsElapsed = 0

                intMonths = math.floor(self.months)
                decMonths = self.months - intMonths

                while monthsElapsed < intMonths:
                    extraDays += monthDays(otherYear, otherMonth)

                    otherMonth += 1
                    if otherMonth > 12:
                        otherMonth = 1
                        otherYear += 1
                    monthsElapsed += 1

                extraDays += decMonths * 30 #arbitrarily picking 30 days for fractional months

            elif self.months < 0:
                otherMonth = value.month
                otherYear = value.year
                monthsElapsed = 0

                intMonths = math.floor(abs(self.months))
                decMonths = abs(self.months) - intMonths

                while monthsElapsed < intMonths:
                    otherMonth -= 1
                    if otherMonth < 1:
                        otherMonth = 12
                        otherYear -= 1
                    monthsElapsed += 1

                    extraDays += monthDays(otherYear,otherMonth)

                extraDays += decMonths * 30 #arbitrarily picking 30 days for fractional months

                extraDays = -extraDays

            if extraDays:
                return Dating(dt=value.datetime + datetime.timedelta(days=extraDays) + self.timeDelta)
            else:
                return Dating(dt=value.datetime + self.timeDelta)
        raise ValueError('[Duration.__add__] Illegal type to add to a Duration instance "%s"' % value)

    def __sub__(self, dating):
        # Duration - Date = Date
        # Duration - Duration = Duration
        # Duration - 3 = Duration
        if isinstance(dating, (int, float, Duration)):
            return self + -dating

        if isinstance(dating, Dating):
            return dating + -self

        raise ValueError('[Duration.__sub__] Illegal type to subtract from a Duration instance "%s"' % dt)

    def __iadd__(self, item):
        return self + item

    def __isub__(self, item):
        return self - item

    def __imul__(self, item):
        return self * item

    def __idiv__(self, item):
        return self / item

    def min(self):
        """Most negative timeDelta object that can be represented.

        """
        return datetime.timedelta.min

    def max(self):
        """Most positivie timeDelta object that can be represented.

        """
        return datetime.timedelta.max

    def resolution(self):
        """Smallest resolvable difference that a timeDelta object can represent.

        """
        return datetime.timedelta.resolution

class Dating:
    """
    The newdate method answers a new datetime instance. If the date is
    None, then answer None. If date is a string, then convert to
    datetime. Check on the month and day boundaries.

    Initialize the current date if the date is equal to now
    Initialize on first day of the week if year and week are defined
    Initialize from existing datetime if "dt" is defined
    Initialize from datetime string, date and time separated by white space.
    Initialize from date string (identical to the result of self.date) if defined
    Initialize from time string (identical to the result of self.time) if defined
    Initialize from (year, month, day) if all of them are defined.
    Otherwise raise an error

    If the trimvalues attribute is set to False (default is True) then the
    input values of the date are <em>not</em> trimmed to their minimum and maximum values. This checking is done in
    context for days in months and years.

    >>> #Dating(date='now') # 2018-03-15 13:50:55
    >>> Dating(date='2018-11-23')
    Dating(date='2018-11-23' time='00:00:00')
    >>> Dating(date='2018-11-23', time='23:11')
    Dating(date='2018-11-23' time='23:11:00')
    >>> Dating(date='2018-11-23', time='23:11:22')
    Dating(date='2018-11-23' time='23:11:22')
    >>> Dating(2018, 11, 23)
    Dating(date='2018-11-23' time='00:00:00')
    >>> Dating(2018, 11, 23, 23, 11, 22, 0)
    Dating(date='2018-11-23' time='23:11:22')
    >>> Dating(2018, week=23)
    Dating(date='2018-06-04' time='00:00:00')
    >>> d1 = Dating(year=2018, month=2, day=10)
    >>> d2 = Dating(year=2018, month=3, day=14)
    >>> d1 + Duration(123)
    Dating(date='2018-06-13' time='00:00:00')
    >>> #d1 - Duration(days=2)
    2018-06-11 00:00:00
    >>> p = Duration(seconds=10) * 6 / 2 # Calculate with durations, 30 seconds
    >>> p
    Duration(0m, 0d, 30s, 0us)
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

    """
    """

    print(d3.nextMonth)
    d3 = datetime(2008, 1, 15)
    print(d3.prevMonth)
    print(d3 - d1)
    d3 = datetime(d1.year, d1.month, 1)
    print(d3 + Duration(days=d3.monthDays - 1))
    print(d1.monthStart, d1.monthEnd)
    print(d1 - Duration(days=1))
    print('First week of this month', datetime(date='2007-12-10').monthStart.week)
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

    def __init__(self, year=None, month=None, day=None, hour=0, minute=0, second=0, microSecond=0, tz=None,
        dt=None, date=None, time=None, week=None, trimvalues=True, mtime=None):

        if dt is not None: # If datetime object, just store it.
            # Assume that dt is of type date string. Direct init from existing datetime
            self.datetime = dt
        else:
            if date == 'now':
                self.datetime = dating.datetime.now()
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
        "Dating(date='2018-11-23' time='00:00:00')"
        """
        return "%s(date='%s' time='%s')" % (self.__class__.__name__, self.date, self.time)

    __repr__ = __str__

    def __nonzero__(self):
        """Always answer True indicating that a dating instance can never be zero.

        """
        return True

    def __lt__(self, dating):
        """Answers True if self is in the past of date dt as in self < dt.
        Note that in evaluating the condition the difference in time is taken into account as well.
        Use self.dateNumber < dt.dateNumber to test on date comparison only instead of dy < self.</br>

        >>> dating1 = Dating(date='2019-11-23')
        >>> dating2 = Dating(date='2018-11-23') # Same date, later in time
        >>> dating2 < dating1
        True
        """
        if isinstance(dating, Dating):
            return self.datetime < dating.datetime
        return False

    def __le__(self, dating):
        """Answers True if self is in the past of or equal to date dt as in self <= dt.
        Note that in evaluating the condition the difference in time is taken into account as well.
        Use self.dateNumber < dt.dateNumber to test on date comparison only instead of dy <= self.</br>

        >>> dt1 = Dating(date='2018-11-25')
        >>> dt2 = Dating(date='2018-11-23')
        >>> dt2 <= dt1
        True
        """
        if isinstance(dating, Dating):
            return self.datetime <= dating.datetime
        return False

    def __gt__(self, dating):
        """Answers True if self is in the future of or equal to date dt as in self > dt.
        Note that in evaluating the condition the difference in time is taken into account as well.
        Use self.dateNumber < dt.dateNumber to test on date comparison only instead of dy <= self.</br>

        >>> dt1 = Dating(date='2019-11-25')
        >>> dt2 = Dating(date='2018-11-23')
        >>> dt2 > dt1
        False
        """
        if isinstance(dating, Dating):
            return self.datetime > dating.datetime
        return False

    def __ge__(self, dating):
        """Answers True if self is in the future of or equal to date dt as in self >= dt.
        Note that in evaluating the condition the difference in time is taken into account as well.
        Use self.dateNumber < dt.dateNumber to test on date comparison only instead of dy <= self.</br>

        >>> dt1 = Dating(date='2019-11-25')
        >>> dt2 = Dating(date='2018-11-23')
        >>> dt2 >= dt1
        False
        """
        if isinstance(dating, Dating):
            return self.datetime >= dating.datetime
        return False

    def __ne__(self, dating):
        """Answers True if self is in the past of or equal to date dt as in self != dt.
        Note that in evaluating the condition the difference in time is taken into account as well.
        Use self.dateNumber < dt.dateNumber to test on date comparison only instead of dy <= self.</br>

        >>> dating1 = Dating(date='2019-11-25')
        >>> dating2 = Dating(date='2018-11-23')
        >>> dating2 != dating1
        True
        """
        if isinstance(dating, Dating):
            return self.datetime != dating.datetime
        return False

    def __eq__(self, dt):
        """Answers True if self is equal to date dt as in self == dt.
        Note that in evaluating the condition the difference in time is taken into account as well.
        Use self.dateNumber < dt.dateNumber to test on date comparison only instead of dy < self.

        >>> dt1 = Dating(date='2019-11-25')
        >>> dt2 = Dating(date='2018-11-23')
        >>> dt2 == dt1
        False
        >>> dt3 = Dating(date='2018-11-23')
        >>> dt2 == dt3
        True
        """
        if isinstance(dt, Dating):
            return self.datetime == dt.datetime
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
    
        """
        if isinstance(duration, (int, float)):
            duration = Duration(days=duration)
        assert isinstance(duration, Duration)
        return Duration.__add__(duration,self)

    def __sub__(self, durationOrDate):
        """
        Date - Duration = Date
        Date - Date = Duration
        Date - 3 = Date

        """
        if isinstance(durationOrDate, (int, float)):
            return Duration(days=durationOrDate)
        if isinstance(durationOrDate, Duration):
            # Date - Duration = Date
            return Duration.__sub__(durationOrDate,self)
        if isinstance(durationOrDate, Dating):
            # Date - Date = Duration
            return Duration(td=self.datetime - durationOrDate.datetime)
        raise ValueError('Cannot subtract %s - %s' % (self, durationOrDate))

    def _get_year(self):
        return self.datetime.year
    year = property(_get_year)

    @classmethod
    def timeStampRandomLong(cls):
        """

        The uniqueNumber property answers a unique number of format '20090621200511993066',
        derived from date, time and a six digit random number. This can be used e.g. in a URL as parameters to make sure that browser
        will not cache the content of the page. The number is also used to create a unique file name for background shell scripts.

        """
        return cls.timeStampLong() + ('%06d' % randint(0, 999999))

    @classmethod
    def timeStampLong(cls):
        import time
        return '%012d' % int(time.time()*100)

    def getTimeStamp(self, usetz=False):
        """
        The dt.getTypeStamp answers a formatted string 2010-10-05 16:47:29+04 of the date. This
        is exactly what SQL needs as timestamp with time zone definition.
        <note>use of tz does not yet work, and is ignored</note>

        """
        if self.tz is None or not usetz:
            tz = ""
        elif self.tz < 0:
            tz = "-%02d" % -self.tz
        else:
            tz = "+%02d" % self.tz
        return  "%s %s%s" % (self.date, self.time, tz)

    def _get_date(self):
        """
        The dt.date property answers a formatted string 2008-10-23 of the date.
        This is exactly what SQL needs as date-string definition.

        """
        return '%04d-%02d-%02d' % (self.year, self.month, self.day)
    date = property(_get_date)

    def _get_year(self):
        return self.datetime.year
    year = property(_get_year)

    def _get_month(self):
        return self.datetime.month
    month = property(_get_month)
    
    def _get_day(self):
        return self.datetime.day
    day = property(_get_day)
    
    def _get_hour(self):
        return self.datetime.hour
    hour = property(_get_hour)
    
    def _get_minute(self):
        return self.datetime.minute
    minute = property(_get_minute)
    
    def _get_second(self):
        return self.datetime.second
    second = property(_get_second)
    
    def _get_euroDate(self):
        """The dt.euroDate property answers a formatted string 23-10-2008 of the date.

        """
        return '%02d-%02d-%02d' % (self.day, self.month, self.year)
    euroDate = property(_get_euroDate)

    def _get_studyYear(self):
        """The dt.studyYear property answers a string 0708 with leading zero for the study year
        from 2007-08-01 until 2008-07-31

        """
        studyYear = (self.year - 2000) * 100 + self.year - 2000 + 1
        if self.month <= 8: # Switch study year on end of summer break
            studyYear -= 101
        return '%04d' % studyYear
    studyYear = property(_get_studyYear)

    def _get_dateNumber(self):
        """The dt.dateNumber property answers a long integer number 20080502 of the date. This can by
        used to compare dates on day only and not on time. Or it can be used as ordering key.

        """
        return self.year * 10000 + self.month * 100 + self.day
    dateNumber = property(_get_dateNumber)

    def _get_dateTuple(self):
        """The dt.dateTuple property answers a tuple (y,m,d) of the date.

        """
        return self.year, self.month, self.day
    dateTuple = property(_get_dateTuple)

    def _get_time(self):
        """The dt.dateNumber property answers a formatted '12:23:45' time string.

        """
        return '%02d:%02d:%02d' % (self.hour, self.minute, self.second)
    time = property(_get_time)

    def _getdatetime(self):
        """The dt.datetime property answers a formatted '2010-12-06 12:23:34' date/time
        string.

        """
        return '%s %s' % (self.date, self.time)
    dateTime = property(_getdatetime)

    def _get_timeTuple(self):
        """The dt.timeTuple property answers a tuple (h, m, s) of the time.

        """
        return self.hour, self.minute, self.second
    timeTuple = property(_get_timeTuple)

    def _get_timeZone(self):
        """The dt.timeZone property answers the timezone dt.tz.

        """
        return self.tz
    timeZone = property(_get_timeZone)

    def _get_week(self):
        """The dt.week property answers the weeknummer according to ISO 8601 where the first week of
        the year that contains a thursday.

        """
        return self.datetime.isocalendar()[1]
    week = property(_get_week)

    def _get_dayName(self):
        """The dt.dayName property answers a 3 letter abbreviation of current day name.

        """
        return self.dayNames[self.weekDay]
    dayName = property(_get_dayName)

    def _get_fullDayName(self):
        """The dt.fullDayName property answers the full name of the current day.

        """
        return self.fullDayNames[self.weekDay]
    fullDayName = property(_get_fullDayName)

    def _get_monthName(self):
        """The dt.monthName property answers a 3 letter abbreviation of current month name.

        """
        return self.monthNames[self.month]
    monthName = property(_get_monthName)

    def _get_fullMonthName(self):
        """The dt.fullMonthName property answers the full name of the current month.

        """
        return self.fullMonthNames[self.month]
    fullMonthName = property(_get_fullMonthName)

    def _get_monthStart(self):
        """The dt.monthStart property answers the first day of the current month.

        """
        return self + (1 - self.day) # Keep integer calculation combined by brackets
    monthStart = property(_get_monthStart)

    def _get_monthEnd(self):
        """The dt.monthEnd property answers the last day of the current month.

        """
        return self - self.day + self.monthDays
    monthEnd = property(_get_monthEnd)

    def _get_weekStart(self):
        """The dt.weekStart property answers the “Monday” date of the current week.

        """
        return self - self.weekDay
    weekStart = property(_get_weekStart)

    def _get_weekEnd(self):
        """Keep integer calculation combined by brackets

        """
        return self + (7 - self.weekDay)
    weekEnd = property(_get_weekEnd)

    def _get_yearStart(self):
        """The dt.yearStart property answers the first day of the current year.

        """
        return Dating(self.year, 1, 1)
    yearStart = property(_get_yearStart)

    def _get_yearEnd(self):
        """The dt.yearEnd property answers the last day of the current year.

        """
        return Dating(self.year, 12, 31)
    yearEnd = property(_get_yearEnd)

    def _get_workDay(self):
        """The dt.workDay property answers True if this day is one of Monday till Friday.

        """
        return 0 <= self.weekDay <= 4
    workDay = property(_get_workDay)

    def _get_weekDay(self):
        """Answer the number of day in the week."""
        return self.datetime.weekday()
    weekDay = property(_get_weekDay)

    def _get_nextWorkDay(self):
        """The dt.nextWorkDay property answers the first next date (including itself) that is a
        workday

        """
        if self.workDay:
            return self
        return self + (7 - self.weekDay) # Keep integer calculation combined by brackets
    nextWorkDay = property(_get_nextWorkDay)

    def _get_leapYear(self):
        """The dt.leapYear property answers a boolean if the dt is a leap year.

        """
        return leapYear(self.year)
    leapYear = property(_get_leapYear)

    def _get_yearDays(self):
        """The dt.yearDays property answers the number of days in the current year.

        """
        if leapYear(self.year):
            return 366
        return 365
    yearDays = property(_get_yearDays)
        
    def _get_monthDays(self):
        """The dt.monthDays property answers the number of days in the current month.

        """
        return monthDays(self.year, self.month)
    monthDays = property(_get_monthDays)
    
    def _get_nextMonth(self):
        """The nextMonth property answers the first day of the month after the current month. Due to
        length differences between the months, it is not consistent to answer the current day number in the next month,
        so it is set to 1.

        """
        return self + (self.monthDays - self.day + 1)
    nextMonth = property(_get_nextMonth)
    
    def _get_prevMonth(self):
        """The prevMonth property answers the first day of the month previous to the current month.
        Due to length differences between the months, it is not consistent to  answer the current day number in the
        previous month

        """
        return (self.monthStart - 1).monthStart
    prevMonth = property(_get_prevMonth)
    
    def _get_calendarMonth(self):
        """The calendarMonth property answers a list of lists containing the weeks with dates of the
        current month. Note that the first and lost week are filled with the days of end of the previous month and the
        start of the next month.

            [
                [p01, p02, p03, d01, d02, d03, d04],
                [d05, d06, d07, d08, d09, d10, d11],
                [d12, d13, d14, d15, d16, d17, d18],
                [d19, d20, d21, d22, d23, d24, d25],
                [d26, d27, d28, d29, d30, n01, n02]
            ]

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
        """The calendarYear property answers a list of lists of lists containing all
        calendarMonths of the year.

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
