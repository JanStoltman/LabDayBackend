from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from drf_multiple_model.views import ObjectMultipleModelAPIView
from itertools import chain
from operator import attrgetter

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .permissions import IsAdminOrReadOnly


class Speakers(viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = (IsAdminOrReadOnly,)


class Events(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAdminOrReadOnly,)


class Places(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (IsAdminOrReadOnly,)


class Paths(viewsets.ModelViewSet):
    queryset = Path.objects.all()
    serializer_class = PathSerializer
    permission_classes = (IsAdminOrReadOnly,)


class Timetables(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = (IsAdminOrReadOnly,)


class AppData(ObjectMultipleModelAPIView):
    querylist = [
        {'queryset': Event.objects.all(), 'serializer_class': EventSerializer, 'label': 'events'},
        {'queryset': Speaker.objects.all(), 'serializer_class': SpeakerSerializer, 'label': 'speakers'},
        {'queryset': Place.objects.all(), 'serializer_class': PlaceSerializer, 'label': 'places'},
        {'queryset': Path.objects.all(), 'serializer_class': PathSerializer, 'label': 'paths'},
        {'queryset': Timetable.objects.all(), 'serializer_class': TimetableSerializer, 'label': 'timetables'}
    ]


class LastUpdate(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = sorted(
            chain(Event.objects.all(), Speaker.objects.all(), Place.objects.all(),
                  Path.objects.all(), Timetable.objects.all()),
            key=attrgetter('updated_at'),
            reverse=True
        )
        return Response({'updated_at': queryset[0].updated_at})
