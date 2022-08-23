import requests

class SendSms:
    # apikey     = '8cJs8Buxicu4EqoY_73cxoSQ5hg0wMDnt3hEGGj6P4s='
    # sender_num = '3000505'
    # url        = 'http://ippanel.com:8080/?apikey={}&fnum={}'.format(apikey, sender_num)
    
    def __init__(self):
        self.apikey     = '8cJs8Buxicu4EqoY_73cxoSQ5hg0wMDnt3hEGGj6P4s='
        self.sender_num = '3000505'
        self.url        = 'http://ippanel.com:8080/?apikey={}&fnum={}'.format(self.apikey, self.sender_num)
    
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
            
        
            
        
            
        