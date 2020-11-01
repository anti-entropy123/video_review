from flask import jsonify, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

from bson.objectid import ObjectId

from .. import client
from . import api
from ..utils import build_response

db = client.db

@api.route('/project/', methods=['POST'])
@jwt_required
def create_project():
    project_name = request.json['projectName']
    
    if db.project.find(
        {'projectName': project_name},
        {'_id': 1}).count():
        return jsonify(build_response(0, '此项目名已被使用'))
    
    db.project.insert_one({
        'projectName': project_name,
        'owner': get_jwt_identity(),
        'member': [],
        'waitJoin': [],
        'hasVideo': []
    })
    return jsonify(build_response())

