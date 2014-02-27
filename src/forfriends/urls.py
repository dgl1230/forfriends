from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from userprofile.views import signup

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'forfriends.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'userprofile.views.signup'),
    url(r'^profile_home$', 'userprofile.views.login_view'),
    #url(r'^test/$', 'userprofile.views.registration'),
    #url(r'submit', 'userprofile.views.registration'),
    
)
