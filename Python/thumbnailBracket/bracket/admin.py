from django.contrib import admin

from .models import *


class betterVoteAdmin(admin.ModelAdmin):
    date_hierarchy = 'voteDatetime'

class YtVidAdmin(admin.ModelAdmin):
    date_hierarchy = 'upload_date'

admin.site.register(Vote)
admin.site.register(betterVote, betterVoteAdmin)
admin.site.register(YtVid, YtVidAdmin)

