from django.contrib import admin

from user_profile.models import Product,ProductColor


# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = (
        "name",
        "price",
        "discount_price",
        "fabric_type",
        "description",
        "size",
        "_user__email",
        "_color_choice__color"
    )
    search_fields = ("name","fabric_type",)
    list_filter = (
        "name",
        "fabric_type",
    )

    def _user__email(self, obj):
        try:
            return obj.user.email
        except Exception:
            return "None"

    _user__email.short_description = "Customer Email"

    def _color_choice__color(self, obj):
        try:
            return obj.color_choice.color
        except Exception:
            return "None"

    _color_choice__color.short_description = "Product Color"

@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ("color",)
