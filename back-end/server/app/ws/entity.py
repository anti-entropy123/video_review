import time

from ..model import Comment, Meeting, User, Video

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
        self.video:Video = None
        self._position = 0
        self._is_play = False
        self.change_point = None

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, p):
        if p < self.duration:
            self._position = p
        else:
            self._position = self.duration

    @property
    def duration(self):
        return self.video.duration if self.video else 1

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
        self.change_point = time.time()
        self._is_play = play

    def play(self):
        self.is_play = True

    def pause(self):
        self.is_play = False

    def move_process(self, position):
        self.position = position if position < self.duration else self.duration
        self.change_point = time.time()

    def change_video(self, video_id):
        video = Video.get_video_by_id(video_id=video_id)
        if not video:
            raise KeyError()
        else:
            self.video = video
        
        self.is_play = False
        self.position = 0
        self.change_point = time.time()

    def get_position(self):
        return 0 if not self.url else (self.position if not self.is_play else (self.position + time.time()-self.change_point))

    def get_isPlay(self):
        if self.url and self.is_play:
            return 1
        else:
            return 0
        # return int(self.url and self.is_play)

    def get_video_status(self):
        return {
            'url': self.url,
            'position': self.get_position(),
            'isPlay': self.get_isPlay(),
            'duration': self.duration,
            'videoName': self.videoName
        }

# 一个会议室
class MeetingRoom:
    def __init__(self, meeting_id) -> None:
        self.member_list = {}
        self.meeting_id = meeting_id
        meeting = Meeting.get_meeting_by_id(meeting_id=meeting_id)
        self.manager_id = meeting.ownerId
        self.player:VideoPlayer = VideoPlayer()
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
        video = self.player.video
        if not video:
            return []

        comments = video.comment
        result = []
        for comment in comments:
            result.append({
                'fromId': comment.fromId,
                'fromName': comment.fromName,
                'imageUrl': comment.image,
                'content': comment.content,
                'position': comment.position
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
