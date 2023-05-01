from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Property(models.Model):
    description = models.CharField(max_length = 180)
    prop_type = models.CharField(max_length = 100)
    address = models.CharField(max_length = 180)
    rooms = models.IntegerField()
    baths = models.IntegerField()
    parking = models.IntegerField()
    max_guests = models.IntegerField()
    is_available = models.BooleanField(default = True) #will have to come back to this
    first_day_available = models.DateTimeField(auto_now = True) 
    rate = models.IntegerField()
    owner = models.IntegerField()
    # owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Reservation(models.Model):
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    num_days = models.IntegerField()
    numGuests = models.IntegerField()
    property_id = models.IntegerField()
    customer_id = models.IntegerField()
    owner_id = models.IntegerField()
    status = models.CharField(max_length = 180)



    
