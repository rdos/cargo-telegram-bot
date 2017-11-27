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
    NEW_NOTICE_ADDRESS_S = "NEW_NOTICE_ADDRESS"
    NEW_NOTICE_MASS_S = "NEW_NOTICE_MASS"
    NEW_NOTICE_SIZE_S = "NEW_NOTICE_SIZE"
    NEW_NOTICE_NAME_S = "NEW_NOTICE_NAME"
