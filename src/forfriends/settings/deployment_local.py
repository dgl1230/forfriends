
import os


EMAIL_USE_TLS = False
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_PORT = 1025
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = "testing@testing.com"




BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


SECRET_KEY = os.environ["FORFRIENDS_KEY"]


DEBUG = True


TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

 
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'registration',
    'south',
    'profiles',
    'interests',
    'directmessages',
    'matches',
    'questions',
    'visitors',
    'social.apps.django_app.default',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'static/templates'),
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
   'django.core.context_processors.debug',
   'django.core.context_processors.i18n',
   'django.core.context_processors.media',
   'django.core.context_processors.static',
   'django.core.context_processors.tz',
   'django.contrib.messages.context_processors.messages',
   'social.apps.django_app.context_processors.backends',
   'social.apps.django_app.context_processors.login_redirect',
)

AUTHENTICATION_BACKENDS = (
   'social.backends.facebook.FacebookOAuth2',
   'social.backends.twitter.TwitterOAuth',
   'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'forfriends.urls'

WSGI_APPLICATION = 'forfriends.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':  os.environ["POSTGRES_DB"],
        'USER': os.environ["POSTGRES_USER"],
        'PASSWORD': os.environ["POSTGRES_USER_PASSWORD"],
        'HOST': 'localhost',
        'PORT': '',
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'static', 'media')

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'static', 'static-only')

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static/static'),
    
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


AUTH_PROFILE_MODULE = "userprofile.UserProfile"

ACCOUNT_ACTIVATION_DAYS = 7

LOGIN_REDIRECT_URL = '/'

SITE_ID = 1

#PYTHONIOENCODING=utf8

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers, this needs to be more secure soon 
ALLOWED_HOSTS = ['*']







    

