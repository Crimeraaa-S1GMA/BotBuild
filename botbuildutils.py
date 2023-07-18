from datetime import datetime, timedelta

def convert_to_unix_time(time_str):
    unit = time_str[-1].lower()  # Get the last character representing the unit
    value = int(time_str[:-1])  # Get the numerical value without the unit
    
    if unit == 's':
        delta = timedelta(seconds=value)
    elif unit == 'm':
        delta = timedelta(minutes=value)
    elif unit == 'h':
        delta = timedelta(hours=value)
    elif unit == 'd':
        delta = timedelta(days=value)
    elif unit == 'w':
        delta = timedelta(weeks=value)
    else:
        raise ValueError("Invalid unit specified. Use s, m, h, d, or w.")
    
    unix_time = int((datetime.now() + delta).timestamp())
    return unix_time
