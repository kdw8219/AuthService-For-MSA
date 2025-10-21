from django.urls import path, include
from auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.auth_login, name='auth_login'),
    path('logout/', auth_views.auth_logout, name='auth_logout'),
    path('refresh/', auth_views.auth_refresh, name='auth_refresh'),
]
