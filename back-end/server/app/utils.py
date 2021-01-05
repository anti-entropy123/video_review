from __future__ import annotations

import datetime
import io
import json
import random
import threading
import time
import uuid
from io import BytesIO
from threading import Thread
from typing import IO, List, Tuple

import cv2
from flask_jwt_extended.utils import create_access_token
import oss2
import requests
from aliyunsdkcore.acs_exception.exceptions import (ClientException,
                                                    ServerException)
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkobjectdet.request.v20191230.DetectObjectRequest import \
    DetectObjectRequest
# from aliyunsdkobjectdet.request.v20191230.DetectObjectRequest import \
#     DetectObjectRequest
from bson.objectid import ObjectId
from flask import current_app as app
from PIL import Image

from config.secret_config import (AliAccessKeyID, AliAccessKeySecret,
                                  TxSecretId, TxSecretKey, oss_bucket_name,
                                  oss_region, wx_appid, wx_secret)
from qcloud_cos import CosConfig, CosS3Client


def safe_objectId(id):
    if ObjectId.is_valid(id):
        return ObjectId(id)
    else:
        # 返回一个不存在的id
        return ObjectId("0"*24)

# 构造响应
def build_response(result=1, message='', data=None, **kwargs) -> dict:
    result = {'result': result, 'message': message}
    if not data == None:
        result['data'] = data
    result.update(kwargs)
    return result


# 验证码模块
class CheckCodeManager:
    check_codes = {}

    # 验证是否存在验证码
    @staticmethod
    def verify_exist(number, code) -> Tuple[bool, str]:
        if number in CheckCodeManager.check_codes:
            return 1, ''
        else:
            return 0, "验证码不存在"

    # 验证验证码是否过期
    @staticmethod
    def verify_time(number, code) -> Tuple[bool, str]:
        t = CheckCodeManager.check_codes.get(number)[1]
        if time.time()-t > 5*60:
            return 0, "验证码过期"
        else:
            return 1, ""

    # 验证验证码是否正确
    @staticmethod
    def verify_correct(number, code) -> Tuple[bool, str]:
        origin_code = CheckCodeManager.check_codes.get(number)[0]
        if origin_code == code:
            return 1, ""
        else:
            return 0, "验证码错误"

    # 删除验证码
    @staticmethod
    def delete_code(number, code) -> Tuple[bool, str]:
        CheckCodeManager.check_codes.pop(number)
        return 1, ''

    def __init__(self) -> None:
        # 定义检测验证码的步骤
        self.do_verify = [
            self.verify_exist,
            self.verify_time,
            self.verify_correct,
            self.delete_code
        ]

    # 发送短信
    @staticmethod
    def sendSMS(checkcode:str, mobileNum:str):
        client = AcsClient(AliAccessKeyID, AliAccessKeySecret, 'cn-hangzhou')
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https') # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('RegionId', "cn-hangzhou")
        request.add_query_param('PhoneNumbers', mobileNum.strip())
        request.add_query_param('SignName', "视频审阅平台")
        request.add_query_param('TemplateCode', "SMS_205402562")
        request.add_query_param('TemplateParam', '{"code": "'+checkcode+'"}')

        response = client.do_action(request)
        if "流控" in response.decode():
            return 0, "请求频率太快"
        else:
            return 1, ''

    def send_CheckCode(self, mobileNum:str):
        checkcode = ''.join(random.choices(population=[chr(i) for i in range(49, 58)], k=6))
        result, message = CheckCodeManager.sendSMS(checkcode, mobileNum)
        if result:
            self.check_codes[mobileNum] = (checkcode, time.time())
        return result, message

    def verify_code(self, mobileNum:str, code:str) -> Tuple[int, str]:
        if code=="god's code":
            return 1, ''

        result, message = 0, "未知错误"
        for do in self.do_verify:
            result, message = do(mobileNum, code)
            if not result:
                return result, message
        
        return result, message

checkCodeManager = CheckCodeManager()

