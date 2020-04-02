from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms


# user registration form
class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField()
	first_name = forms.CharField()
	last_name = forms.CharField()

	class Meta:
		model = User
		fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

	# remove all helptext from form
	def __init__(self, *args, **kwargs):
		super(UserRegistrationForm, self).__init__(*args, **kwargs)
		for fieldname in self.fields:
			self.fields[fieldname].help_text = None


# user update form
class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	first_name = forms.CharField()
	last_name = forms.CharField()

	class Meta:
		model = User
		fields = ["username", "first_name", "last_name", "email"]

	# remove all helptext from form
	def __init__(self, *args, **kwargs):
		super(UserUpdateForm, self).__init__(*args, **kwargs)
		for fieldname in self.fields:
			self.fields[fieldname].help_text = None


# profile update form
class ProfileUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ["bio"]


# password update form
class PasswordForm(PasswordChangeForm):

	# remove all helptext from form and disable autofocus
	def __init__(self, *args, **kwargs):
		super(PasswordForm, self).__init__(*args, **kwargs)
		for fieldname in self.fields:
			self.fields[fieldname].help_text = None
			self.fields[fieldname].widget.attrs.pop("autofocus", None)