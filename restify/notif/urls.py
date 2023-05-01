from django.urls import path
from . import views

app_name="notif"

urlpatterns = [ 
    path('list/', views.ListNotif.as_view(), name='list'),
    path('<int:pk>/', views.mark_notification_read, name='read'),
    path('delete/<int:pk>/', views.delete_notification, name='delete'),
    
]