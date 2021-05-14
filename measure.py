"""measure method."""
import time
import datetime
from functools import wraps

def write_velocity(file_dir, filename, write_str):
    file = open(f"{file_dir}/{filename}", 'a')
    file.write(write_str)
    file.close()

def velocity_measurement(func):
    """velocity_measurement Decorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        dt_now = datetime.datetime.now()
        d_today = datetime.date.today()
        strat_time = time.time()
        result = func(*args,**kwargs)
        end_time = time.time()
        run_time =  end_time - strat_time
        write_velocity("./storage/measured", f"measurement_log_{d_today}.txt", f"[{dt_now}] {func.__name__}:{run_time}[s]\n")
        return result
    return wrapper
