import os
from kavenegar import *
from django.contrib.auth.mixins import UserPassesTestMixin



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


class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self) -> bool | None:
        return self.request.user.is_authenticated and self.request.user.is_admin