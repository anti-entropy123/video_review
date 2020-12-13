from flask import jsonify, request

from ..utils import build_response
from . import api


@api.app_errorhandler(400)
def parm_error(e):
    # print(e.description)
    if 'msg' in e.description:
        message = "缺少参数: " + e.description['msg']
    elif 'type_error' in e.description:
        message = "错误的id参数"
    else:
        message = str(e)
    return jsonify(build_response(0, message=message))

@api.app_errorhandler(403)
def unauthorized(e):
    return jsonify(build_response(0, "没有此操作权限"))

@api.app_errorhandler(500)
def server_error(e):
    return jsonify(build_response(0, str(e)))