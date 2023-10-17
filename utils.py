import os
from kavenegar import *



def send_otp_code(phone_number, code):
    pass
    try:
        api = KavenegarAPI(os.environ.get('KavenegarAPI'))
        params = {
            'sender': '',#optional
            'receptor': phone_number,#multiple mobile number, split by comma
            'message': f'کد تایید شما : {code}',
        } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)