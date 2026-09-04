from django.conf import settings
from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel, unique_slug, upload_to

class ContentType(models.TextChoices):
    LECTURE="lecture","محاضرة"; LESSON="lesson","درس"; POEM="poem","قصيدة / مديح"
    VIDEO="video","فيديو"; AUDIO="audio","صوتية"; BOOK="book","كتاب"; PDF="pdf","ملف PDF"; ARTICLE="article","مقال"

class Collection(TimeStampedModel):
    title=models.CharField(max_length=200); slug=models.SlugField(unique=True,allow_unicode=True,blank=True)
    kind=models.CharField(max_length=20,choices=[("series","سلسلة"),("annual","إصدار سنوي"),("album","ألبوم")],default="series")
    description=models.TextField(blank=True); cover=models.ImageField(upload_to=upload_to("collections"),blank=True)
    year=models.PositiveSmallIntegerField(null=True,blank=True); is_published=models.BooleanField(default=True)
    def __str__(self):return self.title
    def save(self,*a,**k):
        if not self.slug:self.slug=unique_slug(self,self.title)
        super().save(*a,**k)

class ContentQuerySet(models.QuerySet):
    def published(self):return self.filter(status="published",published_at__lte=timezone.now())
    def with_relations(self):return self.select_related("scholar","category","occasion","collection").prefetch_related("tags")
    def featured(self):return self.published().filter(is_featured=True)
    def of_type(self,*types):return self.filter(content_type__in=types)

class Content(TimeStampedModel):
    title=models.CharField(max_length=250); slug=models.SlugField(unique=True,allow_unicode=True,blank=True,max_length=270)
    content_type=models.CharField(max_length=20,choices=ContentType.choices,db_index=True)
    status=models.CharField(max_length=12,choices=[("draft","مسودة"),("published","منشور"),("archived","مؤرشف")],default="draft",db_index=True)
    short_description=models.CharField(max_length=400,blank=True); description=models.TextField(blank=True); body=models.TextField(blank=True)
    thumbnail=models.ImageField(upload_to=upload_to("thumbnails"),blank=True); language=models.CharField(max_length=5,default="ar")
    scholar=models.ForeignKey("scholars.Scholar",null=True,blank=True,on_delete=models.SET_NULL,related_name="contents")
    category=models.ForeignKey("taxonomy.Category",null=True,blank=True,on_delete=models.SET_NULL,related_name="contents")
    occasion=models.ForeignKey("taxonomy.Occasion",null=True,blank=True,on_delete=models.SET_NULL,related_name="contents")
    collection=models.ForeignKey(Collection,null=True,blank=True,on_delete=models.SET_NULL,related_name="contents")
    tags=models.ManyToManyField("taxonomy.Tag",blank=True,related_name="contents")
    youtube_url=models.URLField(blank=True); youtube_id=models.CharField(max_length=20,blank=True,editable=False)
    media_file=models.FileField(upload_to=upload_to("media"),blank=True); pdf_file=models.FileField(upload_to=upload_to("pdf"),blank=True)
    release_year=models.PositiveSmallIntegerField(null=True,blank=True,db_index=True); published_at=models.DateTimeField(default=timezone.now,db_index=True)
    duration=models.DurationField(null=True,blank=True); is_featured=models.BooleanField(default=False); allow_download=models.BooleanField(default=True)
    views_count=models.PositiveIntegerField(default=0); downloads_count=models.PositiveIntegerField(default=0); favorites_count=models.PositiveIntegerField(default=0)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
    objects=ContentQuerySet.as_manager()
    class Meta:ordering=["-published_at"]
    def __str__(self):return self.title
    def save(self,*a,**k):
        import re
        if not self.slug:self.slug=unique_slug(self,self.title)
        match=re.search(r"(?:v=|youtu\.be/|/embed/|/shorts/)([\w-]{11})",self.youtube_url or "")
        self.youtube_id=match.group(1) if match else ""
        if not self.release_year:self.release_year=self.published_at.year
        super().save(*a,**k)
    @property
    def thumbnail_url(self):return self.thumbnail.url if self.thumbnail else (f"https://i.ytimg.com/vi/{self.youtube_id}/hqdefault.jpg" if self.youtube_id else None)
    @property
    def youtube_embed_url(self):return f"https://www.youtube-nocookie.com/embed/{self.youtube_id}" if self.youtube_id else None
    @property
    def duration_seconds(self):return int(self.duration.total_seconds()) if self.duration else None
    @property
    def primary_media(self):return self.media_files.filter(is_primary=True).first() or self.media_files.first()

class PDFDocument(TimeStampedModel):
    content=models.OneToOneField(Content,on_delete=models.CASCADE,related_name="pdf_document")
    file=models.FileField(upload_to=upload_to("pdf_library")); cover_image=models.ImageField(upload_to=upload_to("pdf_covers"),blank=True)
    pages_count=models.PositiveIntegerField(default=0); author=models.CharField(max_length=200,blank=True); publisher=models.CharField(max_length=200,blank=True)
    extracted_text=models.TextField(blank=True,editable=False); processing_status=models.CharField(max_length=10,default="pending")

class MediaFile(TimeStampedModel):
    content=models.ForeignKey(Content,on_delete=models.CASCADE,related_name="media_files")
    kind=models.CharField(max_length=15,choices=[("audio","صوت"),("video","فيديو"),("image","صورة"),("attachment","مرفق")])
    file=models.FileField(upload_to=upload_to("media_center")); duration=models.DurationField(null=True,blank=True)
    mime_type=models.CharField(max_length=100,blank=True); file_size=models.PositiveBigIntegerField(default=0); is_primary=models.BooleanField(default=False)
    @property
    def duration_seconds(self):return int(self.duration.total_seconds()) if self.duration else None
