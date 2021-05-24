from django.contrib import admin

from .models import Thumbnail, Vote

admin.site.register(Thumbnail)
admin.site.register(Vote)