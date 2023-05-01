from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import AbstractUser

# class CustomUser(AbstractUser):
#     is_guest = models.BooleanField(default=True)
    
class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    isComment = models.BooleanField(default=True) #to distinguish reply and comment
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    
# class Property(models.Model):
#     description = models.CharField(max_length = 180)
#     prop_type = models.CharField(max_length = 100)
#     address = models.CharField(max_length = 180)
#     rooms = models.IntegerField()
#     baths = models.IntegerField()
#     parking = models.IntegerField()
#     max_guests = models.IntegerField()
#     is_available = models.BooleanField(default = True) #will have to come back to this
#     first_day_available = models.DateTimeField(auto_now = True) 
#     rate = models.IntegerField()
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     #comments = models.ManyToManyField('Comment', blank=True)


# class Reservation(models.Model):
#     check_in = models.DateTimeField()
#     check_out = models.DateTimeField()
#     num_days = models.IntegerField()
#     numGuests = models.IntegerField()
#     property_id = models.IntegerField()
#     customer_id = models.IntegerField()
#     status = models.CharField(max_length = 180)