from . import client
from bson.objectid import ObjectId

db = client.db

class User:
    @staticmethod
    def find_username_by_userId(user_id: str)->str:
        user = db.user.find_one(
            {'_id': ObjectId(user_id)}, 
            {'username': 1}
        )
        if not user:
            return None
        else:
            return user['username']
    
    @staticmethod
    def has_user(user_id: str)->bool:
        user = db.user.find_one(
            {'_id': ObjectId(user_id)}, 
            {'_id': 1}
        )
        return bool(user)

    @staticmethod
    def send_message_to_user(user_id:str, message:dict):
        db.user.update(
            {'_id': ObjectId(user_id)},
            {'$addToSet': 
                {"message": message}}
        )

    @staticmethod
    def find_message_by_id(user_id:str, message_id:str):
        user = db.user.find_one(
            {'_id': ObjectId(user_id)}, 
            {'message.fromId': 1})
        if user:
            return user['message'][int(message_id)]
        else:
            return None
            
    @staticmethod
    def set_message_process(user_id:str, message_id:str):
        db.user.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': 
                {'message.'+message_id+'.hasProcess': 1}
            }
        )   

    @staticmethod
    def upload_video(user_id, video_id):
        db.user.update(
            {'_id': ObjectId(user_id)},
            {'$addToSet': 
                {'uploadVideo': str(video_id)}}
        )
    
    @staticmethod
    def get_video_list(user_id):
        video_list = list(db.user.find_one(
            {'_id': ObjectId(user_id)},
            {'uploadVideo': 1}
        )['uploadVideo'])
        return [ObjectId(i) for i in video_list]

class Project:
    @staticmethod
    def create_project(project_name:str, owner_id:str) -> str:
        inserted = db.project.insert_one({
            'projectName': project_name,
            'owner': owner_id,
            'member': [],
            'waitJoin': [],
            'hasVideo': []
        })
        return inserted.inserted_id
    
    @staticmethod
    def find_name_by_projectId(project_id: str)->str:
        project = db.project.find_one(
            {'_id': ObjectId(project_id)},
            {'projectName': 1}
        )
        if not project:
            return None
        else:
            return project['projectName']

    @staticmethod
    def has_project_name(project_name: str)->bool:
        if db.project.find(
                {'projectName': project_name},
                {'_id': 1}).count():
            return True
    
    @staticmethod
    def process_invite(project_id, user_id, is_agree):
        operation = {}
        operation['$pull'] = {'waitJoin': user_id} 
        # 是否同意加入
        if int(is_agree):
            operation['$addToSet'] = {
                'member': {
                    'userId': user_id, 
                    'title': '成员'}
                }
        
        db.project.update_one(
            {'_id': ObjectId(project_id)},
            operation
        )

    @staticmethod
    def add_video(project_id, video_id):
        db.project.update(
            {'_id': ObjectId(project_id)},
            {'$addToSet':
                {'hasVideo': str(video_id)}}
        )

class Video:
    @staticmethod
    def create_video(video_name, duration, permission, url, cover ,password=''):
        inserted = db.video.insert_one({
            'videoName': video_name,
            'duration': duration,
            'permission': permission,
            'password': password,
            'url': url,
            'hasReview': 0,
            'reviewResult': -1,
            'reviewSummary': '',
            'cover': cover,
            'comment': []
        })
        return inserted.inserted_id

    @staticmethod
    def finish_review(video_id, review_result, summary):
        db.video.update(
            {'_id': ObjectId(video_id)},
            {'$set': 
                {'hasReview': 1, 
                'reviewResult': review_result,
                'reviewSummary': summary}
            }
        )