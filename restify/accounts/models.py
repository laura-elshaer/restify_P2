from django.db import models
from django.contrib.auth.models import User

class Meta:
    model = User
    fields = ('username', 'password', 'email', 'first_name', 'last_name')