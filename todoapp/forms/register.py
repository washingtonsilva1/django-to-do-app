import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        min_length=4,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Type your username',
                'class': 'span-2',
            }
        ),
        error_messages={
            'required': 'This field can not be empty.',
            'min_length': 'Your username must have at least 4 characters.',
            'unique': 'A user with this name already exists.',
        }
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Type your email',
                'class': 'span-2',
            }
        ),
        error_messages={
            'required': 'This field can not be empty.',
            'invalid': 'Your email address must be valid.',
        }
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Type your password',
            }
        ),
        error_messages={
            'required': 'This field can not be empty.',
        },
        help_text='Your password must contain uppercase and lower case \
        letters, and a number. \
        Also, it must have at least 8 characters.',
    )
    password2 = forms.CharField(
        label='Confirm your password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Type your password again',
            }
        ),
        error_messages={
            'required': 'This field can not be empty.',
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        cleaned_password = self.cleaned_data.get('password', '')
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
        if not regex.match(cleaned_password):
            raise ValidationError(
                message='Your password does not match the requirements.',
                code='invalid',
            )
        return cleaned_password

    def clean(self):
        cleaned_data = super().clean()
        p = cleaned_data.get('password', '')
        p2 = cleaned_data.get('password2', '')
        if p and not p.lower() == p2.lower():
            raise ValidationError({
                'password2': ValidationError(
                    message='Your passwords are not equal.',
                    code='invalid'
                )
            })
        return cleaned_data
