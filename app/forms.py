from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from account.models import Account


from django.forms import ModelForm, TextInput, Textarea, Select, CharField


from .models import *
User = get_user_model()


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({
            'class': 'uk-input',
            'required': '',
            'name': 'name',
            'id': 'name',
            'style': 'height: 4vh; border-radius: 0.5em; font-size: 2em',
            'type': 'text',
            'placeholder': '',
            'minlength': '1'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'uk-input',
            'style': 'height: 4vh; border-radius: 0.5em; font-size: 2em',
            'required': '',
            'name': 'email',
            'id': 'email',
            'type': 'email',
            'placeholder': '',
            'minlength': '8'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'uk-input pswdChecker',
            'required': '',
            'style': 'height: 4vh; border-radius: 0.5em; font-size: 2em',
            'name': 'password1',
            'id': 'password1',
            'type': 'password',
            'placeholder': '',
            'minlength': '8'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'uk-input uk-border uk-border-rounded pswdChecker',
            'required': '',
            'style': 'height: 4vh; border-radius: 0.5em; font-size: 2em',
            'name': 'password2',
            'id': 'password2',
            'type': 'password',
            'placeholder': '',
            'minlength': '8'
        })

    first_name = forms.CharField(max_length=20, label=False)
    email = forms.EmailField(max_length=100)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = Account
        fields = ('email', 'city', 'first_name', 'last_name', 'email', 'payment_account', )

        # 'ogrn', 'inn', 'index','nameFull', 'korr_check','kpp', 'name_small', 'reg_form', 'bik', 
