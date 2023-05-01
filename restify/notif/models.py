from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE) #if a user is deleted, then obv all notifications will be deleted
    #not sure if I need to include notification type 
    
    # def __str__(self): #not sure what this exactly does,  but often used in models
    #     return f"{self.name}"