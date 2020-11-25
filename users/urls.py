from django.urls import path, include
from users import views

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login', views.user_login, name='user_login'),
]
