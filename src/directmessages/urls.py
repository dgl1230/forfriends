
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('directmessages.views',
    url(r'^compose/$', 'compose', name='compose'),
    url(r'^inbox/$', 'inbox', name='inbox'),
    url(r'^sent/$', 'sent', name='sent'),
    url(r'^view/(?P<dm_id>[\d]+)/$', 'view_direct_message', name='view_direct_message'),
    url(r'^view/(?P<dm_id>[\d]+)/reply/$', 'reply', name='reply'),

)