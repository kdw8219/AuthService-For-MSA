from django.http import JsonResponse
from django.conf import settings
from tokens import views as tokens
from django.views.decorators.csrf import csrf_exempt
import jwt
from dotenv import load_dotenv
import os
import json
import logging
import asyncio

logger = logging.getLogger('auth')

@csrf_exempt #csrf exception을 함수 내부에서 처리
async def token_view(request): # POST/DELETE
    response = None
    
    ua = request.META.get("HTTP_USER_AGENT", "")
    if "Mozilla" in ua or "Chrome" in ua or "Safari" in ua:
        return JsonResponse({"detail": "request from invalid source"}, status=400)
    
    if request.method == "POST":
        logger.info('[auth/token_view] get auth post request!')
        response = await create_new_tokens_and_set_response(False)
        response.status_code = 200
        
    elif request.method == "DELETE":
        #logout 시도 시 토큰 블랙리스트 처리
        
        refresh_token = request.COOKIES.get("refresh_token")

        # 굳이 응답 내보내는 걸 기다릴 필요는 없기 때문에 coroutine으로 동작
        asyncio.create_task(tokens.add_token_to_blacklist(refresh_token))
        
        response = JsonResponse({"detail": "logout success"}, status=200)
    else:
        response = JsonResponse({"detail": "method not allowed"}, status=405)
    
    return response

@csrf_exempt #csrf exception을 함수 내부에서 처리
async def token_refresh(request): # POST
    """
    리프레시 토큰으로 액세스 토큰 재발급
    - refresh token은 HttpOnly cookie에서 읽음
    - refresh token 검증 후 새 access/refresh 토큰을 발급
    - 새 access_token은 Authorization 헤더로, 새 refresh_token은 cookie로 설정
    """
    # get refresh token from cookies
    request_string = request.body
    data = json.loads(request_string)
    refresh_token = data['refresh_token']
    
    if not refresh_token:
        return JsonResponse({"detail": "no refresh token"}, status=400)

    # if it is blacklisted, return error
    if not tokens.is_token_valid(refresh_token):
        return JsonResponse({"detail": "invalid refresh token"}, status=403)
    
    return await create_new_tokens_and_set_response(True)

@csrf_exempt #csrf exception을 함수 내부에서 처리
async def create_new_tokens_and_set_response(onlyAccess = False):
    
    new_access_token = tokens.create_new_token(True)
    
    res = None
    if onlyAccess:
        new_access_token = tokens.create_new_token(True)
        res = {
            'access_token': new_access_token, 
        }
    else:
        new_refresh_token = tokens.create_new_token(False)
        res = {
            'access_token': new_access_token,
            'refresh_token': new_refresh_token,
        }
        await tokens.set_refreh_to_redis(new_refresh_token)
   
    response = JsonResponse(res)
    
    return response

@csrf_exempt #csrf exception을 함수 내부에서 처리
async def validate_token(request):
    response = None
    
    if request.method == 'POST':
        request_string = request.body
        data = json.loads(request_string)
        
        refresh_token = data['refresh_token']
        
        if not await tokens.is_in_refresh_token(refresh_token):
            response = JsonResponse({"detail": "invalid refresh token"}, status=403)
        else:
            try:
                load_dotenv()
                secret_key = os.getenv('REFRESH_SECRET_KEY')
                jwt.decode(refresh_token, secret_key, algorithms=["HS256"] )
                response = JsonResponse({"detail": "valid refresh token"}, status=200)
            except jwt.InvalidTokenError or jwt.ExpiredJwtException:
                response = JsonResponse({"detail": "invalid refresh token"}, status=403)
        
        return response
          
    else:
        response = JsonResponse({"detail": "method not allowed"}, status = 405)
        return response
