from kavenegar import *



def send_otp_code(phone_number, code):
    pass
    try:
        api = KavenegarAPI('34574C522F4E7056756A4B707839765533654D49716F61584D3863624E7A5532666F442B374D2F55694F673D')
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