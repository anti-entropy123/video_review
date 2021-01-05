from __future__ import annotations

from . import db
from ..utils import safe_objectId, captrueFrameUtil, ossDetectObject
from typing import Dict, List, Tuple
import time

class Reply(db.EmbeddedDocument):
    fromId = db.StringField(required=True)
    content = db.StringField(required=True)
    date = db.FloatField(required=True)

    replyId = db.IntField(required=False)
    replyTo = db.IntField(required=False) # 回复至哪个回复, 如果是回复某个批注而非回复, 则可以为空.
    alive = db.BooleanField(default=True)

    def __str__(self) -> str:
        return f"批注回复: {self.content}"

class Comment(db.EmbeddedDocument):
    fromId = db.StringField(required=True)
    position = db.FloatField(required=True)
    image = db.StringField(required=True)
    content = db.StringField(required=True)
    date = db.FloatField(required=True)

    commentId = db.IntField(required=False)
    fromName = db.StringField(required=False) # 既然头像每次都需要查一遍库, 那我何必这里还存一次姓名呢
    replies = db.ListField(db.EmbeddedDocumentField(Reply), required=False)
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
        user_cache:Dict[str, User] = {}
        def take_user_from_cache(user_id:str)->User:
            if user_id in user_cache:
                return user_cache[user_id]
            else:
                user = User.get_user_by_id(user_id=user_id, deep=True)
                user_cache[user_id] = user
                return user

        for comment_id, comment in enumerate(comments):
            if deep or comment.alive:
                replies = []
                for reply_id, reply in enumerate(comment.replies or []):
                    reply:Reply
                    from_user:User = take_user_from_cache(reply.fromId)
                    _reply = {}
                    _reply['replyId'] = reply_id
                    _reply['fromId'] = reply.fromId
                    _reply['fromName'] = from_user.username
                    _reply['avatar'] = from_user.avatar
                    _reply['content'] = reply.content if reply.alive else '已删除'
                    if reply.replyTo:
                        replyToUserId:str = comment.replies[reply.replyTo].fromId
                        to_user = take_user_from_cache(replyToUserId)                   
                        _reply['replyToName'] = to_user.username
                        _reply['replyToId'] = replyToUserId

                    replies.append(_reply)

                result.append({
                    'commentId': comment_id,
                    'fromId': comment.fromId,
                    'fromName': comment.fromName,
                    'imageUrl': comment.image if comment.alive else '',
                    'content': comment.content if comment.alive else '已删除',
                    'position': comment.position,
                    'avatar': User.get_user_by_id(comment.fromId, deep=True).avatar,
                    'date': comment.date,
                    'replies': replies if comment.alive else []
                })

        return result

    def insert_comment(self, comment:Comment, from_user:User=None)->int:
        '''新建一条批注

        新建一条批注. 可以缺省comment id, date, from_id等参数.

        Args:
            comment: 要保存的批注的实例
            from_user: 批注的创建者. 如果comment内包含了from_id,
                       则可以缺省.
        
        Returns:
            comment_id: 此批注的id
        
        Raises:
            无
        '''
        if from_user:
            comment.fromId = str(from_user.id)
            # comment.fromName = from_user.username

        comment_Id = len(self.comment)
        comment.date = time.time()
        self.comment.append(comment)
        self.save()
        return comment_Id

    def insert_reply(self, reply:Reply, comment_id:int, from_user:User=None)->int:
        '''新建一条批注的回复

        新建一条批注回复. 可以缺省reply id, date, from_id等参数.

        Args:
            reply: 要保存的批注的实例
            from_user: 批注回复的创建者. 如果 reply 内包含了
                       from_id, 则可以缺省.
        
        Returns:
            replyId: 此回复的id
        
        Raises:
            无
        '''
        comment:Comment = self.comment[comment_id]
        if not comment.replies:
            comment.replies = []
        
        reply_id = len(comment.replies)
        reply.date = time.time()
        if from_user:
            reply.fromId = str(from_user.id)
        comment.replies.append(reply)
        self.save()
        return reply_id

    def delete_comment(self, comment_id: int, user:User)->Tuple[int, str]:
        '''删除视频下某一条批注

        根据comment id删除批注. 因为comment id是递增的int变量, 所以可以
        根据id直接索引对应的批注. 同时删除时不应该直接将批注从数组中删除, 
        而是修改其alive字段为 false.

        Args: 
            comment_id: 批注id
            user: 进行此操作的用户(用以判断是否有权限删除)
        
        Returns:
            代表操作结果的二元组
            (result, message)
            例如: (1, '') 或者 (0, '没有权限')
        
        Raises:
            无
        '''
        # i, j = 0, len(self.comment)
        # m = 0
        # target_comment = None
        # # 二分搜索目标批注
        # while i<j:
        #     m = (i+j)//2
        #     comment:Comment = self.comment[m]
        #     if comment.commentId == comment_id:
        #         target_comment = comment
        #         break
        #     elif comment.commentId < comment_id:
        #         i = m+1
        #     else:
        #         j = m
        if not comment_id > len(self.comment):
            return 0, '无此批注'
        
        target_comment:Comment = self.comment[comment_id]
        if target_comment.fromId != str(user.id):
            return 0, '你不能删除此批注'
        
        self.comment[comment_id].alive = False
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