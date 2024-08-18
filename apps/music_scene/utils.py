from datetime import datetime


def _ds_full(date_str):
    """Convert a date string like '2024-03-14' to string like 'Thursday, March 14, 2024'"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%A, %B %d, %Y")


def _ds_short(date_str):
    """Convert a date string like '2024-03-14' to string like 'March 14'"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%B %d")


def _ts_full(time_str):
    """Convert a time string like '20:00' or '20:15'
    to a friendly local time like '8PM' or '8:15PM'."""
    time_obj = datetime.strptime(time_str, "%H:%M")

    if time_obj.minute != 0:
        # If minute is non-zero, include it in the format.
        return time_obj.strftime("%I:%M %p").lstrip("0")
    else:
        # If minute is zero, only include hour in the format.
        return time_obj.strftime("%I %p").lstrip("0")
