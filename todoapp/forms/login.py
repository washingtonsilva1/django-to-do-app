from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input-control',
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
                'class': 'form-input-control',
            }
        ),
        error_messages={
            'required': 'This field can not be empty.'
        }
    )
