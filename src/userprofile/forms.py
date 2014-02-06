from django.utils.translation import gettext as _

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import strip_tags


from .models import UserProfile

class CreateUserForm(forms.ModelForm): 

	error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    


	birthday = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={'placeholder': 'Birthday'}))
	city = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'City'}))
	country = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Country'}))
	email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email'}))
	first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name'}))
	password = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
	password2 = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
	username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))

	def is_valid(self):
		form = super(CreateUserForm, self).is_valid()
		#for f, error in self.errors.iteritems():
			#if f != '__all__':
				#self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
		return form

	class Meta:
		model = UserProfile
		fields = ['email', 'username', 'first_name', 'last_name', 'birthday', 'city', 'country', 
					'password', 'password']

	def clean_username(self):
		username = self.cleaned_data["username"]
		try: 
			UserProfile._default_manager.get(username=username)
		except UserProfile.DoesNotExist: 
				return username
		raise forms.ValidationError(self.error_messsges['duplicate_username'], 
			code="duplicate_username",)

	def clean_password2(self):
		password = self.cleaned_data.get("password")
		pasword2 = self.cleaned_data.get("password")
		if password and password2 and password != password2:
			raise forms.ValidationError(self.error_messages['password_mismatch'], 
				code="password_mismatch", )
		return password2

	def save(self, commit=True): 
		user = super(CreateUserForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user


class AuthenticateForm(AuthenticationForm):
	username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
	password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))

	def is_valid(self):
		form = super(AuthenticationForm, self).is_valid()
		for f, error in self.errors.iteritems():
			if f!= '__all__':
				self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
		return form