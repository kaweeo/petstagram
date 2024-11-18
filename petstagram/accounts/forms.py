from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

UserModel = get_user_model()  # Return the User model that is active in this project.


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):  # Set model = UserModel, override to be the active user we work with
        model = UserModel


class AppUserChangeForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
