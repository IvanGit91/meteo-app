from datetime import datetime


def is_valid_date(date_string, date_format="%Y-%m-%d") -> bool:
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False

def date_conversion(date_string, date_format="%Y-%m-%d"):
    try:
        date = datetime.strptime(date_string, date_format)
        return date
    except ValueError:
        return None