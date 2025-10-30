import jwt
import datetime
import os
from dotenv import load_dotenv
from typing import Optional
import logging
import redis.asyncio as asyncredis

logger = logging.getLogger('tokens')

# 전역 Redis 객체
redis = None

async def get_redis():
    global redis
    if not redis:
        # 한 번만 연결 생성
        load_dotenv()
        URL = os.getenv('REDIS_URL')
        PORT = os.getenv('REDIS_PORT')
        PASSWORD = os.getenv('REDIS_AUTH')
        redis = await asyncredis.Redis(host=URL
                                       , port=PORT
                                       , password=PASSWORD
                                       , decode_responses=True)
    return redis

async def is_token_valid(token):
    
    if not validate_refresh_token(token):
        add_token_to_blacklist(token)
        return False
    
    conn = await get_redis()
    key = await conn.get(f'blacklist_{token}')
    
    if key is None:# conn 했더니 데이터가 없다. --> 유효하다 --> True
        return True
    
    return False
    
async def add_token_to_blacklist(token):
    conn = await get_redis()
    res = await conn.set(f'blacklist_{token}', 1, ex = 10*24*60*60)  # 10일 동안 블랙리스트에 저장
    
    if res == None:
        logger.info('[tokens/add_token_to_blacklist] get auth post request!')

async def is_in_refresh_token(token):
    conn = await get_redis()
    key = await conn.get(f'{token}')
    
    if key is None: #key가 없으면 유효하지 않으므로 False 리턴
        return False
    
    return True

async def delete_token_from_cache(token):
    conn = await get_redis()
    await conn.delete(f'{token}') #after delete, don't care anything.

async def set_refreh_to_redis(new_refresh_token):
    """
    Create new access and refresh tokens for the given user_id.
    This is a placeholder function. Implement token creation logic here.
    """
    conn = await get_redis()
    await conn.set(new_refresh_token, 1, ex = 7*24*60*60)  # 7일 동안 refresh token에 저장

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

def validate_refresh_token(token:str) -> bool:
        load_dotenv()
        
        SECRET_KEY = os.getenv('REFRESH_SECRET_KEY')
        
        try:
            payload = jwt.decode(
                str(token),
                SECRET_KEY,
                algorithms=["HS256"],
                options={"require": ["exp", "iat"]}
            )
            
            return True

        except jwt.exceptions.ExpiredSignatureError:
            logger.info('[tokens/validate_refresh_token] Token has expired.')
            return False
        except jwt.exceptions.InvalidTokenError:
            logger.info('[tokens/validate_refresh_token] Invalid token')
            return False
