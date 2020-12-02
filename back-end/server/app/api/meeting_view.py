from time import time
from typing import List
from flask import abort, jsonify, request
from flask_jwt_extended import get_jwt_identity

from ..auth import login_required
from ..model import Meeting, Message, Project, User, Video
from ..utils import build_response, safe_objectId
from . import api

@api.route('/meeting/', methods=['POST'])
@login_required
def create_meeting():
    try:
        parms = request.json
        title = parms['title']
        belong_to = parms['belongTo']
        start_time = int(parms['startTime'])
        end_time = int(parms['endTime'])
        note = parms.get('note', '')
    except KeyError as e:
        return abort(400, {'msg': str(e)})
    
    user = User.get_user_by_id(get_jwt_identity())
    project = Project.get_project_by_id(belong_to)
    meeting = Meeting(
        title=title,
        ownerId=str(user.id),
        ownerName=user.username,
        belongTo=str(project.id),
        startTime=start_time,
        endTime=end_time,
        meetingUrl='todo',
        txMeetingId='todo',
        note=note
    )
    meeting.save()
    meeting_id = str(meeting.id)

    user.hasMeeting.append(meeting_id)
    user.save()

    project.hasMeeting.append(meeting_id)
    project.save()

    return jsonify(build_response(1, '', data={
        'meetingId': meeting_id
    }))

@api.route('/meeting/search', methods=['GET'])
@login_required
def search_meeting():
    try:
        meeting_id = request.args['meetingId']
    except KeyError as e:
        abort(400, {'msg': str(e)})
    
    meeting = Meeting.get_meeting_by_id(meeting_id=meeting_id)
    if not meeting:
        return jsonify(build_response(0, '没有此会议'))

    data = {
        'meetingId': str(meeting.id),
        'meetingName': meeting.title,
        'note': meeting.note,
        'time': meeting.startTime,
        'cover': '',
        'userName': meeting.ownerName,
        'status': bool(time()>meeting.endTime),
        'duration': meeting.endTime-meeting.startTime
    }
    return jsonify(build_response(data=data))

@api.route('/meeting/mine', methods=['GET'])
@login_required
def my_meeting():
    user_id = get_jwt_identity()
    
    meetings = Meeting.get_meeting_by_ownerId(user_id)
    meeting_list = []
    for meeting in meetings:
        meeting_list.append({
            'meetingId': str(meeting.id),
            'meetingName': meeting.title,
            'userName': meeting.ownerName,
            'duration': meeting.endTime-meeting.startTime,
            'status': (time()>meeting.endTime),
            'note': meeting.note,
            'time': meeting.startTime,
            # 'cover': '',
        })
    
    data={
        'meetingList': meeting_list
    }
    return jsonify(build_response(data=data))

@api.route('/meeting/todo', methods=['GET'])
@login_required
def meeting_todo():
    try:
        project_id = request.args['projectId']
    except Exception as e:
        project_id = None

    user = User.get_user_by_id(get_jwt_identity())
    if project_id:
        projects_id:List[str] = [project_id]
    else:
        projects_id:List[str] = user.joinProject + user.hasProject
    
    projects = [Project.get_project_by_id(project_id=project_id) for project_id in projects_id]
    meeting_list = []
    current_time = time()
    for project in projects:
        meetings = Meeting.get_meeting_by_projectId(project_id=str(project.id))
        meetings_todo:List[Meeting] = list(filter(lambda x: current_time < x.startTime, meetings))   
        for meeting in meetings_todo:
            meeting_list.append({
                'meetingId': str(meeting.id),
                'title': meeting.title,
                'userName': meeting.ownerName,
                'startTime': meeting.startTime,
                'endTime': meeting.endTime,
                'note': meeting.note,
                'projectId': str(project.id),
                'projectName': project.projectName,
                'meetingUrl': ''
            })
    
    data = {
        'meetingList': meeting_list
    }
    return jsonify(build_response(data=data))

@api.route('/meeting/history', methods=['GET'])
@login_required
def history_meeting():
    try:
        project_id = request.args['projectId']
    except Exception as e:
        project_id = None

    user = User.get_user_by_id(get_jwt_identity())
    if project_id:
        projects_id:List[str] = [project_id]
    else:
        projects_id:List[str] = user.joinProject + user.hasProject
    
    projects = [Project.get_project_by_id(project_id=project_id) for project_id in projects_id]
    data = []
    current_time = time()
    for project in projects:
        meetings = Meeting.get_meeting_by_projectId(project_id=str(project.id))
        meetings_todo:List[Meeting] = list(filter(lambda x: current_time > x.endTime, meetings))   
        for meeting in meetings_todo:
            data.append({
                'meetingId': str(meeting.id),
                'meetingName': meeting.title,
                'userId': meeting.ownerId,
                'userName': meeting.ownerName,
                'time': meeting.startTime,
                'duration': meeting.endTime-meeting.startTime,
                'note': meeting.note,
                'cover': '',
                'projectId': str(project.id),
                'projectName': project.projectName
            })

    return jsonify(build_response(data=data))