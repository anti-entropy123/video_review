from flask import abort, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_refresh_token_required)
from werkzeug.security import check_password_hash, generate_password_hash

import mongoengine as me

from ..model import User
from .. import db
from ..utils import checkCodeManager, build_response
from . import auth

@auth.route('/checkCode', methods=['GET'])
def get_checkcode():
    mobile = request.args.get('mobileNum', 0)
    if not mobile:
        return jsonify(build_response(0, "缺少参数: mobileNum"))

    result, message = checkCodeManager.send_CheckCode(mobile)
    return jsonify(build_response(result, message))

@auth.route('/user/checkCode', methods=['GET'])
def get_reset_pass_code():
    username = request.args.get('username', 0)
    if not username:
        return abort(400, {'msg': 'username'})
    
    user = User.objects(username=username).first()
    if not user:
        return jsonify(build_response(0, "用户不存在"))
    
    mobileNum = user.mobileNum
    result, message = checkCodeManager.send_CheckCode(mobileNum) 
    return jsonify(build_response(result, message, data={'mobileNum': mobileNum[:3]+'*'*4+mobileNum[-4:]}))

@auth.route('/register/', methods=['POST'])
def register():
    data = request.json
    try:
        username  = data['username']
        password  = data['password']
        mobileNum = data['mobileNum']
        checkcode = data['checkCode']
    # 参数检查
    except KeyError as e:
        return jsonify(build_response(0, "缺少参数: " + str(e)))
    
    # 校验验证码
    result, message = checkCodeManager.verify_code(mobileNum, checkcode)
    if not result: return jsonify({'result': result, 'message': message})

    # 查询数据库中是否有此用户名
    if User.objects(username=username).first():
        return jsonify(build_response(0, "此用户名已被使用"))
    
    # 向数据库中增加用户
    user = User(
        username  = username, 
        password  = generate_password_hash(password), 
        mobileNum = mobileNum)
    user.save()

    return jsonify(build_response())

@auth.route('/login/', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not (username and password):
        # 参数不全
        abort(401)

    user = User.objects(username=username).first()
    if not user:
        # 没有此用户
        abort(401)
       
    if not check_password_hash(user.password, password): 
        # 错误的密码
        abort(401)

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return build_response(1, '', token=access_token, refreshToken=refresh_token, userId=str(user.id))

# 访问此接口需要携带有效的refresh_token
@auth.route('/refresh/', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    return jsonify(access_token=create_access_token(identity=current_user)), 200

@auth.route('/user/resetPassword/', methods=['POST'])
def reset_password():
    args = request.json
    try:
        username = args['username']
        password = args['password']
        checkcode = args['checkcode']
    except KeyError as e:
        abort(400, {'msg': str(e)})

    user = User.objects(username=username).first()
    if not user: 
        return jsonify(build_response(0, "用户不存在"))
    
    result, message = checkCodeManager.verify_code(user.mobileNum, checkcode)
    if not result:
        return jsonify(build_response(result, message))

    user.password = generate_password_hash(password)
    user.save()
    return jsonify(build_response())
    
    