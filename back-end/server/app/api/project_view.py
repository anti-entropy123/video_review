import time
from typing import List

from flask import abort, jsonify, request
from flask_jwt_extended import get_jwt_identity
from flask_mongoengine import json

from ..auth import login_required
from ..model import Meeting, Message, Project, ProjectMember, User, Video
from ..utils import build_response, safe_objectId
from . import api


@api.route('/project/', methods=['POST'])
@login_required
def create_project():
    try:
        project_name = request.json['projectName']
    except KeyError as e:
        abort(400, {'msg': str(e)})

    user_id = get_jwt_identity()
    user = User.get_user_by_id(user_id=user_id)
    project = Project(
        projectName=project_name,
        owner=user_id
    )
    project.save()

    user.hasProject.append(str(project.id))
    user.save()
    return jsonify(build_response())

@api.route('/project/<project_id>/inviteUser/', methods=['POST'])
@login_required
def invite_user(project_id):
    try:
        user_id:str = request.json['userId']
        word = request.json['word']
    except KeyError as e:
        abort(400, {'msg': str(e)})

    inviter = User.get_user_by_id(get_jwt_identity())
    target = User.get_user_by_id(user_id)
    # 无邀请目标
    if not target:
        return jsonify(build_response(0, "没有此用户"))

    project = Project.get_project_by_id(project_id)
    # 检查目标用户是否已经在项目中
    if target in project:
        return jsonify(build_response(0, '此用户已经在项目中'))

    new_message = Message(
        fromId=str(inviter.id),
        fromName=inviter.username,
        projectId=project_id,
        projectName=project.projectName,
        type=3,    
        date=time.time()
    )
    new_message.fill_content(word=word)
    target.receive_message(new_message)
    project.wait_to_user_join(user_id=user_id)

    return jsonify(build_response())

@api.route('/project/<project_id>/join/', methods=['POST'])
@login_required
def join_project(project_id):
    try:
        message_id:int = int(request.json['messageId'])
        is_agree = request.json['isAgree']
    except KeyError as e:
        abort(400, {'msg': str(e)})
    except ValueError as e:
        abort(400, {'msg': '无效的messageId'})

    user:User = User.get_user_by_id(get_jwt_identity())
    project:Project = Project.get_project_by_id(project_id)
    if not project:
        return jsonify(build_response(0, '没有此项目'))
        
    origin_message:Message = user.get_message_by_id(message_id)
    
    # 邀请者 用户id
    inviter_id = origin_message.fromId
    inviter = User.get_user_by_id(inviter_id)
    try:
        project.confirm_to_join(user=user, is_agree=is_agree)
    except ValueError as e:
        return jsonify(build_response(0, '你没有被邀请加入此项目'))

    # 已处理此消息
    user.process_message(message_id=message_id)
    # 给邀请者发送提醒
    new_message = Message(
        fromId=str(user.id),
        fromName=user.username,
        projectId=project_id,
        projectName=project.projectName,
        type=4,
        date=time.time()
    )
    new_message.fill_content(process_result=is_agree)
    inviter.receive_message(new_message)

    return jsonify(build_response())

@api.route('/project/<project_id>/userAndVideo', methods=['GET'])
@login_required
def get_project_data(project_id):
    video_list = []
    user_list = []

    # 找到此项目
    project = Project.get_project_by_id(project_id)
    if not project:
        return jsonify(build_response(0, '没有此项目'))
    user = User.get_user_by_id(get_jwt_identity())
    if user not in project:
        return jsonify(build_response(0, '你无法查看此项目'))

    # 项目主
    owner = User.get_user_by_id(project.owner)
    user_list.append({
        'userId': str(owner.id),
        'userName': owner.username,
        'title': '负责人',
        'avatar': owner['avatar']
    })

    # 普通成员
    for member in project.member:
        userId = member.userId
        title = member.title
        member = User.get_user_by_id(userId)
        member.title = title
        member.userId = userId
        user_list.append({
            'userId': userId,
            'userName': member.username,
            'title': title,
            'avatar': member['avatar']
        })

    # 视频列表
    for video_id in project.hasVideo:
        video = Video.get_video_by_id(video_id)
        video_list.append({
            'videoName': video.videoName,
            'coverList': video.cover,
            'cover': video.cover[0],
            'videoId': video_id,
            'hasReview': video.hasReview,
            'createDate': video.createDate,
            'duration': video.duration
        })
    
    data = {'videoList': video_list, 'userList': user_list}
    return jsonify(build_response(1, '', data))

