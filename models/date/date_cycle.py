from datetime import datetime
from util.date_util import DateUtil


class DateCycle:
    """
    Classe para manipulação de ciclos de data.

    """
    month: int
    dayofWeek: int  # 0=Monday, 6=Sunday
    periodOfTheDay: int

    def __init__(self, date: datetime):
        if date is None:
            raise ValueError("A data não pode ser None")
        if not isinstance(date, datetime):
            raise TypeError(
                f"Esperado um objeto datetime, mas recebeu: {type(date)}")
        self.month = date.month
        self.dayofWeek = date.weekday()
        self.periodOfTheDay = DateUtil.process_period_of_day(date.hour)
