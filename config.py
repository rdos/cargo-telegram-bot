# -*- coding: utf-8 -*-
# Этот токен невалидный, можете даже не пробовать :)

# -*- coding: utf-8 -*-

from enum import Enum

token = '478909799:AAEuh8FPg_kEcbAJmB5O8En8Rmbzly2rT_I'

db_file = "database.vdb"


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_ENTER_NAME = "1"
    S_ENTER_AGE = "2"
    S_SEND_PIC = "3"
