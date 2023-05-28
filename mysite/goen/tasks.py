# from celery import shared_task
from django.core.mail import send_mail


# @shared_task
def send_email(subject, message, from_email, recipient_list):
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
        auth_user=None,
        auth_password=None,
        connection=None,
        html_message=message, )
    pass
