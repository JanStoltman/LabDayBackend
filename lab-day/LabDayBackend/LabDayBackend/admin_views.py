import sys
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from django.utils.crypto import get_random_string
from rest_framework.permissions import IsAdminUser
from django.http.response import HttpResponse, HttpResponseNotModified

User = get_user_model()


class CreateUsers(ObtainAuthToken):
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        amount = request.POST['amount']
        if self.create_users(int(amount)):
            return HttpResponse('Users created')
        else:
            return HttpResponseNotModified()

    @staticmethod
    def create_users(amount):
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
