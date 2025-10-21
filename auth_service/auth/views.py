from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from tokens import views as tokens_views

# Create your views here.
def auth_login(request):
    #TODO: User(Robot, Management user)의 login 시도 시 JWT 토큰 발급
    return HttpResponse("login success")

def auth_logout(request):
    #TODO: User(Robot, Management user)의 logout 시 JWT 토큰 무효화(Blacklist 등록)
    return HttpResponse("logout success")

def auth_refresh(request):
    #TODO: access token 만료로 인한 재발급 필요 시 refresh token 검증 후 재발급 요청 수신
    #TODO: 만약 refresh token 도 만료되었으면 재로그인 요구 필요.
    return HttpResponse("token refresh success")