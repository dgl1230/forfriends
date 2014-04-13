from django import forms
from .models import Address, Info, Job, UserPicture

class AddressForm(forms.ModelForm):
	class Meta:
		model = Address

class InfoForm(forms.ModelForm):
	class Meta:
		model = Info

class JobForm(forms.ModelForm):
	class Meta:
		model = Job

class UserPictureForm(forms.ModelForm):
	class Meta:
		model = UserPicture