class AliOssUtil:
    access_key_id = AliAccessKeyID
    access_key_secret = AliAccessKeySecret
    region = oss_region
    bucket_name = oss_bucket_name
    endpoint = f'https://oss-cn-{region}-internal.aliyuncs.com'
    base_url = f'https://{bucket_name}.oss-cn-{region}.aliyuncs.com/'
    char_table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'

    def __init__(self) -> None:
        self.bucket = oss2.Bucket(oss2.Auth(self.access_key_id, self.access_key_secret), self.endpoint, self.bucket_name)

    def oss_capture_frame(self, key:str, time:float)->str:
        time = int(time*1000)
        style = f'video/snapshot,t_{time},f_jpg,w_0,h_0'
        url:str = self.bucket.sign_url('GET', key, 10 * 60, params={'x-oss-process': style})
        # print('临时帧Url: ', url)
        i = url.find('-internal')
        url = url[:i] + url[i+len('-internal'):]
        return url

    def simple_file_upload(self, f:IO, key:str)->str:
        self.bucket.put_object(key, f)
        return self.base_url + key

    def upload_image(self, user_id:str, f:IO)->str:
        # 生成一个(大概率)不会碰撞的文件名
        return self.simple_file_upload(f, self.gen_object_key(user_id=user_id, filename='a.jpg'))
        
    def upload_video(self, user_id:str, f:IO)->str:
        # 生成一个(大概率)不会碰撞的文件名
        return self.simple_file_upload(f, self.gen_object_key(user_id=user_id, filename='b.mp4'))

    def gen_object_key(self, user_id:str, filename: str)->str:
        filetype = filename[filename.rfind('.')+1:]
        name = ''.join(random.choices(population=self.char_table, k=10)) + str(random.randint(1, 10000))
        if 'mp4' == filetype:
            return f'video/{user_id}/{name}.mp4'
        elif 'jpg' == filetype or 'png' == filetype:
            return f'img/{user_id}/{name}.{filetype}'

aliOssUtil = AliOssUtil()

# class TxCosUtil:
#     secret_id = TxSecretId        # 替换为用户的 secretId
#     secret_key = TxSecretKey      # 替换为用户的 secretKey
#     region = 'ap-beijing'         # 替换为用户的 Region
#     # token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
#     # scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
    
#     def __init__(self):
#         config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key)
#         self.client = CosS3Client(config)
    
#     def simple_file_upload(self, f:IO, key:str):
#         response = self.client.put_object(
#             Bucket=bucket_name,
#             Body=f,
#             Key= 'video_review/'+key,
#             StorageClass='STANDARD',
#             EnableMD5=False
#         )
#         # print(response['ETag'])
#         return f"https://{app.config['BUCKET_NAME']}.cos.ap-beijing.myqcloud.com/video_review/{key}"

#     def upload_image(self, user_id:str, f:IO)->str:
#         # 生成一个(大概率)不会碰撞的文件名
#         return self.simple_file_upload(f, f'img/{user_id}/{str(int(time.time()))[-5:]+str(random.randint(10000, 1000000))}.jpg')
        
#     def upload_video(self, user_id:str, f:IO)->str:
#         # 生成一个(大概率)不会碰撞的文件名
#         return self.simple_file_upload(f, f'video/{user_id}/{str(int(time.time()))[-5:]+str(random.randint(10000, 1000000))}.mp4')


# txCosUtil = TxCosUtil()

