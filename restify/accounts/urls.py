from django.urls import path
from . import views
app_name = "accounts"

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='token_obtain_pair'),
    path('update/<int:pk>/', views.UpdateProfileView.as_view(), name='auth_update_profile'),
]