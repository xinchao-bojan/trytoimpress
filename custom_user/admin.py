from django.contrib import admin

from .models import CustomUser,Position

admin.site.register(CustomUser)
admin.site.register(Position)