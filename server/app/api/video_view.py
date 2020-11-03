from flask import jsonify, request, abort
from flask_jwt_extended import get_jwt_identity

from bson.objectid import ObjectId

from .. import db
from . import api
from ..utils import build_response
from ..model import Video, User, Project, Message
from ..auth import login_required

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
    video = Video(
        videoName=video_name,
        duration=3600,
        permission=permission,
        url=url,
        cover=['https://'],
        password=password
    )
    video.save()
    video_id = str(video.id)
    user_id = get_jwt_identity()
    uploader = User.objects(id=ObjectId(user_id)).first()
    video_list = uploader.uploadVideo
    if not video_id in video_list:
        uploader.uploadVideo = video_list + [video_id]
        uploader.save()

    project = Project.objects(id=ObjectId(upload_to_project)).first()
    video_list = project.hasVideo
    if not video_id in video_list:
        project.hasVideo = video_list + [video_id]
        project.save()

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
    video = Video.objects(id=ObjectId(video_id)).first()
    video.reviewResult = review_result
    video.reviewSummary = summary
    video.hasReview = True
    video.save()

    reviewer = User.objects(id=ObjectId(get_jwt_identity())).first()
    project = Project.objects(id=ObjectId(video.belongTo)).first()

    # 通知用户视频被审阅
    user = User.objects(id=ObjectId(video.owner)).first()
    new_message = Message(
        fromId = str(reviewer.id),
        fromName = reviewer.username,
        projectId = str(project.id),
        projectName = project.projectName,
        type = 1,
        content = {
            'videoName': video.videoName,
            'reviewResult': review_result
        }
    )
    reviewer.message.append(new_message)
    reviewer.save()

    return jsonify(build_response())

# 我的视频
@api.route('/video/mine/', methods=['GET'])
@login_required
def my_video():
    user = User.objects(id=ObjectId(get_jwt_identity())).first()
    print(user)

    video_list = user.uploadVideo
    print(video_list)
    data = []
    for video_id in video_list:
        video = Video.objects(id=ObjectId(video_id)).first()
        one = {
            'url': video.url,
            'videoName': video.videoName,
            'description': video.description,
            'duration': video.duration,
            'status': video.hasReview,
            'cover': video.cover,
            'videoId': video_id
        }
        data.append(one)
    
    return jsonify(build_response(1, '', data=data))

    
