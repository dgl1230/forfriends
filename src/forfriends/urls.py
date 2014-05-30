from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from registration.backends.simple.views import RegistrationView

class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return "/"


urlpatterns = patterns('',	

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT }),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT }),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'profiles.views.all', name='home'),
    url(r'^members/(?P<username>\w+)/$', 'profiles.views.single_user', name='profile'),
    url(r'^members/(?P<username>\w+)/interests/$', 'interests.views.single_user_interests', name='view_interests'),
    url(r'^members/(?P<username>\w+)/questions/$', 'questions.views.single_user_questions', name='view_questions'),
    url(r'^members/(?P<username>\w+)/pictures/$', 'profiles.views.single_user_pictures', name='view_pictures'),
    url(r'^members/(?P<username>\w+)/add/$', 'profiles.views.add_friend', name='add_friend'),
    url(r'^sort/$', 'profiles.views.find_friends', name='find_friends'),
    url(r'^edit/$', 'profiles.views.edit_profile', name='edit_profile'),
    (r'^edit/jobs$', 'profiles.views.edit_jobs'),
    (r'^edit/addresses/$', 'profiles.views.edit_address'),
    (r'^edit/pictures/$', 'profiles.views.edit_pictures'),
    (r'^edit/info/$', 'profiles.views.edit_info'),
    url(r'^interests/$', 'interests.views.all_interests', name='interests'),
    url(r'^interests/create/$', 'interests.views.create_interest', name='create'),
    url(r'^interests/edit/$', 'interests.views.edit_interests', name='edit_interests'),
    url(r'^pictures/$', 'profiles.views.all_pictures', name='pictures'),
    url(r'^visitors/$', 'profiles.views.all_visitors', name='all_visitors'),
    url(r'^messages/', include('directmessages.urls')),
    url(r'^search/', 'profiles.views.search', name="search"),
    url(r'^questions/$', 'questions.views.all_questions', name='questions'),
    url(r'^questions/create/$', 'questions.views.create_question', name='create_question'),
    url(r'^questions/edit/$', 'questions.views.edit_questions', name='edit_questions'),
    (r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^about_us/$', TemplateView.as_view(template_name='about_us.html'), name="about_us"),
)
