

class DateUtil:
    """
    Classe utilitária para manipulação de datas e horários.
    """

    @staticmethod
    def process_period_of_day(h: int) -> int:
        """
        Recebe um horário em formato de 24 horas (0-23)
        e retorna o período do dia:
        Arguments:
        h -- Hora no formato 0-23
        Returns:
        1 - madrugada (00:00-05:59)
        2 - manhã (06:00-11:59)
        3- tarde (12:00-17:59)
        4 - noite (18:00-23:59)
        """
        if h < 6:
            return 1
        elif h < 12:
            return 2
        elif h < 18:
            return 3
        elif h <= 23:
            return 4
        else:
            raise ValueError(f"Hora inválida: {h}. Deve estar entre 0 e 23.")
