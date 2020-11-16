from django_registration.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from users.models import User
from django import forms


class RegisterForm(RegistrationForm):
    email = forms.EmailField()
    physics_class = forms.ChoiceField(label = "Which class are you in?", choices=(('AP Physics','AP Physics'),
                                            ('Honors Physics','Honors Physics'),
                                            ('Standard Physics','Standard Physics')))

    class Meta:
        model = User
        fields = ["email", "password1", "password2", "physics_class"]

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'password',
        }))

