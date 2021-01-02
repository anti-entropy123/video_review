from __future__ import annotations

from werkzeug.security import check_password_hash

from ..utils import safe_objectId
from . import db, Message


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
        '''用户接收到一条消息

        用户接收到一条新的消息

        Args:
            message: 一个Message实例, 即发送给此用户的消息的内容.

        Returns:
            无

        Raises:
            无
        '''
        message.messageId = len(self.message)
        self.message.append(message)
        self.save()

    def get_message_by_id(self, message_id:int)->Message:
        '''根据消息id获取此用户的消息

        根据消息id获取此用户的消息, 如果用户没有此id的消息, 会返回空. 

        Args:
            message_id: 消息id, 大于等于0的整数. 

        Returns:
            消息类的一个实例, 代表需要获取的消息id.
        
        Raises:
            无
        '''
        message_id = int(message_id)
        if message_id >= len(self.message):
            return None
        # 这里假设消息不会从数组中移除
        return self.message[int(message_id)]
    
    def read_message(self, message_id:int):
        self.message[int(message_id)].hasRead = 1
        self.save()

    def process_message(self, message_id:int):
        self.message[message_id].hasProcess = 1
        self.save()
