from django.contrib import admin
from .models import Comment, DownloadHistory, Favorite, ViewHistory
admin.site.register([Comment, DownloadHistory, Favorite, ViewHistory])
