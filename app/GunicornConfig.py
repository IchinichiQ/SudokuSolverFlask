from pathlib import Path

log_folder = '/var/log/gunicorn'
access_log_file = log_folder + '/access.log'
error_log_file = log_folder + '/error.log'

Path(log_folder).mkdir(exist_ok=True)
Path(access_log_file).touch()
Path(error_log_file).touch()

bind = '0.0.0.0:8000'
max_requests = 1000
worker_class = 'gevent'
workers = 4
accesslog = access_log_file
errorlog = error_log_file