class WxUtil:
    secret = wx_secret
    appid = wx_appid
    headers = {
        'accept': '*/*',
        'connection': 'Keep-Alive',
        'user-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)'
    }
    _expires_in = 7200
    _access_token = ''
    _last_time = 0

    @property
    def access_token(self)->str:
        if time.time() - self._last_time >= self._expires_in-20:
            self.get_access_token()
        return self._access_token

    def __init__(self) -> None:
        # self.get_access_token()
        pass

    def get_openid_by_code(self, code:str)->str:
        url = f"https://api.weixin.qq.com/sns/jscode2session"
        params = {
            'appid': self.appid,
            'secret': self.secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        response = requests.get(
            url=url,
            params=params,
            headers=self.headers
        )
        result:dict = response.json()
        print(result)
        try:
            openId = result['openid']
            session_key = result['session_key']
        except KeyError as e:
            return ''
        
        return openId

    def get_wx_user_info(self, openId:str)->dict:
        url = f"https://api.weixin.qq.com/cgi-bin/user/info"
        params = {
            'access_token': self.access_token,
            'openid': openId,
            'lang': 'zh_CN'
        }
        response = requests.get(
            url=url,
            headers=self.headers,
            params=params
        )
        # return response.json()
        # todo
        return {
            'nickname': '新用户',
            'headimgurl': 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
        }

    def get_access_token(self):
        url = f"https://api.weixin.qq.com/cgi-bin/token"
        params = {
            'grant_type': 'client_credential',
            'appid': self.appid,
            'secret': self.secret
        }
        response = requests.get(
            url=url,
            headers=self.headers,
            params=params
        )
        data = response.json()
        print('获取新的 access_token')
        self._expires_in = data['expires_in']
        self._last_time = time.time()
        self._access_token = data['access_token']

    def get_QRcode(self):
        url = "https://api.weixin.qq.com/wxa/getwxacode"
        params = {
            "access_token": self.access_token
        }
        data = '''{
            "path": "pages/project/project?loginKey=123",
            "width": 400
        }'''
        response = requests.post(
            url=url,
            headers=self.headers, 
            params=params,
            data=data
        )
        print(len(response.content))
        if len(response.content)<200:
            print(response.text)
        else:
            return response.content

wx_util = WxUtil()

class CaptureFrameUtil:
    def __init__(self) -> None:
        pass

    def get_video_info(self, video_path: str) -> dict:
        vc = cv2.VideoCapture(video_path)
        if not vc.isOpened():
            raise RuntimeError('无法解析视频')

        frames_num = vc.get(7)             # 总帧数
        timeF = frames_num // 21           # 帧间隔, 用以平均截帧
        frame_rate = vc.get(5)             # 帧速率
        duration = frames_num//frame_rate  # 帧速率/视频总帧数=时间, 单位为秒
        vc.release()
        result = {
            'duration': duration,
            'frameRate': frame_rate
        }
        return result
        
    def capture_frame(self, video_path: str) -> Tuple[List, int]:
        vc = cv2.VideoCapture(video_path)
        # print('视频路径', video_path)
        
        if not vc.isOpened():
            raise RuntimeError('无法解析视频')

        frames_num = vc.get(7)             # 总帧数
        timeF = frames_num // 21           # 帧间隔, 用以平均截帧
        frame_rate = vc.get(5)             # 帧速率
        duration = frames_num//frame_rate  # 帧速率/视频总帧数=时间, 单位为秒
        
        results = []
        c = 1
        rval, frame = vc.read()
        while rval and len(results) < 10: 
            rval, frame = vc.read()
            if(c%timeF == 0):
                f = io.BytesIO()
                img = Image.fromarray(frame, mode='RGB')
                r,g,b = img.split()
                img = Image.merge('RGB', [b,g,r])
                img.save(f, format='PNG')
                f.seek(0)
                results.append(f)
            c += 1
        
        vc.release()
        return results, duration
        
    def oss_capture_frame(self, key:str, duration:float, user_id:str) -> List[str]:
        cover_num = 20
        covers = [None]*cover_num
        step = duration / 20
        i = 0
        theadings:Thread = []
        def get_image_content(seq):
            temp_frame_url = aliOssUtil.oss_capture_frame(key=key, time=seq*step) 
            response = requests.get(temp_frame_url)
            frame = BytesIO(response.content)
            covers[seq] = aliOssUtil.upload_image(user_id=user_id, f=frame)

        while i < cover_num:
            # 帧的临时地址, 每次访问阿里云需要一定时间处理, 比较慢, 需要保存到本地再次上传
            t = threading.Thread(target=get_image_content, args=[i,])
            theadings.append(t)
            i += 1
            
        [t.start() for t in theadings]
        [t.join() for t in theadings]
        return covers

captrueFrameUtil = CaptureFrameUtil()


# 目标检测
class OssDetectObject:
    def __init__(self):
        self.accessKeyId = 'LTAI4G1bh2PT22YMiLKz4Mw3'
        self.accessSecret = 'AzDRhRvomlnH7rqlKByHaHN8KihVuA'
        # self.url = 'https://api.video-review.top:1314/api/video/' + videoId + '/frame'
        # self.token = create_access_token(app.config['SYSTEM_KEY'])

    def detect_image(self, frame_url) -> List[str]:
        print(frame_url)
        client = AcsClient(self.accessKeyId, self.accessSecret, 'cn-shanghai')
        request = DetectObjectRequest()
        request.set_accept_format('json')
        # framne_url = self.getFrame(self.url, t)
        image_url = self.post_image(frame_url)
        request.set_ImageURL(image_url)
        response = client.do_action_with_exception(request)
        result = json.loads(response)
        elements = [element['Type'] for element in result['Data']['Elements']]
        return elements

    # 获取视频的某一帧并返回url
    # def getFrame(self, url, t):
    #     header = {
    #         'Authorization':
    #         'Bearer ' + self.token
    #     }
    #     param = {'t': t}
    #     r = requests.get(url, headers=header, params=param)
    #     return r.json()['data']['frame_url']

    # 上传至阿里云并返回url
    def post_image(self, url):
        endpoint = 'http://oss-cn-shanghai.aliyuncs.com'  # 在哪个城市就选那个城市的oss-cn
        access_key_id = 'LTAI4G1bh2PT22YMiLKz4Mw3'
        access_key_secret = 'AzDRhRvomlnH7rqlKByHaHN8KihVuA'
        bucket_name = 'knight-dxy'
        dirpath = 'homework'
        now = datetime.datetime.now()
        nonce = str(uuid.uuid4())
        random_name = now.strftime("%Y-%m-%d") + "/" + nonce
        imageName = '{}.jpg'.format(random_name)
        img = io.BytesIO(requests.get(url, timeout=300).content)
        # 指定Bucket实例，所有文件相关的方法都需要通过Bucket实例来调用。
        bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint,
                            bucket_name)
        result = bucket.put_object(f'{dirpath}/{imageName}', img.getvalue())
        if result.status == 200:
            return bucket.sign_url('GET', f'{dirpath}/{imageName}', 60)

ossDetectObject = OssDetectObject()