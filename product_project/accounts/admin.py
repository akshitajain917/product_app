from django.contrib import admin
from accounts.models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = (
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "password"
    )
    search_fields = ("username","email",)
    list_filter = (
        "email",
        "username",
        "first_name",
        "last_name",
    )

