from flask import jsonify, request

from ..utils import build_response
from . import api


@api.errorhandler(400)
def parm_error(e):
    return jsonify(build_response(0, "请求参数错误: " + str(e)))

@api.app_errorhandler(403)
def unauthorized(e):
    return jsonify(build_response(0, "没有此操作权限"))
