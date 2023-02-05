from django.urls import path
from .views import CreateProduct

urlpatterns = [
    path('add_product', CreateProduct.as_view(),name="add"),
]