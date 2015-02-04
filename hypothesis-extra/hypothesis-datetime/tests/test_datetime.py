from hypothesis import falsify, assume
from datetime import datetime
from hypothesis.internal.compat import hrange
import hypothesis.settings as hs

hs.default.max_examples = 1000


def test_can_find_after_the_year_2000():
    falsify(lambda x: x.year > 2000, datetime)


def test_can_find_before_the_year_2000():
    falsify(lambda x: x.year < 2000, datetime)


def test_can_find_each_month():
    for i in hrange(1, 12):
        falsify(lambda x: x.month != i, datetime)


def test_can_find_midnight():
    falsify(
        lambda x: not (x.hour == 0 and x.minute == 0 and x.second == 0),
        datetime
    )


def test_can_find_non_midnight():
    falsify(lambda x: x.hour == 0, datetime)


def test_can_find_off_the_minute():
    falsify(lambda x: x.second == 0, datetime)


def test_can_find_on_the_minute():
    falsify(lambda x: x.second != 0, datetime)


def test_can_find_february_29():
    falsify(lambda d: assume(d.month == 2) and (d.day != 29), datetime)


def test_can_find_christmas():
    falsify(lambda d: assume(d.month == 12) and d.day == 25, datetime)


def test_simplifies_towards_midnight():
    d = falsify(lambda x: False, datetime)[0]
    assert d.hour == 0
    assert d.minute == 0
    assert d.second == 0
    assert d.microsecond == 0


def test_simplifies_towards_2000():
    d = falsify(lambda x: x.year <= 2000, datetime)[0]
    assert d.year == 2001
    d = falsify(lambda x: x.year >= 2000, datetime)[0]
    assert d.year == 1999