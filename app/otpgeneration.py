import random
from django.core.mail import send_mail
import os


class OTPgen:
    @staticmethod
    def send_email(data):
        print(data)
        l1 = []
        l1.append([data['to_email']])
        print(l1)

        send_mail(data['subject'], data['body'], os.environ.get(
            'EMAIL_FROM'), ['karthiksbh@gmail.com'], fail_silently=False)
