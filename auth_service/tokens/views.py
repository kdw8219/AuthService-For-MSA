import jwt
import datetime
import os
from dotenv import load_dotenv
from django_redis import get_redis_connection
from typing import Optional

def is_token_valid(token):
    conn = get_redis_connection("default")
    key = conn.get(f'blacklist_{token}')
    
    print ('token_valid check: '+str(key is None))
    
    if key is None:# conn 했더니 데이터가 없다. --> 유효하다 --> True
        return True
    
    return False
    
def add_token_to_blacklist(token):
    conn = get_redis_connection("default")
    res = conn.set(f'blacklist_{token}', 1, ex = 10*24*60*60)  # 10일 동안 블랙리스트에 저장
    
    if res == None:
        print("add token to blacklist success")

def is_in_refresh_token(token):
    conn = get_redis_connection("default")
    key = conn.get(f'{token}')
    
    if key is None: #key가 없으면 유효하지 않으므로 False 리턴
        return False
    
    return True

def delete_token_from_cache(token):
    conn = get_redis_connection("default")
    conn.delete(f'{token}') #after delete, don't care anything.

def set_refreh_to_redis(new_refresh_token):
    """
    Create new access and refresh tokens for the given user_id.
    This is a placeholder function. Implement token creation logic here.
    """
    conn = get_redis_connection("default")
    conn.set(new_refresh_token, 1, ex = 7*24*60*60)  # 7일 동안 refresh token에 저장

def create_new_token(isAccess) -> Optional[str]:
    load_dotenv()
    ISS = os.getenv("ISS")
    if isAccess:
        ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
        payload = {
            "iss": ISS,
            "username": ISS,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5),
            "iat": datetime.datetime.now(datetime.timezone.utc)
        }
        return jwt.encode(payload, ACCESS_SECRET_KEY, algorithm="HS256")
    
    else:
        REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
        payload = {
            "iss": ISS,
            "username": ISS,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=14),
            "iat": datetime.datetime.now(datetime.timezone.utc)
        }
        
        return jwt.encode(payload, REFRESH_SECRET_KEY, algorithm="HS256")



def get_access_token(Cookie):
    
    
    return ''
