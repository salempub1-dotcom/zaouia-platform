from django.db import models
from apps.core.models import TimeStampedModel, unique_slug, upload_to

class Scholar(TimeStampedModel):
    honorific = models.CharField(max_length=50, default="الشيخ سيدي")
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True)
    short_bio = models.CharField(max_length=300, blank=True)
    biography = models.TextField(blank=True)
    photo = models.ImageField(upload_to=upload_to("scholars"), blank=True)
    is_current_sheikh = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    class Meta: ordering = ["order", "name"]
    def __str__(self): return f"{self.honorific} {self.name}"
    def save(self,*a,**k):
        if not self.slug: self.slug=unique_slug(self,self.name)
        super().save(*a,**k)
