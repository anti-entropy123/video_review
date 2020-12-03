from __future__ import annotations

import time
from typing import List

from bson.objectid import ObjectId

from . import db
from .utils import safe_objectId


class Message(db.EmbeddedDocument):
    # messageId = db.StringField(required=True, unique=True)
    fromId = db.StringField(required=True)
    fromName = db.StringField(required=True)
    projectId = db.StringField(required=True)
    projectName = db.StringField(required=True)
    type = db.IntField(required=True)
    content = db.DictField(required=True)
    messageId = db.IntField(required=True)

    hasProcess = db.IntField(default=0)
    hasRead = db.IntField(default=0)
    date = db.FloatField(default=time.time())

    def __str__(self):
        return f'消息: {self.content}'


class User(db.Document):
    username = db.StringField(required=True)
    password = db.StringField(required=True)
    mobileNum = db.StringField(required=True)

    mail = db.StringField(default='')
    avatar = db.StringField(default='')
    company = db.StringField(default='')
    # 自己创建的项目
    hasProject = db.ListField(db.StringField(), default=[]) 
    # 加入的项目
    joinProject = db.ListField(db.StringField(), default=[])
    uploadVideo = db.ListField(db.StringField(), default=[])
    message = db.ListField(db.EmbeddedDocumentField(Message), default=[])
    hasMeeting = db.ListField(db.StringField(), default=[])
    admin = db.BooleanField(default=False)
    alive = db.BooleanField(default=True)

    def __str__(self):
        return f"用户: {self.username}"
    
    @classmethod
    def has_user(cls, userId:str):
        return bool(cls.objects(id=safe_objectId(userId), alive=True))

    @classmethod
    def get_user_by_id(cls, user_id:str)->User:
        return cls.objects(id=safe_objectId(user_id), alive=True).first()

    @classmethod
    def get_user_by_mobileNum(cls, mobileNum)->User:
        return User.objects(mobileNum=mobileNum, alive=True).first()

    def receive_message(self, message: Message):
        message.messageId = len(self.message)
        self.message.append(message)
        self.save()

    def get_message_by_id(self, message_id:int):
        message_id = int(message_id)
        if message_id >= len(self.message):
            return None
        return self.message[int(message_id)]
    
    def read_message(self, message_id:int):
        self.message[int(message_id)].hasRead = 1
        self.save()

    def process_message(self, message_id:int):
        self.message[message_id].hasProcess = 1
        self.save()

class ProjectMember(db.EmbeddedDocument):
    userId = db.StringField(primary_key=True, required=True, db_field='_id')
    
    title = db.StringField(default='审阅人员')

class Project(db.Document):
    projectName = db.StringField(required=True)
    owner = db.StringField(required=True)

    member = db.ListField(db.EmbeddedDocumentField(ProjectMember), default=[])
    waitJoin = db.ListField(db.StringField(), default=[])
    hasVideo = db.ListField(db.StringField(), default=[])
    hasMeeting = db.ListField(db.StringField(), default=[])
    alive = db.BooleanField(default=True)

    def __str__(self):
        return f"项目: {self.projectName}"

    @classmethod
    def has_project(cls, project_id:str):
        return bool(cls.objects(id=safe_objectId(project_id), alive=True))

    @classmethod
    def get_project_by_id(cls, project_id:str)->Project:
        return cls.objects(id=safe_objectId(project_id), alive=True).first()

    def wait_to_user_join(self, user_id:str):
        self.waitJoin.append(user_id)
        self.save()
    
    # 项目解散
    def dissolution(self):
        # 删除项目下所有的会议
        meetings_id = self.hasMeeting
        for meeting_id in meetings_id:
            Meeting.get_meeting_by_id(meeting_id=meeting_id).delete_meeting()
        # 删除项目下所有的视频
        videos_id = self.hasVideo
        for video_id in videos_id:
            Video.get_video_by_id(video_id=video_id).delete_video()
        # 删除所有项目成员
        users_id = [member.userId for member in self.member]
        for user_id in users_id:
            user = User.get_user_by_id(user_id)
            user.joinProject.remove(str(self.id))
            user.save()
        owner = User.get_user_by_id(self.owner)
        owner.hasProject.remove(str(self.id))
        owner.save()
        # 删除自身
        self.alive = False
        self.save()

class Comment(db.EmbeddedDocument):
    commentId = db.IntField(required=True)
    fromId = db.StringField(required=True)
    fromName = db.StringField(required=True)
    position = db.IntField(required=True)
    image = db.StringField(required=True)
    content = db.StringField(required=True)
    
    alive = db.BooleanField(default=True)
    
    def __str__(self):
        return f"批注: {self.content}"

class Video(db.Document):
    videoName = db.StringField(required=True)
    owner = db.StringField(required=True)
    duration = db.IntField(required=True)
    permission = db.IntField(required=True)
    url = db.StringField(required=True)
    cover = db.ListField(db.StringField(), required=True, max_length=50)
    belongTo = db.StringField(required=True)

    comment = db.ListField(db.EmbeddedDocumentField(Comment), default=[])    
    password = db.StringField(default='')
    description = db.StringField(default='')
    hasReview = db.IntField(default=0)
    reviewResult = db.IntField(default=0)
    reviewSummary = db.StringField(default='')
    createDate = db.FloatField(default=time.time())
    alive = db.BooleanField(default=True)

    def __str__(self):
        return f"视频: {self.videoName}"

    @classmethod
    def get_video_by_id(cls, video_id)->Video:
        return cls.objects(id=safe_objectId(video_id), alive=True).first()

    def delete_video(self):
        # 删除用户下相关信息
        user = User.get_user_by_id(self.owner)
        user.uploadVideo.remove(str(self.id))
        user.save()
        # TODO 将来可以考虑删除COS中的视频文件
        # 删除自身
        self.alive = False
        self.save()

class Meeting(db.Document):
    title = db.StringField(required=True)
    ownerId = db.StringField(required=True)
    ownerName = db.StringField(required=True)
    belongTo = db.StringField(required=True)
    startTime = db.FloatField(required=True)
    endTime = db.FloatField(required=True)
    meetingUrl = db.StringField(required=True)
    txMeetingId = db.StringField(required=True)
    
    note = db.StringField(default="")
    alive = db.BooleanField(default=True)

    def __str__(self) -> str:
        return f"会议: {self.title}"

    @classmethod
    def get_meeting_by_id(cls, meeting_id)->Meeting:
        return cls.objects(id=safe_objectId(meeting_id), alive=True).first()

    @classmethod
    def get_meeting_by_projectId(cls, project_id)->List[Meeting]:
        return cls.objects(belongTo=project_id, alive=True)
    
    @classmethod
    def get_meeting_by_ownerId(cls, user_id:str)->List[Meeting]:
        return cls.objects(ownerId=user_id, alive=True)
    
    def delete_meeting(self):
        # 删除用户下的数据
        user = User.get_user_by_id(self.ownerId)
        user.hasMeeting.remove(str(self.id))
        user.save()
        # 删除自身
        self.alive = False
        self.save()
    
        
        