from django.utils.translation import gettext as _

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.forms import extras
from .models import UserProfile

class CreateUserForm(UserCreationForm): 
    

	GENDER = (
	('M', 'Male'),
	('F', 'Female'),
)

	#birthday = forms.DateField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Birthday'}))
	birthday = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={'placeholder': 'Birthday'}))
	email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email'}))
	first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name'}))
	gender = forms.ChoiceField(choices=GENDER)
	last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name'}))
	password1 = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
	password2 = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
	username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
	
	def is_valid(self):
		form = super(CreateUserForm, self).is_valid()
		return form


	class Meta:
		model = User
		fields = ['email', 'username', 'first_name', 'last_name',  
					'password1', 'password2']



class AuthenticateForm(AuthenticationForm):
	username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
	password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))

	def is_valid(self):
		form = super(AuthenticationForm, self).is_valid()
		return form
