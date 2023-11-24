from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from account.models import Account
User = get_user_model()

# class with the form for creating a new user
class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'username',
            'id': 'username',
            'type': 'text',
            'placeholder': 'John Doe',
            'maxlength': '16',
            'minlength': '6',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'email',
            'id': 'email',
            'type': 'email',
            'placeholder': 'JohnDoe@mail.com',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'password1',
            'id': 'password1',
            'type': 'password',
            'placeholder': 'password',
            'minlength': '8'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'password1',
            'id': 'password1',
            'type': 'password',
            'placeholder': 'password',
            'minlength': '8'
        })


    username = forms.CharField(max_length=20, label=False)
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

