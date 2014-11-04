from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView
from sitemaps import FrenvuSitemap

from django.contrib import admin


from registration.backends.simple.views import RegistrationView

class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return "/"

sitemaps = {
    'home':FrenvuSitemap
}


urlpatterns = patterns('',	

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT }),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT }),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'profiles.views.all', name='home'),
    #url(r'^my_circle/$', 'profiles.views.calculate_circle', name='calculate_circle'),
    url(r'^my_circle/$', 'profiles.views.generate_circle', name='generate_circle'),
    url(r'^new_user/$', 'profiles.views.register_new_user', name='register_user'),
    url(r'^login_user/$', 'profiles.views.login_user', name='login_user'),
    url(r'^logged_out/$', 'profiles.views.logout_user', name='logout_user'),
    url(r'^delete_account/$', 'profiles.views.delete_account', name='delete_account'),
    url(r'^members/(?P<username>\w+)/$', 'profiles.views.single_user', name='profile'),
    url(r'^members/(?P<username>\w+)/interests/$', 'interests.views.single_user_interests', name='view_interests'),
    url(r'^members/(?P<username>\w+)/pictures/$', 'profiles.views.single_user_pictures', name='view_pictures'),
    url(r'^members/(?P<single_user>\w+)/message$', 'directmessages.views.su_compose', name='su_compose'),
    url(r'^members/(?P<username>\w+)/add/$', 'profiles.views.add_friend', name='add_friend'),
    url(r'^members/(?P<username>\w+)/(?P<page>[\w]+)/$', 'profiles.views.add_friend_discovery', name='add_friend_discovery'),
    url(r'^edit/$', 'profiles.views.edit_profile', name='edit_profile'),
    (r'^edit/jobs$', 'profiles.views.edit_jobs'),
    (r'^edit/addresses/$', 'profiles.views.edit_address'),
    (r'^edit/pictures/$', 'profiles.views.edit_pictures'),
    url(r'^edit/pictures/delete/(?P<pic_id>[\d]+)/$', 'profiles.views.delete_picture', name='delete_picture'),
    (r'^edit/info/$', 'profiles.views.edit_info'),
    url(r'^interests/all$', 'interests.views.all_interests', name='interests'),
    #url(r'^interests/new_user$', 'interests.views.new_user_interests', name='new_user_interests'),
    url(r'^interests/create/$', 'interests.views.create_interest', name='create'),
    url(r'^interests/experimental/$', 'interests.views.all_interests_experimental', name='interests_all_experimental'),
    url(r'^interests/edit/$', 'interests.views.edit_interests', name='edit_interests'),
    url(r'^pictures/$', 'profiles.views.all_pictures', name='pictures'),
    url(r'^terms_and_agreement/$', 'profiles.views.terms_and_agreement', name='terms_and_agreement'),
    url(r'^messages/', include('directmessages.urls')),
    url(r'^search/', 'profiles.views.search', name="search"),
    url(r'^search_interests/', 'interests.views.search_interests', name="search_interests"),
    url(r'^questions/$', 'questions.views.all_questions', name='questions'),
    #url(r'^questions/new_user$', 'questions.views.new_user_questions', name='new_user_questions'),
    url(r'^questions/edit/$', 'questions.views.edit_questions', name='edit_questions'),
    url(r'^contact_us$', 'profiles.views.contact_us', name='contact_us'),
    #(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^about_us/$', TemplateView.as_view(template_name='about_us.html'), name="about_us"),
    url(r'^user/password/reset/$', 
        'django.contrib.auth.views.password_reset', {'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset"),
    (r'^user/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect' : '/user/password/done/'}),
    (r'^user/password/done/$', 'django.contrib.auth.views.password_reset_complete'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^new_picture/$', 'profiles.views.new_picture', name='new_picture'),
    url(r'^make_profile_pic/(?P<pic_id>[\d]+)/$', 'profiles.views.make_profile_pic', name='make_profile_pic'),
    url(r'^ice_breaker/$', 'profiles.views.ice_breaker', name='ice_breaker'),
    #url(r'^handle/$', 'profiles.views.handle_new_user', name='handle_new_user'),
    url(r'^new_user_info/$', 'profiles.views.new_user_info', name='new_user_info'),
    #url(r'^new_user_registration/$', 'profiles.views.new_user_registration2', name='new_user_registration2'),
    url(r'^discover/$', 'profiles.views.discover', name='discover'),
    url(r'^friends/$', 'profiles.views.friends', name='friends'),


    url(r'^press/$', 'profiles.views.press', name='press'),

    url(r'^sitemap\.xml', 'django.contrib.sitemaps.views.sitemap', {'sitemaps':sitemaps}),

)
