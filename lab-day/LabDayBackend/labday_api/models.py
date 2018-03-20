from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from geoposition import Geoposition
from geoposition.fields import GeopositionField
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Speaker(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    info = models.TextField(blank=True)
    img = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + '. ' + self.name


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
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.id) + '. ' + self.name + ' | ' + self.address

class Place(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField()
    name = models.CharField(max_length=100)
    info = models.TextField(blank=True)
    img = models.TextField(blank=True)
    position = GeopositionField(blank=True)
    latitude = models.TextField(blank=True, max_length=20, editable=False)
    longitude = models.TextField(blank=True, max_length=20, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.latitude = self.position.latitude
        self.longitude = self.position.longitude
        super().save(force_insert, force_update, using, update_fields)


    def __str__(self):
        return str(self.id) + '. ' + self.name


class Path(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True)
    info = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + '. ' + self.name + ' | '  +self.info


class Timetable(models.Model):
    id = models.AutoField(primary_key=True)
    path_id = models.ForeignKey(Path, on_delete=models.SET_NULL,
                                null=True, blank=True, default=None)
    event_id = models.ForeignKey(Event, on_delete=models.SET_NULL,
                                 null=True, blank=True, default=None)
    time_start = models.BigIntegerField(default=0, blank=True)
    time_end = models.BigIntegerField(default=0, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.id) + '. Path: ' + str(self.path_id)

class UserDetails(models.Model):
    path = models.ForeignKey(to=Path, on_delete=models.DO_NOTHING, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password_used = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    @receiver(post_save, sender=User)
    def save_user_password_changes(sender, instance, created, **kwargs):
        if created:
            changes = UserDetails(user=instance)
            changes.save()
