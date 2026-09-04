from django.conf import settings
from django.db import models
class Notification(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="notifications")
    kind=models.CharField(max_length=20,default="system");title=models.CharField(max_length=200);body=models.CharField(max_length=500,blank=True)
    content=models.ForeignKey("dorouss.Content",null=True,blank=True,on_delete=models.CASCADE);url=models.CharField(max_length=300,blank=True)
    is_read=models.BooleanField(default=False);created_at=models.DateTimeField(auto_now_add=True)
    class Meta:ordering=["-created_at"]
class NotificationPreference(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="notification_pref")
    in_app=models.BooleanField(default=True);email_new_content=models.BooleanField(default=False);push_new_content=models.BooleanField(default=False)
