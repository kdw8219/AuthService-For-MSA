from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def auth_login(request):
    return HttpResponse("login success")

def auth_logout(request):
    return HttpResponse("logout success")

def auth_refresh(request):
    return HttpResponse("token refresh success")

def auth_register(request):
    return HttpResponse("register success")