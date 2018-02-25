import sys
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()


def create_users(amount):
    users_number = User.objects.all().count()

    for i in range(users_number, amount + users_number):
        try:
            print('Creating user {0}.'.format(username))
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()

            assert authenticate(username=username, password=password)
            print('User {0} successfully created.'.format(username))

        except:
            print('There was a problem creating the user: {0}.  Error: {1}.'
                  .format(username, sys.exc_info()[1]))
