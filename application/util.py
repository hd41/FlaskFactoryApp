from datetime import datetime as dt
from .models import db, RawData


def validate_dates(date_a, date_b, date_c):

    date_announce, estimated_set, status_change = None, None, None
    try:
        date_announce = dt.strptime(date_a, "%d/%m/%Y").date()
    except Exception as ex:
        pass

    try:
        estimated_set = dt.strptime(date_b, "%d/%m/%Y").date()
    except Exception as ex:
        pass

    try:
        status_change = dt.strptime(date_c, "%d/%m/%Y").date()
    except Exception as ex:
        pass

    return date_announce, estimated_set, status_change


def validate_state_daily_date(date_a):
    state_daily_date = None
    try:
        state_daily_date = dt.strptime(date_a, "%d-%b-%y").date()     # 21-Mar-20
    except Exception as ex:
        pass
    return state_daily_date


def get_state_by_state_code(code):
    if code == 'dd':
        return 'Daman and Diu'
    elif code == 'ld':
        return 'Lakshadweep'
    elif code == 'ml':
        return 'Meghalaya'
    elif code == 'nl':
        return 'Nagaland'
    elif code == 'sk':
        return 'Sikkim'
    elif code == 'tt':
        return 'Total'
    else:
        raw_dta = RawData.query.filter_by(state_code=code).first()
        return raw_dta.detected_state