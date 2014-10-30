from django import forms
from .models import Address, Info, Job, UserPicture

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.datastructures import MultiValueDictKeyError
from PIL import Image

#from forfriends.settings.deployment import EMAIL_HOST_USER, DEBUG, MEDIA_ROOT, MEDIA_URL 
#from forfriends.settings.deployment_local import MEDIA_URL as LOCAL_MEDIA_URL


class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = ('city', 'state', 'zipcode',)


class InfoForm(forms.ModelForm):
	class Meta:
		model = Info
		fields = ('bio', 'gender',)


class JobForm(forms.ModelForm):
	class Meta:
		model = Job
		fields = ('position', 'employer',)


class UserPictureForm(forms.ModelForm):
	class Meta:
		model = UserPicture
		fields = ('image', 'caption', 'is_profile_pic')
		labels = {
        	'is_profile_pic': 'Make Profile Pic',
		}

