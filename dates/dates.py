#!env python
#
# This file is part of dates, a program that prints dates.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2012 Christophe-Marie Duquesne <chm.duquesne@gmail.com>
#
"""
NAME
    dates - prints a list of dates

SYNOPSIS
    dates [OPTIONS]

OPTIONS
    --help:
        Print this help

    --freq <frequency>:
        Choose frequency (values admitted: YEARLY, MONTHLY, WEEKLY,
        DAILY). Defaults to DAILY.

    --from, --dtstart:
        Recurrence start

    --to, --until:
        limit of the recurrence

    --step, --interval:
        The interval between each freq iteration. For example, when using
        YEARLY, an interval of 2 means once every two years.

    --wkst:
        The week start day. Must be one of the MO, TU, WE constants, or an
        integer, specifying the first day of the week.

    --count:
        How many occurrences will be generated.

    --byweekday:
        If given, it must be either an integer (0 == MO), a sequence of
        integers, one of the weekday constants (MO, TU, etc), or a
        sequence of these constants. When given, these variables will
        define the weekdays where the recurrence will be applied.

    --bysetpos:
        If given, it must be either an integer, or a sequence of integers,
        positive or negative. Each given integer will specify an
        occurrence number, corresponding to the nth occurrence of the rule
        inside the frequency period. For example, a bysetpos of -1 if
        combined with a MONTHLY frequency, and a byweekday of (MO, TU, WE,
        TH, FR), will result in the last work day of every month. )

    --bymonth:
        If given, it must be either an integer, or a sequence of integers,
        meaning the months to apply the recurrence to.

    --bymonthday:
        If given, it must be either an integer, or a sequence of integers,
        meaning the month days to apply the recurrence to.

    --byyearday:
        If given, it must be either an integer, or a sequence of integers,
        meaning the year days to apply the recurrence to.

    --byweekno:
        If given, it must be either an integer, or a sequence of integers,
        meaning the week numbers to apply the recurrence to. Week numbers
        have the meaning described in ISO8601, that is, the first week of
        the year is that containing at least four days of the new year.

    --byweekday:
        If given, it must be either an integer (0 == MO) or a sequence of
        integers. When given, these variables will define the weekdays
        where the recurrence will be applied.

    --byeaster
        If given, it must be either an integer, or a sequence of integers,
        positive or negative. Each integer will define an offset from the
        Easter Sunday. Passing the offset 0 to byeaster will yield the
        Easter Sunday itself.

EXAMPLES:
    Prints the Mondays and Tuesdays that occur every 5 days in 2010:
    dates --from 2010-01-01 --to 2011-01-01 --step 5 --byweekday '["MO","TU"]'

    Prints the last friday of each month of 2010:
    dates --freq MONTHLY --from 2010-01-01 --to 2011-01-01 --byweekday 'FR(-1)'
"""
import sys
import getopt
from dateutil.parser import *
from dateutil.rrule import *
from datetime import *
import calendar
try:
    import simplejson as json
except ImportError:
    import json

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h", [
                    "help",
                    "freq=",
                    "from=", "dtstart=",
                    "step=", "interval=",
                    "wkst=",
                    "count=",
                    "to=", "until=",
                    "byweekday=",
                    "bysetpos=",
                    "bymonth=",
                    "bymonthday=",
                    "byyearday=",
                    "byweekno=",
                    "byweekday=",
                    "byeaster="
                    ])
    except getopt.GetoptError, err:
        print str(err)
        print __doc__
        sys.exit(2)

    freq = DAILY
    dtstart = None # from, dtstart
    interval = 1 # interval, step
    wkst = None # wkst
    count = None # count
    until = None # to, until
    bysetpos = None # bysetpos
    bymonth = None # bymonth
    bymonthday = None # bymonthday
    byyearday = None # byyearday
    byweekno = None # byweekno
    byweekday = None # byweekday
    byeaster = None # byeaster

    days_of_week = {"MO": MO, "TU": TU, "WE": WE, "TH": TH, "FR": FR,
            "SA": SA, "SU": SU}
    frequencies = {"YEARLY": YEARLY, "MONTHLY": MONTHLY, "WEEKLY": WEEKLY,
            "DAILY": DAILY}
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print __doc__
            sys.exit()
        elif opt == "--freq":
            freq = frequencies[arg]
        elif opt in ("--from", "--dtstart"):
            dtstart = parse(arg).date()
        elif opt in ("--step", "--interval"):
            interval = int(arg)
        elif opt == "--wkst":
            if arg in ("MO", "TU", "WE"):
                wkst = days_of_week[arg]
            else:
                wkst = int(arg)
        elif opt == "--count":
            count = int(arg)
        elif opt in ("--to", "--until"):
            until = parse(arg).date()
        elif opt == "--bysetpos":
            bysetpos = json.loads(arg)
        elif opt == "--bymonth":
            bymonth = json.loads(arg)
        elif opt == "--bymonthday":
            bymonthday = json.loads(arg)
        elif opt == "--byyearday":
            byyearday = json.loads(arg)
        elif opt == "--byweekno":
            byweekno = json.loads(arg)
        elif opt == "--byweekday":
            if arg in days_of_week.keys():
                byweekday = days_of_week[arg]
            elif arg in ("0", "1", "2", "3", "4", "5", "6"):
                byweekday = int(arg)
            elif arg[-1] == ")":
                try:
                    day = days_of_week[arg[:2]]
                    offset = int(arg.split("(")[1].strip(")"))
                    byweekday = day(offset)
                except:
                    print "Could not parse %s" % arg
                    raise
            else:
                byweekday = []
                for weekday in iter(json.loads(arg)):
                    if days_of_week.get(weekday):
                        byweekday.append(days_of_week.get(weekday))
                    else:
                        days_of_week.append(weekday)
        elif opt == "--byeaster":
            byeaster = json.loads(arg)
        else:
            raise getopt.GetoptError("Unrecognized option")

    #print freq
    #print dtstart
    #print interval
    #print wkst
    #print count
    #print until
    #print bysetpos
    #print bymonth
    #print bymonthday
    #print byyearday
    #print byweekno
    #print byweekday
    #print byeaster

    for d in rrule(freq, dtstart=dtstart, interval=interval, wkst=wkst,
            count=count, until=until, bysetpos=bysetpos, bymonth=bymonth,
            bymonthday=bymonthday, byyearday=byyearday, byweekno=byweekno,
            byweekday=byweekday, byeaster=byeaster):
        print d.date().isoformat()

if __name__ == "__main__":
    main()
