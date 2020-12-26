from flask import abort, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_refresh_token_required)
from werkzeug.security import check_password_hash, generate_password_hash

from ..model import User
from ..utils import checkCodeManager, build_response, wx_util
from . import auth, openId_required

@auth.route('/checkCode', methods=['GET'])
def get_checkcode():
    mobile = request.args.get('mobileNum', 0)
    # operation = request.args.get('operation', 'register')

    if not mobile:
        return jsonify(build_response(0, "缺少参数: mobileNum"))

    result, message = checkCodeManager.send_CheckCode(mobile)
    return jsonify(build_response(result, message))

@auth.route('/wx/checkCode', methods=['GET'])
def wx_get_checkcode():
    try:
        mobileNum = request.args['mobileNum']
    # operation = request.args.get('operation', 'register')
    except KeyError as e:
        abort(400, {'msg': str(e)})
    
    result, message = checkCodeManager.send_CheckCode(mobileNum=mobileNum)
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
    if User.objects(username=username, alive=True).first():
        return jsonify(build_response(0, "此用户名已被使用"))
    
    if User.objects(mobileNum=mobileNum, alive=True).first():
        return jsonify(build_response(0, "此手机号已经被使用"))

    # 向数据库中增加用户
    user = User(
        username  = username, 
        password  = generate_password_hash(password), 
        mobileNum = mobileNum,
        # avatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
        )
    user.save()

    return jsonify(build_response())

@auth.route('/login/', methods=['POST'])
def login():
    try:
        mobileNum = request.json['mobileNum']
        password = request.json.get('password', None)
        checkcode = request.json.get('checkcode', None)
    except KeyError as e:
        abort(400, {'msg': str(e)})

    user = User.get_user_by_mobileNum(mobileNum=mobileNum)
    if not user:
        # 没有此用户
        abort(401)
    
    result, message = 1, ''
    # 使用密码登录
    if password:
        if user.verify_password(password=password):
            pass
        else:
            abort(401)  
    # 使用验证码登录
    elif checkcode:
        result, message = checkCodeManager.verify_code(mobileNum=mobileNum, code=checkcode)
    else:
        return jsonify(build_response(0, "无效的登录方式"))
        
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

    user = User.objects(mobileNum=mobileNum, alive=True).first()
    if not user: 
        return jsonify(build_response(0, "用户不存在"))
    # user = User.get_user_by_id(get_jwt_identity())
    # if user.mobileNum != mobileNum:
    #     return jsonify(build_response(0, "请输入本人手机号"))

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
    
@auth.route('/wx/login/', methods=['POST'])
def wx_login():
    try:
        code = request.json['code']
    except KeyError as e:
        abort(400, {'msg': str(e)})
    
    open_id = wx_util.get_openid_by_code(code=code)
    if not open_id:
        return jsonify(build_response(0, '无效的code'))
    user = User.get_user_by_openId(open_id=open_id)
    data = {
        'openId': open_id
    }
    if not user:
        data['firstTime'] = True
        data['tempToken'] = create_access_token(identity=open_id)
    else:
        data['firstTime'] = False
        data['userId'] = str(user.id)
        data['token'] = create_access_token(identity=str(user.id))
        data['refreshToken'] = create_refresh_token(identity=str(user.id))
    
    return jsonify(build_response(1, '', **data))

@auth.route('/wx/bindMobileNum/', methods=['POST'])
@openId_required
def bind_mobileNum():
    try:
        checkcode = request.json['checkCode']
        mobileNum = request.json['mobileNum']
    except KeyError as e:
        abort(400, {'msg': str(e)})
    open_id = get_jwt_identity()
    # 校验验证码
    result, message = checkCodeManager.verify_code(mobileNum, checkcode)
    if not result: 
        return jsonify({'result': result, 'message': message})
    
    user = User.get_user_by_mobileNum(mobileNum=mobileNum)
    if not user:
        needUserInfo = True
        user_info = wx_util.get_wx_user_info(openId=open_id)
        user = User(
            username  = user_info['nickname'], 
            mobileNum = mobileNum,
            openId    = open_id,
            avatar    = user_info['headimgurl'],
        )
        user.save()
    else:
        needUserInfo = False
        user.openId = open_id
        user.save()
    
    return jsonify(build_response(
        token=create_access_token(identity=str(user.id)),
        refreshToken=create_refresh_token(identity=str(user.id)),
        userId=str(user.id),
        needUserInfo=needUserInfo
    ))