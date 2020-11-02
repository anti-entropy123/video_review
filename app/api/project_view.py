import time

from bson.objectid import ObjectId
from flask import abort, jsonify, request
from flask_jwt_extended import get_jwt_identity

from .. import client
from ..model import Project, User
from ..utils import build_response
from . import api
from ..auth import login_required

db = client.db

@api.route('/project/', methods=['POST'])
@login_required
def create_project():
    try:
        project_name = request.json['projectName']
    except KeyError as e:
        abort(400, {'msg': str(e)})

    if Project.has_project_name(project_name):
        return jsonify(build_response(0, '此项目名已被使用'))
    
    Project.create_project(project_name, get_jwt_identity())
    return jsonify(build_response())

@api.route('/project/<project_id>/inviteUser/', methods=['POST'])
@login_required
def invite_user(project_id):
    try:
        user_id = request.json['userId']
        word = request.json['word']
    except KeyError as e:
        abort(400, {'msg': str(e)})

    # 无邀请目标
    if not User.has_user(user_id):
        return jsonify(build_response(0, "没有此用户"))
        
    from_id = get_jwt_identity()
    from_name = User.find_username_by_userId(from_id)
    project_name = Project.find_name_by_projectId(project_id)
    #message_num = target_user['messageNum']
    new_message = {
        # "messageId": message_num,
        "fromId": from_id,
        "fromName": from_name,
        "date": time.time(),
        'projectId': project_id,
        'projectName': project_name,
        'hasRead': 0,
        'hasProcess': 0,
        'type': 3,
        "content": {
            "word": word
        }
    }
    User.send_message_to_user(user_id, new_message)
    db.project.update(
        {'_id': ObjectId(project_id)},
        {'$addToSet':
            {"waitJoin": user_id}}
    )
    return jsonify(build_response())

@api.route('/project/<project_id>/join/', methods=['POST'])
@login_required
def join_project(project_id):
    try:
        message_id:str = request.json['messageId']
        is_agree = request.json['isAgree']
    except KeyError as e:
        abort(400, {'msg': str(e)})

    user_id = get_jwt_identity()
    username = User.find_username_by_userId(user_id)
    project_name = Project.find_name_by_projectId(project_id)
    
    # 邀请者 用户id
    inviter_id = User.find_message_by_id(user_id, message_id)['fromId']
    
    # 标为已处理
    User.set_message_process(user_id, message_id)
    Project.process_invite(user_id, message_id, is_agree)
    
    # 给邀请者发送提醒
    new_message = {
        'fromId': user_id,
        'fromName': username,
        'date': time.time(),
        'projectId': project_id,
        'projectName': project_name,
        'hasRead': 0,
        'hasProcess': 1,
        'type': 4,
        'content': {
            'processResult': is_agree
        }
    }
    User.send_message_to_user(inviter_id, new_message)
    return jsonify(build_response())

@api.route('/project/userAndVideo', methods=['GET'])
@login_required
def get_project_data():
    try:
        project_name = request.args['projectName']
    except KeyError as e:
        abort(400, str(e))
    
    video_list = []
    user_list = []

    # 找到此项目
    project = db.project.find_one(
        {'projectName': project_name},
        {'owner': 1, 'member': 1, 'waitJoin': 1, 'hasVideo': 1}
    )
    # 用户文档中需要的数据
    selected = {'username': 1, 'avatar': 1}
    # 项目主
    owner = db.user.find_one(
        {'_id': ObjectId(project['owner'])},
        selected
    )
    owner['title'] = '负责人'
    owner['userId'] = str(owner.pop('_id'))
    user_list.append(owner)
    # 普通成员
    for user in project['member']:
        userId = user['userId']
        title = user['title']
        member = db.user.find_one(
            {'_id': ObjectId(userId)},
            selected
        )
        member['title'] = title
        member['userId'] = str(member.pop('_id'))
        user_list.append(member)
    # 视频列表
    selected =  {'cover': 1, 'videoName': 1}
    for video_id in project['hasVideo']:
        video = db.video.find_one(
            {'_id': ObjectId(video_id)},
            selected
        )
        video['videoId'] = str(video.pop('_id'))
        video_list.append(video)
    
    data = {'videoList': video_list, 'userList': user_list}
    return jsonify(build_response(1, '', data))
        
