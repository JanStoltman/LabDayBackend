from itertools import chain
from operator import attrgetter

from django.http import HttpResponse
import json
from django.utils.crypto import get_random_string
from drf_multiple_model.views import ObjectMultipleModelAPIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponseForbidden
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from django.db.models import Q

from .permissions import IsAdminOrReadOnly
from .serializers import *


class Speakers(viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated,)


class Events(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated,)


class Places(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated,)


class Paths(viewsets.ModelViewSet):
    queryset = Path.objects.all()
    serializer_class = PathSerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated,)


class Timetables(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated,)


class AppData(ObjectMultipleModelAPIView):
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated,)
    querylist = [
        {'queryset': Event.objects.all(), 'serializer_class': EventSerializer, 'label': 'events'},
        {'queryset': Speaker.objects.all(), 'serializer_class': SpeakerSerializer, 'label': 'speakers'},
        {'queryset': Place.objects.all(), 'serializer_class': PlaceSerializer, 'label': 'places'},
        {'queryset': Path.objects.all(), 'serializer_class': PathSerializer, 'label': 'paths'},
        {'queryset': Timetable.objects.all(), 'serializer_class': TimetableSerializer, 'label': 'timetables'}
    ]

    def get(self, request, *args, **kwargs):
        if request.user.userdetails is not None:
            self.path_id = request.user.userdetails.path_id
        else:
            self.path_id = 1
        return super().get(request, *args, **kwargs)

    def get_querylist(self):
        paths = Path.objects.select_for_update().filter(~Q(pk=self.path_id))
        paths.update(active=False)
        path = Path.objects.select_for_update().filter(pk=self.path_id)
        path.update(active=True)
        self.querylist = [
            {'queryset': Event.objects.all(), 'serializer_class': EventSerializer, 'label': 'events'},
            {'queryset': Speaker.objects.all(), 'serializer_class': SpeakerSerializer, 'label': 'speakers'},
            {'queryset': Place.objects.all(), 'serializer_class': PlaceSerializer, 'label': 'places'},
            {'queryset': sorted(list(chain(path, paths)),key=attrgetter('pk')),
             'serializer_class': PathSerializer, 'label': 'paths'},
            {'queryset': Timetable.objects.all(), 'serializer_class': TimetableSerializer, 'label': 'timetables'}
        ]

        assert self.querylist is not None, (
            '{} should either include a `querylist` attribute, '
            'or override the `get_querylist()` method.'.format(
                self.__class__.__name__
            )
        )

        return self.querylist


class LastUpdate(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request):
        queryset = sorted(
            chain(Event.objects.all(), Speaker.objects.all(), Place.objects.all(),
                  Path.objects.all(), Timetable.objects.all()),
            key=attrgetter('updated_at'),
            reverse=True
        )
        return Response({'updated_at': queryset[0].updated_at})


class ObtainToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # Change password so each login/password can be used only once
        if not (user.username == 'test' or request.user.is_staff):
            user.set_password(get_random_string(32))
            user.userdetails.password_used = True
            user.save()

        return Response({'token': token.key})
