"""logger method."""

from logging.config import dictConfig
import datetime

def create_logfile():
    """create log file """
    dt_now = datetime.datetime.now()
    current_date = dt_now.strftime("%Y-%m-%d")
    logger_file_dir = '/storage/logs/face-recognition_{}.log'.format(current_date)

    dictConfig({
        'version': 1,
        'formatters': {
            'file': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'file',
            'filename': logger_file_dir,
            'backupCount': 3,
            'when': 'D',
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['file']
        }
    })
