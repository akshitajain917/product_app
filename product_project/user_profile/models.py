from django.db import models
from django.conf import settings

class Fabric(object):
    CHIFFON = "Chiffon"
    COTTON = "Cotton"
    SILK = "Silk"
    VELVET = "Velvet"
    SYNTHETIC = "Synthetic"
    CREPE = "Crepe"
    DENIM = "Denim"
    LEATHER = "Leather"
    LINEN = "Linen"
    SATIN = "Satin"
    
class Size(object):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"

class Product(models.Model):
    FABRIC_CHOICE = (
        (Fabric.CHIFFON, "Chiffon"),
        (Fabric.COTTON, "Cotton"),
        (Fabric.SILK, "Silk"),
        (Fabric.VELVET, "Velvet"),
        (Fabric.SYNTHETIC, "Synthetic"),
        (Fabric.CREPE, "Crepe"),
        (Fabric.DENIM, "Denim"),
        (Fabric.LEATHER, "Leather"),
        (Fabric.LINEN, "Linen"),
        (Fabric.SATIN, "Satin"),
    )

    SIZE_CHOICES =(
        (Size.XS,"XS"),
        (Size.S, "S"),
        (Size.M, "M"),
        (Size.L, "L"),
        (Size.XL, "XL")
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
