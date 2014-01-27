from django.utils.translation import gettext as _

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import strip_tags


from .models import UserProfile

class CreateUserForm(UserCreationForm): #may also be forms.ModelForm

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
	password_confirm = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
	username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))

	class Meta:
		model = User #may want this to be CustomUserModel
		#fields = ("username")

	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			User._default_manager.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError(
			self.error_messages['duplicate_username'],
			code='duplicate_username',
		)


	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
			)
		return password2

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

	def is_valid(self):
		form = super(CreateUserForm, self).is_valid()
		for f, error in self.errors.iteritems():
			if f != '__all__':
				self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
		return form


class AuthenticateForm(AuthenticationForm):
	username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
	password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))

	def is_valid(self):
		form = super(AuthenticationForm, self).is_valid()
		for f, error in self.errors.iteritems():
			if f!= '__all__':
				self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
		return form