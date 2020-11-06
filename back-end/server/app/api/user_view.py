from flask import jsonify, request, abort
from flask_jwt_extended import get_jwt_identity

from .. import db
from . import api
from ..utils import build_response, safe_objectId
from ..auth import login_required
from ..model import User

@api.route('/user/<target_id>', methods=['GET'])
@login_required
def get_user_info(target_id:str):
    user = User.get_user_by_id(target_id)

    if not user:
        return jsonify(build_response(0, "无此用户"))
    print(dir(user))
    parm_list = ['username', 'avatar', 'mobileNum', 'company']
    data = {'userId': target_id}
    for parm in parm_list:
        data[parm] = getattr(user, parm)

    return jsonify(build_response(data=data))

@api.route('/userInfo/', methods=['POST'])
@login_required
def update_user_info():
    user_id = get_jwt_identity()
    params = request.json
    try:
        username = params['username']
        avatar = params['avatar']
        mobile = params['mobile']
        company = params['company']
    except KeyError as e:
        abort(400)
    
    user = User.get_user_by_id(user_id=user_id)
    user.username = username
    user.avatar = avatar
    user.mobileNum = mobile
    user.company = company
    user.save()
    
    return jsonify(build_response())

@api.route('/userlist/', methods=['GET'])
@login_required
def get_userlist():
    key = request.args['data']
    
    user_list = User.objects()
    data = []
    for user in user_list:
        if (key in user['username'] or
            key in user['mail'] or
            key in user['mobileNum']):

           data.append({
               'userId': str(user.id),
               'username': user.username,
               'avatar': user.avatar,
               'mail': user.mail,
               'mobileNum': user.mobileNum
           })
    
    return jsonify(build_response(1, '', data))