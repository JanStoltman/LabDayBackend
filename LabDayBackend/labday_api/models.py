from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Speaker(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    info = models.TextField(blank=True)
    img = models.TextField(blank=True)


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    img = models.TextField(blank=True)
    address = models.TextField(blank=True)
    room = models.TextField(blank=True)
    info = models.TextField(blank=True)
    topic = models.TextField(blank=True)
    speaker_id = models.ForeignKey(Speaker, on_delete=models.SET_NULL,
                                   null=True, blank=True, default=None,
                                   related_name='events')
    dor1_img = models.TextField(blank=True)
    dor2_img = models.TextField(blank=True)
    latitude = models.TextField(blank=True)
    longitude = models.TextField(blank=True)


class Place(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField()
    name = models.CharField(max_length=100)
    info = models.TextField(blank=True)
    img = models.TextField(blank=True)
    latitude = models.TextField(blank=True, max_length=15)
    longitude = models.TextField(blank=True, max_length=15)


class Path(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True)
    info = models.TextField(blank=True)
    active = models.BooleanField(default=True)


class Timetable(models.Model):
    id = models.AutoField(primary_key=True)
    path_id = models.ForeignKey(Path, on_delete=models.SET_NULL,
                                null=True, blank=True, default=None)
    event_id = models.ForeignKey(Event, on_delete=models.SET_NULL,
                                 null=True, blank=True, default=None)
    time_start = models.BigIntegerField(default=0, blank=True)
    time_end = models.BigIntegerField(default=0, blank=True)
