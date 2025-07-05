from util.date_util import DateUtil


def test_process_period_of_day_evening():
    assert DateUtil.process_period_of_day(0) == 1
    assert DateUtil.process_period_of_day(5) == 1


def test_process_period_of_day_morning():
    assert DateUtil.process_period_of_day(6) == 2
    assert DateUtil.process_period_of_day(11) == 2


def test_process_period_of_day_afternoon():
    assert DateUtil.process_period_of_day(12) == 3
    assert DateUtil.process_period_of_day(17) == 3


def test_process_period_of_day_night():
    assert DateUtil.process_period_of_day(18) == 4
    assert DateUtil.process_period_of_day(23) == 4


def test_wrong_hour():
    try:
        DateUtil.process_period_of_day(24)
    except ValueError as e:
        assert str(e) == "Hora inválida: 24. Deve estar entre 0 e 23."
    try:
        DateUtil.process_period_of_day(-1)
    except ValueError as e:
        assert str(e) == "Hora inválida: -1. Deve estar entre 0 e 23."
