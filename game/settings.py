from default_settings import *

try:
    from local_settings import *
except ImportError:
    pass

DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
