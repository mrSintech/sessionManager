from celery import shared_task
from .sms_handler import SendSms

@shared_task
def send_reminder_sms(receiver, title):
    sms = SendSms().send_session_reminder(
        receiver, 
        title
    )
    
    print(sms.json())