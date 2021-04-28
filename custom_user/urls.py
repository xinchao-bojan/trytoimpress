from django.urls import path

from . import views

urlpatterns = [
    path('public/', views.public),
    path('private/', views.private),
]
