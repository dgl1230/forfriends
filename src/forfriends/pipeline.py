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


from profiles.models import Address, Job, Info, UserPicture, Gamification



def save_profile_picture(strategy, user, response, details, is_new=False,*args,**kwargs):
    if strategy.backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture?width=9999&type=large&height=9999'.format(response['id'])
        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        #num_of_pics = UserPicture.objects.filter(user=self.user).count()
        image_content = ContentFile(requests.get(url).content)

        picture = UserPicture.objects.create(user=user)
       
        picture.image.save("facebook-%s.jpg" %(user.username), image_content)
    return




# User details pipeline
'''def user_details(strategy, details, response, user=None, *args, **kwargs):
    """Update user details using data from provider."""
    if user:
        if kwargs['is_new']:
            attrs = {'user': user}
           #if facebook
            if strategy.backend.__class__.__name__ == 'FacebookOAuth2':
                fb_data = {
                    
                    'gender': response['gender'],
                    
                }
                attrs = dict(attrs.items() + fb_data.items())
            Info.objects.create(
                **attrs
            )
'''

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



    
