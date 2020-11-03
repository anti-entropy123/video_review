import logging
import time
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from config.secret_config import AccessKeyID, AccessKeySecret
import random
from typing import Tuple

def build_response(result=1, message='', data=None, **kwargs) -> dict:
    result = {'result': result, 'message': message}
    if not data == None:
        result['data'] = data
    result.update(kwargs)
    return result

# 发送短信
def sendSMS(checkcode:str, mobileNum:str):
    client = AcsClient(AccessKeyID, AccessKeySecret, 'cn-hangzhou')
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

# 验证码模块
class CheckCodeManager:
    check_codes = {}

    def send_CheckCode(self, mobileNum:str):
        checkcode = ''.join(random.choices(population=[chr(i) for i in range(49, 58)], k=6))
        try:
            sendSMS(checkcode, mobileNum)
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