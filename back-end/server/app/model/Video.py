from __future__ import annotations

from . import db
from ..utils import safe_objectId, captrueFrameUtil, ossDetectObject
from typing import List
import time

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
    createDate = db.FloatField(required=True)

    size = db.IntField(required=False)
    frameRate = db.FloatField(required=False)
    comment = db.ListField(db.EmbeddedDocumentField(Comment), default=[])
    password = db.StringField(default='')
    description = db.StringField(default='')
    hasReview = db.IntField(default=0)
    reviewResult = db.IntField(default=0)
    reviewSummary = db.StringField(default='')   
    alive = db.BooleanField(default=True)
    tags = db.ListField(db.StringField(), required=False)

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
        '''删除视频

        删除一个视频, 移除和用户之间的引用.
        由于在设定上, 视频是属于项目的, 所以必须在项目的作用域中调用此方法, 禁止在项目之外的地方调用此方法.
        即应该通过 Project.remove_video 方法来删除视频.
        同时, 应该在项目的方法中删除对此视频的引用.

        Args:
            无
        
        Returns:
            无
        
        Raises:
            无
        '''
        # 删除用户下相关信息
        user = User.get_user_by_id(self.owner, deep=True)
        video_id = str(self.id)
        if video_id in user.uploadVideo:
            user.uploadVideo.remove(video_id)

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

    def delete_comment(self, comment_id: int, user:User)->None:
        i, j = 0, len(self.comment)
        m = 0
        target_comment = None
        # 二分搜索目标批注
        while i<j:
            m = (i+j)//2
            comment:Comment = self.comment[m]
            if comment.commentId == comment_id:
                target_comment = comment
                break
            elif comment.commentId < comment_id:
                i = m+1
            else:
                j = m
        if not target_comment:
            return 0, '无此批注'
        
        if target_comment.fromId != str(user.id):
            return 0, '你不能删除此批注'
        
        del self.comment[m]
        self.save()
        return 1, ''

    def get_video_info(self)->dict:
        project = Project.get_project_by_id(project_id=self.belongTo)
        return {
            'videoId': str(self.id),
            'videoName': self.videoName,
            'uploader': self.owner,
            'duration': self.duration,
            'covers': self.cover,
            'project': project.projectName,
            'description': self.description,
            'createDate': self.createDate,
            'url': self.url,
            'tags': self.tags
        }

    def generate_covers(self)->None:
        key = self.url[self.url.find('aliyuncs.com/')+len('aliyuncs.com/'):]
        covers = captrueFrameUtil.oss_capture_frame(key=key, duration=self.duration, user_id=self.owner)
        self.cover = covers
        self.save()
        self.generate_tags()

    def generate_tags(self)->None:
        tags = []
        for cover_url in self.cover[:1]:
            tags += ossDetectObject.detect_image(cover_url)
        
        self.tags = list(set(tags))
        self.save()

from .User import User
from .Project import Project