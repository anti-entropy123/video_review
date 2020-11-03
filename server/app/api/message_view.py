from flask import jsonify, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

from bson.objectid import ObjectId

from .. import db
from . import api
from ..utils import build_response
from ..model import Video, User, Project
from ..auth import login_required


@api.route('/messages/', methods=['GET'])
@login_required
def get_message_list():
    user_id = get_jwt_identity()

    messages = db.user.find_one(
        {'_id': ObjectId(user_id)},
        {'message': 1}
    )['message']
    
    data = []
    for messageId, message in enumerate(messages):
        one = {
            'messageId': messageId,
            'fromId': message['fromId'],
            'fromName': message['fromName'],
            'date': message['date'],
            'projectId': message['projectId'],
            'projectName': message['projectName'],
            'hasRead': message['hasRead'],
            'hasProcess': message['type'],
            'type': message['type']
        }
        data.append(one)
    
    data = sorted(data, key=lambda x: x['date'], reverse=True)
    return jsonify(build_response(data=data))
        
@api.route('/message/<message_id>')
@login_required
def get_message_detail(message_id):
    user_id = get_jwt_identity()
    
    user = db.user.find_one(
        {'_id': ObjectId(user_id)},
        {'message': 1}
    )
    
    message = user['message'][int(message_id)]
    data = {
        'fromId': message['fromId'],
        'fromName': message['fromName'],
        'date': message['date'],
        'projectId': message['projectId'],
        'projectName': message['projectName'],
        'type': message['type']
    }
    content = message['content']
    data.update(content)

    return jsonify(build_response(data=data))