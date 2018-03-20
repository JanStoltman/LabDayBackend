"""LabDayBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .admin_views import CreateUsers, SendUsers, CreateUsersForPaths

urlpatterns = [
    path('api/', include('labday_api.urls')),
    path('admin/', admin.site.urls),
    path('admin/create-users', CreateUsers.as_view()),
    path('admin/create-users-for-paths', CreateUsersForPaths.as_view()),
    path('admin/send-users', SendUsers.as_view()),
]
