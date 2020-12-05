import math
from typing import List

from flask import request
from flask.json import jsonify

from app.model import Meeting, Project, User, Video
from app.utils import build_response

from ..auth import admin_required
from ..ws.entity import sid_manager
from . import admin

number_per_page = 8

@admin.route('/userManage', methods=['GET'])
@admin_required
def user_manage():
    username = request.args.get('username', None)
    mail = request.args.get('mail', None)
    mobile_num = request.args.get('mobileNum', None)
    page = int(request.args.get('page', 1))-1

    select = {}
    if username:
        select['username'] = username
    if mail:
        select['mail'] = mail
    if mobile_num:
        select['mobileNum'] = mobile_num
    
    total_page = math.ceil(User.objects(**select).count() / number_per_page)
    users:List[User] = User.objects(**select).skip(page*number_per_page).limit(number_per_page)
    user_list = []
    for user in users:
        user_list.append({
            'avatar': user.avatar,
            'userId': str(user.id),
            'username': user.username,
            'mobileNum': user.mobileNum,
            'mail': user.mail,
            'uploadNum': len(user.uploadVideo),
            'projectNum': len(user.joinProject)+len(user.hasProject),
            'alive': user.alive
        })
    data = {
        'totalPage': total_page,
        'userList': user_list
    }
    return jsonify(build_response(data=data))

@admin.route('/videoManage', methods=['GET'])
@admin_required
def video_manage():
    username = request.args.get('username', None)
    projectName = request.args.get('projectName', None)
    page = int(request.args.get('page', 1))-1

    select = {}
    data = []    
    videos:List[Video]  = []
    projects_name:List[str] = []
    if username:
        select['owner'] = username
    if projectName:
        _projects:List[Project] = Project.objects(projectName=projectName)
        for project in _projects:
            select['belongTo'] = str(project.id)
            videos += Video.objects(**select)
        for i in range(len(videos)):
            projects_name.append(projectName)
    
    else:
        videos:List[Video] = Video.objects(**select)
        # print(videos)
        for i in range(len(videos)):
            projects_name.append(Project.get_project_by_id(videos[i].belongTo).projectName)
            # print(videos[i].projectName)
  
    total_page = math.ceil(len(videos)/number_per_page)
    video_list = []
    for i, video in enumerate(videos[page*number_per_page:page*number_per_page+number_per_page]):
        owner = username if username else User.get_user_by_id(video.owner).username
        video_list.append({
            'videoId': str(video.id),
            'videoName': video.videoName,
            'videoUrl': video.url,
            'owner': owner,
            'belongTo': projects_name[i],
            'comment': video.comment,
            'alive': video.alive,
            'cover': video.cover[0]
        })

    data = {
        'totalPage': total_page,
        'videoList': video_list
    }
    return jsonify(build_response(data=data))

@admin.route('projectManage', methods=['GET'])
@admin_required
def project_manage():
    projectName = request.args.get('projectName', None)
    owner = request.args.get('owner', None)
    page = int(request.args.get('page', 1))-1

    select = {}
    if projectName:
        select['projectName'] = projectName
    if owner:
        user = User.objects(username=owner).first()
        if not user:
            return jsonify(build_response(data=[]))
        select['owner'] = str(user.id)
    
    project_list = []
    projects:List[Project] = Project.objects(**select)
    total_page = math.ceil(len(projects)/number_per_page)
    for project in projects[page*number_per_page:page*number_per_page+number_per_page]:
        owner_name = User.get_user_by_id(project.owner).username if not owner else owner
        project_list.append({
            'projectId': str(project.id),
            'projectName': project.projectName,
            'owner': owner_name,
            'memberNum': len(project.member) + 1,
            'videoNum': len(project.hasVideo),
            'meetingNum': len(project.hasMeeting),
            'alive': project.alive
        })
    
    data = {
        'totalPage': total_page,
        'projectList': project_list
    }
    return jsonify(build_response(data=data))


@admin.route('/meetingManage', methods=['GET'])
@admin_required
def meeting_manage():
    project_name = request.args.get('projectName', None)
    page = int(request.args.get('page', 1))-1

    select = {}
    if project_name:
        project = Project.objects(projectName=project_name)
        if not project:
            return jsonify(build_response(data=[]))
        select['belongTo'] = str(project.id)
    
    meetings:List[Meeting] = Meeting.objects(**select)
    total_page = math.ceil(len(meetings)/number_per_page)
    meeting_list = []
    for meeting in meetings:
        belongTo = project_name if project_name else Project.get_project_by_id(meeting.belongTo).projectName
        meeting_list.append({
            'title': meeting.title,
            'belongTo': belongTo,
            'onlineNum': 0 if str(meeting.id) not in sid_manager.meetingrooms else len(sid_manager.get_meetingRoom_by_meetingId(str(meeting.id)).member_list),
            'currentVideo': '' if str(meeting.id) not in sid_manager.meetingrooms else  sid_manager.get_meetingRoom_by_meetingId(str(meeting.id)).player.video.videoName,
            'alive': meeting.alive
        })

    data = {
        'totalPage': total_page,
        'meetingList': meeting_list
    }
    return jsonify(build_response(data=data))
