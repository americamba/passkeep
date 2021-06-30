from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from keep.models import Password, Category
from keep.utils.password import test_complexity


class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )


class PasswordForm(forms.ModelForm):

    class Meta:
        model = Password
        # exclude = ('category', 'user')
        fields = ("title", "username", "password", "url", "category", "notes")

    def clean_password(self):

        if test_complexity(self.cleaned_data['password']):
            return self.cleaned_data['password']
        else:
            raise ValidationError(
                _('Invalid password: %(pw)s'),
                code='invalid',
                params={'pw': self.cleaned_data['password']},
            )


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name', )
