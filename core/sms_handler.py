import requests
from decouple import config

class SendSms:

    def __init__(self):
        self.apikey     = config('FARAZ_SMS_APIKEY')
        self.sender_num = '3000505'
        self.url = 'http://ippanel.com:8080/?apikey={}&fnum={}'.format(
            self.apikey, 
            self.sender_num
        )
    
    def send_login_sms(self, receiver, verification):
        pattern = 'zs0tc0rf0k'
        
        # shaping request
        self.url = self.url + \
            '&tnum={}&pid={}&p1=verification_code&v1={}'.format(
                receiver, 
                pattern, 
                verification
            )
            
        # send request
        response = requests.get(self.url)
        
        return response
            
        
            
        
            
        