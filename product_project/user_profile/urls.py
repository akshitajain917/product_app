from django.urls import path
from .views import CreateProduct,GetAllProducts,GetProduct,UpdateProduct,DeleteProduct,SheetUpload

urlpatterns = [
    path('add_product', CreateProduct.as_view(),name="add"),
    path('upload_sheet', SheetUpload.as_view(),name="add_via_excel"),
    path('view_all_products', GetAllProducts.as_view(),name="view_all"),
    path('<pk>/', GetProduct.as_view(),name="view_product"),
    path('<int:pk>/update', UpdateProduct.as_view(),name="update"),
    path('<pk>/delete/', DeleteProduct.as_view(),name="delete"),
]