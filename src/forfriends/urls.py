from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',	

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT }),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT }),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'profiles.views.all', name='home'),
    url(r'^members/(?P<username>\w+)/$', 'profiles.views.single_user', name='profile'),
    url(r'^sort/$', 'profiles.views.find_friends', name='find_friends'),
    url(r'^edit/$', 'profiles.views.edit_profile', name='edit_profile'),
    (r'^edit/jobs$', 'profiles.views.edit_jobs'),
    (r'^edit/addresses/$', 'profiles.views.edit_address'),
    (r'^edit/info/$', 'profiles.views.edit_info'),
    url(r'^interests/$', 'interests.views.all_interests', name='interests'),
    url(r'^interests/create/$', 'interests.views.create_interest', name='create'),
    url(r'^interests/edit/$', 'interests.views.edit_interests', name='edit_interests'),
    url(r'^pictures/$', 'profiles.views.all_pictures', name='pictures'),
    url(r'^messages/', include('directmessages.urls')),
    url(r'^search/', 'profiles.views.search', name="search"),
    url(r'^questions/$', 'questions.views.all_questions', name='questions'),
    url(r'^questions/create/$', 'questions.views.create_question', name='create_question'),
    url(r'^questions/edit/$', 'questions.views.edit_questions', name='edit_questions'),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^about_us/$', TemplateView.as_view(template_name='about_us.html'), name="about_us"),
)
