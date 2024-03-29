# Django settings for beaver project.

# Used for building absolute paths
BEAVER_DIR = u'/Users/sebastian/git/beaver/beaver'

# Jeeves external URL
BEAVER_EXTERNAL_URL = u'http://localhost:8000'
BEAVER_EXTERNAL_CALENDAR_URL = u'%s/calendar/' % (BEAVER_EXTERNAL_URL)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Sebastian Dahlgren', 'sebastian.dahlgren@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '%s/db.sql' % BEAVER_DIR,       # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Stockholm'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '%s/media/' % BEAVER_DIR

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '%s/media/' % BEAVER_EXTERNAL_URL

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1-+0g1guyjc6wwk-atz_#(td@z^fds5h(eu_sflsamp;-s%*!*3p^9b%'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'beaver.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'beaver.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '%s/templates' % BEAVER_DIR,
)

AUTHENTICATION_BACKENDS = ( 'django.contrib.auth.backends.ModelBackend',
                            'core.backends.BeaverAuthenticationBackend',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'core',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
    },
    'loggers': {
        'core.views': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'core.models': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'core.management.commands.accounts': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

DATETIME_FORMAT     = "Y-m-d H:i:s"
DATE_FORMAT         = "Y-m-d"
TIME_FORMAT         = "H:i:s"
SHORT_DATE_FORMAT   = "%d/%m"

# Sunday = 0, Monday = 1
FIRST_DAY_OF_WEEK   = 1

# Keep inactive accounts for n days
BEAVER_INACTIVE_DAYS_LIMIT = 7

# Email settings
EMAIL_BACKEND           = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS           = True
EMAIL_HOST              = 'smtp.gmail.com'
EMAIL_HOST_USER         = 'sebastian.dahlgren@gmail.com'
EMAIL_HOST_PASSWORD     = 'fr4uSw1eH3'
EMAIL_PORT              = '587'
BEAVER_NO_REPLY_ADDRESS = 'noreply@beaver.com'
BEAVER_CONTACT_US_ADDRESS = 'sebastian.dahlgren@gmail.com'


# File upload size limit in bytes
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440

# File upload temp dir. Will default to /tmp on Linux
#FILE_UPLOAD_TEMP_DIR = None
