
import time

import flask_socketio as io
from app.utils import build_response
from flask import request
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from ..model import Comment, User, Meeting, Video
from . import ws

name_space = '/meetingRoom'
# meetingId => MeetingMember()
meetingroom_manager = {}
# sid => userId
userId_manager = {}
# sid => meetingId
meetingId_manager = {}

# 会议中的一个成员
class MeetingMember:
    def __init__(self, user_id) -> None:
        self.user = User.get_user_by_id(user_id=user_id)
        self.control = True
        self.comment = True

    def get_member_item(self):
        return {
            'userId': str(self.user.id),
            'username': str(self.user.username),
            'avatar': str(self.user.avatar),
            'control': self.control,
            'comment': self.comment
        }

# 视频播放器
class VideoPlayer:
    def __init__(self) -> None:
        self.position = 0
        self.url = None
        self.is_play = False
        self.change_point = None

    def play(self):
        self.is_play = True
        self.change_point = time.time()

    def pause(self):
        if self.is_play:
            self.position += round(time.time()-self.change_point) / 100
        self.is_play = False
        self.change_point = time.time()

    def move_process(self, postion):
        self.position = postion
        self.change_point = time.time()

    def change_video(self, url):
        self.url = url
        self.position = 0
        self.is_play = False
        self.change_point = time.time()

    def get_postion(self):
        return 0 if not self.url else (self.position if not self.is_play else self.position + (time.time()-self.change_point))

    def get_isPlay(self):
        if self.url and self.is_play:
            return 1
        else:
            return 0
        # return int(self.url and self.is_play)

    def get_video_status(self):
        return {
            'url': self.url,
            'postion': self.get_postion(),
            'isPlay': self.get_isPlay()
        }
        

# 一个会议室
class MeetingRoom:
    def __init__(self, meeting_id) -> None:
        self.member_list = {}
        self.meeting_id = meeting_id
        meeting = Meeting.get_meeting_by_id(meeting_id=meeting_id)
        self.manager_id = meeting.ownerId
        self.player = VideoPlayer()
        meetingroom_manager[meeting_id] = self

    def get_member_list(self):
        return {
            'memberNum': len(self.member_list),
            'memberList': [member.get_member_item() for member in self.member_list.values()]
        }

    def add_member(self, user_id):
        self.member_list[user_id] = MeetingMember(user_id=user_id)

    def delete_member(self, user_id):
        self.member_list.pop(user_id)
        # 如果此会议室没人在了, 则销毁此会议室
        if not len(self.member_list):
            meetingroom_manager.pop(self.meeting_id)
    
    def get_comment_list(self):
        video = Video.objects(url=self.player.url).first()
        comments = video.comment if video else []
        result = []
        for comment in comments:
            result.append({
                'fromId': comment.fromId,
                'fromName': comment.fromName,
                'imageUrl': comment.url,
                'content': comment.content,
                'position': comment.postion
            })
        return result
    
    def add_comment(self, from_id, from_name, content, image_url, postion):
        comment = Comment(
            from_=from_id,
            fromName=from_name,
            postion=postion,
            image=image_url,
            content=content
        )
        video = Video.objects(url=self.player.url).first()
        video.comment.append(comment)
        video.save()

@ws.on('connect', namespace=name_space)
def connected_msg():
    print('client connected.')

@ws.on('init', namespace=name_space)
def init(data):
    print(data)
    meeting_id = data['meetingId']
    user_id = data['userId']
    
    userId_manager[request.sid] = user_id
    meetingId_manager[request.sid] = meeting_id

    if meeting_id in meetingroom_manager:
        meeting_room: MeetingRoom = meetingroom_manager[meeting_id]
    else:
        meeting_room = MeetingRoom(meeting_id=meeting_id)
    meeting_room.add_member(user_id=user_id)
    
    # 加入会议室room, 方便广播
    join_room(meeting_id)
    print(rooms(request.sid))
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
    meeting_id = meetingId_manager[request.sid]
    # print('client disconnected.')
    leave_room(meeting_id)
    userId_manager.pop(request.sid)

# @ws.on('my_event', namespace=name_space)
# def test_message(message):
#     print(message)
#     emit('my_response',
#          {'data': message['data'], 'count': 1})

@ws.on('changeProcess', namespace=name_space)
def controll_player(data):
    type = int(data['type'])
    postion = data['postion']
    url = data['url']
    meeting_id = meetingId_manager[request.sid]
    user = User.get_user_by_id(userId_manager[request.sid])

    meeting_room: MeetingRoom = meetingroom_manager[meeting_id]
    video_player: VideoPlayer = meeting_room.player
    video_status = {
        'userName': user.username,
        'reason': type,
    }
    if type == 0 or type == 1:
        video_player.pause()
    elif type==2:
        video_player.move_process(postion=postion)
    elif type == 3 or type==4:
        video_player.play()
    elif type == 5:
        video_player.change_video(url=url)
    else:
        raise RuntimeError('无效的type')

    video_status.update(video_player.get_video_status())
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
    postion = data['postion']
    from_id = userId_manager[request.sid]
    user = User.get_user_by_id(from_id)
    from_name = user.username

    meeting_room: MeetingRoom = meetingroom_manager[meeting_id]
    meeting_room.add_comment(
        from_id=from_id,
        from_name=from_name,
        content=content,
        image_url=image_url,
        postion=postion
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