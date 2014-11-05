from django import forms
from .models import Address, Info, Job, UserPicture


from django import forms






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

