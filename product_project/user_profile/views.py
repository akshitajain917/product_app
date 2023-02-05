# Create your views here.
from django.shortcuts import render
from django.urls import reverse_lazy
from accounts.models import User
from django.contrib.auth import login
from django.views.generic.edit import FormView
from user_profile.forms import RegistrationForm,LoginForm,UpdatePasswordForm
from django.shortcuts import redirect, render
import time

def home(request):
    return render(request,"index.html")

class UserRegistrationView(FormView):
    form_class = RegistrationForm
    template_name = "signup.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')
    def form_valid(self,form):
        user = form.save()
        if user is not None:
            return redirect('login')

class UserLoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('homepage')
    def form_valid(self,form):
        username_email_field = form.cleaned_data["username_or_email"] 
        try:
            user = User.objects.get(username=username_email_field)
        except:
            try:
                user = User.objects.get(email=username_email_field)
            except:
                return render(self.request, self.template_name, {'message': f"{username_email_field} doesn't exist. Please signup","form":form})
        if user is not None:
            form = login(self.request, user)
            return redirect('homepage')

class UpdatePasswordView(FormView):
    form_class = UpdatePasswordForm
    template_name = "update_password.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')
    def form_valid(self,form):
        email = form.cleaned_data["email"]
        new_password = form.cleaned_data["password1"] 
        confirmed_new_password = form.cleaned_data["password2"] 
        try:
            user = User.objects.get(email=email)
        except:
            try:
                user = User.objects.get(email=email)
            except:
                return render(self.request, self.template_name, {'message': f"{email} doesn't exist. Please signup","form":form})
        
        if len(new_password) < 6 :
            return render(self.request, self.template_name, {'message': "Password length should be greater than 6","form":form})

        if new_password != confirmed_new_password:
            return render(self.request, self.template_name, {'message': "Password doesn't match","form":form})

        user.password = new_password
        user.save()
        if user is not None:
            return redirect('home')

def homepage(request):
    print(request.user.is_authenticated)
    return render(request,'homepage.html',{})


        
