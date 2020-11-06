from collections import UserDict
from flask import jsonify, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_mongoengine import json

from .. import db
from . import api
from ..utils import build_response, safe_objectId
from ..model import Message, Video, User, Project
from ..auth import login_required


@api.route('/messages/', methods=['GET'])
@login_required
def get_message_list():
    user_id = get_jwt_identity()

    messages = User.get_user_by_id(user_id=user_id).message
    
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
    user = User.get_user_by_id(get_jwt_identity())
    message = Message.get_message_by_id(message_id=message_id)
    if message not in user.message:
        jsonify(build_response(0, "找不到此消息"))

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