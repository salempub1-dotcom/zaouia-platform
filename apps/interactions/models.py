from django.conf import settings
from django.db import models
from apps.core.models import TimeStampedModel

class Favorite(TimeStampedModel):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="favorites")
    content=models.ForeignKey("dorouss.Content",on_delete=models.CASCADE,related_name="favorited_by")
    class Meta:constraints=[models.UniqueConstraint(fields=["user","content"],name="uniq_favorite")]

class ViewHistory(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.CASCADE,related_name="view_history")
    session_key=models.CharField(max_length=40,blank=True,db_index=True);content=models.ForeignKey("dorouss.Content",on_delete=models.CASCADE,related_name="view_history")
    last_position=models.PositiveIntegerField(default=0);total=models.PositiveIntegerField(default=0);progress_percent=models.PositiveSmallIntegerField(default=0);completed=models.BooleanField(default=False);last_viewed_at=models.DateTimeField(auto_now=True)
    class Meta:constraints=[models.UniqueConstraint(fields=["user","content"],condition=models.Q(user__isnull=False),name="uniq_user_history"),models.UniqueConstraint(fields=["session_key","content"],condition=models.Q(user__isnull=True),name="uniq_session_history")]

class DownloadHistory(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="downloads")
    content=models.ForeignKey("dorouss.Content",on_delete=models.CASCADE,related_name="downloads");created_at=models.DateTimeField(auto_now_add=True)

class Comment(TimeStampedModel):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="comments")
    content=models.ForeignKey("dorouss.Content",on_delete=models.CASCADE,related_name="comments")
    parent=models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE,related_name="replies")
    body=models.TextField(max_length=2000);is_approved=models.BooleanField(default=False);is_flagged=models.BooleanField(default=False)
