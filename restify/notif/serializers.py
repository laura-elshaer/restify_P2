from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [ 'timestamp', 'is_read', 'message','id'] #remember, different users will have different notifications, need to include user