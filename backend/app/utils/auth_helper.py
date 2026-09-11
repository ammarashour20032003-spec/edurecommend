import jwt
import uuid
from datetime import datetime, timedelta
from app.config import Config

def generate_token(user_id):
    payload = {
        'user_id':  user_id,
        'exp':      datetime.utcnow() + timedelta(hours=24),
        'iat':      datetime.utcnow(),
        'jti':      str(uuid.uuid4())
    }
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, 'Token has expired'
    except jwt.InvalidTokenError:
        return None, 'Invalid token'