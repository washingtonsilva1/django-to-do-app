from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Type your username'
            }
        ),
        error_messages={
            'required': 'This field can not be empty.',
        },
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Type your password'
            }
        ),
        error_messages={
            'required': 'This field can not be empty.'
        }
    )
