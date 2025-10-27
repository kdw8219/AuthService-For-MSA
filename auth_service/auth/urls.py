from django.urls import path, include
from auth import views as auth_views

urlpatterns = [
    path('', auth_views.token_view, name='auth_login'), # POST/DELETE
    path('refresh/', auth_views.token_refresh, name='auth_refresh'), # POST
    path('validate/', auth_views.validate_token, name='validate_token') #GET
]
