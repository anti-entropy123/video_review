
import flask_socketio as io
from flask import request
from flask_socketio import emit, join_room, rooms

from app.utils import build_response

from ..model import Meeting, User
from . import ws
from .entity import (MeetingMember, MeetingRoom, VideoPlayer,
                     meetingId_manager, meetingroom_manager, userId_manager)

name_space = '/meetingRoom'

@ws.on('connect', namespace=name_space)
def connected_msg():
    pass
    # print('client connected.')

@ws.on('init', namespace=name_space)
def init(data):
    # print(data)
    meeting_id = data['meetingId']
    user_id = data['userId']
    
    # 获取会议对象
    meeting = Meeting.get_meeting_by_id(meeting_id=meeting_id)
    if not meeting:
        return emit('errorHandle',build_response(0, '无效的meetingId'))

    # 获取会议室对象
    if meeting_id in meetingroom_manager:
        meeting_room: MeetingRoom = meetingroom_manager[meeting_id]
    else:
        try: 
            meeting_room = MeetingRoom(meeting_id=meeting_id)
        except RuntimeError as e:
            emit('errorHandle',build_response(0, str(e)))
            return

    # 保存此连接的用户的id
    meetingId_manager[request.sid] = meeting_id
    userId_manager[request.sid] = user_id
    meeting_room.add_member(user_id=user_id)
    
    # 加入会议室room, 方便广播
    join_room(meeting_id)
    # print(rooms(request.sid))
    # 向会议中所有人更新最新的成员列表
    io.emit(
        'sycnMember',
        build_response(data=meeting_room.get_member_list()),
        # broadcast=True
        room=meeting_id
    )
    # 向新成员发送当前视频的播放
    video_status = meeting_room.player.get_video_status()
    video_status['reason'] = ''
    video_status['userName'] = ''
    emit(
        'sycnVideoState', 
        build_response(data=video_status) 
    )
    # 向新成员发送当前批注的列表
    emit(
        'updateComment',
        build_response(data=meeting_room.get_comment_list())
    )

@ws.on('disconnect', namespace=name_space)
def disconnect_msg():
    # meeting_id = meetingId_manager[request.sid]
    print('sid 有效性检测:', request.sid in meetingId_manager)
    # FIXME 这里的 request.id 貌似不好用 ? 
    # todo 应该在断开链接时从meetingRoom中去掉这个用户.
    # meetingId_manager.pop(request.sid)
    # userId_manager.pop(request.sid)

@ws.on('changeProcess', namespace=name_space)
def controll_player(data):
    type = int(data['type'])
    position = data['position']
    video_id = data['videoId']
    meeting_id = meetingId_manager[request.sid]
    user = User.get_user_by_id(userId_manager[request.sid])

    meeting_room: MeetingRoom = meetingroom_manager[meeting_id]
    video_player: VideoPlayer = meeting_room.player
    video_status = {
        'userName': user.username,
        'reason': type,
    }
    # 注: 变量 flag 的作用是, 标记此请求是否确实改变了后端播放器的某些状态
    #     例如设置进度条时, 如果新的位置和原位置过于接近, 就不会发生更改
    #     此时flag就为false
    flag = True
    # 暂停
    if type == 0 or type == 1:
        flag = video_player.pause(position)
    # 拖动进度条
    elif type==2:
        flag = video_player.move_process(position=position)
    # 播放
    elif type == 3 or type==4:
        flag = video_player.play(position)
    # 切换视频
    elif type == 5:
        if not meeting_room.manager_id == str(user.id):
            emit('errorHandle', build_response(0, "你不是管理员"))

        video_player.change_video(video_id=video_id)
        io.emit(
            'updateComment',
            build_response(data=meeting_room.get_comment_list()),
            room=meeting_id
        )
    else:
        emit('errorHandle', build_response(0, '无效的type'))

    video_status.update(video_player.get_video_status())
    # print(video_status)
    if flag:
        io.emit(
            'sycnVideoState',
            build_response(data=video_status),
            room=meeting_id
        )

@ws.on('addComment', namespace=name_space)
def addComment(data):
    meeting_id = data['meetingId']
    content = data['content']
    image_url = data['imageUrl']
    position = data['position']
    from_id = userId_manager[request.sid]
    user = User.get_user_by_id(from_id)
    from_name = user.username

    meeting_room: MeetingRoom = meetingroom_manager[meeting_id]
    meeting_room.add_comment(
        from_id=from_id,
        from_name=from_name,
        content=content,
        image_url=image_url,
        position=position
    )
    
    emit(
        'updateComment',
        build_response(data=meeting_room.get_comment_list()),
        room=meeting_id
    )

@ws.on('memberPermission', namespace=name_space)
def setPermission(data):
    target_id = data['userId']
    meeting_id = data['meetingId']
    meeting_room: MeetingRoom = meetingroom_manager[meeting_id]
    user_id = userId_manager[request.sid]
    if not user_id == meeting_room.manager_id:
        return
    target_user: MeetingMember = meeting_room.member_list[target_id]
    
    control = data.get('control', -1)
    if control >= 0:
        target_user.control = control

    comment = data.get('comment', -1)
    if comment >= 0:
        target_user.comment = comment

    io.emit(
        'sycnMember',
        build_response(data=meeting_room.get_member_list()),
        room=meeting_id
    )
