
import flask_socketio as io
from flask import request
from flask_socketio import emit, join_room, rooms

from app.utils import build_response

from ..model import Meeting, User, Video
from . import ws
from .entity import (MeetingMember, MeetingRoom, VideoPlayer, sid_manager)

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
    print('初始化:', '会议id', meeting_id, '用户id', user_id)

    # 获取会议对象
    meeting = Meeting.get_meeting_by_id(meeting_id=meeting_id)
    if not meeting:
        return emit('errorHandle',build_response(0, '无效的meetingId'))

    # # 获取会议室对象
    # if meeting_id in meetingroom_manager:
    #     meeting_room: MeetingRoom = meetingroom_manager[meeting_id]
    # else:
    #     try: 
    #         meeting_room = MeetingRoom(meeting_id=meeting_id)
    #     except RuntimeError as e:
    #         emit('errorHandle',build_response(0, str(e)))
    #         return

    # # 保存此连接的用户的id
    # meetingId_manager[request.sid] = meeting_id
    # userId_manager[request.sid] = user_id
    # meeting_room.add_member(user_id=user_id)
    
    try:
        member = sid_manager.enter_meetingroom(sid=request.sid, meeting_id=meeting_id, user_id=user_id)
    except RuntimeError as e:
        emit('errorHandle',build_response(0, str(e)))
        return

    meetingroom = member.room
    # 加入会议室room, 方便广播
    join_room(meeting_id)
    # print(rooms(request.sid))
    # 向会议中所有人更新最新的成员列表
    io.emit(
        'sycnMember',
        build_response(data=meetingroom.get_member_list()),
        # broadcast=True
        room=meeting_id
    )
    # 向新成员发送当前视频的播放
    video_status = meetingroom.player.get_video_status()
    video_status['reason'] = ''
    video_status['userName'] = ''
    meetingroom.push_cache(video_status['isPlay'], video_status['position'], video_status['url'], type=-1)
    emit(
        'sycnVideoState', 
        build_response(data=video_status) 
    )
    # 向新成员发送当前批注的列表
    emit(
        'updateComment',
        build_response(data=meetingroom.get_comment_list())
    )

@ws.on('disconnect', namespace=name_space)
def disconnect_msg():
    # meeting_id = meetingId_manager[request.sid]
    pass

@ws.on('destory', namespace=name_space)
def destory():
    # print('destory被调用')
    # sid_manager._sid_test_total += 1
    # test = False
    if request.sid in sid_manager:
        meeting_room = sid_manager[request.sid].room
        meeting_id = meeting_room.meeting_id
        # sid_manager._sid_test_true += 1
        # test = True
        sid_manager.disconnect_sid(request.sid)
        # print('现在的成员数量有', len(meeting_room.member_list))
        io.emit(
            'sycnMember',
            build_response(data=meeting_room.get_member_list()),
            # broadcast=True
            room=meeting_id
        )

    # print('sid 有效性检测:', test, round(sid_manager._sid_test_true / sid_manager._sid_test_total, 2))

@ws.on('changeProcess', namespace=name_space)
def controll_player(data):
    try:
        type = int(data['type'])
        position = float(data['position'])
        video_id = data['videoId']
        comment_id = int(data['commentId']) if type==6 else None
        print(type, comment_id)

    except KeyError as e:
        emit('errorHandle', build_response(0, '缺失参数'+str(e)))
        return
    except TypeError as e:
        emit('errorHandle', build_response(0, '参数类型有误'))
        return

    member = sid_manager[request.sid]

    meeting_room:MeetingRoom = member.room
    meeting_id = meeting_room.meeting_id
    user = member.user
    
    video_player:VideoPlayer = meeting_room.player
    video_status = {
        'userName': user.username,
        'reason': type,
    }
 
    try:
        is_play, position, url = meeting_room.guess_states(type=type, video_id=video_id, position=position, comment_id=comment_id)
        # 如果检测到回声, 直接阻断
        if meeting_room.is_echo(is_play=is_play, position=position, url=url, type=type):
            return
        args = {
            'position': position,
            'video_id': video_id
        }
        member.do_operation(type=type, **args)
        # 切换视频
        if type == 5:
            io.emit(
                'updateComment',
                build_response(data=meeting_room.get_comment_list()),
                room=meeting_id
            )
        if type == 6:
            video_status.update({
                'commentId': comment_id
            })
        
    except RuntimeError as e:
        emit('errorHandle', build_response(0, str(e)))
        return

    video_status.update(video_player.get_video_status())
    meeting_room.push_cache(video_status['isPlay'], video_status['position'], video_status['url'], type=type)
    # print(video_status)
    io.emit(
        'sycnVideoState',
        build_response(data=video_status),
        room=meeting_id
    )

@ws.on('addComment', namespace=name_space)
def addComment(data):
    try:
        meeting_id = data['meetingId']
        content = data['content']
        image_url = data['imageUrl']
        position = data['position']
    except KeyError as e:
        emit('errorHandle', build_response(0, str(e)))
        return

    member = sid_manager[request.sid]

    from_id = str(member.user.id)
    from_name = member.user.username

    meeting_room: MeetingRoom = member.room
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

@ws.on('removeComment', namespace=name_space)
def removeComment(data):
    try:
        comment_id = int(data['commentId'])
    except KeyError as e:
        emit('errorHandle', build_response(0, str(e)))
        return
    
    member = sid_manager[request.sid]
    meetingroom = member.room
    try:
        meetingroom.remove_comment(user_id=str(member.user.id), comment_id=comment_id)
    except RuntimeError as e:
        emit('errorHandle', build_response(0, str(e)))
        return    
    emit(
        'updateComment',
        build_response(data=meetingroom.get_comment_list()),
        room=meetingroom.meeting_id
    )

@ws.on('memberPermission', namespace=name_space)
def setPermission(data):
    try:
        target_id = data['userId']
        # meeting_id = data['meetingId']
    except KeyError as e:
        emit('errorHandle', build_response(0, str(e)))
        return

    member:MeetingMember = sid_manager[request.sid]

    meeting_room: MeetingRoom = member.room
    user_id = str(member.user.id)
    if not user_id == meeting_room.manager_id:
        emit('errorHandle', build_response(0, "你不是管理员"))
        return

    target_user: MeetingMember = meeting_room.member_list[target_id]
    
    print('member', 'target', member is target_user)

    control = data.get('control', -1)
    if control >= 0:
        target_user.control = control

    comment = data.get('comment', -1)
    # print('接受到的参数为', control, comment)
    if comment >= 0:
        target_user.comment = comment

    print('设置后的权限', target_user.control, target_user.comment)
    io.emit(
        'sycnMember',
        build_response(data=meeting_room.get_member_list()),
        room=meeting_room.meeting_id
    )
