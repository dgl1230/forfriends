from django import forms

from .models import Interest, InterestPicture

class InterestForm(forms.ModelForm):
	class Meta:
		model = Interest
		fields = ('interest')


class InterestPictureForm(forms.ModelForm):
	class Meta:
		model = InterestPicture
		fields = ('interest', 'image', )
