from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
import random

class RegistrationForm(UserCreationForm):

    USER_CHOICES= [
        ('is_superuser', 'Distributor'),
        ('is_staff', 'Retailer'),
        ('is_customer', 'Customer'),
    ]
    email = forms.EmailField(max_length=254,required=True)
    password1 = forms.CharField(label='Enter password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput)
    user_type = forms.CharField(label="Sign Up as", widget=forms.Select(choices=USER_CHOICES))

    def __init__(self,**kwargs):
        super(RegistrationForm, self).__init__(**kwargs)

        for fieldname in ['username', 'password1','password2']:
            self.fields[fieldname].help_text = None

    def save(self, commit=True):
        obj = super(RegistrationForm,self).save(commit=False)
        user_type = self.cleaned_data["user_type"]
        if user_type == 'is_superuser':
            obj.is_superuser = obj.is_staff = obj.is_customer = True
        elif user_type == 'is_staff':
            obj.is_staff = obj.is_customer =  True
            obj.is_superuser  = False
        else:
            obj.is_superuser = obj.is_staff = False
            obj.is_customer = True
        obj.login_otp = random.randint(1,100000)
        if commit:
            obj.save()
        return obj

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

    
