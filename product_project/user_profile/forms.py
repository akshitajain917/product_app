from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
import random

class RegistrationForm(UserCreationForm):

    USER_CHOICES= [
        (1, 'Distributor'),
        (2, 'Retailer'),
        (3, 'Customer'),
    ]
    email = forms.EmailField(max_length=254,required=True)
    password1 = forms.CharField(label='Enter password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput)
    user_type = forms.CharField(label="Sign Up as", widget=forms.Select(choices=USER_CHOICES))

    def __init__(self,**kwargs):
        super(RegistrationForm, self).__init__(**kwargs)

        for fieldname in ['username', 'password1','password2']:
            self.fields[fieldname].help_text = None
    class Meta:
        model = User
        fields = ('user_type','username','first_name','last_name','email', 'password1','password2')
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'off'}),
        }

class LoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=254,required=True,label="Enter Username/Email")
    otp = forms.IntegerField(required=True,label="Enter OTP")

class UpdatePasswordForm(forms.Form):
    email = forms.EmailField(max_length=254,required=True,label="Enter Email")
    password1 = forms.CharField(label='Enter new password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','password1','password2')
        widgets = {
            'email': forms.TextInput(attrs={'autocomplete': 'off'}),
        }

    
