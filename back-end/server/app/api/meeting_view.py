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

