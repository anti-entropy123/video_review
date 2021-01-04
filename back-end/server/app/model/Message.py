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

    content = db.EmbeddedDocumentField(MessageContent, required=False)
    hasProcess = db.IntField(default=0)
    hasRead = db.IntField(default=0)

    def fill_content(self, **kwargs):
        '''为消息实例填入内容参数(不推荐使用)
        
        不同类型的参数有不同的内容参数. 调用本方法会根据消息的类型, 从传入的参数
        中选择所需的填入成员变量.

        Args:
            videoName: 视频名称
            reviewResult: 审阅结果
            meetingId: 会议id
            word: 邀请附加消息
            processResult: 处理结果
        
        Returns:
            无
        
        Raises:
            无
        '''
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
    
    def upload_new_video_message(self, video_name:str):
        self.type = 0
        self.content = MessageContent(videoName=video_name)
    
    def video_has_reviewd(self, video_name:str, review_result:bool):
        self.type = 1
        self.content = MessageContent(videoName = video_name, reviewResult = review_result)

    def book_new_meeting(self, meeting_id:str):
        self.type = 2
        self.content = MessageContent(meetingId=meeting_id)
    
    def invite_join_project(self, word:str):
        self.type = 3
        self.content = MessageContent(word=word)

    def invite_has_processed(self, process_result:bool):
        self.type = 4
        self.content = MessageContent(processResult=process_result)

    def remove_project_member(self):
        self.type = 5
        self.content = MessageContent(word="")

    def __str__(self):
        sentence = ""
        if self.type == 0:
            sentence = f"{self.fromName}在项目《{self.projectName}》中上传了新的视频: 《{self.content['videoName']}》"
        elif self.type == 1:
            sentence = f"你上传的视频《{self.content['videoName']}》被{self.fromName}审阅了"
        elif self.type == 2:
            sentence = f"{self.fromName}为项目《{self.projectName}》预定了新的审阅会议"
        elif self.type == 3:
            sentence = f"{self.fromName}邀请你加入项目《{self.projectName}》"
        elif self.type == 4:
            sentence = f"{self.fromName}{'同意' if self.content['processResult'] else '拒绝'}加入项目《{self.projectName}》"
        elif self.type == 5:
            sentence = f"你已被移出项目《{self.projectName}》"