# Create your views here.
from django.shortcuts import render
from django.urls import reverse_lazy
from accounts.models import User
from django.contrib.auth import login
from django.views.generic.edit import FormView
from user_profile.forms import RegistrationForm,LoginForm,UpdatePasswordForm
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView
from django.contrib import messages
from .models import Product


def home(request):
    return render(request,"index.html")

def homepage(request):
    return render(request,'homepage.html')

class UserRegistrationView(FormView):
    form_class = RegistrationForm
    template_name = "signup.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')
    def form_valid(self,form):
        user = form.save()
        if user is not None:
            messages.success(self.request, "Registered successfully!")
            return super(UserRegistrationView,self).form_valid(form)

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
                return render(self.request, self.template_name, {'result': f"{username_email_field} doesn't exist. Please signup","form":form})
        if user is not None:
            form = login(self.request, user)
            messages.success(self.request, "Login successfully!")
            return super(UserLoginView,self).form_valid(form)

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
                return render(self.request, self.template_name, {'result': f"{email} doesn't exist. Please signup","form":form})
        
        if len(new_password) < 6 :
            return render(self.request, self.template_name, {'result': "Password length should be greater than 6","form":form})

        if new_password != confirmed_new_password:
            return render(self.request, self.template_name, {'result': "Password doesn't match","form":form})

        user.password = new_password
        user.save()
        if user is not None:
            messages.success(self.request, "Passsword updated successfully!")
            return super(UpdatePasswordView,self).form_valid(form)


class CreateProduct(CreateView):
    model = Product 
    template_name = "add_product.html"
    fields = ['name', 'price', 'discount_price','fabric_type', 'color_choice','size','description',]
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "The task was created successfully.")
        return super(TaskCreate,self).form_valid(form)
    

        
