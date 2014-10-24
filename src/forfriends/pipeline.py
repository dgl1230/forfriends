import datetime
import urllib2
import urllib


from requests import request, HTTPError
from social.pipeline.user import get_username as social_get_username


from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


from profiles.models import Address, Job, Info, UserPicture, Gamification



def save_profile_picture(strategy, user, response, details, is_new=False,*args,**kwargs):
    if strategy.backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass

        picture = UserPicture.objects.create(user=user)
        name = urlparse(url).path.split('/')[-1]
        picture.image.save(name, File(urllib2.urlopen(self.url).read(), save=True)


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



    
