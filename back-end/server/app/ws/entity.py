from types import ClassMethodDescriptorType
from app.api import project_view
from os import truncate
import time
from typing import Dict, List

from ..model import Comment, Meeting, Project, User, Video



# 会议中的一个成员
class MeetingMember:
    def __init__(self, user_id) -> None:
        self.user = User.get_user_by_id(user_id=user_id)
        self.control = True
        self.comment = True
    
    @property
    def avatar(self):
        return self.user.avatar

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
    def __init__(self, video_id:str) -> None:
        self.video: Video = None
        self._position = 0
        self._is_play = False
        self.change_video(video_id=video_id)

    @property
    def cover(self):
        return self.video.cover[0] if self.video else ''

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, p):
        if p < self.duration:
            self._position = p
        else:
            self._position = self.duration
        self.change_point = time.time()

    @property
    def duration(self):
        return self.video.duration if self.video else 0

    @duration.setter
    def duration(self, d):
        raise RuntimeError('不能修改此值')

    @property
    def url(self):
        return self.video.url if self.video else ""
    
    @url.setter
    def url(self, u):
        raise RuntimeError('不能修改此值')

    @property
    def videoName(self):
        return self.video.videoName if self.video else ''
    
    @videoName.setter
    def video_name(self, n):
        raise RuntimeError('不能修改此值')

    @property
    def is_play(self):
        return self._is_play
    
    @is_play.setter
    def is_play(self, play):
        if self._is_play:
            self.position += round(time.time()-self.change_point)
        self._is_play = play

    def play(self, position):
        if self.is_play:
            return False
        self.is_play = True
        self.position = position
        return True

    def pause(self, position):
        if not self.is_play:
            return False
        self.is_play = False
        self.position = position
        return True

    def move_process(self, position):
        if abs(position-self.position) < 1:
            return False
        self.position = position if position < self.duration else self.duration
        return True

    def change_video(self, video_id:str):
        video = Video.get_video_by_id(video_id=video_id)
        if not video:
            raise KeyError()
        else:
            self.video = video
        
        self.is_play = False
        self.position = 0
        self.change_point = time.time()

    def get_video_info(self)->dict:
        project = Project.get_project_by_id(project_id=self.video.belongTo)
        return {
            'videoName': self.video.videoName,
            'uploader': self.video.owner,
            'duration': self.video.duration,
            'covers': self.video.cover,
            'project': project.projectName,
            'description': self.video.description,
            'createDate': self.video.createDate
        }

    def get_video_status(self):
        return {
            'url': self.url,
            'position': self.position,
            'isPlay': self.is_play,
            'duration': self.duration,
            'videoName': self.videoName,
            'cover': self.cover,
            'videoInfo': self.get_video_info()
        }

    def guess_states(self, type, video_id):
        if type == 0 or type == 1:
            is_play = False
            url = self.url
        elif type == 2:
            is_play = self.is_play
            url = self
        elif type == 3 or type == 4:
            is_play = True
            url = self.url
        elif type == 5:
            is_play = False
            url = Video.get_video_by_id(video_id=video_id).url
        else:
            raise RuntimeError('无效的type')
        
        return is_play, url

# 一个会议室
class MeetingRoom:
    def __init__(self, meeting_id) -> None:
        self.member_list:Dict[str, MeetingMember] = {}
        self.meeting_id = meeting_id
        meeting:Meeting = Meeting.get_meeting_by_id(meeting_id=meeting_id)
        self.manager_id = meeting.ownerId
        project:Project = Project.get_project_by_id(meeting.belongTo)
        if project.hasVideo:
            video_id = project.hasVideo[-1]
            self.player:VideoPlayer = VideoPlayer(video_id=video_id)
        else:
            raise RuntimeError('没有视频')
        self.command_cache = (None, None, None)

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
            sid_manager.destroy_meetingroom(self.meeting_id)
    
    def get_comment_list(self):
        video:Video = self.player.video
        if not video:
            return []

        comments:List[Comment] = video.comment
        result = []
        for comment in comments:
            result.append({
                'fromId': comment.fromId,
                'fromName': comment.fromName,
                'imageUrl': comment.image,
                'content': comment.content,
                'position': comment.position,
                'avatar': self.member_list[comment.fromId].avatar
            })

        return result
    
    def add_comment(self, from_id, from_name, content, image_url, position):
        comment = Comment(
            fromId=from_id,
            fromName=from_name,
            position=position,
            image=image_url,
            content=content
        )
        video = self.player.video
        if not video:
            raise RuntimeError('当前没在播放视频')

        video.comment.append(comment)
        video.save()

    def push_cache(self, is_play:bool, position:int, url:str):
            self.command_cache = (is_play, position, url)

    def is_echo(self, is_play:bool, position:int, url:str):
        return self.command_cache[0] == is_play and self.command_cache[1] == position and self.command_cache[2] == url
# # meetingId => MeetingMember()
# meetingroom_manager:Dict[str, MeetingRoom] = {}
# # sid => userId
# userId_manager:Dict[str, str] = {}
# # sid => meetingId
# meetingId_manager:Dict[str, str] = {}

class SidObject:
    def __init__(self, sid, meeting_id, user_id, meetingroom:MeetingRoom) -> None:
        self.sid = sid
        self.meeting_id = meeting_id
        self.user_id = user_id
        self.meetingroom = meetingroom

# sid -> all data
class SidManager:
    # meetingId -> MeetingRomm
    meetingrooms = {}
    sid_objects = {}
    _sid_test_total = 0
    _sid_test_true = 0
    
    def enter_meetingroom(self, sid, meeting_id, user_id) -> SidObject:
        meeting_room = self.meetingrooms.get(meeting_id, None)
        if not meeting_room:
            meeting_room = MeetingRoom(meeting_id)
        self.meetingrooms[meeting_id] = meeting_room
        sid_object = SidObject(sid, meeting_id, user_id, meeting_room)
        self.sid_objects[sid] = sid_object
        return sid_object

    def destroy_meetingroom(self, meeting_id):
        self.meetingrooms.pop(meeting_id)

    def get_meetingRoom_by_meetingId(self, meeting_id:str)->MeetingRoom:
        return self.meetingrooms.get(meeting_id, None)
    
    def __getitem__(self, sid:str)->SidObject:
        return self.sid_objects.get(sid, None)

    def __contains__(self, sid:str)->bool:
        return sid in self.sid_objects

sid_manager = SidManager()