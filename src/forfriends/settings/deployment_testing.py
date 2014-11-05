
import os
from django.core.urlresolvers import reverse_lazy


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]




BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


SECRET_KEY = os.environ["FORFRIENDS_KEY"]


DEBUG = True


DEBUG_TOOLBAR_PATCH_SETTINGS = False

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'profiles.views.custom_show_toolbar',
}



INTERNAL_IPS = ('67.169.73.204',)

SHOW_TOOLBAR_CALLBACK = True

TEMPLATE_DEBUG = True


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
    'storages',
    'social.apps.django_app.default',
    'debug_toolbar',
    
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'static/templates'),
)


MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GooglePlusAuth',
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

# may want it to be AUTH_PROFILE_MODULE = "profiles.blah"
AUTH_PROFILE_MODULE = "profiles.Info"

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

    
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

DEFAULT_FILE_STORAGE = 'forfriends.s3utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'forfriends.s3utils.StaticRootS3BotoStorage'

AWS_PRELOAD_METADATA = True 

S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL + 'static/'
MEDIA_URL = S3_URL + 'media/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

DMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

#Facebook social authentication info for Frenvu-Staging app 
SOCIAL_AUTH_FACEBOOK_KEY = '705757932842907' 
SOCIAL_AUTH_FACEBOOK_SECRET = '180f498d374ab9d421534418751d0564' 

SOCIAL_AUTH_FACEBOOK_SCOPE = [
    'email',
]

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'forfriends.pipeline.get_username',
    'forfriends.pipeline.associate_user_by_email',
    #'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    #'forfriends.pipeline.save_profile_picture',
    #'forfriends.pipeline.user_details',
)

#Google soical authentication info 
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "406119441085-n7d7srjnlsj0eqg8d0jomai2o56o8f5e.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "rr6yAYsfLim6aikBZCArDW9M"

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [ 
    'email',
]

#Caching with heroku 
def get_cache():
    try:
        os.environ['MEMCACHE_SERVERS'] = os.environ['MEMCACHIER_SERVERS'].replace(',', ';')
        os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHIER_USERNAME']
        os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHIER_PASSWORD']
        return {
          'default': {
            'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
            'TIMEOUT': 500,
            'BINARY': True,
            'OPTIONS': { 'tcp_nodelay': True }
          }
        }
    except:
        return {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
            }
        }

CACHES = get_cache()



DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]


STATICFILES_DIRS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static/static')





    

