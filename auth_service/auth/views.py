from django.http import JsonResponse
from django.conf import settings
from tokens import views as tokens
from django.views.decorators.csrf import csrf_exempt
import jwt
from dotenv import load_dotenv
import os

# Helper: decide cookie security based on settings.DEBUG (secure in production)
def _cookie_secure_flag():
    return not getattr(settings, "DEBUG", True)

@csrf_exempt #csrf exception을 함수 내부에서 처리
def token_view(request): # POST/DELETE
    response = None
    
    ua = request.META.get("HTTP_USER_AGENT", "")
    if "Mozilla" in ua or "Chrome" in ua or "Safari" in ua:
        return JsonResponse({"detail": "request from invalid source"}, status=400)
    
    if request.method == "POST":
        print("get auth post!")
        response = create_new_tokens_and_set_response()
        response.status_code = 200
        
    elif request.method == "DELETE":
        #logout 시도 시 토큰 블랙리스트 처리
        
        refresh_token = request.COOKIES.get("refresh_token")

        tokens.delete_token_from_refresh_token(refresh_token)
        tokens.add_token_to_blacklist(refresh_token)
        
        response = JsonResponse({"detail": "logout success"}, status=200)
    else:
        response = JsonResponse({"detail": "method not allowed"}, status=405)
    
    return response

def token_refresh(request): # POST
    """
    리프레시 토큰으로 액세스 토큰 재발급
    - refresh token은 HttpOnly cookie에서 읽음
    - refresh token 검증 후 새 access/refresh 토큰을 발급
    - 새 access_token은 Authorization 헤더로, 새 refresh_token은 cookie로 설정
    """
    # get refresh token from cookies
    refresh_token = request.COOKIES.get("refresh_token")

    if not refresh_token:
        return JsonResponse({"detail": "no refresh token"}, status=400)

    # if it is blacklisted, return error
    if not tokens.is_token_valid(refresh_token):
        return JsonResponse({"detail": "invalid refresh token"}, status=400)
    
    return create_new_tokens_and_set_response()


def create_new_tokens_and_set_response():
    
    access_token, new_refresh_token = tokens.create_new_tokens()

    res = {
        'access_token': access_token, 
        'refresh_token' : new_refresh_token
        }
    
    response = JsonResponse(res)
    
    return response

def validate_token(request):
    response = None
    
    if request.method == 'POST':
        
        refresh_token = ''
        if tokens.is_in_refresh_token(refresh_token):
            response = JsonResponse({"detail": "invalid refresh token"}, status=403)
        else:
            try:
                load_dotenv()
                secret_key = os.getenv('REFRESH_SECRET_KEY')

                jwt.decode(refresh_token, secret_key, algorithms=["HS256"] )
                response = JsonResponse({"detail": "valid refresh token"}, status=200)
            except jwt.InvalidTokenError:
                return JsonResponse({"valid": False}, status=401)
                
    else:
        response = JsonResponse({"detail": "method not allowed"}, status = 405)
        
    return response