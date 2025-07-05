from models.date.date_cycle import DateCycle
from datetime import datetime


def test_cycle_date_weekday_sunday():
    # Teste de criação de um objeto DateCycle
    datetime_obj = datetime(2025, 10, 6, 0, 0)  # Domingo
    dateCycle = DateCycle(datetime_obj)
    assert dateCycle.dayofWeek == 0  # Domingo


def test_cycle_date_weekday_monday():
    # Teste de criação de um objeto DateCycle
    datetime_obj = datetime(2025, 10, 7, 0, 0)  # Domingo
    dateCycle = DateCycle(datetime_obj)
    assert dateCycle.dayofWeek == 1  # Segunda-feira


def test_cycle_date_weekday_tuesday():
    # Teste de criação de um objeto DateCycle
    datetime_obj = datetime(2025, 10, 8, 0, 0)  # Terça-feira
    dateCycle = DateCycle(datetime_obj)
    assert dateCycle.dayofWeek == 2  # Terça-feira


def test_cycle_date_weekday_wednesday():
    # Teste de criação de um objeto DateCycle
    datetime_obj = datetime(2025, 10, 9, 0, 0)  # Quarta-feira
    dateCycle = DateCycle(datetime_obj)
    assert dateCycle.dayofWeek == 3  # Quarta-feira


def test_cycle_date_weekday_thursday():
    # Teste de criação de um objeto DateCycle
    datetime_obj = datetime(2025, 10, 10, 0, 0)  # Quinta-feira
    dateCycle = DateCycle(datetime_obj)
    assert dateCycle.dayofWeek == 4  # Quinta-feira


def test_cycle_date_weekday_friday():
    # Teste de criação de um objeto DateCycle
    datetime_obj = datetime(2025, 10, 11, 0, 0)  # Sexta-feira
    dateCycle = DateCycle(datetime_obj)
    assert dateCycle.dayofWeek == 5  # Sexta-feira


def test_cycle_date_weekday_saturday():
    # Teste de criação de um objeto DateCycle
    datetime_obj = datetime(2025, 10, 12, 0, 0)  # Sábado
    dateCycle = DateCycle(datetime_obj)
    assert dateCycle.dayofWeek == 6  # Sábado

