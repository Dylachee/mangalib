from django.test import TestCase
from celery import shared_task
from django.core.mail import send_mail
from bookstore.settings import EMAIL_HOST

@shared_task
def send_email(subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email= EMAIL_HOST,
        recipient_list=recipient_list,
        fail_silently=False,
    )
