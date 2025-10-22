from django.http import JsonResponse, HttpResponse
from django.conf import settings
from tokens import views as tokens


# Helper: decide cookie security based on settings.DEBUG (secure in production)
def _cookie_secure_flag():
    return not getattr(settings, "DEBUG", True)


def token_view(request): # POST/DELETE
    #TODO: User(Robot, Management user)의 login 시도 시 JWT 토큰 발급
    return HttpResponse("login success")

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

    # TODO: 실제 구현에서는 refresh_token에서 user_id를 안전하게 파싱/검증
    # 아래는 tokens.create_new_tokens의 테스트용 포맷에 맞춘 간단한 파싱 예시
    user_id = None
    prefix = "refresh_token_for_"
    if isinstance(refresh_token, str) and refresh_token.startswith(prefix):
        user_id = refresh_token[len(prefix) :]

    if not user_id:
        return JsonResponse({"detail": "cannot determine user from refresh token"}, status=400)

    access_token, new_refresh_token = tokens.create_new_tokens(user_id)

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