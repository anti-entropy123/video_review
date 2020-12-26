from __future__ import annotations

import time
from typing import List

from werkzeug.security import check_password_hash

from . import db
from .utils import safe_objectId


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

class User(db.Document):
    username = db.StringField(required=True)
    mobileNum = db.StringField(required=True)

    openId = db.StringField(required=False)
    password = db.StringField(required=False)
    mail = db.StringField(default='')
    avatar = db.StringField(default='https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png')
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
    def has_user(cls, userId:str, deep:bool=False)->bool:
        select = {
            'id': safe_objectId(userId)
        }
        if not deep:
            select['alive'] = True

        return bool(cls.objects(**select))

    @classmethod
    def get_user_by_id(cls, user_id:str, deep:bool=False)->User:
        select = {
            'id': safe_objectId(user_id)
        }
        if not deep:
            select['alive'] = True

        return cls.objects(**select).first()

    @classmethod
    def get_user_by_openId(cls, open_id:str, deep:bool=False)->User:
        select = {
            'openId': open_id
        }
        if not deep:
            select['alive'] = True

        return cls.objects(**select).first()

    @classmethod
    def get_user_by_mobileNum(cls, mobileNum, deep:bool=False)->User:
        select = {
            'mobileNum': mobileNum
        }
        if not deep:
            select['alive'] = True

        return cls.objects(**select).first()

    def verify_password(self, password:str)->bool:
        pwhash = self.password
        if not pwhash:
            return False
            
        return check_password_hash(pwhash=pwhash, password=password)

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
    def has_project(cls, project_id:str, deep:bool=False):
        select = {
            'id': safe_objectId(project_id)
        }
        if not deep:
            select['alive'] = True

        return bool(cls.objects(**select))

    @classmethod
    def get_project_by_id(cls, project_id:str, deep:bool=False)->Project:
        select = {
            'id': safe_objectId(project_id)
        }
        if not deep:
            select['alive'] = True

        return cls.objects(**select).first()

    def wait_to_user_join(self, user_id:str):
        self.waitJoin.append(user_id)
        self.save()
    
    def confirm_to_join(self, user:User, is_agree:bool):
        try:
            self.waitJoin.remove(str(user.id))
        except ValueError as e:
            pass

        if is_agree:
            # 同意邀请
            self.member.append(
                ProjectMember(userId=str(user.id))
            )
            user.joinProject.append(str(self.id))
            user.save()

        self.save()

    # 删除项目下的视频
    def remove_video(self, video_id:str):
        if not video_id in self.hasVideo:
            return
        
        video = Video.get_video_by_id(video_id=video_id, deep=True).delete_video()
        try:
            self.hasVideo.remove(video_id)
        except ValueError as e:
            print('项目中没有视频', video_id)
        self.save()

    def remove_member(self, user:User, is_leave:bool=True, is_owner=False):
        try:
            if is_owner:
                user.hasProject.remove(str(self.id))
            else:
                user.joinProject.remove(str(self.id))
            user.save()
        except ValueError as e:
            pass
        
        if not is_owner:
            try:
                i = self.member_id_list().index(str(user.id))
                del self.member[i]
                self.save()
            except ValueError as e:
                print(self, '没有此成员', user)
            
        # 如果是项目负责人解散或者成员自己退出, 则不需要发通知
        if not (is_owner or is_leave):
            new_message = Message(
                fromId = self.owner,
                fromName = User.get_user_by_id(self.owner).username,
                projectId = str(self.id),
                projectName = str(self.projectName),
                type = 5,
                date = time.time()
            )
            new_message.fill_content()
            user.receive_message(new_message)
       
    

    # 项目解散
    def dissolution(self):
        # 删除项目下所有的会议
        meetings_id = self.hasMeeting
        for meeting_id in meetings_id:
            Meeting.get_meeting_by_id(meeting_id=meeting_id, deep=True).delete_meeting()
        # 删除项目下所有的视频
        videos_id = self.hasVideo
        for video_id in videos_id:
            Video.get_video_by_id(video_id=video_id, deep=True).delete_video()
        # 删除所有项目成员
        for user_id in self.member_id_list():
            user = User.get_user_by_id(user_id, deep=True)
            self.remove_member(user)

        owner = User.get_user_by_id(self.owner, deep=True)
        self.remove_member(owner, is_owner=True)
        # 删除自身
        self.alive = False
        self.save()

    def member_id_list(self)->List[str]:
        return [member.userId for member in self.member]

    def __contains__(self, key):
        object_id = str(key.id)
        # 用户
        if isinstance(key, User):
            # print(object_id, self.member_id_list(), object_id in self.member_id_list())
            return object_id == self.owner or object_id in self.member_id_list()
        # 视频
        elif isinstance(key, Video):
            return object_id in self.hasVideo
        # 会议
        elif isinstance(key, Meeting):
            return object_id in self.hasMeeting
        else:
            return False

