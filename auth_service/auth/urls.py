from django.urls import path, include
from auth import views as auth_views

urlpatterns = [
    path('api/tokens/', auth_views.token_view, name='auth_login'), # POST/DELETE
    path('api/tokens/refresh/', auth_views.token_refresh, name='auth_refresh'), # POST
]
