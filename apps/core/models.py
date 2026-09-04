import os, uuid
from django.db import models
from django.utils.text import slugify
from django.utils.deconstruct import deconstructible
from solo.models import SingletonModel

@deconstructible
class UploadTo:
    def __init__(self, prefix): self.prefix = prefix
    def __call__(self, instance, filename):
        return f"{self.prefix}/{uuid.uuid4().hex}{os.path.splitext(filename)[1].lower()}"

def upload_to(prefix): return UploadTo(prefix)

def unique_slug(instance, value):
    base = slugify(value, allow_unicode=True) or "item"
    slug, i = base, 2
    while instance.__class__.objects.exclude(pk=instance.pk).filter(slug=slug).exists():
        slug, i = f"{base}-{i}", i + 1
    return slug

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: abstract = True

class SiteSettings(SingletonModel):
    site_name = models.CharField(max_length=150, default="الزاوية البلقائدية الهبرية")
    tagline = models.CharField(max_length=255, blank=True)
    about_short = models.TextField(blank=True)
    about_full = models.TextField(blank=True)
    logo = models.ImageField(upload_to=upload_to("site"), blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=255, blank=True)
    youtube_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    allow_registration = models.BooleanField(default=True)
    def __str__(self): return self.site_name

class Banner(TimeStampedModel):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to=upload_to("banners"), blank=True)
    content = models.ForeignKey("dorouss.Content", null=True, blank=True, on_delete=models.SET_NULL)
    link_url = models.URLField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    class Meta: ordering = ["order", "-created_at"]

class ContactMessage(TimeStampedModel):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_handled = models.BooleanField(default=False)
