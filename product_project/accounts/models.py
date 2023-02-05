from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

# Register your models here.
class MyUserManager(BaseUserManager):

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    # Generic function for creating multiple users
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError("Email must be set for the user")
        email = self.normalize_email(email)
        user = self.model(
            username= username, 
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, username, email, password, **extra_fields):
        '''
        Differentiating multiple users by is_customer and is_retailer flag
        '''
        is_customer = extra_fields.pop("is_customer", False)
        if is_customer:
            is_staff, is_superuser = False, False
        else:
            is_staff, is_superuser = True, False
        return self._create_user(username,email,password, is_staff, is_superuser, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,**extra_fields)
        
    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the address by lowercasing the domain part of the email address.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    def get_by_natural_key(self, username):
        return self.get(username=username)

class User(AbstractBaseUser,PermissionsMixin):
    username_validator = ASCIIUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email address already exists."),
        },
    ) 
    is_staff = models.BooleanField(_("staff status"),default=False)
    is_superuser = models.BooleanField(_("superuser status"),default=False)
    is_customer = models.BooleanField(_("customer status"),default=False)

    

    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
    

