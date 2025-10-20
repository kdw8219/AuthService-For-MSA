from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from accounts import views as accounts_views
from tokens import views as tokens_views

# Create your views here.
def auth_login(request):
    #TODO: login 시 ID/PWD 정합성 체크(accounts DB)
    #TODO: 로그인 성공 후 JWT 토큰 발급, refresh token 발급
    return HttpResponse("login success")

def auth_logout(request):
    #TODO: logout 시 JWT 토큰 무효화(Blacklist 등록)
    return HttpResponse("logout success")

def auth_refresh(request):
    #TODO: access token 만료로 인한 재발급 필요 시 refresh token 검증 후 재발급
    #TODO: 만약 refresh token 도 만료되었으면 재로그인 요구 필요.
    return HttpResponse("token refresh success")

def auth_register(request):
    #TODO: register 시 ID/PWD/EMAIL 등 정보 수집, 중복여부 체크
    #TODO: 중복 체크 결과 별다른 문제가 없다면 accounts DB에 사용자 정보 저장
    #TODO: 중복 체크 결과 중복 발생 시 에러 리턴(409 conflict)
    #TODO: 포맷에러 시 에러 리턴(400 bad request)
    #TODO : 등록 성공 시 성공 리턴(201 created)
    #TODO : 비밀번호는 해싱하여 저장할 것 
    return HttpResponse("register success")