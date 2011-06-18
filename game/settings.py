from default_settings import *

try:
    from local_settings import *
except ImportError:
    pass

DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

INSTALLED_APPS += (
    'sentry.client',
)

ADMINS = ()
MANAGERS = ADMINS

SENTRY_KEY = 'JXImOoyrVIaOEMxrWbUJ'
SENTRY_REMOTE_URL = 'https://sentrybrute.ep.io/store/'
