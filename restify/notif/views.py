from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, \
    ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class ListNotif(APIView):  #this returns notification messages as sepaparte pages
   
      def get(self, request):
        notifs = Notification.objects.all()
        paginator = PageNumberPagination()
        paginated_notifs = paginator.paginate_queryset(notifs, request)
        serialized_stores = [
            {
               'message': notif.message,
                'id':notif.id
                
            }
            for notif in paginated_notifs
        ]
        return paginator.get_paginated_response(serialized_stores)
      
    
@api_view(['GET']) #THEY DID IT W PATCH
def mark_notification_read(request, pk):
    notification = Notification.objects.get(id=pk)
    notification.is_read = True
    notification.save()
    serializer = NotificationSerializer(notification)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_notification(request, pk):
    notification = Notification.objects.get(id=pk)
    notification.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)