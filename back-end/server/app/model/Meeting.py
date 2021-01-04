from __future__ import annotations

from typing import List

from ..utils import safe_objectId
from . import db


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
        '''删除项目中的一个会议

        删除项目中的一个会议, 移除和用户之间的引用.
        由于在设定上, 会议是属于项目的, 所以必须在项目的作用域中调用此方法, 禁止在项目之外的地方调用此方法.
        同时, 应该在项目的方法中删除对此会议的引用.

        Args:
            无
        
        Returns:
            无
        
        Raises:
            无
        '''
        user = User.get_user_by_id(self.ownerId, deep=True)
        try:
            user.hasMeeting.remove(str(self.id))
        except KeyError as e:
            print('用户', user, '没有建立会议', self)
        
        user.save()
        # 删除自身
        self.alive = False
        self.save()

from .User import User
