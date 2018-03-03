from itertools import chain
from operator import attrgetter

from django.utils.crypto import get_random_string
from drf_multiple_model.views import ObjectMultipleModelAPIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponseForbidden
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken

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
    querylist = [
        {'queryset': Event.objects.all(), 'serializer_class': EventSerializer, 'label': 'events'},
        {'queryset': Speaker.objects.all(), 'serializer_class': SpeakerSerializer, 'label': 'speakers'},
        {'queryset': Place.objects.all(), 'serializer_class': PlaceSerializer, 'label': 'places'},
        {'queryset': Path.objects.all(), 'serializer_class': PathSerializer, 'label': 'paths'},
        {'queryset': Timetable.objects.all(), 'serializer_class': TimetableSerializer, 'label': 'timetables'}
    ]
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated,)


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
        if not user.username == 'test':
            user.set_password(get_random_string(32))
            user.save()

        return Response({'token': token.key})
