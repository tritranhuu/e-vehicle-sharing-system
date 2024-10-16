from datetime import datetime


def get_duration(start_time, end_time):
    start_time_obj = datetime.fromisoformat(start_time)
    end_time_obj = datetime.fromisoformat(end_time)

    duration = end_time_obj - start_time_obj
    return duration.total_seconds()

def get_total_hours(start_time, end_time=None):
    time_obj = datetime.fromisoformat(start_time)
    if end_time is None:
        end_time_obj = datetime.now()
    else:
        end_time_obj = datetime.fromisoformat(end_time)
    duration = end_time_obj - time_obj

    seconds = duration.total_seconds()
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return f'{int(hours)}h{int(minutes)}m{int(seconds)}s', duration.total_seconds()

def beautify_time(time):
    time_obj = datetime.fromisoformat(time)
    return time_obj.strftime("%m/%d/%y, %Hh%Mm")
