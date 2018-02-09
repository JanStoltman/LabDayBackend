from django.shortcuts import render
from rest_framework import viewsets

from .models import *
from .serializers import *


class Speakers(viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer

class Events(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
