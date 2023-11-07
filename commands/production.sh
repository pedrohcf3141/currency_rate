#! usr/bin/bash

/opt/currency_rate_test/src/manage.py makemigrations

/opt/currency_rate_test/src/manage.py migrate

gunicorn --bind :8000 --workers=2 currency_rate_test.wsgi --logger-class='currency_rate_test.settings.CustomGunicornLogger' --access-logfile=- --access-logformat='%(h)s %(t)s "%(r)s" %(s)s %(B)s %(L)s "%(a)s"'