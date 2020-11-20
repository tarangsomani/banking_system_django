import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from django.conf import settings


# Will add actual credentials during actual implementation
DEFAULT_FROM_EMAIL = '<settings.DEFAULT_FROM_EMAIL>'
SENDGRID_API_KEY = '<settings.SENDGRID_API_KEY>'


class SendGridService:

    def send_mail(self, receiver, subject, content):

        message = Mail(
            from_email=DEFAULT_FROM_EMAIL,
            to_emails=receiver,
            subject=subject,
            html_content='<strong> %s </strong>' % content)
        try:
            send_grid = SendGridAPIClient(api_key=SENDGRID_API_KEY)
            response = send_grid.send(message)
            return True

        except Exception as e:
            return False
