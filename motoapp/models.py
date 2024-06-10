from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=255, null=True, blank=True)
    shipping_country = models.CharField(max_length=255)


	# Don't pluralize address
    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'

# Create a user Shipping Address by default when user signs up
def create_shipping(sender, instance, created, **kwargs):
	if created:
		user_shipping = ShippingAddress(user=instance)
		user_shipping.save()

# Automate the profile thing
post_save.connect(create_shipping, sender=User)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username

#Create a user profile by default when user sign up
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()

# Automate the profile thing
post_save.connect(create_profile, sender=User)
	

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100,null=False, blank=False)

    def __str__(self):
        return self.name

FUEL_CHOICES = [
        ('none', 'Select Fuel type'),
        ('cng_hybrid', 'CNG and Hybrid'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('lpg', 'LPG'),
        ('petrol', 'Petrol'),
    ]

OWNER_CHOICES = [
        ('none', 'Select No.of Owners'),
        ('first', '1st'),
        ('second', '2nd'),
        ('third', '3rd'),
        ('fourth_plus', '4+'),]

class Sell(models.Model):
    category=models.ForeignKey(Category,on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.CharField(max_length=100)
    modelv = models.CharField(max_length=50)
    year=models.IntegerField()
    fuel = models.CharField(max_length=20, choices=FUEL_CHOICES, default='none')
    km_driven = models.CharField(max_length=50, blank=True, null=True)
    no_owners = models.CharField(max_length=20, choices=OWNER_CHOICES, default='none')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    pname = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.brand

class Bcategory(models.Model):
    name=models.CharField(max_length=100,null=False, blank=False)

    def __str__(self):
        return self.name

BFUEL_CHOICES = [
        ('none', 'Select Fuel type'),
        ('cng_hybrid', 'CNG and Hybrid'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('lpg', 'LPG'),
        ('petrol', 'Petrol'),
        ('none', 'none'),
    ]

class Buy(models.Model):
    bcategory=models.ForeignKey(Bcategory,on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.CharField(max_length=100)
    price = models.IntegerField()
    Fuel_Type = models.CharField(max_length=20, choices=BFUEL_CHOICES, default='none')
    Mileage = models.CharField(max_length=100)
    Power = models.CharField(max_length=100)
    Launch_Date = models.CharField(max_length=100)
    Engine_Capacity = models.CharField(max_length=100)
    bdescription = models.CharField(max_length=100)
    color=models.CharField(max_length=100)
    Tyre = models.CharField(max_length=100)
    image = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    model=models.CharField(max_length=100)


    def __str__(self):
        return self.brand

class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Buy,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)

    @property
    def price(self):
        new_price = self.pid.price * self.qty
        return new_price

class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Buy,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)

class SendQuotation(models.Model):
    quotation_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Buy,on_delete=models.CASCADE,db_column="pid")


# Vehicle service

class Request(models.Model):
    cat=(('two wheeler with gear','two wheeler with gear'),('two wheeler without gear','two wheeler without gear'),('three wheeler','three wheeler'),('four wheeler','four wheeler'))
    scategory=models.CharField(max_length=50,choices=cat)

    vehicle_no=models.IntegerField(null=False)
    vehicle_name = models.CharField(max_length=40,null=False)
    vehicle_model = models.CharField(max_length=40,null=False)
    vehicle_brand = models.CharField(max_length=40,null=False)

    problem_description = models.CharField(max_length=500,null=False)
    date=models.DateField(auto_now=True)
    cost=models.IntegerField(null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
 
    stat=(('Pending','Pending'),('Approved','Approved'),('Repairing','Repairing'),('Repairing Done','Repairing Done'),('Released','Released'))
    status=models.CharField(max_length=50,choices=stat,default='Pending',null=True)

    def __str__(self):
        return self.problem_description




