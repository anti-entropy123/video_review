import os
import time
from typing import List

from flask import abort
from flask import current_app as app
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity

from .. import db
from ..auth import login_required
from ..model import Comment, Message, Project, User, Video
from ..utils import build_response, captrueFrameUtil, safe_objectId, txCosUtil
from . import api


# 新建视频
@api.route('/video/', methods=['POST'])
@login_required
def create_video():
    parm = request.form
    files = request.files
    try:
        video_name = parm['videoName']
        description = parm['description']
        permission = parm['permission']
        upload_to_project = parm['uploadToProject']

        file = files['video']
    except KeyError as e:
        abort(400, {'msg': str(e)})

    project = Project.get_project_by_id(project_id=upload_to_project)
    if not project:
        return jsonify(build_response(0, "无此项目"))

    if sum([(i in video_name) for i in r"\/"]) and (".mp4" in video_name or '.mkv' in video_name):
        return jsonify(build_response(0, "video_name 不合法"))

    user_id = get_jwt_identity()
    uploader = User.get_user_by_id(user_id=user_id)
    if not uploader in project:
        return jsonify(build_response(0, "你不是此项目的成员"))

    password = parm.get('password', '')
    if permission == 1 and password == '':
        return jsonify(build_response(0, 'password不能为空'))

    # 这里把request里的文件存到了一个临时的目录下
    filename = os.path.join(app.config['UPLOAD_FOLDER'], video_name) 
    file.save(filename)

    try:
        with open(filename, 'rb') as f:
            url = txCosUtil.upload_video(user_id=user_id, f=f)
        
        frames, duration = captrueFrameUtil.capture_frame(filename)
        covers = []
        for i, frame in enumerate(frames):
            u = txCosUtil.upload_image(user_id=user_id, f=frame)
            covers.append(u)
    finally:
        os.remove(filename)

    # 数据库插入此视频
    video = Video(
        videoName=video_name,
        duration=duration,
        owner=get_jwt_identity(),
        belongTo=upload_to_project,
        permission=permission,
        url=url,
        cover=covers,
        password=password
    )
    video.save()
    video_id = str(video.id)
    if not video_id in uploader.uploadVideo:
        uploader.uploadVideo.append(video_id)
        uploader.save()

    if not video_id in project.hasVideo:
        project.hasVideo.append(video_id)
        project.save()

    data = {
        'url': video.url,
        'videoId': video_id
    }
    return jsonify(build_response(data=data))
    
# 完成审阅
@api.route('/video/<video_id>/review/', methods=['POST'])
@login_required
def review_finish(video_id):
    parm = request.json or {}
    try:
        review_result = parm['reviewResult']
        summary = parm['summary']
    except KeyError as e:
        abort(400, {'msg': str(e)})

    # 数据库中写入视频
    video = Video.get_video_by_id(video_id=video_id)
    if not video:
        return jsonify(build_response(0, '没有此视频'))
    video.set_review_result(result=review_result, summary=summary)

    # 视频审阅者
    reviewer = User.get_user_by_id(get_jwt_identity())
    project = Project.get_project_by_id(video.belongTo)
    # 视频上传者
    user = User.get_user_by_id(video.owner)
    new_message = Message(
        fromId = str(reviewer.id),
        fromName = reviewer.username,
        projectId = str(project.id),
        projectName = project.projectName,
        type = 1,
        date=time.time()
    )
    new_message.fill_content(
        videoName = video.videoName,
        reviewResult = review_result
    )
    reviewer.message.append(new_message)
    reviewer.save()

    return jsonify(build_response())

# 我的视频
@api.route('/video/mine/', methods=['GET'])
@login_required
def my_video():
    user = User.get_user_by_id(get_jwt_identity())
    video_list = user.uploadVideo
    # print(video_list)
    data = []
    for video_id in video_list:
        video = Video.get_video_by_id(video_id=video_id)
        one = {
            'url': video.url,
            'videoName': video.videoName,
            'description': video.description,
            'duration': video.duration,
            'status': video.hasReview,
            'cover': video.cover,
            'videoId': video_id,
            'date': video.createDate
        }
        data.append(one)
    
    return jsonify(build_response(data=data))

@api.route('/video/<video_id>/comments', methods=['GET'])
@login_required
def get_comment(video_id:str):
    user = User.get_user_by_id(get_jwt_identity())
    video = Video.get_video_by_id(video_id=video_id)
    if not video:
        return jsonify(build_response(message='没有此视频'))
    
    project = Project.get_project_by_id(video.belongTo)
    if not user in project:
        return jsonify(build_response(message='你不能查看此视频的批注'))
    
    data = video.get_comment_list()
    return jsonify(build_response(data=data))

@api.route('/video/<video_id>/comment/', methods=['POST'])
@login_required
def insert_comment(video_id:str):
    args = request.json or {}
    try:
        content:str = args['content']
        imageUrl:str = args['imageUrl']
        position:float = args['position']
    except KeyError as e:
        abort(400, {'msg': str(e)})

    user = User.get_user_by_id(get_jwt_identity())
    video = Video.get_video_by_id(video_id=video_id)
    if not video:
        return jsonify(build_response(message='没有此视频'))
    
    project = Project.get_project_by_id(video.belongTo)
    if not user in project:
        return jsonify(build_response(message='你不能对此视频做批注'))
    
    comment = Comment(
        position=position,
        image=imageUrl,
        content=content
    )
    comment_id = video.insert_comment(comment=comment, from_user=user)
    data = {'commentId': comment_id}
    return jsonify(build_response(data=data))
