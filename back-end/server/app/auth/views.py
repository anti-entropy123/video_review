from flask import abort, jsonify, request
from flask import json
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_refresh_token_required)
from werkzeug.security import check_password_hash, generate_password_hash

from ..model import User
from ..utils import checkCodeManager, build_response
from . import auth

@auth.route('/checkCode', methods=['GET'])
def get_checkcode():
    mobile = request.args.get('mobileNum', 0)
    # operation = request.args.get('operation', 'register')

    if not mobile:
        return jsonify(build_response(0, "缺少参数: mobileNum"))

    result, message = checkCodeManager.send_CheckCode(mobile)
    return jsonify(build_response(result, message))

# @auth.route('/user/checkCode', methods=['GET'])
# def get_reset_pass_code():
#     username = request.args.get('username', 0)
#     if not username:
#         return abort(400, {'msg': 'username'})
    
#     user = User.objects(username=username).first()
#     if not user:
#         return jsonify(build_response(0, "用户不存在"))
    
#     mobileNum = user.mobileNum
#     result, message = checkCodeManager.send_CheckCode(mobileNum) 
#     return jsonify(build_response(result, message, data={'mobileNum': mobileNum[:3]+'*'*4+mobileNum[-4:]}))

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
    
    if User.objects(mobileNum=mobileNum).first():
        return jsonify(build_response(0, "此手机号已经被使用"))

    # 向数据库中增加用户
    user = User(
        username  = username, 
        password  = generate_password_hash(password), 
        mobileNum = mobileNum)
    user.save()

    return jsonify(build_response())

@auth.route('/login/', methods=['POST'])
def login():
    try:
        mobileNum = request.json['mobileNum']
        password = request.json.get('password', None)
        checkcode = request.json.get('checkcode', None)
        if not password and not checkcode:
            raise KeyError('password or checkcode')
    except KeyError as e:
        abort(400, {'msg': str(e)})

    user = User.get_user_by_mobileNum(mobileNum=mobileNum)
    if not user:
        # 没有此用户
        abort(401)

    result, message = 1, ''
    if password and not check_password_hash(user.password, password): 
        # 错误的密码
        abort(401)
    elif checkcode:
        result, message = checkCodeManager.verify_code(mobileNum=mobileNum, code=checkcode)

    if result:
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        return jsonify(build_response(1, '', token=access_token, refreshToken=refresh_token, userId=str(user.id)))
    else:
        return jsonify(build_response(result=result, message=message))

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
        mobileNum = args['mobileNum']
        password = args['password']
        checkcode = args['checkcode']
    except KeyError as e:
        abort(400, {'msg': str(e)})

    user = User.objects(mobileNum=mobileNum).first()
    if not user: 
        return jsonify(build_response(0, "用户不存在"))
    
    result, message = checkCodeManager.verify_code(user.mobileNum, checkcode)
    if not result:
        return jsonify(build_response(result, message))

    user.password = generate_password_hash(password)
    user.save()
    return jsonify(build_response())
    
@auth.route('/admin/login/', methods=['POST'])
def admin_login():
    args = request.json
    try:
        mobile_num = args['mobileNum']
        password = args['password']
    except KeyError as e:
        abort(400, {'msg': str(e)})
    
    user = User.get_user_by_mobileNum(mobileNum=mobile_num)
    if not user:
        # 没有此用户
        abort(401)

    if password and not check_password_hash(user.password, password): 
        # 错误的密码
        abort(401)

    if not user.admin:
        return jsonify(build_response(0, '你不是管理员'))

    access_token = create_access_token(
        identity=str(user.id), 
        # user_claims={'admin': 1}
        )
    refresh_token = create_refresh_token(
        identity=str(user.id), 
        # user_claims={'admin': 1}
        )
    return jsonify(build_response(1, '', token=access_token, refreshToken=refresh_token, userId=str(user.id), username=user.username))
    