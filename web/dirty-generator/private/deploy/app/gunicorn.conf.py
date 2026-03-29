# gunicorn.conf.py
import sys
import gunicorn
import gunicorn.http.wsgi

bind = "0.0.0.0:8080"
workers = 1
accesslog = "-"

py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
_server = f"gunicorn/{gunicorn.__version__} Python/{py_version} myqrcode/1.0.0"

gunicorn.http.wsgi.SERVER = _server