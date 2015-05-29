#!/usr/bin/python
#-*-coding:utf-8-*-

import os

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'monitor',                      # Or path to database file if using sqlite3.
#        'USER': 'monitor',                      # Not used with sqlite3.
#        'PASSWORD': 'monitor',                  # Not used with sqlite3.
#        'HOST': '221.2.164.60',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }
   'default' : {
      'ENGINE' : 'django_mongodb_engine',
      'NAME' : 'InfoSecurity',
      #'HOST': '221.2.164.60',
      'HOST': '192.168.0.234',
   }
}

DATETIME_FORMAT = 'Y-m-d H:i:s'

IFEMSMODEL = False

# from django.core.mail import EmailMessage
# email = EmailMessage('Hello', 'World', to=['user@gmail.com'])
# email.send()


TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID=u'516627512de2bf192aaddfca'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
# ADMIN_MEDIA_PREFIX = '/static/admin/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

PROJECT_ROOT = "/var/www/WebServer/webserver"

GRAPPELLI_ADMIN_TITLE = ""
# Additional locations of static files
STATICFILES_DIRS = (
    'static',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'hawkeye.service2013@gmail.com'
EMAIL_HOST_PASSWORD = 'hawkeyelab'
# EMIAL_EMAIL_FROM = 'hawkeye_service@163.com'


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ia0d$jc01ndz!21&!w$erm=sbe&!q8ysu2!vfajt=w%b-dwps^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'webserver.urls'

TEMPLATE_PATH = 'templates' if DEBUG else os.path.join(PROJECT_ROOT,'templates')

TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)

INSTALLED_APPS = (
    'djangotoolbox',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'engine',
    'grappelli',
    'django.contrib.admin',
    'captcha',
    #'south',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}



import djcelery
djcelery.setup_loader()

CELERY_RESULT_BACKEND = "mongodb"

BROKER_URL = "mongodb://192.168.0.234:27017/InfoSecurity"

CELERY_MONGODB_BACKEND_SETTINGS = {
    "host":BROKER_URL,
    "taskmeta_collection":"taskmeta",
}

CELERY_IMPORTS = ("engine.tasks", )
