from typing import List

from flask import abort, jsonify, request
from flask_jwt_extended import get_jwt_identity

from ..auth import login_required
from ..model import Message, User
from ..utils import build_response, txCosUtil
from . import api


@api.route('/user/<target_id>', methods=['GET'])
@login_required
def get_user_info(target_id:str):
    user = User.get_user_by_id(target_id)

    if not user:
        return jsonify(build_response(0, "无此用户"))
    # print(dir(user))
    messages: List[Message] = user.message
    messageToRead = sum([not message.hasRead for message in messages])
    data = {
        'username': user.username,
        'userId': str(user.id),
        'avatar': user.avatar,
        'mobileNum': user.mobileNum,
        'company': user.company,
        'messageToRead': messageToRead
    }
    return jsonify(build_response(data=data))

@api.route('/userInfo/', methods=['POST'])
@login_required
def update_user_info():
    user_id = get_jwt_identity()
    params = request.json
    try:
        username = params['username']
        avatar = params['avatar']
        mobile = params['mobileNum']
        company = params['company']
    except KeyError as e:
        abort(400, {'msg': str(e)})
    
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
    
    user_id = get_jwt_identity()
    # print(user_id)
    user_list:List[User] = User.objects(alive=True)
    data = []
    for user in user_list:
        if (str(user.id) != user_id) and (
            key in user['username'] or
            key in user['mail'] or
            key in user['mobileNum']
        ):
           data.append({
               'userId': str(user.id),
               'username': user.username,
               'avatar': user.avatar,
               'mail': user.mail,
               'mobileNum': user.mobileNum
           })
    
    return jsonify(build_response(1, '', data))

@api.route('/uploadImg/', methods=['POST'])
@login_required
def upload_avatar():
    try:
        image = request.files['image']
    except KeyError as e:
        abort(400, {'msg': str(e)})
    
    user_id = get_jwt_identity()

    url = txCosUtil.upload_image(user_id=user_id, f=image)
    # print(url)
    return jsonify(build_response(data={
        'url': url
    }))

@api.route('/userAvatar', methods=['GET'])
def get_user_avatar():
    try:
        mobileNum = request.args['mobileNum']
    except KeyError as e:
        abort(400, {'msg': str(e)})
    
    user:User = User.objects(mobileNum=mobileNum).first()
    
    avatar = None
    if user:
        avatar = user.avatar
    else:
        avatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
    
    data = {
        'avatarUrl': avatar
    }
    return jsonify(build_response(1, '', data))