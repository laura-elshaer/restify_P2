from django.urls import path
from . import views
app_name = "comments"

urlpatterns = [
    path('add/', views.AddComment.as_view(), name='add_comment'),
    path('addproperty/', views.AddCommentP.as_view(), name='add_comment_property'),
    path('view/', views.GetComments.as_view(), name='viewcomments'),
    path('reply/', views.Reply.as_view(), name='add_reply'),
]