from django.urls import path, include
from auth import views as auth_views

urlpatterns = [
    path('', auth_views.token_view, name='auth_login'), # POST/DELETE
    #Token refresh -> Security Issue --> POST
    path('refresh/', auth_views.token_refresh, name='auth_refresh'), # POST
    #Token validate check -> Security Issue --> POST
    path('validate/', auth_views.validate_token, name='validate_token') # POST
]
