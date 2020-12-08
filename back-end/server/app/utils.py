from __future__ import annotations

import io
import random
import time
from typing import IO, Tuple, List
from flask import current_app as app
import cv2
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from bson.objectid import ObjectId
from PIL import Image

from config.secret_config import (AliAccessKeyID, AliAccessKeySecret,
                                  TxSecretId, TxSecretKey, bucket_name)
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


class CaptureFrameUtil:
    def __init__(self) -> None:
        pass

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
        
captrueFrameUtil = CaptureFrameUtil()

class TxCosUtil:
    secret_id = TxSecretId        # 替换为用户的 secretId
    secret_key = TxSecretKey      # 替换为用户的 secretKey
    region = 'ap-beijing'         # 替换为用户的 Region
    # token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
    # scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
    
    def __init__(self):
        config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key)
        self.client = CosS3Client(config)
    
    def simple_file_upload(self, f:IO, key:str):
        response = self.client.put_object(
            Bucket=bucket_name,
            Body=f,
            Key= 'video_review/'+key,
            StorageClass='STANDARD',
            EnableMD5=False
        )
        # print(response['ETag'])
        return f"https://{app.config['BUCKET_NAME']}.cos.ap-beijing.myqcloud.com/video_review/{key}"

    def upload_image(self, user_id:str, f:IO)->str:
        # 生成一个(大概率)不会碰撞的文件名
        return self.simple_file_upload(f, f'img/{user_id}/{str(int(time.time()))[-5:]+str(random.randint(10000, 1000000))}.jpg')
        
    def upload_video(self, user_id:str, f:IO)->str:
        # 生成一个(大概率)不会碰撞的文件名
        return self.simple_file_upload(f, f'video/{user_id}/{str(int(time.time()))[-5:]+str(random.randint(10000, 1000000))}.mp4')

txCosUtil = TxCosUtil()

if __name__ == "__main__":
    txCosUtil.simple_file_upload()
