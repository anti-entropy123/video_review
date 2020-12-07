
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


# 一个会议室
class MeetingRoom:
    def __init__(self, meeting_id) -> None:
        self.member_list:Dict[str, MeetingMember] = {}
        self.meeting_id = meeting_id
        meeting:Meeting = Meeting.get_meeting_by_id(meeting_id=meeting_id)
        self.manager_id = meeting.ownerId
        project:Project = Project.get_project_by_id(meeting.belongTo)
        self.project = project
        if project.hasVideo:
            video_id = project.hasVideo[-1]
            self.player:VideoPlayer = VideoPlayer(video_id=video_id)
        else:
            raise RuntimeError('没有视频')
        self.command_cache = (None, None, None)
        self.time_lock = time.time()

    def get_member_list(self):
        return {
            'memberNum': len(self.member_list),
            'memberList': [member.get_member_item() for member in self.member_list.values()]
        }

    def add_member(self, user_id):
        user = User.get_user_by_id(user_id=user_id)
        if user not in self.project:
            raise RuntimeError('你不是项目成员')
        
        self.member_list[user_id] = MeetingMember(user_id=user_id)

    def delete_member(self, user_id):
        # print(self.member_list)
        meeting_id_list = self.member_list.pop(user_id)
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
            if comment.alive:
                result.append({
                    'commentId': comment.commentId,
                    'fromId': comment.fromId,
                    'fromName': comment.fromName,
                    'imageUrl': comment.image,
                    'content': comment.content,
                    'position': comment.position,
                    'avatar': User.get_user_by_id(comment.fromId, deep=True).avatar
                })

        return result
    
    def add_comment(self, from_id, from_name, content, image_url, position):
        video = self.player.video
        if not video:
            raise RuntimeError('当前没在播放视频')
        comment = Comment(
            commentId=len(video.comment),
            fromId=from_id,
            fromName=from_name,
            position=position,
            image=image_url,
            content=content,
            date=time.time()
        )
        video.comment.append(comment)
        video.save()

    def remove_comment(self, user_id, comment_id):
        video = self.player.video
        if not video:
            raise RuntimeError('当前没在播放视频')
        comment_id = int(comment_id)
        if comment_id >= len(video.comment):
            raise RuntimeError('没有此批注')
        if not video.comment[comment_id].fromId == user_id:
            raise RuntimeError('你无法删除此批注')
        
        video.comment[comment_id].alive = False
        video.save()

    def push_cache(self, is_play:bool, position:int, url:str, type:int):
            self.command_cache = (is_play, position, url, type)

    def is_echo(self, is_play:bool, position:float, url:str, type:int):
        # print('指令:', is_play, position, url, type)
        # print('缓存指令', self.command_cache)
        reason = ''
        current_time = time.time()
        if self.command_cache[3] != 2 and type != 2 and current_time-self.time_lock < 0.08:
            reason = '过于频繁'
            result = True
        # elif self.command_cache[3] == 2 and (type==2 or type==3):
        #     result = True
        #     reason = '过于频繁'
        else:
            result = (
                self.command_cache[0] == is_play and abs(self.command_cache[1]-position)<1 and self.command_cache[2] == url
            ) or (
                self.player.is_play == is_play and abs(self.player.position-position)<1 and self.player.url == url        
            )
            reason = '状态没有实质性改变'
        # print('回声检测结果', result, reason)
        if not result: self.time_lock = current_time
        return result

    def guess_states(self, type, video_id, position, comment_id):
        player = self.player
        if type == 0 or type == 1:
            is_play = False
            url = player.url
        elif type == 2:
            is_play = player.is_play
            url = player
        elif type == 3 or type == 4:
            is_play = True
            url = player.url
        elif type == 5:
            is_play = False
            url = Video.get_video_by_id(video_id=video_id).url
        elif type == 6:
            is_play = False
            url = player.url
            comment:Comment = player.video.comment[comment_id]
            position = comment.position
        else:
            raise RuntimeError('无效的type')
        
        return is_play, position, url
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
        meeting_room.add_member(user_id=user_id)
        sid_object = SidObject(sid, meeting_id, user_id, meeting_room)
        self.sid_objects[sid] = sid_object
        return sid_object

    def destroy_meetingroom(self, meeting_id):
        self.meetingrooms.pop(meeting_id)

    def get_meetingRoom_by_meetingId(self, meeting_id:str)->MeetingRoom:
        return self.meetingrooms.get(meeting_id, None)
    
    def disconnect_sid(self, sid):
        if not sid in self:
            return
        sid_object = self[sid]
        sid_object.meetingroom.delete_member(sid_object.user_id)
        self.sid_objects.pop(sid)

    def __getitem__(self, sid:str)->SidObject:
        return self.sid_objects.get(sid, None)

    def __contains__(self, sid:str)->bool:
        return sid in self.sid_objects

sid_manager = SidManager()
