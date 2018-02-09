from django.urls import path
from rest_framework.authtoken import views as authViews
from rest_framework import routers

from .views import Speakers, Events

router = routers.DefaultRouter()
router.register(r'speakers', Speakers, base_name='Speaker')
router.register(r'events', Events, base_name='Event')

app_name = 'labday_api'
urlpatterns = [
    path(r'login', authViews.obtain_auth_token, name='login')
]

urlpatterns += router.urls
