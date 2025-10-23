from django.http import JsonResponse, HttpResponse
from django.conf import settings
from tokens import views as tokens


# Helper: decide cookie security based on settings.DEBUG (secure in production)
def _cookie_secure_flag():
    return not getattr(settings, "DEBUG", True)


def token_view(request): # POST/DELETE
    response = None
    
    if request.method == "POST":
        response = create_new_tokens_and_set_response()
        response.json({"detail": "login success"})
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

    response = JsonResponse({"detail": "token refresh success"})
    response["Authorization"] = f"Bearer {access_token}"
    response.set_cookie(
        "refresh_token",
        new_refresh_token,
        httponly=True,
        secure=_cookie_secure_flag(),
        samesite="Lax",
        path="/",
    )
    return response