@api.route('/projects', methods=['GET'])
@login_required
def get_project_list():
    user_id = get_jwt_identity()
    user = User.get_user_by_id(user_id)
    projects = user.hasProject + user.joinProject

    data = []

    for project_id in projects:
        project = Project.get_project_by_id(project_id)
        if project:
            data.append({
                "projectId": project_id,
                "projectName": project.projectName
            })         
    
    return jsonify(build_response(data=data))

@api.route('/project/<project_id>/removeUser', methods=['DELETE'])
@login_required
def remove_user_from_project(project_id:str):
    try:
        userId = request.args['userId']
    except KeyError as e:
        abort(400, {'msg': str(e)})
    
    user = User.get_user_by_id(get_jwt_identity())
    project = Project.get_project_by_id(project_id=project_id)
    target = User.get_user_by_id(userId)
    
    if not project:
        return jsonify(build_response(0, '无此项目'))
    
    if not target:
        return jsonify(build_response(0, '无此用户'))

    if not str(user.id) == project.owner:
        return jsonify(build_response(0, '你没有此权限'))
    
    # print(str(target.id), project.member_id_list(), str(user.id) in project.member_id_list())
    if not target in project:
        return jsonify(build_response(0, "对方不是此项目的成员"))

    project.remove_member(target, False, False)

    message = Message(
        fromId=str(user.id),
        fromName=user.username,
        projectId=str(project.id),
        projectName=project.projectName,
        type=5,
        date=time.time()
    )
    message.fill_content()
    target.receive_message(message)
    return jsonify(build_response())

@api.route('/project/<project_id>/getMeeting')
@login_required
def get_meeting(project_id):
    project = Project.get_project_by_id(project_id=project_id)
    user = User.get_user_by_id(get_jwt_identity())

    if not project:
        return jsonify(build_response(0, '无此项目'))

    if user not in project:
        return jsonify(build_response(0, '你不在此项目中'))

    meetings = Meeting.get_meeting_by_projectId(project_id=project_id)
    data = []
    for meeting in meetings:
        data.append({
            'meetingId': str(meeting.id),
            'title': meeting.title,
            'ownerName': meeting.ownerName,
            'ownerId': meeting.ownerId,
            'startTime': meeting.startTime,
            'endTime': meeting.endTime,
            'note': meeting.note,
            'meetingUrl': ''
        })
    return jsonify(build_response(1, '', data=data))

@api.route('/project/<project_id>/leave', methods=['POST'])
@login_required
def leave_project(project_id):
    user_id = get_jwt_identity()
    user = User.get_user_by_id(user_id=user_id)
    project = Project.get_project_by_id(project_id=project_id)
    if not project:
        return jsonify(build_response(0, '没有此项目'))
    
    # if user not in project:
    #     return jsonify(build_response(0, "你不是项目成员"))
    
    # 用户是项目的建立者, 该项目解散
    if user_id == project.owner:
        project.dissolution()
    # 用户是项目的成员, 该项目中删去此用户
    else:
        project.remove_member(user, True, False)
    
    return jsonify(build_response())

@api.route('/project/<project_id>/removeVideo', methods=['DELETE'])
@login_required
def remove_video(project_id):
    try:
        video_id = request.args['videoId']
    except KeyError as e:
        abort(400, {'msg': str(e)})
    
    project = Project.get_project_by_id(project_id=project_id)
    if not project:
        return jsonify(0, '没有此项目')

    project.remove_video(video_id=video_id)
    return jsonify(build_response())
