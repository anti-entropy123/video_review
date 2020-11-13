
import time
from app.utils import build_response
from flask import request
from flask_socketio import SocketIO, emit, join_room, leave_room
from ..model import User, Meeting, Video
from . import ws

name_space = '/meetingRoom'

meetingroom_manager = {}

# 会议中的一个成员
class MeetingMember:
    def __init__(self, user_id) -> None:
        self.user = User.get_user_by_id(user_id=user_id)
        self.control = True
        self.comment = True

    def get_member_item(self):
        return {
            'userId': str(self.user.userId),
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
        self.is_play = False
        self.position += (time.time()-self.change_point)
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
        return int(self.is_play and self.url)

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
        comments = video.comment
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

@ws.on('connect', namespace=name_space)
def connected_msg(data):
    print('client connected.')
    meeting_id = data['meetingId']
    user_id = data['userId']
    
    meeting_room: MeetingRoom = meetingroom_manager[meeting_id]
    meeting_room.add_member(user_id=user_id)
    
    # 加入会议室room, 方便广播
    join_room(meeting_id)

    # 向会议中所有人更新最新的成员列表
    ws.emit(
        'sycnMember',
        build_response(data=meeting_room.get_member_list()),
        room=meeting_id
    )
    # 向新成员发送当前视频的播放
    emit(
        'sycnVideoState', 
        meeting_room.player.get_video_status()
    )
    # 向新成员发送当前批注的列表
    emit(
        'updateComment',
        meeting_room.get_comment_list()
    )

@ws.on('disconnect', namespace=name_space)
def disconnect_msg(data):
    meeting_id = data['meetingId']
    # print('client disconnected.')
    leave_room(meeting_id)

# @ws.on('my_event', namespace=name_space)
# def test_message(message):
#     print(message)
#     emit('my_response',
#          {'data': message['data'], 'count': 1})

