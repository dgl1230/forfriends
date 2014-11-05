from django import forms

from .models import Interest

class InterestForm(forms.ModelForm):
	class Meta:
		model = Interest
		fields = ('interest',)


