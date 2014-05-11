from django import forms
from .models import Address, Info, Job, UserPicture

class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = ('city', 'state', 'zipcode',)


class InfoForm(forms.ModelForm):
	class Meta:
		model = Info
		fields = ('bio', 'birthday', 'first_name', 'gender', 'last_name',)


class JobForm(forms.ModelForm):
	class Meta:
		model = Job
		fields = ('position', 'employer',)


class UserPictureForm(forms.ModelForm):
	class Meta:
		model = UserPicture
		fields = ('image',)