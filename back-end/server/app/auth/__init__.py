from flask import Blueprint, jsonify
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import abort
from flask_jwt_extended.utils import get_jwt_claims, user_loader
from ..model import User
from ..utils import build_response
from bson import ObjectId
import bson

# 角色权限管理装饰器, permission为所需权限
def role_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            identity = get_jwt_identity()
            # print(identity, "can do this permission ?")
            # 在此处验证角色权限, 如果无对应权限, 则抛出 403
            if not permission:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

auth = Blueprint('auth', __name__)

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        try:
            if not User.has_user(user_id):
                raise Exception()
        except Exception as e:
            return jsonify(build_response(0, "token失效, 请重新登陆"))
        else:
            return fn(*args, **kwargs)

    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        # claims = get_jwt_claims()
        user = User.get_user_by_id(user_id=user_id)
        if not user:
            return jsonify(build_response(0, "token失效, 请重新登陆"))
        elif not user.admin:
            return jsonify(build_response(0, '你不是管理员'))
        else:
            return fn(*args, **kwargs)

    return wrapper

from . import views
from . import error
