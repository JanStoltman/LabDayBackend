from django.urls import path
from django.conf.urls import url, include
from rest_framework.authtoken import views as authViews
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'speakers', Speakers, base_name='Speaker')
router.register(r'events', Events, base_name='Event')
router.register(r'places', Places, base_name='Place')
router.register(r'paths', Paths, base_name='Path')
router.register(r'timetables', Timetables, base_name='Timetable')

app_name = 'labday_api'
urlpatterns = [
    path(r'login', ObtainToken.as_view(), name='Login'),
    path(r'app-data', AppData.as_view(), name='AppData'),
    path(r'last-update', LastUpdate.as_view(), name='LastUpdate'),
    url(r'^', include(router.urls))
]
