import logging
import random
import time
from typing import Tuple

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from config.secret_config import (AliAccessKeyID, AliAccessKeySecret,
                                  TxSecretId, TxSecretKey, bucket_name)
from qcloud_cos import CosConfig, CosS3Client

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
            raise RuntimeError

    def send_CheckCode(self, mobileNum:str):
        checkcode = ''.join(random.choices(population=[chr(i) for i in range(49, 58)], k=6))
        try:
            CheckCodeManager.sendSMS(checkcode, mobileNum)
        except RuntimeError as e:
            return 0, "请求频率太快"
        self.check_codes[mobileNum] = (checkcode, time.time())
        return 1, ""

    def verify_code(self, mobileNum:str, code:str) -> Tuple[int, str]:
        if mobileNum not in self.check_codes:
            return 0, "无此验证码"
        origin_code, t = self.check_codes.get(mobileNum, ('', 0))
        if code != origin_code: 
            return 0, "验证码错误"
        elif time.time() - t > 60*5:
            return 0, '超时'
        elif code == origin_code:
            self.check_codes.pop(mobileNum)
            return 1, ''
        else:
            return 0, "未知错误"
 
checkCodeManager = CheckCodeManager()

class TxCosUtil:
    secret_id = TxSecretId      # 替换为用户的 secretId
    secret_key = TxSecretKey    # 替换为用户的 secretKey
    region = 'ap-beijing'       # 替换为用户的 Region
    # token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
    # scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
    
    def __init__(self):
        config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key)
        self.client = CosS3Client(config)
    
    def simple_file_upload(self, f, key:str):
        response = self.client.put_object(
            Bucket=bucket_name,
            Body=f,
            Key= 'video_review/'+key,
            StorageClass='STANDARD',
            EnableMD5=False
        )
        print(response['ETag'])

txCosUtil = TxCosUtil()

if __name__ == "__main__":
    txCosUtil.simple_file_upload()