class Comment(db.EmbeddedDocument):
    commentId = db.IntField(required=True)
    fromId = db.StringField(required=True)
    fromName = db.StringField(required=True)
    position = db.FloatField(required=True)
    image = db.StringField(required=True)
    content = db.StringField(required=True)
    date = db.FloatField(required=True)
    
    alive = db.BooleanField(default=True)
    
    def __str__(self):
        return f"批注: {self.content}"

class Video(db.Document):
    videoName = db.StringField(required=True)
    owner = db.StringField(required=True)
    duration = db.FloatField(required=True)
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
    def get_video_by_id(cls, video_id, deep:bool=False)->Video:
        select = {
            'id': safe_objectId(video_id)
        }
        if not deep:
            select['alive'] = True

        return cls.objects(**select).first()

    def delete_video(self):
        # 删除用户下相关信息
        user = User.get_user_by_id(self.owner, deep=True)
        try:
            user.uploadVideo.remove(str(self.id))
        except KeyError as e:
            print('用户', user, '没有上传', self)
        user.save()
        # TODO 将来可以考虑删除COS中的视频文件
        # 删除自身
        self.alive = False
        self.save()
    
    def set_review_result(self, result:bool, summary:str):
        self.reviewResult = result
        self.reviewSummary = summary
        self.hasReview = True
        self.save()

    def get_comment_list(self, deep:bool=False)->List:
        comments:List[Comment] = self.comment
        result = []
        for comment in comments:
            if deep or comment.alive:
                result.append({
                    'commentId': comment.commentId,
                    'fromId': comment.fromId,
                    'fromName': comment.fromName,
                    'imageUrl': comment.image,
                    'content': comment.content,
                    'position': comment.position,
                    'avatar': User.get_user_by_id(comment.fromId, deep=True).avatar,
                    'date': comment.date
                })

        return result

    def insert_comment(self, comment:Comment, from_user:User=None)->int:
        if from_user:
            comment.fromId = str(from_user.id)
            comment.fromName = from_user.username

        comment.commentId = len(self.comment)
        comment.date = time.time()
        self.comment.append(comment)
        self.save()
        return comment.commentId

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
    def get_meeting_by_id(cls, meeting_id, deep:bool=False)->Meeting:
        select = {
            'id': safe_objectId(meeting_id)
        }
        if not deep:
            select['alive'] = True

        return cls.objects(**select).first()

    @classmethod
    def get_meeting_by_projectId(cls, project_id, deep:bool=False)->List[Meeting]:
        select = {
            'belongTo': project_id
        }
        if not deep:
            select['alive'] = True

        return cls.objects(**select)
    
    @classmethod
    def get_meeting_by_ownerId(cls, user_id:str, deep:bool=False)->List[Meeting]:
        select = {
            'ownerId': user_id
        }
        if not deep:
            select['alive'] = True

        return cls.objects(**select)
    
    def delete_meeting(self):
        # 删除用户下的数据
        user = User.get_user_by_id(self.ownerId, deep=True)
        try:
            user.hasMeeting.remove(str(self.id))
        except KeyError as e:
            print('用户', user, '没有建立会议', self)
        
        user.save()
        # 删除自身
        self.alive = False
        self.save()
    
        
        