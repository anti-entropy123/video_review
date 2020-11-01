from flask import jsonify, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

from bson.objectid import ObjectId

from .. import client
from . import api
from ..utils import build_response

db = client.db

@api.route('/video/', methods=['POST'])
@jwt_required
def login():
    parm = request.json
    try:
        url = parm['url']
        video_name = parm['videoName']
        description = parm['description']
        permission = parm['permission']
    except KeyError as e:
        abort(400, {'msg': str(e)})

    password = parm.get('password', '')
    if permission == 1 and password == '':
        return jsonify(build_response(0, 'password不能为空'))

    db.video.insert_one({
        'videoName': video_name,
        'duration': 3600,
        'permission': permission,
        'password': password,
        'url': url,
        'hasReview': 0,
        'reviewResult': -1,
        'reviewSummary': '',
        'cover': '',
        'comment': []
    })
    return jsonify(build_response())
    
@api.route('/video/<video_id>/review/', methods=['POST'])
@jwt_required
def review_finish(video_id):
    try:
        parm = request.json
        review_result = parm['reviewResult']
        summary = parm['summary']
    except KeyError as e:
        abort(400, {'msg': str(e)})

    # 数据库中写入视频
    db.video.update(
        {'_id': ObjectId(video_id)},
        {'$set': 
            {'hasReview': 1, 
             'reviewResult': review_result,
             'reviewSummary': summary}
        }
    )
    user_id = get_jwt_identity()
    print(user_id)
    db.user.update(
        {'_id': ObjectId(user_id)},
        {'$addToSet': 
            {'uploadVideo': video_id}}
    )
    return jsonify(build_response())

@api.route('/video/mine/', methods=['GET'])
@jwt_required
def my_video():
    video_list = list(db.user.find_one(
        {'_id': ObjectId(get_jwt_identity())},
        {'uploadVideo': 1}
    )['uploadVideo'])
    video_list = [ObjectId(i) for i in video_list]
    print(video_list)
    data = []
    for video in db.video.find(
        {'_id': {'$in': video_list}},
        {
            'url': 1,
            'videoName': 1,
            'description': 1,
            'duration': 1,
            'hasReview': 1,
            'cover': 1,
            '_id': 1
        }
    ):
        video['status'] = video.pop('hasReview')
        video['videoId'] = str(video.pop('_id'))
        data.append(video)
    print(data)
    return jsonify(build_response(1, '', data=data))

    
