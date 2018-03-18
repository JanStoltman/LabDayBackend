import email
import smtplib
import sys
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db.models.functions import Length
from rest_framework.authtoken.views import ObtainAuthToken
from django.utils.crypto import get_random_string
from rest_framework.permissions import IsAdminUser
from django.http.response import HttpResponseRedirect, HttpResponseNotModified, HttpResponseNotFound
from django.core.mail import EmailMessage
from .settings_secret import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from .settings import EMAIL_PORT, EMAIL_HOST
import re

User = get_user_model()


class CreateUsers(ObtainAuthToken):
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        amount = request.POST['amount']
        if self.create_users(int(amount)):
            nxt = request.POST.get('next', '/')
            return HttpResponseRedirect(nxt)
        else:
            return HttpResponseNotModified()

    @staticmethod
    def create_users(amount):
        # TODO: Change this, so we could better assert the number of users
        users_number = User.objects.all().count()

        for i in range(users_number, amount + users_number):
            username = 'User{0}'.format(i + 1)
            password = get_random_string(10)
            try:
                user = User.objects.create_user(username=username)
                user.set_password(password)
                user.save()

                assert authenticate(username=username, password=password)

            except:
                print('There was a problem creating the user: {0}.  Error: {1}.'
                      .format(username, sys.exc_info()[1]))
                return False
        return True


# TODO: Chage users/one-time-passwords distribution system
class SendUsers(ObtainAuthToken):
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        if self.send_email(email):
            nxt = request.POST.get('next', '/')
            return HttpResponseRedirect(nxt)
        else:
            return HttpResponseNotModified()

    def send_email(self, email):
        users = User.objects. \
            filter(username__contains='User'). \
            filter(userdetails__password_used=False)
        try:
            us = ''

            for user in users:
                password = get_random_string(10)  # Create one-time-use password
                us += "{0} {1}\n".format(user.get_username(), password, user.UserDetails.path.name)

                user.set_password(password)
                user.save()
                assert authenticate(username=user.get_username(), password=password)

            self.send_mail(
                email,
                'Users',
                us,
            )
            return True

        except:
            print('There was a problem sending the email: Error: {0}.'
                  .format(sys.exc_info()[1]))
            return False

    def send_mail(self, recipient, subject, message, contenttype='plain'):
        mime_msg = email.mime.text.MIMEText(message, contenttype, _charset="UTF-8")
        mime_msg['Subject'] = subject
        mime_msg['From'] = EMAIL_HOST_USER
        mime_msg['To'] = recipient

        smtpserver = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        smtpserver.sendmail(EMAIL_HOST_USER, recipient, mime_msg.as_string())
        smtpserver.close()
