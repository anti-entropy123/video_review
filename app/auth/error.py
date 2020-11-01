from . import auth
from flask import request, jsonify
from ..utils import build_response

@auth.app_errorhandler(404)
def page_not_found(e):
    return jsonify(build_response(0, '没有此接口'))
    
@auth.errorhandler(401)
def unauthorized(e):
    return jsonify(build_response(0, '用户名或密码错误'))

@auth.app_errorhandler(500)
def server_error(e):
    return jsonify(build_response(0, str(e)))