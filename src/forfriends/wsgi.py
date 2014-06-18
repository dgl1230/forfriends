"""
WSGI config for forfriends project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
reload(sys)     
sys.setdefaultencoding("utf-8")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forfriends.settings")

from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()

from dj_static import Cling

application = Cling(get_wsgi_application())