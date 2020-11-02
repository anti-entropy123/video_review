from flask import abort, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_refresh_token_required)
from werkzeug.security import check_password_hash, generate_password_hash

from .. import client
from ..utils import CheckCode, build_response
from . import auth

db = client.db

@auth.route('/checkCode')
def get_checkcode():
    mobile = request.json.get('mobileNum', 0)
    if not mobile:
        return jsonify(build_response(0, "缺少参数: mobileNum"))

    CheckCode.sendSMS(mobile)
    return jsonify(build_response())

@auth.route('/register/', methods=['POST'])
def register():
    data = request.json
    try:
        username = data['username']
        password = data['password']
        mail = data['mail']
        mobileNum = data['mobileNum']
        checkcode = data['checkCode']
    
    # 参数检查
    except KeyError as e:
        return jsonify(build_response(0, "缺少参数: " + str(e)))
    
    # 校验验证码
    # result, message = CheckCode.verify_code(mobileNum, checkcode)
    # if not result: return jsonify({'result': result, 'message': message})

    # 查询数据库中是否有此用户名
    if db.user.find(
        {'username': username},
        {'_id': 1}).count():
        return jsonify(build_response(0, "此用户名已被使用"))

    # 向数据库中增加用户
    try:
        db.user.insert_one({
            'username': username,
            'password': generate_password_hash(password),
            'mobileNum': mobileNum,
            'mail': '',
            'avatar': '',
            'company': '',
            'hasProject': [],
            'joinProject': [],
            'uploadVideo': [],
            'message': []
        })
    except RuntimeError as e:
        return jsonify(build_response(0, str(e)))

    return jsonify(build_response())

@auth.route('/login/', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not (username and password):
        # 参数不全
        abort(401)

    user = db.user.find_one(
        {'username': username},
        {'password': 1})
    if not user:
        # 没有此用户
        abort(401)
       
    if not check_password_hash(user['password'], password): 
        # 错误的密码
        abort(401)

    access_token = create_access_token(identity=str(user['_id']))
    refresh_token = create_refresh_token(identity=str(user['_id']))
    return build_response(1, '', token=access_token, refreshToken=refresh_token, userId=str(user['_id']))

@auth.route('/refresh/', methods=['POST'])
# 访问此接口需要携带有效的refresh_token
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    return jsonify(access_token=create_access_token(identity=current_user)), 200


