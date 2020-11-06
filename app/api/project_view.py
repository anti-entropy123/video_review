import time

from flask import abort, jsonify, request
from flask_jwt_extended import get_jwt_identity

from .. import db
from ..auth import login_required
from ..model import Message, Project, User, Video
from ..utils import build_response, safe_objectId
from . import api


@api.route('/project/', methods=['POST'])
@login_required
def create_project():
    try:
        project_name = request.json['projectName']
    except KeyError as e:
        abort(400, {'msg': str(e)})

    if Project.objects(projectName=project_name):
        return jsonify(build_response(0, '此项目名已被使用'))
    
    project = Project(
        projectName=project_name,
        owner=str(get_jwt_identity())
    )
    project.save()
    return jsonify(build_response())

@api.route('/project/<project_id>/inviteUser/', methods=['POST'])
@login_required
def invite_user(project_id):
    try:
        user_id = request.json['userId']
        word = request.json['word']
    except KeyError as e:
        abort(400, {'msg': str(e)})

    inviter = User.objects(id=safe_objectId(get_jwt_identity())).first()
    target = User.objects(id=safe_objectId(user_id)).first()
    # 无邀请目标
    if not target:
        return jsonify(build_response(0, "没有此用户"))

    project = Project.objects(id=safe_objectId(project_id)).first()

    new_message = Message(
        fromId=str(inviter.id),
        fromName=inviter.username,
        projectId=project_id,
        projectName=project.projectName,
        type=3,
        content={
            "word": word
        }
    )

    target.message.append(new_message)
    target.save()

    project.waitJoin.append(user_id)
    project.save()

    return jsonify(build_response())

@api.route('/project/<project_id>/join/', methods=['POST'])
@login_required
def join_project(project_id):
    try:
        message_id:str = request.json['messageId']
        is_agree = request.json['isAgree']
    except KeyError as e:
        abort(400, {'msg': str(e)})

    user = User.objects(id=safe_objectId(get_jwt_identity())).first()
    project = Project.objects(id=safe_objectId(project_id)).first()
    origin_message = Message.objects(id=message_id).first()
    
    # 邀请者 用户id
    inviter_id = origin_message.fromId
    inviter = User.objects(id=safe_objectId(inviter_id))

    origin_message.hasProcess = True
    origin_message.save()

    project.waitJoin.remove(str(user.id))
    
    if is_agree:
        # 同意邀请
        project.objects.append(str(user.id))
    project.save()
    
    # 给邀请者发送提醒
    new_message = Message(
        fromId=str(user.id),
        fromName=user.username,
        projectId=project_id,
        projectName=project.projectName,
        type=4,
        content={
            'processResult': is_agree
        }
    )
    inviter.message.append(new_message)
    inviter.save()

    return jsonify(build_response())

@api.route('/project/userAndVideo', methods=['GET'])
@login_required
def get_project_data():
    try:
        project_name = request.args['projectName']
    except KeyError as e:
        abort(400, {'msg': 'projectName'})
    
    video_list = []
    user_list = []

    # 找到此项目
    project = Project.objects(projectName=project_name).first()
    print(project)
    # 项目主
    owner = User.objects(id=safe_objectId(project.owner)).first()
    user_list.append({
        'userId': str(owner.id),
        'userName': owner.username,
        'title': '负责人',
        'avatar': owner['avatar']
    })

    # 普通成员
    for user in project.member:
        userId = user['userId']
        title = user['title']
        member = User.objects(id=safe_objectId(userId)).first()
        member.title = title
        member.userId = userId
        user_list.append({
            'userId': str(member.id),
            'userName': member.username,
            'title': title,
            'avatar': member['avatar']
        })

    # 视频列表
    for video_id in project.hasVideo:
        video = Video.objects(id=safe_objectId(video_id)).first()
        video_list.append({
            'videoName': video.videoName,
            'cover': video.cover,
            'videoId': video_id
        })
    
    data = {'videoList': video_list, 'userList': user_list}
    return jsonify(build_response(1, '', data))
