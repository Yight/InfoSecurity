import os, sys
sys.path.append('/var/www/WebServer')
os.environ['DJANGO_SETTINGS_MODULE'] = 'webserver.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
