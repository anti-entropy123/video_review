from __future__ import annotations

import time

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
    hasProject = db.ListField(db.StringField(), default=[])
    joinProject = db.ListField(db.StringField(), default=[])
    uploadVideo = db.ListField(db.StringField(), default=[])
    message = db.ListField(db.EmbeddedDocumentField(Message), default=[])
    hasMeeting = db.ListField(db.StringField(), default=[])

    def __str__(self):
        return f"用户: {self.username}"
    
    @classmethod
    def has_user(cls, userId:str):
        return bool(cls.objects(id=safe_objectId(userId)))

    @classmethod
    def get_user_by_id(cls, user_id:str)->User:
        return cls.objects(id=safe_objectId(user_id)).first()

    def receive_message(self, message: Message):
        message.messageId = len(self.message)
        self.message.append(message)
        self.save()

    def get_message_by_id(self, message_id:int):
        return self.message[message_id]
    
    def read_message(self, message_id:int):
        self.message[message_id].hasRead = 1
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

    def __str__(self):
        return f"项目: {self.projectName}"

    @classmethod
    def has_project(cls, project_id:str):
        return bool(cls.objects(id=safe_objectId(project_id)))

    @classmethod
    def get_project_by_id(cls, project_id:str)->Project:
        return cls.objects(id=safe_objectId(project_id)).first()

    def wait_to_user_join(self, user_id:str):
        self.waitJoin.append(user_id)
        self.save()

class Comment(db.EmbeddedDocument):
    from_ = db.StringField(db_field='from', required=True)
    fromName = db.StringField(required=True)
    position = db.IntField(required=True)
    image = db.StringField(required=True)
    content = db.StringField(required=True)

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
    
    def __str__(self):
        return f"视频: {self.videoName}"

    @classmethod
    def get_video_by_id(cls, video_id)->Video:
        return cls.objects(id=safe_objectId(video_id)).first()

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

    def __str__(self) -> str:
        return f"会议: {self.title}"

    @classmethod
    def get_meeting_by_id(cls, meeting_id)->Meeting:
        return cls.objects(id=safe_objectId(meeting_id)).first()
