import datetime
import urllib2
import urllib
import requests

from requests import request, HTTPError
from social.pipeline.user import get_username as social_get_username


from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse


from profiles.models import Address, Job, Info, UserPicture, Gamification



def save_profile_picture(strategy, user, response, details, is_new=False,*args,**kwargs):
    if is_new and strategy.backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture?width=9999&height=9999'.format(response['id'])
        try:
            response = request('GET', url)
            response.raise_for_status()
        except HTTPError:
            pass
        #num_of_pics = UserPicture.objects.filter(user=self.user).count()
        image_content = ContentFile(requests.get(url).content)

        picture = UserPicture.objects.create(user=user)
       
        picture.image.save("facebook-%s.jpg" %(user.username), image_content)

    return


def facebook_basic_data(strategy, user, response, is_new=False, *args, **kwargs):
    if is_new and strategy.backend.name == 'facebook':
        email = kwargs['details']['email']
        user = User.objects.get(email=email)
        user.is_active = False
        user.first_name = response['first_name']
        user.last_name = response['last_name']
        try:
            info = Info.objects.get(user=user)
        except:
            info = Info.objects.create(user=user)
        if response['gender'][0].lower() == 'f':
            info.gender = 'Female'
        else:
            info.gender = 'Male'
        user.save()
        info.save()
        return HttpResponseRedirect(reverse('new_user_fb_or_goog', kwargs={'email': email}))
    return 


def associate_user_by_email(**kwargs):
    try:
        email = kwargs['details']['email']
        kwargs['user'] = User.objects.get(email=email)
    except:
        pass
    return kwargs


def get_username(strategy, details, user=None, *args, **kwargs):
    result = social_get_username(strategy, details, user=user, *args, **kwargs)
    result['username'] = str(result['username']).translate(None, " ?.!/;:")
    return result



    
