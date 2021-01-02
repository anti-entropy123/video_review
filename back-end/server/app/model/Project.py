from __future__ import annotations

from ..utils import safe_objectId
from . import Project, User, db, Video, Meeting
from typing import List

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
        '''确认加入项目的邀请.

        处理邀请用户加入项目的邀请(可以同意或者拒绝). 并且需维护成员相关字段以保持一致性. 

        Args: 
            user: 被邀请加入项目的用户实例, 其user id应该在waitJoin数组中.
            is_agree: 是否同意加入项目.

        Returns:
            无

        Raises:
            无
        '''
        try:
            self.waitJoin.remove(str(user.id))
        except ValueError as e:
            pass
        # 如果同意邀请
        if is_agree:
            # 需要检查是否已经在项目中了, 避免重复
            str(user.id) in self.member_id_list() or self.member.append(ProjectMember(userId=str(user.id)))
            str(self.id) in user.joinProject or user.joinProject.append(str(self.id))
            user.save()

        self.save()


    def remove_video(self, video_id:str):
        '''从项目中删除一个视频

        从项目中删除视频, 且在self.hasVideo字段中移除对此视频的引用, 以保持数据完整性.
        如果项目中没有此视频, 则什么都不做.

        Args:
            video_id: 此项目中的视频的 id. 如果video id不在项目中, 则什么也不做.
            
        Returns:
            无.
 
        Raises:
            无.
        '''
        if not video_id in self.hasVideo:
            return
        
        video = Video.get_video_by_id(video_id=video_id, deep=True).delete_video()
        try:
            self.hasVideo.remove(video_id)
        except ValueError as e:
            print('项目中没有视频', video_id)

        self.save()

    def remove_member(self, user:User):
        '''从项目中移除一个用户.
        
        从项目中移除一个成员.
        同时应该在self.member中移除此成员, 并且在user.hasProject或user.joinProject中移除对此项目的引用, 以保证一致性.
        当项目需要解散时, 也需要对项目owner调用此方法.

        Args:
            user: User的一个实例, 代表要删除的用户
        
        Returns:
            无
        
        Raises:
            无
        '''
        is_owner = self.owner == str(user.id)
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
        
        # ! 不应该在model中发送消息.
        # # 如果是项目负责人解散或者成员自己退出, 则不需要发通知
        # if not (is_owner or is_leave):
        #     new_message = Message(
        #         fromId = self.owner,
        #         fromName = User.get_user_by_id(self.owner).username,
        #         projectId = str(self.id),
        #         projectName = str(self.projectName),
        #         type = 5,
        #         date = time.time()
        #     )
        #     new_message.fill_content()
        #     user.receive_message(new_message)
       
    
    def dissolution(self):
        '''解散本项目

        解散项目, 包括删除所有的会议, 视频, 和成员.
        具体流程:
            1. 删除项目下所有的会议.
            2. 删除项目下所有的视频
            3. 移除项目的所有成员(需保证移除用户对此项目的引用.) 
            4. 删除自身

        Args:
            无

        Returns:
            无

        Raises:
            无
        '''
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
        self.remove_member(owner)
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
