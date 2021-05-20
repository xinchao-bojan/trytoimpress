from django.urls import path
from .views import *

urlpatterns = [
    path('public/', public),
    path('private/', private),
    path('addposition/', GivePositionView.as_view()),
    path('roles/', ListUserRoles.as_view()),
    path('info/', UserInfo.as_view()),
]
