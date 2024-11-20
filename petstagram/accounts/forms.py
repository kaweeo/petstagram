from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from petstagram.accounts.models import Profile


UserModel = get_user_model()  # Return the User model that is active in this project.


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):  # Set model = UserModel, override to be the active user we work with
        model = UserModel
        fields = ('email',)


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', )
