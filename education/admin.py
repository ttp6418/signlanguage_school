from django.contrib import admin
from .models import video, video_history, video_like, video_subscribe, subject

# Register your models here.

admin.site.register(subject)
admin.site.register(video)