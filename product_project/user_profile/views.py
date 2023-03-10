# Create your views here.
from django.shortcuts import render
from django.urls import reverse_lazy
from accounts.models import User
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.core.files.storage import FileSystemStorage
from user_profile.constants import UPLOAD_PATH
from django.contrib.auth import logout
from user_profile.forms import ProductUploadForm, RegistrationForm,LoginForm,UpdatePasswordForm
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib import messages
from .models import Product, ProductColor
import pandas as pd

# Default home page for all users of website
def home(request):
    return render(request,"index.html")

# Homepage for login users
@login_required
def homepage(request):
    return render(request,'homepage.html')

def logout_view(request):
    logout(request)
    return redirect('home')

# This view will provide a signup form for the user
class UserRegistrationView(FormView):
    form_class = RegistrationForm
    template_name = "signup.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')
    def form_valid(self,form):
        user = form.save()
        if user is not None:
            # once the form data is validated, we display message on login page and redirect to it
            messages.success(self.request, "Registered successfully!")
            return super(UserRegistrationView,self).form_valid(form)

# This view will enable user to login
class UserLoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('homepage')
    def form_valid(self,form):
        username_email_field = form.cleaned_data["username_or_email"] 
        # checks if user exists else user has to signup and then login
        try:
            user = User.objects.get(username=username_email_field)
        except:
            try:
                user = User.objects.get(email=username_email_field)
            except:
                return render(self.request, self.template_name, {'result': f"{username_email_field} doesn't exist. Please signup","form":form})
        if user is not None:
            # once the form data is validated, we display message on website's homepage and redirect to homepage for login users
            # this enables to create session for user 
            form = login(self.request, user)
            messages.success(self.request, "Login successfully!")
            return super(UserLoginView,self).form_valid(form)

# This view enables user to update password if it's username or email exists
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
        
        # validating password 
        if len(new_password) < 6 :
            return render(self.request, self.template_name, {'result': "Password length should be greater than 6","form":form})

        if new_password != confirmed_new_password:
            return render(self.request, self.template_name, {'result': "Password doesn't match","form":form})

        user.password = new_password
        user.save()
        if user is not None:
            # once the form data is validated, we display message on website's default homepage where user can login.
            messages.success(self.request, "Passsword updated successfully!")
            return super(UpdatePasswordView,self).form_valid(form)

# class-based View to create a product
class CreateProduct(PermissionRequiredMixin,CreateView):
    model = Product 
    template_name = "add_product.html"
    fields = ['name', 'price', 'discount_price','fabric_type', 'color_choice','size','description',]
    success_url = reverse_lazy('homepage')
    permission_required = ('user_profile.add_product',)

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Added product successfully.")
        return super(CreateProduct,self).form_valid(form)

# class-based View to list down all products
class GetAllProducts(PermissionRequiredMixin,ListView):
    template_name = "view_all_products.html"
    model = Product
    permission_required = ('user_profile.view_product',)

# class-based View to get details of a product
class GetProduct(PermissionRequiredMixin,DetailView):
    template_name = "view_product.html"
    model = Product
    permission_required = ('user_profile.view_product',)

# class-based View to update details of a product
class UpdateProduct(PermissionRequiredMixin,UpdateView):
    template_name = "update_product.html"
    model = Product
    fields = '__all__'
    success_url =reverse_lazy('view_all')
    permission_required = ('user_profile.change_product',)

# class-based View to delete details of a product
class DeleteProduct(PermissionRequiredMixin,DeleteView):
    template_name = "delete_product.html"
    model = Product
    success_url = reverse_lazy('view_all')
    permission_required = ('user_profile.delete_product',)

# provided a feature to add multiple products by uploading CSV file
class SheetUpload(FormView):
    template_name = "upload_product_sheet.html"
    form_class = ProductUploadForm
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        try:
            product_list = []
            file_name = form.files["file"]
            file_path = FileSystemStorage(location=UPLOAD_PATH)
            filename = file_path.save(file_name.name, file_name)
            product_file_path = UPLOAD_PATH + filename
            product_df = pd.read_csv(product_file_path)
            for index, row in product_df.iterrows():
                user = User.objects.get(email=self.request.user.email)
                try:
                    color = ProductColor.objects.get(color__icontains=row["Color"])
                except:
                    ProductColor.objects.create(color=row["Color"])
                    color = ProductColor.objects.get(color=color)
                try:
                    price = float(row["Price"])
                    discounted_price = float(row["Discount Price"])
                except:
                    print("Prices are not in proper format.")
                    continue
                product_list.append(Product(
                    user = user,
                    name=row["Name"],
                    price=price,
                    discount_price=discounted_price,
                    fabric_type=row["Fabric"],
                    description = row["Description"],
                    size = row["Size"],
                    color_choice=color,
                ))
            Product.objects.bulk_create(product_list)
            messages.success(self.request, "Added products successfully.")
            return super(SheetUpload,self).form_valid(form)

        except Exception as ex:
            return render(self.request, self.template_name, {"result":f"Can't read file properly due to {ex}. Correct it and try to upload again"})



        
