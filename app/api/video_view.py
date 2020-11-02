from flask import jsonify, request, abort
from flask_jwt_extended import get_jwt_identity

from bson.objectid import ObjectId

from .. import client
from . import api
from ..utils import build_response
from ..model import Video, User, Project
from ..auth import login_required

db = client.db

# 新建视频
@api.route('/video/', methods=['POST'])
@login_required
def create_video():
    parm = request.json
    try:
        url = parm['url']
        video_name = parm['videoName']
        description = parm['description']
        permission = parm['permission']
        upload_to_project = parm['uploadToProject']
    except KeyError as e:
        abort(400, {'msg': str(e)})

    password = parm.get('password', '')
    if permission == 1 and password == '':
        return jsonify(build_response(0, 'password不能为空'))
    
    # 数据库插入此视频
    video_id = Video.create_video(
        video_name=video_name,
        duration=3600,
        permission=permission,
        url=url,
        cover=[],
        password=password
    )
    user_id = get_jwt_identity()
    # 由此用户上传
    User.upload_video(user_id, video_id)
    # 上传至哪个项目
    Project.add_video(upload_to_project, video_id)
    return jsonify(build_response())
    
# 完成审阅
@api.route('/video/<video_id>/review/', methods=['POST'])
@login_required
def review_finish(video_id):
    try:
        parm = request.json
        review_result = parm['reviewResult']
        summary = parm['summary']
    except KeyError as e:
        abort(400, {'msg': str(e)})

    # 数据库中写入视频
    Video.finish_review(video_id, review_result, summary)
    return jsonify(build_response())

# 我的视频
@api.route('/video/mine/', methods=['GET'])
@login_required
def my_video():
    video_list = User.get_video_list(user_id=get_jwt_identity())
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

    
