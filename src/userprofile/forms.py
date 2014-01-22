from django import forms


from .models import UserProfile

class UserProfileForms(forms.ModelForm):
	class Meta:
		model = UserProfile