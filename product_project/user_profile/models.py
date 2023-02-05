from django.db import models
from django.conf import settings

class Fabric(object):
    CHIFFON = "chiffon"
    COTTON = "cotton"
    SILK = "silk"
    VELVET = "velvet"
    SYNTHETIC = "synthetic"
    CREPE = "pending"
    DENIM = "denim"
    LEATHER = "denim"
    LINEN = "linen"
    SATIN = "satin"
    
class Size(object):
    XS = "extra_small"
    S = "small"
    M = "medium"
    L = "large"
    XL = "extra large"

class Product(models.Model):
    FABRIC_CHOICE = (
        (Fabric.CHIFFON, "chiffon"),
        (Fabric.COTTON, "cotton"),
        (Fabric.SILK, "silk"),
        (Fabric.VELVET, "velvet"),
        (Fabric.SYNTHETIC, "synthetic"),
        (Fabric.CREPE, "pending"),
        (Fabric.DENIM, "denim"),
        (Fabric.LEATHER, "denim"),
        (Fabric.LINEN, "linen"),
        (Fabric.SATIN, "satin"),
    )

    SIZE_CHOICES =(
        (Size.XS,"extra_small"),
        (Size.S, "small"),
        (Size.M, "medium"),
        (Size.L, "large"),
        (Size.XL, "extra large")
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name =  models.CharField(max_length=100, null=False,help_text="Product Name")
    price =  models.FloatField(null=False,help_text="Actual Price of Product")
    discount_price = models.FloatField(null=True,blank=True,help_text="Discounted Price of Product")
    fabric_type = models.CharField(max_length=100, null=True,blank=True,choices=FABRIC_CHOICE,help_text="Products' Fabric Type")
    description = models.CharField(null=True,blank=True,help_text="Product Description",max_length=250)
    size = models.CharField(max_length=100, null=True,blank=True,choices=SIZE_CHOICES,help_text="Products' size choice")
    color_choice = models.ForeignKey('ProductColor',null=True, blank=True,on_delete=models.PROTECT)   

    def __str__(self):
        return self.name + ":" + self.user.email

class ProductColor(models.Model):
    color = models.CharField(max_length=50,null=True,blank=True,help_text="Product Colour")
    
    def __str__(self):
        return self.color
