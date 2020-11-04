from . import db
from bson.objectid import ObjectId
import time

class Message(db.EmbeddedDocument):
    fromId = db.StringField(required=True)
    fromName = db.StringField(required=True)
    projectId = db.StringField(required=True)
    projectName = db.StringField(required=True)
    type = db.IntField(required=True)
    content = db.DictField(required=True)

    hasProcess = db.IntField(default=0)
    hasRead = db.IntField(default=0)
    date = db.FloatField(default=time.time())
    
    def __str__(self):
        return f'消息: {self.content}'
    
    def send_to(self, user):
        user.message.append(self)
        user.save()

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

    def __str__(self):
        return f"用户: {self.username}"

    @classmethod
    def has_user(cls, userId:str):
        return bool(cls.objects(id=ObjectId(userId)))

class ProjectMember(db.EmbeddedDocument):
    userId = db.StringField(primary_key=True, required=True, db_field='_id')
    
    title = db.StringField(default='审阅人员')

class Project(db.Document):
    projectName = db.StringField(required=True)
    owner = db.StringField(required=True)

    member = db.ListField(db.EmbeddedDocumentField(ProjectMember), default=[])
    waitJoin = db.ListField(db.StringField(), default=[])
    hasVideo = db.ListField(db.StringField(), default=[])

    def __str__(self):
        return f"项目: {self.projectName}"

    @classmethod
    def has_project(cls, projectId:str):
        return bool(cls.objects(id=ObjectId(projectId)))

class Comment(db.EmbeddedDocument):
    from_ = db.StringField(db_field='from', required=True)
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
    
    def __str__(self):
        return f"视频: {self.videoName}"
