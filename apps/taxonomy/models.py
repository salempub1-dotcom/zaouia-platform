from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from apps.core.models import TimeStampedModel, unique_slug

class Category(MPTTModel, TimeStampedModel):
    name=models.CharField(max_length=120); slug=models.SlugField(unique=True,allow_unicode=True,blank=True)
    parent=TreeForeignKey("self",null=True,blank=True,on_delete=models.CASCADE,related_name="children")
    icon=models.CharField(max_length=60,blank=True); order=models.PositiveSmallIntegerField(default=0)
    is_active=models.BooleanField(default=True); show_on_home=models.BooleanField(default=False)
    def __str__(self): return self.name
    def save(self,*a,**k):
        if not self.slug:self.slug=unique_slug(self,self.name)
        super().save(*a,**k)

class Tag(TimeStampedModel):
    name=models.CharField(max_length=80,unique=True); slug=models.SlugField(unique=True,allow_unicode=True,blank=True)
    def __str__(self): return self.name
    def save(self,*a,**k):
        if not self.slug:self.slug=unique_slug(self,self.name)
        super().save(*a,**k)

class Occasion(TimeStampedModel):
    name=models.CharField(max_length=150); slug=models.SlugField(unique=True,allow_unicode=True,blank=True)
    description=models.TextField(blank=True); is_active=models.BooleanField(default=True)
    def __str__(self):return self.name
    def save(self,*a,**k):
        if not self.slug:self.slug=unique_slug(self,self.name)
        super().save(*a,**k)
