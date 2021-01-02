from __future__ import annotations

from . import db

class MessageContent(db.EmbeddedDocument):
    videoName = db.StringField(required=False)
    reviewResult = db.StringField(required=False)
    meetingId = db.StringField(required=False)
    word = db.StringField(required=False)
    processResult = db.BooleanField(required=False)

    # type = 0
    @classmethod
    def upload_new_video_message(cls, video_name:str, **kwargs)->MessageContent:
        return MessageContent(videoName=video_name)
    
    # type = 1
    @classmethod
    def video_has_reviewd(cls, video_name:str, review_result:bool, **kwargs)->MessageContent:
        return MessageContent(videoName = video_name, reviewResult = review_result)

    # type = 2
    @classmethod
    def book_new_meeting(cls, meeting_id:str, **kwargs)->MessageContent:
        return MessageContent(meetingId=meeting_id)
    
    # type = 3
    @classmethod
    def invite_join_project(cls, word:str, **kwargs)->MessageContent:
        return MessageContent(word=word)

    # type = 4
    @classmethod
    def invite_has_processed(cls, process_result:bool, **kwargs)->MessageContent:
        return MessageContent(processResult=process_result)

    # type = 5
    @classmethod
    def remove_project_member(cls, **kwargs)->MessageContent:
        return MessageContent(word="")

class Message(db.EmbeddedDocument):
    # messageId = db.StringField(required=True, unique=True)
    fromId = db.StringField(required=True)
    fromName = db.StringField(required=True)
    projectId = db.StringField(required=True)
    projectName = db.StringField(required=True)
    type = db.IntField(required=True)
    messageId = db.IntField(required=True)
    date = db.FloatField(required=True)
    content = db.EmbeddedDocumentField(MessageContent, required=True)
    
    hasProcess = db.IntField(default=0)
    hasRead = db.IntField(default=0)

    def __str__(self):
        return f'消息: {self.content}'

    def fill_content(self, **kwargs):
        content = None
        if self.type == 0:
            content = MessageContent.upload_new_video_message(**kwargs)
        elif self.type == 1:
            content = MessageContent.video_has_reviewd(**kwargs)
        elif self.type == 2:
            content = MessageContent.book_new_meeting(**kwargs)
        elif self.type == 3:
            content = MessageContent.invite_join_project(**kwargs)
        elif self.type == 4:
            content = MessageContent.invite_has_processed(**kwargs)
        elif self.type == 5:
            content = MessageContent.remove_project_member(**kwargs)
        else:
            raise RuntimeError('无效的type')
        
        self.content = content
