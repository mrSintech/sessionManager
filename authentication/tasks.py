from celery import shared_task
from core.sms_handler import SendSms
    
@shared_task
def send_auth_sms(receiver, verif_code):
    sms = SendSms().send_login_sms(
        receiver, 
        verif_code
    )
    
    print(sms.json())
    

    