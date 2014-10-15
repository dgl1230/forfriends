
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('directmessages.views',
    url(r'^compose/$', 'compose', name='compose'),
    #url(r'^(?P<single_user>\w+)/$', 'su_compose', name='su_compose'),
    url(r'^inbox/$', 'inbox', name='inbox'),
    url(r'^sent/$', 'sent', name='sent'),

    url(r'^view/(?P<dm_id>[\d]+)/$', 'view_direct_message', name='view_direct_message'),
    url(r'^view_sent/(?P<dm_id>[\d]+)/$', 'view_sent_message', name='view_sent_message'),
    url(r'^view/(?P<dm_id>[\d]+)/reply/$', 'reply', name='reply'),
    #url(r'^inbox/delete/(?P<dm_id>[\d]+)/$', 'delete_messages', name='delete_messages'),
    url(r'^inbox/delete/$', 'delete_messages', name='delete_messages'),
    url(r'^inbox/delete_individual/(?P<dm_id>[\d]+)$', 'delete_individual_message', name='delete_individual_message'),
    url(r'^sent/delete_sent/$', 'delete_sent_messages', name='delete_sent_messages'),
    url(r'^sent/delete_individual_sent/(?P<dm_id>[\d]+)$', 'delete_individual_sent_message', name='delete_individual_sent_message'),


)