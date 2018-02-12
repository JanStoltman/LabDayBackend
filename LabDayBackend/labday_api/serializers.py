from rest_framework import serializers
from .models import *


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ('id', 'name', 'info', 'img')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id', 'name', 'img', 'address', 'room',
            'topic', 'speaker_id', 'dor1_img',
            'dor2_img', 'latitude', 'longitude')


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id', 'type', 'name', 'info', 'latitude', 'longitude')


class PathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Path
        fields = ('id', 'name', 'info', 'active')


class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = ('id', 'path_id', 'event_id', 'time_start', 'time_end')


class AppDataSerializer(serializers.Serializer):
    speakers = SpeakerSerializer(many=True)
    events = EventSerializer(many=True)
    places = PlaceSerializer(many=True)
    paths = PathSerializer(many=True)
    timetables = TimetableSerializer(many=True)
