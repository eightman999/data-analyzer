from datetime import datetime

import math


def copylight():
    today = datetime.today()
    res = "#©︎ " + f'{today:%Y}' + " EIGHTMAN\n"
    return res


def significant_figures(number, n):
    n = 10^n
    result = math.floor(number * n) / n
    return result