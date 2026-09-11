from functools import wraps
from flask import request, jsonify
from app.utils.auth_helper import decode_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        payload, error = decode_token(token)
        if error:
            return jsonify({'error': error}), 401

        return f(payload['user_id'], *args, **kwargs)

    return decorated