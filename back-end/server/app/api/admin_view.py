from app.utils import build_response
from typing import List

from flask.json import jsonify
from app.model import Meeting, Project, User, Video
from . import admin
from ..auth import admin_required
from flask import request
from ..ws.entity import meetingroom_manager

@admin.route('/userManager', methods=['GET'])
@admin_required
def user_manage():
    username = request.args.get('username', None)
    mail = request.args.get('mail', None)
    mobile_num = request.args.get('mobileNum', None)
    
    select = {}
    if username:
        select['username'] = username
    if mail:
        select['mail'] = mail
    if mobile_num:
        select['mobileNum'] = mobile_num
    
    users:List[User] = User.objects(**select)
    data = []
    for user in users:
        data.append({
            'avatar': user.avatar,
            'username': user.username,
            'mobileNum': user.mobileNum,
            'mail': user.mail,
            'uploadNum': len(user.uploadVideo),
            'projectNum': len(user.joinProject)+len(user.hasProject)
        })

    return jsonify(build_response(data=data))

@admin.route('/videoManage', methods=['GET'])
@admin_required
def video_manage():
    username = request.args.get('username', None)
    projectName = request.args.get('projectName', None)
    
    select = {}
    data = []
    videos:List[Video]  = []
    projects:List[Project] = []
    if username:
        select['owner'] = username
    if projectName:
        _projects:List[Project] = Project.objects(projectName=projectName)
        for project in _projects:
            select['belongTo'] = str(project.id)
            videos += Video.objects(**select)
        
        for i in range(len(videos)):
            videos[i].projectName = projectName
    
    else:
        videos = Video.objects(**select)
        for i in range(len(videos)):
            videos[i].projectName = Project.get_project_by_id(videos[i].belongTo).projectName
  
    for project, video in zip(projects, videos):
        data.append({
            'videoName': video.videoName,
            'videoUrl': video.url,
            'owner': video.owner,
            'belongTo': video.projectName,
            'comment': video.comment
        })

    return jsonify(build_response(data=data))

@admin.route('/projectManage', methods=['GET'])
@admin_required
def project_manage():
    projectName = request.args.get('projectName', None)
    owner = request.args.get('owner', None)

    select = {}
    if projectName:
        select['projectName'] = projectName
    if owner:
        user = User.objects(username=owner).first()
        if not user:
            return jsonify(build_response(data=[]))
        select['owner'] = str(user.id)
    
    data = []
    projects:List[Project] = Project.objects(**select)
    for project in projects:
        owner_name = User.get_user_by_id(project.owner).username if not owner else owner
        data.append({
            'projectName': project.projectName,
            'owner': owner_name,
            'memberNum': len(project.member) + 1,
            'videoNum': len(project.hasVideo),
            'meetingNum': len(project.hasMeeting)
        })
    
    return jsonify(build_response(data=data))
    
@admin.route('/meetingManage', methods=['GET'])
@admin_required
def meeting_manage():
    project_name = request.args.get('projectName', None)
    
    select = {}
    if project_name:
        project = Project.objects(projectName=project_name)
        if not project:
            return jsonify(build_response(data=[]))
        select['belongTo'] = str(project.id)
    
    meetings:List[Meeting] = Meeting.objects(**select)
    data = []
    for meeting in meetings:
        belongTo = project_name if project_name else Project.get_project_by_id(meeting.belongTo).projectName
        data.append({
            'title': meeting.title,
            'belongTo': belongTo,
            'onlineNum': 0 if str(meeting.id) not in meetingroom_manager else len(meetingroom_manager[str(meeting.id)].member_list),
            'currentVideo': '' if str(meeting.id) not in meetingroom_manager else meetingroom_manager[str(meeting.id)].player.video.videoName
        })

    return jsonify(build_response(data=data))