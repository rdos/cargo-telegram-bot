# -*- coding: utf-8 -*-
# Этот токен невалидный, можете даже не пробовать :)

# -*- coding: utf-8 -*-

from enum import Enum

token = '478909799:AAEuh8FPg_kEcbAJmB5O8En8Rmbzly2rT_I'

db_file = 'cargo.sqlite'


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    START_S = "START"  # Начало нового диалога
    ENTER_NAME_S = "ENTER_NAME"
    ENTER_AGE_S = "ENTER_AGE"
    SEND_PIC_S = "SEND_PIC"
