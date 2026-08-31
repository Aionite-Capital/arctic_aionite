import os
import sys
from datetime import datetime as dt

import tzlocal
from mock import patch
from pytest import raises

from arctic.date import mktz, TimezoneError

lz = tzlocal.get_localzone()
DEFAULT_TIME_ZONE_NAME = getattr(lz, 'key', getattr(lz, 'zone', str(lz)))


def test_mktz():
    tz = mktz("Europe/London")
    d = dt(2012, 2, 2, tzinfo=tz)
    assert d.tzname() in ('GMT', 'UTC')
    d = dt(2012, 7, 2, tzinfo=tz)
    assert d.tzname() in ('BST', 'British Summer Time')

    tz = mktz('UTC')
    d = dt(2012, 2, 2, tzinfo=tz)
    assert d.tzname() in ('UTC', 'Coordinated Universal Time')
    d = dt(2012, 7, 2, tzinfo=tz)
    assert d.tzname() in ('UTC', 'Coordinated Universal Time')


def test_mktz_noarg():
    tz = mktz()
    assert tz is not None
    assert getattr(tz, 'zone', None) == DEFAULT_TIME_ZONE_NAME or DEFAULT_TIME_ZONE_NAME in str(tz)


def test_mktz_zone():
    tz = mktz('UTC')
    assert tz.zone == "UTC"
    if os.path.exists('/usr/share/zoneinfo/UTC'):
        tz = mktz('/usr/share/zoneinfo/UTC')
        assert tz.zone == "UTC"


def test_mktz_fails_if_invalid_timezone():
    with patch('os.path.exists') as file_exists:
        file_exists.return_value = False
        with raises(TimezoneError):
            mktz('junk')
