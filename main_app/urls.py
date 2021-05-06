from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('create/', CreateApplicationView.as_view()),
    path('get/<int:app_pk>/', GetApplicationReadyView.as_view()),
    path('close/', CloseApplicationReadyView.as_view()),
    path('check/<int:app_pk>/', CheckApplicationView.as_view()),
    path('get/closed/', GetClosedApplicationsView.as_view()),
    path('close/all/', CloseAllApplicationsView.as_view()),
    path('own/list/', ListOwnApplicationView.as_view()),
    path('last/', GetIdOfLastApplicationView.as_view()),

]
