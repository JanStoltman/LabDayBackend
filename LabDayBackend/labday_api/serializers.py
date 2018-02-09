from rest_framework import serializers
from .models import Speaker, Event


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ('id', 'name', 'info', 'img')


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id', 'name', 'img', 'address', 'room',
            'topic', 'speaker_id', 'dor1_img',
            'dor2_img', 'latitude', 'longitude')
