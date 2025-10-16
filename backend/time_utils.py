from datetime import datetime
def time_converter(time):
    if isinstance(time, str):
        print(123)
        if len(time) == 5:
            return datetime.strptime(time, '%H:%M').time()
        elif len(time) == 8: 
            return datetime.strptime(time, '%H:%M:%S').time()
    return time


def date_converter(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d').date()