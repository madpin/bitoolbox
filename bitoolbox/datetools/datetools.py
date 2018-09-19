# -*- coding: utf-8 -*-
"""Funcionalidades relacionadas com Omniture."""


def get_dates_list(date1, date2):
    from datetime import timedelta

    delta = max(date1, date2) - min(date1, date2)
    dates_list = []
    for i in range(delta.days + 1):
        dates_list.append(min(date1, date2) + timedelta(days=i))

    return dates_list


def get_yesterday():
    from datetime import date
    from datetime import timedelta
    return date.today() - timedelta(1)


def get_n_days_ago_list(n):
    from datetime import date
    from datetime import timedelta
    return get_dates_list(date.today() - timedelta(1), date.today() - timedelta(n))


def date_to_iso(date):
    iso = date.strftime('%Y-%m-%d')
    return iso


def diff_in_s(dt_ini, round_value=2):
    from datetime import datetime
    return str(
        round(
            (datetime.now() - dt_ini).total_seconds(),
            round_value
        )
    )
