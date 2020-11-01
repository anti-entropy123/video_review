import logging
import time

def build_response(result=1, message='', data=None, **kwargs) -> dict:
    result = {'result': result, 'message': message}
    if not data == None:
        result['data'] = data
    result.update(kwargs)
    return result

class CheckCode:
    check_codes = {

    }

    @staticmethod
    def sendSMS(mobileNum:str):
        # send
        CheckCode.check_codes[mobileNum] = ('abc', time.time())

    @staticmethod
    def verify_code(mobileNum:str, code:str):
        if mobileNum not in CheckCode.check_codes:
            return 0, "无此验证码"
        
        origin_code, t = CheckCode.check_codes.get(mobileNum)
        if time.time() - t > 4:
            return 0, '超时'
            
        if code == origin_code:
            return 1, ''
