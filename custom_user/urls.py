from django.urls import path

from . import views

urlpatterns = [
    path('public/', views.public),
    path('private/', views.private),
    path('addposition/', views.GivePositionView.as_view()),
    path('roles/', views.ListUserRoles.as_view()),
]
