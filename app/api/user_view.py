from flask import jsonify, request, abort
from flask_jwt_extended import get_jwt_identity

from bson.objectid import ObjectId

from .. import client
from . import api
from ..utils import build_response
from ..auth import login_required

db = client.db
# 设置端点url和被允许的method
@api.route('/test/', methods=['GET'])
# 访问此接口需携带有效的token
@login_required
def api_test():
    # 使用jsonify的好处是, flask会自动将content-type字段设置为 text/json
    return jsonify({'result': 1, 'message': 'its ok', 'user_id': get_jwt_identity()})

@api.route('/user/<target_id>', methods=['GET'])
@login_required
def get_user_info(target_id:str):
    user = db.user.find_one(
        {'_id': ObjectId(target_id)}, 
        {'username': 1, 'avatar': 1, 'mobileNum': 1, 'company': 1})
    
    if not user:
        return jsonify(build_response(0, "无此用户"))
    
    parm_list = ['username', 'avatar', 'mobileNum', 'company']
    data = {'userId': target_id}
    for parm in parm_list:
        data[parm] = user[parm]

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
    
    db.user.update(
        {'_id': ObjectId(user_id)},
        {'$set': {'username': username, 'avatar': avatar, 'mobileNum': mobile, 'company': company}}
    )
    return jsonify(build_response())

@api.route('/userlist/', methods=['GET'])
@login_required
def get_userlist():
    key = request.args['data']
    
    user_list = db.user.find(
        {},
        {'_id':1, 'username':1, 'avatar':1, 'mail':1, 'mobileNum':1}
    )
    data = []
    for user in user_list:
        if (key in user['username'] or
            key in user['mail'] or
            key in user['mobileNum']):
           user['userId'] = str(user.pop('_id'))
           data.append(user)
    
    return jsonify(build_response(1, '', data))